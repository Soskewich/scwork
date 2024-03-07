from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession as Session

from src.routers.admin.service import service_admin_check
from src.routers.publication.schema import Publication_params
from src.routers.publication.service import service_get_publications, service_get_publication, \
    service_get_publication_publication_types, service_post_author_publication, service_delete_author_publication, \
    service_get_publications_excel
from src.schemas.schemas import SchemeUser


async def controller_get_publications(params: Publication_params, db: Session):
    publications = await service_get_publications(params, db)
    return publications


async def controller_get_publications_excel(params: Publication_params, db: Session):
    excel = await service_get_publications_excel(params, db)
    return excel


async def controller_get_publication_by_id(id: int, db: Session):
    publication = await service_get_publication(id, db)
    if not publication:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return publication


async def controller_get_publication_types(db: Session):
    publication_types = await service_get_publication_publication_types(db)
    return publication_types


async def controller_post_author_publication(user: SchemeUser, id: int, author_id: int, db: Session):
    is_admin = await service_admin_check(user.role_id, db)
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Доступ запрещен")
    message = await service_post_author_publication(id, author_id, db)
    return message


async def controller_delete_author_publication(user: SchemeUser, id: int, author_id: int, db: Session):
    is_admin = await service_admin_check(user.role_id, db)
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Доступ запрещен")
    message = await service_delete_author_publication(id, author_id, db)
    if not message:
        raise HTTPException(status_code=status.HTTP_400)
    return message
