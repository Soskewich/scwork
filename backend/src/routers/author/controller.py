from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession as Session

from src.routers.admin.service import service_admin_check
from src.routers.author.service import service_get_authors, service_get_authors_search, \
    service_get_author, service_get_author_publications, service_merge_authors, service_get_unconfirmed_omstu_authors, \
    service_update_author_identifier, service_delete_author_identifier, service_update_authors, \
    service_post_author_identifier, service_post_authors, service_delete_author
from src.schemas.schemas import SchemeUser


async def controller_get_authors(search: str, page: int, limit: int, confirmed: bool, db: Session):
    offset = page * limit
    if search is None and search != "":
        authors = await service_get_authors(offset, limit, confirmed, db)
        return authors
    else:
        authors = await service_get_authors_search(search, offset, limit, confirmed, db)
        return authors


async def controller_get_author(id: int, db: Session):
    author = await service_get_author(id, db)
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return author


async def controller_post_author(user: SchemeUser, name: str, surname: str, patronymic: str,
                                   confirmed: bool, db: Session):
    is_admin = await service_admin_check(user.role_id, db)
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Доступ запрещен")
    message = await service_post_authors(name, surname, patronymic, confirmed, db)
    return message


async def controller_delete_author(id: int, user: SchemeUser, db: Session):
    is_admin = await service_admin_check(user.role_id, db)
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Доступ запрещен")
    message = await service_delete_author(id, db)
    return message


async def controller_get_author_publications(id: int, page: int, limit: int, db: Session):
    offset = page * limit
    publications = await service_get_author_publications(id, offset, limit, db)
    return publications


async def controller_get_unconfirmed_omstu_authors(search: str, page: int, limit: int, db: Session):
    offset = page * limit
    authors = await service_get_unconfirmed_omstu_authors(search, offset, limit, db)
    return authors


async def controller_merge_authors(user: SchemeUser, id_base: int, id_merge: int, db: Session):
    is_admin = await service_admin_check(user.role_id, db)
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Доступ запрещен")
    message = await service_merge_authors(id_base, id_merge, db)
    return message


async def controller_post_author_identifier(user: SchemeUser, id: int, identifier_id: int, identifier_value: str, db: Session):
    is_admin = await service_admin_check(user.role_id, db)
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Доступ запрещен")
    message = await service_post_author_identifier(id, identifier_id, identifier_value, db)
    return message


async def controller_delete_author_identifier(user: SchemeUser, id: int, db: Session):
    is_admin = await service_admin_check(user.role_id, db)
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Доступ запрещен")
    message = await service_delete_author_identifier(id, db)
    return message


async def controller_update_author_identifier(user: SchemeUser, id: int, identifier_value: str, db: Session):
    is_admin = await service_admin_check(user.role_id, db)
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Доступ запрещен")
    message = await service_update_author_identifier(id, identifier_value, db)
    return message


async def controller_update_author(user: SchemeUser, id: int, name: str, surname: str, patronymic: str,
                                   confirmed: bool, db: Session):
    is_admin = await service_admin_check(user.role_id, db)
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Доступ запрещен")
    message = await service_update_authors(id, name, surname, patronymic, confirmed, db)
    return message