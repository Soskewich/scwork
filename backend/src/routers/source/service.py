from sqlalchemy import func, desc, or_, select
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy.orm import joinedload

from src.model.model import Source, Publication, SourceLink, SourceRatingType, SourceRating, AuthorPublication, \
    PublicationLink, SourceType, SourceRatingSubject
from src.model.storage import get_count
from src.schemas.schemas import SchemeSourceWithType, SchemeSourceWithRating, SchemePublication


async def service_get_sources(offset: int, limit: int, db: Session):
    query = select(Source).options(joinedload(Source.source_type)).options(joinedload(Source.publications))\
        .join(Source.publications, isouter=True)\
        .order_by(desc(func.count(Source.publications))).group_by(Source.id)
    sources_result = await db.execute(query.offset(offset).limit(limit))
    sources = sources_result.scalars().unique().all()
    count = await get_count(query, db)
    scheme_sources = [SchemeSourceWithType.from_orm(source) for source in sources]
    return dict(sources=scheme_sources, count=count)


async def service_get_sources_search(search: str, offset: int, limit: int, db: Session):
    query = select(Source).options(joinedload(Source.source_type)).options(joinedload(Source.publications))\
        .join(Source.publications, isouter=True)\
        .order_by(desc(func.count(Source.publications))).group_by(Source.id)
    query = query.options(joinedload(Source.source_links)).join(Source.source_links)\
        .filter(func.lower(Source.name).contains(search.lower()))
    sources_result = await db.execute(query.offset(offset).limit(limit))
    sources = sources_result.scalars().unique().all()
    count = await get_count(query, db)
    scheme_sources = [SchemeSourceWithType.from_orm(source) for source in sources]
    return dict(sources=scheme_sources, count=count)


async def service_get_source(id: int, db: Session):
    query = select(Source).filter(Source.id == id).options(joinedload(Source.source_type))\
        .options(joinedload(Source.source_links).joinedload(SourceLink.source_link_type))\
        .options(joinedload(Source.source_ratings).joinedload(SourceRating.source_rating_type))\
        .options(joinedload(Source.source_ratings).joinedload(SourceRating.source_rating_subjects)
                 .joinedload(SourceRatingSubject.subject))\
        .options(joinedload(Source.source_ratings).joinedload(SourceRating.source_rating_dates))
    source_result = await db.execute(query)
    source = source_result.scalars().first()
    if source is None:
        return False
    scheme_source = SchemeSourceWithRating.from_orm(source)
    return dict(source=scheme_source)


async def service_get_source_publications(id: int, offset: int, limit: int, db: Session):
    query = select(Publication).join(Source).order_by(desc(Publication.publication_date))\
        .order_by(Publication.title).filter(Source.id == id)
    publications_result = await db.execute(query.options(joinedload(Publication.publication_type))
                                           .options(joinedload(Publication.source)
                                                    .joinedload(Source.source_links)
                                                    .joinedload(SourceLink.source_link_type))
                                           .options(joinedload(Publication.publication_authors)
                                                    .joinedload(AuthorPublication.author))
                                           .options(joinedload(Publication.publication_links)
                                                    .joinedload(PublicationLink.publication_link_type))
                                           .offset(offset).limit(limit))

    publications = publications_result.scalars().unique().all()
    scheme_publications = [SchemePublication.from_orm(publication) for publication in publications]
    count = await get_count(query, db)
    return dict(publications=scheme_publications, count=count)


async def service_get_source_types(db: Session):
    source_types = await db.execute(select(SourceType))
    return dict(source_types=source_types.scalars().all())


async def service_source_rating_types(db: Session):
    source_rating_types = await db.execute(select(SourceRatingType))
    return dict(source_rating_types=source_rating_types.scalars().all())

