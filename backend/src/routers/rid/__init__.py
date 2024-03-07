from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession as Session
from src.model.database import get_db
from src.routers.rid.schema import Rid_params
from src.routers.rid.service import service_update_rid
from src.routers.rid.controller import controller_get_rids_by_id, controller_get_rids
from src.schemas.routers import SchemeRidsRouter, SchemeRidRouter

router = APIRouter(
    prefix="/api/rid",
    tags=["rid"],
    responses={404: {"description": "Not found"}}
)


@router.post("/upload/rid")
async def rid_update(db: Session = Depends(get_db)):
    message = await service_update_rid(db)
    return message


@router.get("", response_model=SchemeRidsRouter)
async def get_rids(params: Rid_params = Depends(), db: Session = Depends(get_db)):
    rids = await controller_get_rids(params, db)
    return rids


@router.get("/{id}", response_model=SchemeRidRouter)
async def get_rid_by_id(id: int, db: Session = Depends(get_db)):
    rid = await controller_get_rids_by_id(id, db)
    return rid

