from datetime import date

from fastapi import HTTPException, status, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession as Session

from src.routers.admin.openalex_service import service_update_from_openalex
from src.routers.admin.pandas_service import service_fill_authors, service_fill_scopus, service_white_list_fill, \
    service_jcr_list_fill, service_white_list_jcr_citescore, service_fill_vak_journals_rank, \
    service_fill_rsci_journals_rank, service_fill_elibrary, service_fill_author_department, \
    service_vak_list_fill
from src.routers.admin.service import service_admin_check, service_get_feedbacks
from src.schemas.schemas import SchemeUser


async def controller_get_feedbacks(page: int, limit: int, solved: bool, user: SchemeUser, db: Session):
    is_admin = await service_admin_check(user.role_id, db)
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Доступ запрещен")
    offset = page * limit
    feedbacks = await service_get_feedbacks(offset, limit, solved, db)
    return feedbacks


async def controller_fill_authors(file: UploadFile, user: SchemeUser, db: Session):
    is_admin = await service_admin_check(user.role_id, db)
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Доступ запрещен")
    message = await service_fill_authors(file, db)
    return message


async def controller_fill_author_departments(file: UploadFile, user: SchemeUser, db: Session):
    is_admin = await service_admin_check(user.role_id, db)
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Доступ запрещен")
    message = await service_fill_author_department(file, db)
    return message

async def controller_fill_scopus(rating_date: date, file: UploadFile, user: SchemeUser, db: Session):
    is_admin = await service_admin_check(user.role_id, db)
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Доступ запрещен")
    message = await service_fill_scopus(rating_date, file, db)
    return message


async def controller_fill_elibrary(file: UploadFile, user: SchemeUser, db: Session):
    is_admin = await service_admin_check(user.role_id, db)
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Доступ запрещен")
    message = await service_fill_elibrary(file, db)
    return message


async def controller_fill_white_list(rating_date: date, file: UploadFile, user: SchemeUser, db: Session):
    is_admin = await service_admin_check(user.role_id, db)
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Доступ запрещен")
    message = await service_white_list_fill(rating_date, file, db)
    return message


async def controller_jcr_list_fill(rating_date: date, file: UploadFile, user: SchemeUser, db: Session):
    is_admin = await service_admin_check(user.role_id, db)
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Доступ запрещен")
    message = await service_jcr_list_fill(rating_date, file, db)
    return message


async def controller_whitelist_jcr_citescore(rating_date: date, file: UploadFile, user: SchemeUser, db: Session):
    is_admin = await service_admin_check(user.role_id, db)
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Доступ запрещен")
    message = await service_white_list_jcr_citescore(rating_date, file, db)
    return message


async def controller_vak_journals_rank(rating_date: date, file: UploadFile, user: SchemeUser, db: Session):
    is_admin = await service_admin_check(user.role_id, db)
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Доступ запрещен")
    message = await service_fill_vak_journals_rank(rating_date, file, db)
    return message


async def controller_rsci_journals_rank(rating_date: date, file: UploadFile, user: SchemeUser, db: Session):
    is_admin = await service_admin_check(user.role_id, db)
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Доступ запрещен")
    message = await service_fill_rsci_journals_rank(rating_date, file, db)
    return message


async def controller_fill_from_openalex(user: SchemeUser, db: Session):
    is_admin = await service_admin_check(user.role_id, db)
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Доступ запрещен")
    message = await service_update_from_openalex(db)
    return message


async def controller_vak_list_fill(file: UploadFile, user: SchemeUser, db: Session):
    is_admin = await service_admin_check(user.role_id, db)
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Доступ запрещен")
    message = await service_vak_list_fill(file, db)
    return message
