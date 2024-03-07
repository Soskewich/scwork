from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession as Session
from src.model.database import get_db
from src.routers.analysis.controller import controller_get_publication_count, controller_get_source_rating_publications, \
    controller_get_organization_publications


from datetime import date

from src.schemas.routers import SchemeAnalysisRouter, SchemeAnalysisRatingRouter, SchemeAnalysisOrganizationRouter

router = APIRouter(
    prefix="/api/analysis",
    tags=["analysis"],
    responses={404: {"description": "Not found"}}
)


@router.get('/', response_model=SchemeAnalysisRouter)
async def get_publication_count(from_date: date = date(date.today().year - 5, 1, 1), to_date: date = date.today(),
                   db: Session = Depends(get_db)):
    result = await controller_get_publication_count(from_date, to_date, db)
    return result


@router.get('/source_rating', response_model=SchemeAnalysisRatingRouter)
async def get_source_rating_publications(from_date: date = date(date.today().year - 5, 1, 1), to_date: date = date.today(),
                   db: Session = Depends(get_db)):
    result = await controller_get_source_rating_publications(from_date, to_date, db)
    return result


@router.get('/organization', response_model=SchemeAnalysisOrganizationRouter)
async def get_organization_publications(search: str = None, max_count: int = 5, from_date: date = date(date.today().year - 5, 1, 1),
                   to_date: date = date.today(), db: Session = Depends(get_db)):
    result = await controller_get_organization_publications(search, max_count, from_date, to_date, db)
    return result

