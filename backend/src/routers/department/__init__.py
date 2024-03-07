from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession as Session

from src.model.database import get_db
from src.routers.department.controller import controller_get_departments, controller_get_faculties, \
    controller_get_faculty, controller_department_publication, controller_department_authors

router = APIRouter(
    prefix="/api/faculty",
    tags=["faculty"],
    responses={404: {"description": "Not found"}}
)


@router.get("")
async def get_faculties(page: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    faculties = await controller_get_faculties(page, limit, db)
    return faculties


@router.get("/{id}")
async def get_faculty(id: int, db: Session = Depends(get_db)):
    faculty = await controller_get_faculty(id, db)
    return faculty


@router.get("/departments/all")
async def get_departments(page: int = 0, limit: int = 20,
                      db: Session = Depends(get_db)):
    departments = await controller_get_departments(page, limit, db)
    return departments


@router.get("/departments/{id}/publications")
async def get_departments_publications(id: int, page: int = 0, limit: int = 20,
                      db: Session = Depends(get_db)):
    publications = await controller_department_publication(id, page, limit, db)
    return publications


@router.get('/departments/{id}/authors')
async def get_departments_authors(id: int, db: Session = Depends(get_db)):
    authors = await controller_department_authors(id, db)
    return authors
