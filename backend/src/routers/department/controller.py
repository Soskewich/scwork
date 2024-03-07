from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession as Session

from src.routers.department.service import service_get_departments, service_get_faculties, service_get_faculty, \
    service_get_department_publications, service_get_department_authors


async def controller_get_departments(page: int, limit: int, db: Session):
    offset = page * limit
    departments = await service_get_departments(offset, limit, db)
    return departments


async def controller_get_faculties(page: int, limit: int, db: Session):
    offset = page * limit
    faculties = await service_get_faculties(offset, limit, db)
    return faculties


async def controller_get_faculty(id: int, db: Session):
    faculty = await service_get_faculty(id, db)
    if not faculty:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return faculty


async def controller_department_publication(id: int, page: int, limit: int, db: Session):
    offset = page * limit
    publications = await service_get_department_publications(id, offset, limit, db)
    if not publications:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return publications


async def controller_department_authors(id: int, db: Session):
    authors = await service_get_department_authors(id, db)
    if not authors:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return authors
