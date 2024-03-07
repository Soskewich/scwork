from sqlalchemy.ext.asyncio import AsyncSession as Session
from datetime import date

from src.routers.analysis.service import service_get_publication_count, service_get_source_rating_publications, \
    service_get_organization_publication


async def controller_get_publication_count(from_date: date, to_date: date, db: Session):
    result = await service_get_publication_count(from_date, to_date, db)
    return result


async def controller_get_source_rating_publications(from_date: date, to_date: date, db: Session):
    result = await service_get_source_rating_publications(from_date, to_date, db)
    return result


async def controller_get_organization_publications(search: str, max_count: int,
                                                   from_date: date, to_date: date, db: Session):
    result = await service_get_organization_publication(search, max_count, from_date, to_date, db)
    return result