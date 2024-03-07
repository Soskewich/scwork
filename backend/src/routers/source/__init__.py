from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession as Session

from src.model.database import get_db
from src.routers.source.controller import controller_get_sources, controller_get_source, \
    controller_get_source_publications, controller_source_rating_types, controller_get_source_types
from src.schemas.routers import SchemeSourcesRouter, SchemeSourceRouter, SchemePublicationsRouter

router = APIRouter(
    prefix="/api/source",
    tags=["source"],
    responses={404: {"description": "Not found"}}
)


@router.get("", response_model=SchemeSourcesRouter)
async def get_sources(search: str = None,
                      page: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    sources = await controller_get_sources(search, page, limit, db)
    return sources


@router.get('/source_types')
async def get_source_types(db: Session = Depends(get_db)):
    source_types = await controller_get_source_types(db)
    return source_types


@router.get("/source_rating_types")
async def get_source_rating_types(db: Session = Depends(get_db)):
    source_rating_types = await controller_source_rating_types(db)
    return source_rating_types


@router.get("/{id}", response_model=SchemeSourceRouter)
async def get_source(id: int, db: Session = Depends(get_db)):
    source = await controller_get_source(id, db)
    return source


@router.get('/{id}/publications', response_model=SchemePublicationsRouter)
async def get_source_publications(id: int, page: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    publications = await controller_get_source_publications(id, page, limit, db)
    return publications

