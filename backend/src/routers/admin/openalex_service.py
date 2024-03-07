from datetime import date

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy.orm import joinedload

from src.model.model import Identifier, AuthorIdentifier, PublicationLink, Publication, Source, SourceLink, Author, \
    AuthorPublication, AuthorPublicationOrganization, Organization
from src.model.storage import get_or_create_publication_link_type, get_source_by_name_or_identifiers, \
    get_or_create_source_link_type, get_or_create_source_type, get_or_create_publication_type, create_publication, \
    create_publication_link, get_or_create_organization_omstu
from src.utils.aiohttp import SingletonAiohttp


async def service_update_from_openalex(db: Session):
    identifier_orcid_result = await db.execute(select(Identifier).filter(Identifier.name == "ORCID"))
    identifier_orcid = identifier_orcid_result.scalars().first()
    pub_link_type_doi = await get_or_create_publication_link_type("DOI", db)
    source_link_type_issn = await get_or_create_source_link_type("ISSN", db)
    source_link_type_eissn = await get_or_create_source_link_type("eISSN", db)
    source_type_journal = await get_or_create_source_type("Журнал", db)
    source_type_conference = await get_or_create_source_type("Конференция", db)
    organization_omstu = await get_or_create_organization_omstu(db)

    if identifier_orcid is None:
        return None
    orcids_result = await db.execute(select(AuthorIdentifier).join(Author)
                                     .filter(AuthorIdentifier.identifier == identifier_orcid).filter(Author.confirmed))
    orcids = orcids_result.scalars().all()
    for orcid in orcids:
        filters = f'author.orcid:https://orcid.org/{orcid.identifier_value}'
        filtered_works_url = f'https://api.openalex.org/works?filter={filters}'
        cursor = '*'
        select_openalex = ",".join((
            'id',
            'doi',
            'ids',
            'title',
            'display_name',
            'publication_year',
            'publication_date',
            'primary_location',
            'type',
            'open_access',
            'authorships',
            'cited_by_count',
            'is_retracted',
            'is_paratext',
            'updated_date',
            'created_date',
            'abstract_inverted_index',
        ))
        works = []
        while cursor:
            url = f'{filtered_works_url}&select={select_openalex}&cursor={cursor}'
            page_with_results = await SingletonAiohttp.query_url(url)
            results = page_with_results['results']
            works.extend(results)

            cursor = page_with_results['meta']['next_cursor']

        for work in works:
            if work['doi']:
                doi = work['doi'].replace('https://doi.org/', '')
                link_doi_result = await db.execute(select(PublicationLink).filter(PublicationLink.link == doi))
                link_doi = link_doi_result.scalars().first()
                if link_doi is not None:
                    continue
            else:
                continue
            if not work['title']:
                continue
            if not work['primary_location']['source']:
                continue
            publication_result = await db.execute(select(Publication).filter(Publication.title.ilike(work['title'])))
            publication = publication_result.scalars().first()
            if publication is not None:
                continue
            issns = work['primary_location']['source']['issn']
            source_title = ''
            if work['primary_location']['source']['display_name']:
                source_title = work['primary_location']['source']['display_name']
            source = None
            if not (issns is None):
                source = await get_source_by_name_or_identifiers(source_title, issns, db)
            if source is None:
                if source_title == '':
                    continue
                source = Source(name=source_title)
                if work['primary_location']['source']['type'] == 'journal':
                    source.source_type = source_type_journal
                else:
                    source.source_type = source_type_conference
                db.add(source)
                if not (issns is None):
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
                    elif len(issns) == 1:
                        source_link_issn = SourceLink(
                            source=source,
                            source_link_type=source_link_type_issn,
                            link=issns[0]
                        )
                        db.add(source_link_issn)
            publication_type = await get_or_create_publication_type(work["type"].replace('-', ' ').title(), db)
            date_values = [int(i) for i in work['publication_date'].split('-')]
            date_openalex = date(date_values[0], date_values[1], date_values[2])
            abstract: str | None
            if work['abstract_inverted_index']:
                abstract = inverted_index_to_string(work['abstract_inverted_index'])
            else:
                abstract = None
            publication = await create_publication(publication_type, source, work['title'], abstract,
                                                   date_openalex, True, db)
            await create_publication_link(publication, pub_link_type_doi,
                                          work['doi'].replace('https://doi.org/', ''), db)
            for author in work['authorships']:
                author_db: Author | None
                author_name = "undefined undefined"
                if author['author']['display_name']:
                    author_name = author['author']['display_name'].split(' ', maxsplit=1)
                if author['author']['orcid']:
                    orcid = author['author']['orcid'].replace('https://orcid.org/', '')
                    identifier_result = await db.execute(select(AuthorIdentifier)
                    .filter(
                        and_(AuthorIdentifier.identifier_id == identifier_orcid.id,
                             AuthorIdentifier.identifier_value == orcid)).options(joinedload(AuthorIdentifier.author)))
                    identifier = identifier_result.scalars().first()
                    if identifier is None:
                        if len(author_name) > 1:
                            author_db = Author(
                                name=author_name[1],
                                surname=author_name[0],
                                confirmed=False
                            )
                        else:
                            author_db = Author(
                                name='-',
                                surname=author_name[0],
                                confirmed=False
                            )
                        db.add(author_db)
                        author_identifier = AuthorIdentifier(
                            author=author_db,
                            identifier=identifier_orcid,
                            identifier_value=orcid
                        )
                        db.add(author_identifier)
                    else:
                        author_db = identifier.author
                else:
                    if len(author_name) > 1:
                        author_db_result = await db.execute(select(Author)
                                                            .filter(and_(Author.name == author_name[0],
                                                                         Author.surname == author_name[1])))
                        author_db = author_db_result.scalars().first()
                    else:
                        author_db_result = await db.execute(select(Author)
                                                            .filter(and_(Author.name == '-',
                                                                         Author.surname == author_name[0])))
                        author_db = author_db_result.scalars().first()
                    if author_db is None:
                        if len(author_name) > 1:
                            author_db = Author(
                                name=author_name[0],
                                surname=author_name[1],
                                confirmed=False
                            )
                            db.add(author_db)
                        else:
                            author_db = Author(
                                name='-',
                                surname=author_name[0],
                                confirmed=False
                            )
                author_publication = AuthorPublication(
                    publication=publication,
                    author=author_db
                )
                db.add(author_publication)
                if not author['institutions']:
                    continue
                for institute in author['institutions']:
                    if institute['ror'] == 'https://ror.org/01kzjg088':
                        author_publication_organization = AuthorPublicationOrganization(
                            author_publication=author_publication,
                            organization=organization_omstu
                        )
                        db.add(author_publication_organization)
                    else:
                        organization_result = await db.execute(select(Organization)
                                                               .filter(Organization.name == institute['display_name']))
                        organization = organization_result.scalars().first()
                        if organization is None:
                            organization = Organization(name=institute['display_name'])
                            db.add(organization)
                        author_publication_organization = AuthorPublicationOrganization(
                            author_publication=author_publication,
                            organization=organization
                        )
                        db.add(author_publication_organization)
                    await db.commit()
            await db.commit()
    return {"message": "OK"}


def inverted_index_to_string(inverted_index):
    terms = sorted(list(inverted_index.keys()), key=lambda x: inverted_index[x][0])
    # Create an empty list to store the tokens
    tokens = {}
    # Iterate through the sorted terms
    for term in terms:
        # Iterate through the list of document positions and add the corresponding token
        for pos in inverted_index[term]:
            tokens[pos] = term

    # Join the tokens to form the string
    string = ' '.join(dict(sorted(tokens.items())).values())

    return string
