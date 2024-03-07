from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession as Session
from src.routers.nioktr import Nioktr_params
from src.routers.nioktr.service import service_get_nioktrs, service_get_nioktr


async def controller_get_nioktrs(params: Nioktr_params, db: Session):
    nioktrs = await service_get_nioktrs(params, db)
    return nioktrs


async def controller_get_nioktrs_by_id(id: int, db: Session):
    nioktr = await service_get_nioktr(id, db)
    if not nioktr:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return nioktr


