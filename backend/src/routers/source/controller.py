from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession as Session

from src.routers.source.service import service_get_sources, service_get_sources_search, service_get_source, \
    service_get_source_publications, service_source_rating_types, service_get_source_types


async def controller_get_sources(search: str, page: int, limit: int, db: Session):
    offset = page * limit
    if (search is None) or (search == ""):
        sources = await service_get_sources(offset, limit, db)
        return sources
    else:
        sources = await service_get_sources_search(search, offset, limit, db)
        return sources


async def controller_get_source(id: int, db: Session):
    source = await service_get_source(id, db)
    if not source:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return source


async def controller_get_source_publications(id: int, page: int, limit: int, db: Session):
    offset = page * limit
    publications = await service_get_source_publications(id, offset, limit, db)
    return publications


async def controller_source_rating_types(db: Session):
    source_rating_types = await service_source_rating_types(db)
    return source_rating_types


async def controller_get_source_types(db: Session):
    source_types = await service_get_source_types(db)
    return source_types

