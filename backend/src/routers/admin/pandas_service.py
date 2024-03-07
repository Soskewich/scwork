import pandas as pd
import numpy as np
from fastapi import UploadFile
from sqlalchemy import and_, or_, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy.orm import joinedload

import datetime
import re

from src.model.model import Identifier, Source, SourceLink, Publication, PublicationLink, \
    AuthorIdentifier, AuthorPublication, Author, AuthorPublicationOrganization, Keyword, \
    KeywordPublication, SourceRating, Organization, Department, Faculty, AuthorDepartment, Subject, \
    SourceRatingSubject
from src.model.storage import get_or_create_publication_link_type, get_or_create_source_type, \
    get_or_create_source_link_type, get_or_create_identifier, get_or_create_source_rating_type, \
    get_or_create_organization_omstu, get_source_by_name_or_identifiers, get_or_create_publication_type, \
    create_publication, create_publication_link, create_source, create_source_link, get_publication_by_doi_or_name, \
    get_subject_by_code


empty_annotations = [None, '-', '', '[краткое описание не найдено]', '[No abstract available]']


async def service_fill_scopus(date: datetime.date, file: UploadFile, db: Session):
    scopus_df = pd.read_csv(file.file, on_bad_lines='skip')
    scopus_df = scopus_df.replace(np.nan, "")
    pub_link_type_doi = await get_or_create_publication_link_type("DOI", db)
    pub_link_type_scopus = await get_or_create_publication_link_type("Scopus", db)
    source_type_journal = await get_or_create_source_type("Журнал", db)
    source_type_conference = await get_or_create_source_type("Конференция", db)
    source_link_type_issn = await get_or_create_source_link_type("ISSN", db)
    identifier_scopus = await get_or_create_identifier("Scopus Author ID", db)
    organization_omstu = await get_or_create_organization_omstu(db)

    for _, row in scopus_df.iterrows():

        issn = str(row['ISSN']).rjust(8, '0')
        issn = issn[:4] + '-' + issn[4:]
        source = await get_source_by_name_or_identifiers(str(row['Source title']), [issn], db)
        if source is None:
            if row['Document Type'] == "Conference Paper":
                source = await create_source(row['Source title'], source_type_conference, db)
            else:
                source = await create_source(row['Source title'], source_type_journal, db)
            if row['ISSN'] != "":
                await create_source_link(source, source_link_type_issn, row['ISSN'], db)

        publication_type = await get_or_create_publication_type(row["Document Type"], db)
        date = datetime.date(int(row['Year']), 1, 1)
        publication = await get_publication_by_doi_or_name(row["DOI"], row['Title'], db)
        if publication is None:
            publication = await create_publication(publication_type, source, row["Title"], row["Abstract"], date, True, db)
            await create_publication_link(publication, pub_link_type_scopus, row["Link"], db)
            if row['DOI'] != "":
                await create_publication_link(publication, pub_link_type_doi, row["DOI"], db)
        else:
            if publication.abstract in empty_annotations:
                publication.abstract = row["Abstract"]
            publication_link_types_ids = [link.link_type_id for link in publication.publication_links]
            if pub_link_type_scopus.id not in publication_link_types_ids:
                await create_publication_link(publication, pub_link_type_scopus, row["Link"], db)
            if row['DOI'] != "" and (pub_link_type_doi.id not in publication_link_types_ids):
                await create_publication_link(publication, pub_link_type_doi, row["DOI"], db)
            continue

        authors_orgs = row['Authors with affiliations'].split(';')
        authors_scopus = row['Author(s) ID'].split(';')
        for i, author_row in enumerate(authors_orgs):
            if i >= len(authors_scopus):
                continue
            author_data = author_row.split(', ')
            identifier_result = await db.execute(select(AuthorIdentifier).options(joinedload(AuthorIdentifier.author)).
                                                 filter(and_(AuthorIdentifier.identifier_id == identifier_scopus.id,
                                                             AuthorIdentifier.identifier_value == authors_scopus[i])))
            identifier = identifier_result.scalars().first()
            author: Author
            if identifier is None:
                author: Author
                if len(author_data) > 1:
                    author = Author(
                        name=author_data[1],
                        surname=author_data[0],
                        confirmed=False
                    )
                else:
                    author = Author(
                        name='-',
                        surname=author_data[0],
                        confirmed=False
                    )
                db.add(author)
                author_identifier = AuthorIdentifier(
                    author=author,
                    identifier=identifier_scopus,
                    identifier_value=authors_scopus[i]
                )
                db.add(author_identifier)
            else:
                author = identifier.author
            author_publication = AuthorPublication(
                publication=publication,
                author=author
            )
            db.add(author_publication)
            if 'Omsk State Technical University' in author_data:
                author_publication_organization = AuthorPublicationOrganization(
                    author_publication=author_publication,
                    organization=organization_omstu
                )
                db.add(author_publication_organization)
            elif len(author_data) > 2:
                organization_result = await db.execute(select(Organization).filter(Organization.name == author_data[2]))
                organization = organization_result.scalars().first()
                if organization is None:
                    organization = Organization(name=author_data[2])
                    db.add(organization)
                author_publication_organization = AuthorPublicationOrganization(
                    author_publication=author_publication,
                    organization=organization
                )
                db.add(author_publication_organization)
            await db.commit()
        if row['Author Keywords'] != "":
            keywords = set(row['Author Keywords'].split('; '))
            for keyword_value in keywords:
                keyword_result = await db.execute(select(Keyword).filter(Keyword.keyword == keyword_value))
                keyword = keyword_result.scalars().first()
                if keyword is None:
                    keyword = Keyword(
                        keyword=keyword_value
                    )
                    db.add(keyword)
                publication_keyword = KeywordPublication(
                    publication=publication,
                    keyword=keyword
                )
                db.add(publication_keyword)
        await db.commit()
    await db.commit()
    return {'Message': 'OK'}


