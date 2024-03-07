from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy.orm import joinedload

from src.model.model import Department, Faculty, Publication, Author, AuthorPublication, AuthorDepartment
from src.model.storage import get_count
from src.schemas.schemas import SchemeDepartment, SchemeFaculty, SchemePublication, SchemeAuthor


async def service_get_faculties(offset: int, limit: int, db: Session):
    query = select(Faculty).order_by(Faculty.id)
    faculties_result = await db.execute(query.offset(offset).limit(limit))
    faculties = faculties_result.scalars().all()
    count = await get_count(query, db)
    faculties_schemas = [SchemeFaculty.from_orm(faculty) for faculty in faculties]
    return dict(faculties=faculties_schemas, count=count)


async def service_get_departments(offset: int, limit: int, db: Session):
    query = select(Department).options(joinedload(Department.faculty))
    departments_result = await db.execute(query.offset(offset).limit(limit))
    departments = departments_result.scalars().all()
    count = await get_count(query, db)
    departments_schemas = [SchemeDepartment.from_orm(department) for department in departments]
    return dict(departments=departments_schemas, count=count)


async def service_get_faculty(id: int, db: Session):
    faculty_result = await db.execute(select(Faculty).filter(Faculty.id == id))
    faculty = faculty_result.scalars().first()
    if faculty is None:
        return None
    departments_result = await db.execute(select(Department).filter(Department.faculty_id == id))
    departments = departments_result.scalars().all()
    return dict(faculty=faculty, departments=departments)


async def service_get_department_publications(id: int, offset: int, limit: int, db: Session):
    query = select(Publication).join(AuthorPublication).join(Author).join(AuthorDepartment) \
        .filter(AuthorDepartment.department_id == id).order_by(desc(Publication.publication_date)) \
        .distinct()
    publications_result = await db.execute(query.options(joinedload(Publication.publication_type))
                                           .options(joinedload(Publication.source))
                                           .options(joinedload(Publication.publication_authors)
                                                    .joinedload(AuthorPublication.author))
                                           .offset(offset).limit(limit))
    publications = publications_result.scalars().unique().all()
    scheme_publications = [SchemePublication.from_orm(publication) for publication in publications]
    count = await get_count(query, db)
    return dict(publications=scheme_publications, count=count)


async def service_get_department_authors(id: int, db: Session):
    query = select(Author).join(AuthorDepartment).filter(AuthorDepartment.department_id == id).distinct()
    authors_result = await db.execute(query)
    authors = authors_result.scalars().unique().all()
    count = await get_count(query, db)
    scheme_authors = [SchemeAuthor.from_orm(author) for author in authors]
    return dict(authors=scheme_authors, count=count)
