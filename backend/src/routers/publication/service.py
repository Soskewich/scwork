import io

import pandas
from sqlalchemy import func, desc, select, and_
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy.orm import joinedload
from starlette.responses import StreamingResponse

from src.model.model import Publication, AuthorPublication, Source, SourceRating, PublicationType, \
    Author, AuthorDepartment, KeywordPublication, PublicationLink, AuthorPublicationOrganization, SourceLink, \
    AuthorIdentifier, PublicationTypeView
from src.model.storage import get_count
from src.routers.publication.schema import Publication_params
from src.schemas.schemas import SchemePublication, SchemePublicationPage


async def service_get_publications(params: Publication_params, db: Session):
    query = select(Publication).filter(Publication.accepted == True)
    query = query.filter(Publication.publication_date >= params.from_date) \
        .filter(Publication.publication_date <= params.to_date)

    if not (params.search is None) and params.search != "":
        query = query.filter(func.lower(Publication.title).contains(params.search.lower()))
    if not (params.source_rating_type_id is None):
        query = query.join(Source).join(SourceRating) \
            .filter(SourceRating.source_rating_type_id == params.source_rating_type_id)
    if not (params.publication_type_id is None):
        query = query.join(PublicationType).filter(PublicationType.view_id == params.publication_type_id).distinct()
    if not (params.author_id is None):
        query = query.join(AuthorPublication).filter(AuthorPublication.author_id == params.author_id).distinct()
    if not (params.department_id is None):
        query = query.join(AuthorPublication).join(Author).join(AuthorDepartment) \
            .filter(AuthorDepartment.department_id == params.department_id).distinct()
    offset = params.limit * params.page
    publications_result = await db.execute(query.order_by(desc(Publication.publication_date))
                                           .order_by(Publication.title)
                                           .options(joinedload(Publication.publication_type))
                                           .options(joinedload(Publication.source)
                                                    .joinedload(Source.source_links)
                                                    .joinedload(SourceLink.source_link_type))
                                           .options(joinedload(Publication.publication_authors)
                                                    .joinedload(AuthorPublication.author))
                                           .options(joinedload(Publication.publication_links)
                                                    .joinedload(PublicationLink.publication_link_type))
                                           .offset(offset).limit(params.limit))
    publications = publications_result.scalars().unique().all()
    scheme_publications = [SchemePublication.from_orm(publication) for publication in publications]
    count = await get_count(query, db)
    return dict(publications=scheme_publications, count=count)