async def service_fill_elibrary(file: UploadFile, db: Session):
    elibrary_df = pd.read_csv(file.file, on_bad_lines='skip')
    elibrary_df = elibrary_df.replace(np.nan, "")

    pub_link_type_doi = await get_or_create_publication_link_type("DOI", db)
    pub_link_type_elibrary = await get_or_create_publication_link_type("Elibrary", db)
    source_type_journal = await get_or_create_source_type("Журнал", db)
    source_link_type_issn = await get_or_create_source_link_type("ISSN", db)
    source_link_type_eissn = await get_or_create_source_link_type("eISSN", db)
    identifier_elibrary = await get_or_create_identifier("Elibrary ID", db)
    publication_type = await get_or_create_publication_type('Article', db)
    organization_omstu = await get_or_create_organization_omstu(db)

    for _, row in elibrary_df.iterrows():
        issns = []
        if row['ISSN'] != '-':
            issns.append(row['ISSN'])
        if row['eISSN'] != '-':
            issns.append(row['ISSN'])
        source = await get_source_by_name_or_identifiers(str(row['Журнал']), issns, db)
        if source is None:
            source = Source(name=row['Журнал'])
            source.source_type = source_type_journal
            db.add(source)
            if row['ISSN'] != "-":
                source_link = SourceLink(
                    source=source,
                    source_link_type=source_link_type_issn,
                    link=row['ISSN']
                )
                db.add(source_link)
            if row['eISSN'] != "-":
                source_link = SourceLink(
                    source=source,
                    source_link_type=source_link_type_eissn,
                    link=row['eISSN']
                )
                db.add(source_link)
            await db.commit()
        date = datetime.date(int(row['Год']), 1, 1)
        if row['DOI'] != "-":
            link_doi_result = await db.execute(select(PublicationLink).filter(PublicationLink.link == row['DOI']))
            link_doi = link_doi_result.scalars().first()
            if link_doi is not None:
                continue
        publication_result = await db.execute(select(Publication).filter(or_(Publication.title.ilike(row['Название']))))
        publication = publication_result.scalars().first()
        if publication is not None:
            continue
        publication = await create_publication(publication_type, source, row["Название"],
                                               row["Аннотация"], date, True, db)
        await create_publication_link(publication, pub_link_type_elibrary, f'https://www.elibrary.ru{row["Ссылка"]}',
                                      db)
        if row['DOI'] != "":
            await  create_publication_link(publication, pub_link_type_doi, row["DOI"], db)
        authors = row['Авторы'].split('|')
        authors_id = row['ID авторов'].split('|')
        authors_org = row['Аффилиации в публикации'].split('|')
        orgs = row['Организации'].split('|')
        orgs_id = row['ID организаций'].split('|')
        for i, author_row in enumerate(authors):
            author_data = re.subn(r'\([^()]*\)', '', author_row)[0]
            author_data = author_data.replace('  ', ' ').split()
            if len(author_data) <= 1:
                continue
            author: Author | None
            if authors_id[i] != '-':
                identifier_result = await db.execute(select(AuthorIdentifier)
                                                     .options(joinedload(AuthorIdentifier.author))
                                                     .filter(and_(AuthorIdentifier.identifier_id ==
                                                                  identifier_elibrary.id,
                                                                  AuthorIdentifier.identifier_value == authors_id[i])))
                identifier = identifier_result.scalars().first()
                if identifier is None:
                    if len(author_data) > 2:
                        author = Author(
                            name=author_data[1],
                            surname=author_data[0],
                            patronymic=author_data[2],
                            confirmed=False
                        )
                    else:
                        author = Author(
                            name=author_data[1],
                            surname=author_data[0],
                            confirmed=False
                        )
                    db.add(author)
                    author_identifier = AuthorIdentifier(
                        author=author,
                        identifier=identifier_elibrary,
                        identifier_value=authors_id[i]
                    )
                    db.add(author_identifier)
                else:
                    author = identifier.author
            else:
                if len(author_data) > 2:
                    author_result = await db.execute(select(Author).filter(and_(Author.name == author_data[1],
                                                                                Author.surname == author_data[0],
                                                                                Author.patronymic == author_data[2])))
                    author = author_result.scalars().first()
                else:
                    author_result = await db.execute(select(Author).filter(and_(Author.name == author_data[1],
                                                                                Author.surname == author_data[0])))
                    author = author_result.scalars().first()
                if author is None:
                    if len(author_data) > 2:
                        author = Author(
                            name=author_data[1],
                            surname=author_data[0],
                            patronymic=author_data[2],
                            confirmed=False
                        )
                        db.add(author)
                    else:
                        author = Author(
                            name=author_data[1],
                            surname=author_data[0],
                            confirmed=False
                        )
                        db.add(author)
            author_publication = AuthorPublication(
                publication=publication,
                author=author
            )
            db.add(author_publication)
            if authors_org[i] != '-':
                author_orgs = authors_org[i].split(',')
                for org in author_orgs:
                    author_org = orgs[int(org) - 1]
                    org_id = orgs_id[int(org) - 1]
                    if org_id == '401':
                        author_publication_organization = AuthorPublicationOrganization(
                            author_publication=author_publication,
                            organization=organization_omstu
                        )
                        db.add(author_publication_organization)
                    else:
                        organization_result = await db.execute(select(Organization)
                                                               .filter(Organization.name == author_org))
                        organization = organization_result.scalars().first()
                        if organization is None:
                            organization = Organization(name=author_org)
                            db.add(organization)
                        author_publication_organization = AuthorPublicationOrganization(
                            author_publication=author_publication,
                            organization=organization
                        )
                        db.add(author_publication_organization)
                    await db.commit()
            await db.commit()
        await db.commit()
    return {'Message': 'OK'}


