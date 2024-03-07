from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession as Session
from src.model.database import get_db
from src.routers.dissertation.service import service_update_dissertation
from src.routers.nioktr.schema import Nioktr_params
from src.routers.nioktr.service import service_update_nioktr
from src.routers.nioktr.controller import controller_get_nioktrs, controller_get_nioktrs_by_id
from src.schemas.routers import SchemeNioktrsRouter, SchemeNioktrRouter

router = APIRouter(
    prefix="/api/dissertation",
    tags=["dissertation"],
    responses={404: {"description": "Not found"}}
)


@router.post("/upload/dissertation")
async def dissertation_update(db: Session = Depends(get_db)):
    message = await service_update_dissertation(db)
    return message

#
# @router.get("", response_model=SchemeDissertationsRouter)
# async def get_nioktrs(params: Dissertation_params = Depends(), db: Session = Depends(get_db)):
#     dissertations = await controller_get_dissertations(params, db)
#     return dissertations
#
#
# @router.get("/{id}", response_model=SchemeDissertationRouter)
# async def get_nioktr_by_id(id: int, db: Session = Depends(get_db)):
#     dissertations = await controller_get_dissertation_by_id(id, db)
#     return dissertation

