from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession as Session
from src.model.database import get_db
from src.routers.nioktr.schema import Nioktr_params
from src.routers.nioktr.service import service_update_nioktr
from src.routers.nioktr.controller import controller_get_nioktrs, controller_get_nioktrs_by_id
from src.schemas.routers import SchemeNioktrsRouter, SchemeNioktrRouter

router = APIRouter(
    prefix="/api/nioktr",
    tags=["nioktr"],
    responses={404: {"description": "Not found"}}
)


@router.post("/update/nioktr")
async def nioktr_update(db: Session = Depends(get_db)):
    message = await service_update_nioktr(db)
    return message


@router.get("", response_model=SchemeNioktrsRouter)
async def get_nioktrs(params: Nioktr_params = Depends(), db: Session = Depends(get_db)):
    nioktrs = await controller_get_nioktrs(params, db)
    return nioktrs


@router.get("/{id}", response_model=SchemeNioktrRouter)
async def get_nioktr_by_id(id: int, db: Session = Depends(get_db)):
    nioktr = await controller_get_nioktrs_by_id(id, db)
    return nioktr