async def service_fill_authors(file: UploadFile, db: Session):
    author_df = pd.read_csv(file.file)
    author_df = author_df.replace(np.nan, "")
    identifier_spin_result = await db.execute(select(Identifier).filter(Identifier.name == "SPIN-код"))
    identifier_spin = identifier_spin_result.scalars().first()
    if identifier_spin is None:
        identifier_spin = Identifier(name="SPIN-код")
        db.add(identifier_spin)
    identifier_orcid_result = await db.execute(select(Identifier).filter(Identifier.name == "ORCID"))
    identifier_orcid = identifier_orcid_result.scalars().first()
    if identifier_orcid is None:
        identifier_orcid = Identifier(name="ORCID")
        db.add(identifier_orcid)
    identifier_scopus_result = await db.execute(select(Identifier).filter(Identifier.name == "Scopus Author ID"))
    identifier_scopus = identifier_scopus_result.scalars().first()
    if identifier_scopus is None:
        identifier_scopus = Identifier(name="Scopus Author ID")
        db.add(identifier_scopus)
    identifier_researcher_result = await db.execute(select(Identifier).filter(Identifier.name == "ResearcherID"))
    identifier_researcher = identifier_researcher_result.scalars().first()
    if identifier_researcher is None:
        identifier_researcher = Identifier(name="ResearcherID")
        db.add(identifier_researcher)
    identifier_elibrary_id_result = await db.execute(select(Identifier).filter(Identifier.name == "Elibrary ID"))
    identifier_elibrary_id = identifier_elibrary_id_result.scalars().first()
    if identifier_elibrary_id is None:
        identifier_elibrary_id = Identifier(name="Elibrary ID")
        db.add(identifier_elibrary_id)

    for _, row in author_df.iterrows():
        author_result = await db.execute(select(Author).filter(and_(Author.name == row['name'].title(),
                                                                    Author.surname == row['surname'].title(),
                                                                    Author.patronymic == row['patronymic'].title())))
        author = author_result.scalars().first()
        if author is None:
            author = Author(
                name=row['name'].title(),
                surname=row['surname'].title(),
                patronymic=row['patronymic'].title(),
                confirmed=True
            )
            db.add(author)
            await db.commit()
        if row['faculty'] != "":
            faculty_result = await db.execute(select(Faculty).filter(Faculty.name == row['faculty']))
            faculty = faculty_result.scalars().first()
            if faculty is None:
                faculty = Faculty(name=row['faculty'])
                db.add(faculty)
                await db.commit()
            department_result = await db.execute(select(Department).filter(and_(Department.name == row['department'],
                                                                                Department.faculty == faculty)))
            department = department_result.scalars().first()
            if department is None:
                department = Department(
                    name=row['department'],
                    faculty=faculty
                )
                db.add(department)
                await db.commit()
            author_department_result = await db.execute(select(AuthorDepartment)
                                                        .filter(and_(AuthorDepartment.department == department,
                                                                     AuthorDepartment.author == author)))
            author_department = author_department_result.scalars().first()
            if author_department is None:
                author_department = AuthorDepartment(
                    department=department,
                    author=author,
                    position=row['position']
                )
                db.add(author_department)
        if str(row['spin']) != "0":
            author_identifier_spin_result = await db.execute(select(AuthorIdentifier)
                                                             .filter(and_(AuthorIdentifier.author == author,
                                                                          AuthorIdentifier.identifier == identifier_spin,
                                                                          AuthorIdentifier.identifier_value == str(
                                                                              row['spin']))))
            author_identifier_spin = author_identifier_spin_result.scalars().first()
            if author_identifier_spin is None:
                author_identifier_spin = AuthorIdentifier(
                    author=author,
                    identifier=identifier_spin,
                    identifier_value=str(row['spin'])
                )
                db.add(author_identifier_spin)
        if str(row['orcid']) != "0":
            author_identifier_orcid_result = await db.execute(select(AuthorIdentifier)
                                                              .filter(and_(AuthorIdentifier.author == author,
                                                                           AuthorIdentifier.identifier ==
                                                                           identifier_orcid,
                                                                           AuthorIdentifier.identifier_value == str(
                                                                               row['orcid']))))
            author_identifier_orcid = author_identifier_orcid_result.scalars().first()
            if author_identifier_orcid is None:
                author_identifier_orcid = AuthorIdentifier(
                    author=author,
                    identifier=identifier_orcid,
                    identifier_value=str(row['orcid'])
                )
                db.add(author_identifier_orcid)
        if str(row['scopus author id']) != "0":
            author_identifier_scopus_result = await db.execute(select(AuthorIdentifier)
                                                               .filter(and_(AuthorIdentifier.author == author,
                                                                            AuthorIdentifier.identifier
                                                                            == identifier_scopus,
                                                                            AuthorIdentifier.identifier_value == str(
                                                                                row['scopus author id']))))
            author_identifier_scopus = author_identifier_scopus_result.scalars().first()
            if author_identifier_scopus is None:
                author_identifier_scopus = AuthorIdentifier(
                    author=author,
                    identifier=identifier_scopus,
                    identifier_value=str(row['scopus author id'])
                )
                db.add(author_identifier_scopus)
        if str(row['researcher id']) != "0":
            author_identifier_researcher_result = await db.execute(select(AuthorIdentifier)
                                                                   .filter(and_(AuthorIdentifier.author == author,
                                                                                AuthorIdentifier.identifier
                                                                                == identifier_researcher,
                                                                                AuthorIdentifier.identifier_value == str(
                                                                                    row['researcher id']))))
            author_identifier_researcher = author_identifier_researcher_result.scalars().first()
            if author_identifier_researcher is None:
                author_identifier_researcher = AuthorIdentifier(
                    author=author,
                    identifier=identifier_researcher,
                    identifier_value=str(row['researcher id'])
                )
                db.add(author_identifier_researcher)
        if str(row['elibrary id']) != "0":
            author_identifier_elibrary_result = await db.execute(select(AuthorIdentifier)
                                                                 .filter(and_(AuthorIdentifier.author == author,
                                                                              AuthorIdentifier.identifier
                                                                              == identifier_researcher,
                                                                              AuthorIdentifier.identifier_value == str(
                                                                                  row['elibrary id']))))
            author_identifier_elibrary = author_identifier_elibrary_result.scalars().first()
            if author_identifier_elibrary is None:
                author_identifier_elibrary = AuthorIdentifier(
                    author=author,
                    identifier=identifier_elibrary_id,
                    identifier_value=str(row['elibrary id'])
                )
                db.add(author_identifier_elibrary)
        await db.commit()
    return {"message": "OK"}


