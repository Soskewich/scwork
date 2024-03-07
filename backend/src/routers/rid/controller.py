from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession as Session
from src.routers.rid import Rid_params
from src.routers.rid.service import service_get_rid, service_get_rids


async def controller_get_rids(params: Rid_params, db: Session):
    rids = await service_get_rids(params, db)
    return rids


async def controller_get_rids_by_id(id: int, db: Session):
    rid = await service_get_rid(id, db)
    if not rid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return rid