async def service_get_publications_excel(params: Publication_params, db: Session):
    query = select(Publication).filter(Publication.accepted == True)
    query = query.filter(Publication.publication_date >= params.from_date) \
        .filter(Publication.publication_date <= params.to_date)

    if not (params.search is None) and params.search != "":
        query = query.filter(func.lower(Publication.title).contains(params.search.lower()))
    if not (params.source_rating_type_id is None):
        query = query.join(Source).join(SourceRating) \
            .filter(SourceRating.source_rating_type_id == params.source_rating_type_id)
    if not (params.publication_type_id is None):
        query = query.join(PublicationType).filter(PublicationType.view_id == params.publication_type_id).distinct()
    if not (params.author_id is None):
        query = query.join(AuthorPublication).filter(AuthorPublication.author_id == params.author_id).distinct()
    if not (params.department_id is None):
        query = query.join(AuthorPublication).join(Author).join(AuthorDepartment) \
            .filter(AuthorDepartment.department_id == params.department_id).distinct()
    publications_result = await db.execute(query.order_by(desc(Publication.publication_date))
                                           .order_by(Publication.title)
                                           .options(joinedload(Publication.source)
                                                    .joinedload(Source.source_links)
                                                    .joinedload(SourceLink.source_link_type))
                                           .options(joinedload(Publication.source)
                                                    .joinedload(Source.source_ratings)
                                                    .joinedload(SourceRating.source_rating_type))
                                           .options(joinedload(Publication.publication_authors)
                                                    .joinedload(AuthorPublication.author)
                                                    .joinedload(Author.author_identifiers)
                                                    .joinedload(AuthorIdentifier.identifier))
                                           .options(joinedload(Publication.publication_links)
                                                    .joinedload(PublicationLink.publication_link_type))
                                           .offset(params.page).limit(params.limit))
    publications = publications_result.scalars().unique().all()
    data_list = []
    for publication in publications:
        try:
            issn = next(link.link for link in publication.source.source_links if link.source_link_type.name == 'ISSN')
        except StopIteration:
            issn = '-'
        try:
            eissn = next(link.link for link in publication.source.source_links if link.source_link_type.name == 'eISSN')
        except StopIteration:
            eissn = '-'
        try:
            doi = next(doi.link for doi in publication.publication_links if doi.publication_link_type.name == 'DOI')
        except StopIteration:
            doi = '-'
        data = {
            'Publication': publication.title,
            'Date': publication.publication_date,
            'DOI': doi,
            'Authors': '; '.join([f'{publication_author.author.name} {publication_author.author.surname}'
                                  for publication_author in publication.publication_authors]),
            # 'Authors Identifiers': '; '.join([', '.join([f'{identifier.identifier.name}: {identifier.identifier_value}'
            #                                              for identifier
            #                                              in author_publication.author.author_identifiers])
            #                                   for author_publication in publication.publication_authors]),
            'Source': publication.source.name,
            'ISSN': issn,
            'eISSN': eissn,
            'Ratings': '/'.join([f'{source_rating.source_rating_type.name}: {source_rating.rating}'
                                 for source_rating in publication.source.source_ratings]),
            'OmSTU fraction': publication.rate
        }
        data_list.append(data)
    df = pandas.DataFrame(data_list)
    output = io.BytesIO()
    writer = pandas.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False)
    writer.save()
    xlsx_data = output.getvalue()
    return StreamingResponse(
            io.BytesIO(xlsx_data),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename=output.xlsx"}
    )


async def service_get_publication(id: int, db: Session):
    publication_result = await db.execute(select(Publication).filter(Publication.id == id)
                                          .options(joinedload(Publication.publication_type))
                                          .options(joinedload(Publication.source)
                                                   .joinedload(Source.source_links)
                                                   .joinedload(SourceLink.source_link_type))
                                          .options(joinedload(Publication.publication_authors)
                                                   .joinedload(AuthorPublication.author))
                                          .options(joinedload(Publication.publication_authors)
                                                   .joinedload(AuthorPublication.author_publication_organizations)
                                                   .joinedload(AuthorPublicationOrganization.organization)
                                                   )
                                          .options(joinedload(Publication.keyword_publications)
                                                   .joinedload(KeywordPublication.keyword))
                                          .options(joinedload(Publication.publication_links)
                                                   .joinedload(PublicationLink.publication_link_type)))
    publication = publication_result.scalars().first()
    if publication is None:
        return False
    scheme_publication = SchemePublicationPage.from_orm(publication)
    return dict(publication=scheme_publication)


async def service_get_publication_publication_types(db: Session):
    publcation_types = await db.execute(select(PublicationTypeView))
    return dict(publication_types=publcation_types.scalars().all())


async def service_post_author_publication(id: int, author_id: int, db: Session):
    author_publication = AuthorPublication(
        publication_id=id,
        author_id=author_id,
    )
    db.add(author_publication)
    await db.commit()
    return dict(publication=id)


async def service_delete_author_publication(id: int, author_id: int, db: Session):
    author_publication_result = await db.execute(select(AuthorPublication)
                                                 .filter(and_(AuthorPublication.publication_id == id,
                                                              AuthorPublication.author_id == author_id)))
    author_publication = author_publication_result.scalars().first()
    if not author_publication:
        return None

    author_publication_organizations_result = await db.execute(select(AuthorPublicationOrganization)
                                                               .filter(AuthorPublicationOrganization
                                                                       .author_publication == author_publication))
    author_publication_organizations = author_publication_organizations_result.scalars().all()
    for author_publication_organization in author_publication_organizations:
        await db.delete(author_publication_organization)
    await db.delete(author_publication)
    await db.commit()
    return dict(message="OK")