async def service_fill_author_department(file: UploadFile, db: Session):
    authors_df = pd.read_excel(file.file)
    await db.execute(delete(AuthorDepartment))
    await db.execute(delete(Department))
    await db.execute(delete(Faculty))
    await db.execute(update(Author).values(confirmed=False))
    await db.commit()
    for _, row in authors_df.iterrows():
        name = row['Сотрудник'].split(' ')
        if len(name) < 3:
            name.append("")
        author_result = await db.execute(select(Author).filter(and_(Author.name == name[1].title(),
                                                                    Author.surname == name[0].title(),
                                                                    Author.patronymic == name[2].title())))
        author = author_result.scalars().first()
        if author is None:
            author = Author(
                name=name[1].title(),
                surname=name[0].title(),
                patronymic=name[2].title(),
            )
            db.add(author)
        author.confirmed = True
        birthday = row['Дата рождения'].split('.')
        author.birthday = datetime.date(year=int(birthday[2]), month=int(birthday[1]), day=int(birthday[0]))
        await db.commit()
        if row['Подразделение.Группа подразделений (Подразделения)'] == "ПО":
            workplace = row['Полное наименование подразделения'].split('/')
            if len(workplace) == 1:
                workplace.append('')
            if len(workplace) > 2:
                workplace = [workplace[0], '/'.join(workplace[1:])]
            faculty_result = await db.execute(select(Faculty).filter(Faculty.name == workplace[0]))
            faculty = faculty_result.scalars().first()
            if faculty is None:
                faculty = Faculty(name=workplace[0])
                db.add(faculty)
                await db.commit()
            department_result = await db.execute(select(Department).filter(and_(Department.name == workplace[1],
                                                                                Department.faculty == faculty)))
            department = department_result.scalars().first()
            if department is None:
                department = Department(
                    name=workplace[1],
                    faculty=faculty
                )
                db.add(department)
                await db.commit()
            author_department_result = await db.execute(select(AuthorDepartment)
                                                        .filter(and_(AuthorDepartment.author_id == author.id,
                                                                     AuthorDepartment.department_id == department.id,
                                                                     AuthorDepartment.position ==
                                                                     row[
                                                                         'Должность, Код по ОКЗ, Категории ВПО-1 (Должности)']
                                                                     .split(',')[0])))
            author_department = author_department_result.scalars().first()
            if author_department is None:
                author_department = AuthorDepartment(
                    department=department,
                    author=author,
                    position=row['Должность, Код по ОКЗ, Категории ВПО-1 (Должности)'].split(',')[0],
                    rate=float(row['Количество ставок'])
                )
                db.add(author_department)
            else:
                author_department.rate += float(row['Количество ставок'])
            await db.commit()
    return dict(message="OK")


async def service_white_list_fill(date: datetime.date, file: UploadFile, db: Session):
    white_list_df = pd.read_csv(file.file, on_bad_lines='skip', sep='\t')
    white_list_df = white_list_df.replace(np.nan, "")
    white_list_rating_type = await get_or_create_source_rating_type('«Белый список» РЦНИ', db)
    source_link_type_issn = await get_or_create_source_link_type("ISSN", db)
    source_link_type_eissn = await get_or_create_source_link_type("eISSN", db)
    source_type_journal = await get_or_create_source_type("Журнал", db)
    for _, row in white_list_df.iterrows():
        issns = row['ISSN'].split('|')
        source = await get_source_by_name_or_identifiers(str(row['Title']), issns, db)
        if not (source is None):
            source_rating_white_list = SourceRating(
                source_rating_type=white_list_rating_type,
                source=source,
                rating="Входит",
                rating_date=date
            )
            db.add(source_rating_white_list)
            continue
        else:
            source = Source(
                name=row['Title'],
                source_type=source_type_journal
            )
            db.add(source)
            source_rating_white_list = SourceRating(
                source_rating_type=white_list_rating_type,
                source=source,
                rating="Входит",
                rating_date=date
            )
            db.add(source_rating_white_list)
            if len(issns) > 1:
                source_link_issn = SourceLink(
                    source=source,
                    source_link_type=source_link_type_issn,
                    link=issns[0]
                )
                db.add(source_link_issn)
                source_link_eissn = SourceLink(
                    source=source,
                    source_link_type=source_link_type_eissn,
                    link=issns[1]
                )
                db.add(source_link_eissn)
            else:
                source_link_issn = SourceLink(
                    source=source,
                    source_link_type=source_link_type_issn,
                    link=issns[0]
                )
                db.add(source_link_issn)
    await db.commit()
    return dict(message="OK")


async def service_fill_vak_journals_rank(date: datetime.date, file: UploadFile, db: Session):
    vak_df = pd.read_excel(file.file, 'rank')
    vak_df = vak_df.replace(np.nan, "")
    vak_rating_type = await get_or_create_source_rating_type('ВАК', db)
    source_link_type_issn = await get_or_create_source_link_type("ISSN", db)
    source_link_type_eissn = await get_or_create_source_link_type("eISSN", db)
    source_type_journal = await get_or_create_source_type("Журнал", db)
    for _, row in vak_df.iterrows():
        issns = row['issn'].split(',')
        source = await get_source_by_name_or_identifiers(str(row['title']), issns, db)
        if not (source is None):
            source_rating_white_list = SourceRating(
                source_rating_type=vak_rating_type,
                source=source,
                rating=row['Q'],
                rating_date=date
            )
            db.add(source_rating_white_list)
            continue
        else:
            source = Source(
                name=row['title'],
                source_type=source_type_journal
            )
            db.add(source)
            source_rating_white_list = SourceRating(
                source_rating_type=vak_rating_type,
                source=source,
                rating=row['Q'],
                rating_date=date
            )
            db.add(source_rating_white_list)
            if len(issns) > 1:
                source_link_issn = SourceLink(
                    source=source,
                    source_link_type=source_link_type_issn,
                    link=issns[0]
                )
                db.add(source_link_issn)
                source_link_eissn = SourceLink(
                    source=source,
                    source_link_type=source_link_type_eissn,
                    link=issns[1]
                )
                db.add(source_link_eissn)
            else:
                source_link_issn = SourceLink(
                    source=source,
                    source_link_type=source_link_type_issn,
                    link=issns[0]
                )
                db.add(source_link_issn)
    await db.commit()
    return dict(message='OK')


async def service_fill_rsci_journals_rank(date: datetime.date, file: UploadFile, db: Session):
    rsci_df = pd.read_csv(file.file, on_bad_lines='skip')
    rsci_df = rsci_df.replace(np.nan, "")
    rsci_rating_type = await get_or_create_source_rating_type('RSCI', db)
    source_link_type_issn = await get_or_create_source_link_type("ISSN", db)
    source_link_type_eissn = await get_or_create_source_link_type("eISSN", db)
    source_type_journal = await get_or_create_source_type("Журнал", db)
    for _, row in rsci_df.iterrows():
        issns = []
        if row['issn1'] != 'NA':
            issns.append(row['issn1'])
        if row['issn2'] != 'NA':
            issns.append(row['issn2'])
        source = await get_source_by_name_or_identifiers(str(row['title']), issns, db)
        if not (source is None):
            source_rating_white_list = SourceRating(
                source_rating_type=rsci_rating_type,
                source=source,
                rating=f'OECD: {row["oecd"]}; Квартиль: {row["q"]}',
                rating_date=date
            )
            db.add(source_rating_white_list)
            continue
        else:
            source = Source(
                name=row['title'],
                source_type=source_type_journal
            )
            db.add(source)
            source_rating_white_list = SourceRating(
                source_rating_type=rsci_rating_type,
                source=source,
                rating=f'OECD: {row["oecd"]}; Квартиль: {row["q"]}',
                rating_date=date
            )
            db.add(source_rating_white_list)
            if row['issn1'] != 'NA':
                source_link_issn = SourceLink(
                    source=source,
                    source_link_type=source_link_type_issn,
                    link=row['issn1']
                )
                db.add(source_link_issn)
            if row['issn2'] != 'NA':
                source_link_issn = SourceLink(
                    source=source,
                    source_link_type=source_link_type_eissn,
                    link=row['issn2']
                )
                db.add(source_link_issn)
    await db.commit()
    return dict(message="OK")


async def service_white_list_jcr_citescore(date: datetime.date, file: UploadFile, db: Session):
    white_list_df = pd.read_csv(file.file, on_bad_lines='skip')
    white_list_df = white_list_df.replace(np.nan, "")
    white_list_rating_type = await get_or_create_source_rating_type('«Белый список» РЦНИ', db)
    jcr_rating_type = await get_or_create_source_rating_type('Journal Citation Reports WoS', db)
    citescore_rating_type = await get_or_create_source_rating_type('CiteScore Scopus', db)
    source_link_type_issn = await get_or_create_source_link_type("ISSN", db)
    source_link_type_eissn = await get_or_create_source_link_type("eISSN", db)
    source_type_journal = await get_or_create_source_type("Журнал", db)
    for _, row in white_list_df.iterrows():
        issns = row['ISSN'].split('|')
        source = await get_source_by_name_or_identifiers(str(row['Title']), issns, db)
        if not (source is None):
            source_rating_white_list = SourceRating(
                source_rating_type=white_list_rating_type,
                source=source,
                rating="Входит",
                rating_date=date
            )
            db.add(source_rating_white_list)
            if row['Direction'] != "":
                source_rating_citescore = SourceRating(
                    source_rating_type=citescore_rating_type,
                    source=source,
                    rating=row['Direction'].replace('|', '; '),
                    rating_date=date
                )
                db.add(source_rating_citescore)
            if row['JCR categories'] != "":
                source_rating_jcr = SourceRating(
                    source_rating_type=jcr_rating_type,
                    source=source,
                    rating=row['JCR categories'],
                    rating_date=date
                )
                db.add(source_rating_jcr)
            continue
        else:
            source = Source(
                name=row['Title'],
                source_type=source_type_journal
            )
            db.add(source)
            source_rating_white_list = SourceRating(
                source_rating_type=white_list_rating_type,
                source=source,
                rating="Входит",
                rating_date=date
            )
            db.add(source_rating_white_list)
            if row['Direction'] != "":
                source_rating_citescore = SourceRating(
                    source_rating_type=citescore_rating_type,
                    source=source,
                    rating=row['Direction'].replace('|', '; '),
                    rating_date=date
                )
                db.add(source_rating_citescore)
            if row['JCR categories'] != "":
                source_rating_jcr = SourceRating(
                    source_rating_type=jcr_rating_type,
                    source=source,
                    rating=row['JCR categories'],
                    rating_date=date
                )
                db.add(source_rating_jcr)
            if len(issns) > 1:
                source_link_issn = SourceLink(
                    source=source,
                    source_link_type=source_link_type_issn,
                    link=issns[0]
                )
                db.add(source_link_issn)
                source_link_eissn = SourceLink(
                    source=source,
                    source_link_type=source_link_type_eissn,
                    link=issns[1]
                )
                db.add(source_link_eissn)
            else:
                source_link_issn = SourceLink(
                    source=source,
                    source_link_type=source_link_type_issn,
                    link=issns[0]
                )
                db.add(source_link_issn)
    await db.commit()
    return dict(message="OK")


async def service_jcr_list_fill(date: datetime.date, file: UploadFile, db: Session):
    jcr_df = pd.read_excel(file.file)
    jcr_df = jcr_df.replace(np.nan, "")
    jcr_rating_type = await get_or_create_source_rating_type('Journal Citation Reports WoS', db)
    source_link_type_issn = await get_or_create_source_link_type("ISSN", db)
    source_link_type_eissn = await get_or_create_source_link_type("eISSN", db)
    source_type_journal = await get_or_create_source_type("Журнал", db)
    for _, row in jcr_df.iterrows():
        source = await get_source_by_name_or_identifiers(str(row['Title']), [row['issn'], row['eissn']], db)
        if not (source is None):
            source_rating_white_list = SourceRating(
                source_rating_type=jcr_rating_type,
                source=source,
                rating=row['category'],
                rating_date=date
            )
            db.add(source_rating_white_list)
            continue
        source = Source(
            name=row['journal name'],
            source_type=source_type_journal
        )
        db.add(source)
        source_rating_white_list = SourceRating(
            source_rating_type=jcr_rating_type,
            source=source,
            rating=row['category'],
            rating_date=date
        )
        db.add(source_rating_white_list)
        if row['issn'] != "N/A":
            source_link_issn = SourceLink(
                source=source,
                source_link_type=source_link_type_issn,
                link=row['issn']
            )
            db.add(source_link_issn)
        if row['eissn'] != "N/A":
            source_link_issn = SourceLink(
                source=source,
                source_link_type=source_link_type_eissn,
                link=row['eissn']
            )
            db.add(source_link_issn)
    await db.commit()
    return dict(message="OK")


async def service_vak_list_fill(file: UploadFile, db: Session):
    df = pd.read_excel(file.file, 'subjects')
    df = df.replace(np.nan, "")
    source_type_journal = await get_or_create_source_type("Журнал", db)
    source_link_type_issn = await get_or_create_source_link_type("ISSN", db)
    source_link_type_eissn = await get_or_create_source_link_type("eISSN", db)
    vak_list_rating_type = await get_or_create_source_rating_type('ВАК "Список журналов"', db)
    # subj-type vak

    for _, row in df.iterrows():
        issns = row['issn'].split(',')
        source = await get_source_by_name_or_identifiers(str(row['title_main']), issns, db)
        if source is None:
            source = Source(
                name=row['title_main'],
                source_type=source_type_journal
            )
            if len(issns) > 1:
                source_link_issn = SourceLink(
                    source=source,
                    source_link_type=source_link_type_issn,
                    link=issns[0]
                )
                db.add(source_link_issn)
                source_link_eissn = SourceLink(
                    source=source,
                    source_link_type=source_link_type_eissn,
                    link=issns[1]
                )
                db.add(source_link_eissn)
            else:
                source_link_issn = SourceLink(
                    source=source,
                    source_link_type=source_link_type_issn,
                    link=issns[0]
                )
                db.add(source_link_issn)
            await db.commit()
        source_rating = await db.execute(select(SourceRating)
                                         .filter(and_(SourceRating.source_id == source.id,
                                                      SourceRating.source_rating_type_id == vak_list_rating_type.id)))
        source_rating = source_rating.scalars().first()
        if source_rating is None:
            source_rating = SourceRating(
                source=source,
                source_rating_type=vak_list_rating_type
            )
            db.add(source_rating)
            await db.commit()

        to_rating_date = datetime.date(9999, 1, 1) if str(row['till']) == '' \
            else datetime.datetime.strptime(str(row['till']), "%d.%m.%Y").date()

        subject = await get_subject_by_code(row['subj_code'], db)
        if subject is None:
            subject = Subject(
                subj_code=row['subj_code'],
                name=row['subj_name'],
                #subj-type_id vak
            )
        source_rating_subject = SourceRatingSubject(
                rating_date=datetime.datetime.strptime(str(row['from']), "%d.%m.%Y").date(),
                to_rating_date=to_rating_date,
                active=True if row['status'] == 'Active' else False,
                subject=subject,
                source_rating=source_rating,
        )
        db.add(source_rating_subject)
    await db.commit()
    return dict(message="OK")
