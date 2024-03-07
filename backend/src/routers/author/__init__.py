from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession as Session

from src.model.database import get_db
from src.routers.author.controller import controller_get_authors, controller_get_author, \
    controller_get_author_publications, controller_merge_authors, controller_get_unconfirmed_omstu_authors, \
    controller_delete_author_identifier, controller_update_author_identifier, controller_post_author_identifier, \
    controller_update_author, controller_post_author, controller_delete_author
from src.routers.user import controller_get_current_user
from src.schemas.routers import SchemePublicationsRouter, SchemeAuthorsRouter, SchemeAuthorRouter
from src.schemas.schemas import SchemeUser, SchemeAuthorIdentifier, SchemeAuthor

router = APIRouter(
    prefix="/api/author",
    tags=["author"],
    responses={404: {"description": "Not found"}}
)


@router.get("", response_model=SchemeAuthorsRouter)
async def get_authors(search: str = None,
                      page: int = 0, limit: int = 20, confirmed: bool = True,
                      db: Session = Depends(get_db)):
    authors = await controller_get_authors(search, page, limit, confirmed, db)
    return authors


@router.post("", response_model=SchemeAuthor)
async def post_author(name: str, surname: str, patronymic: str, confirmed: bool,
                      user: SchemeUser = Depends(controller_get_current_user),
                      db: Session = Depends(get_db)):
    author = await controller_post_author(user, name, surname, patronymic, confirmed, db)
    return author


@router.get("/unconfirmed_omstu", response_model=SchemeAuthorsRouter)
async def get_unconfirmed_omstu_authors(search: str = None,
                                        page: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    authors = await controller_get_unconfirmed_omstu_authors(search, page, limit, db)
    return authors


@router.get("/{id}", response_model=SchemeAuthorRouter)
async def get_author_by_id(id: int, db: Session = Depends(get_db)):
    author = await controller_get_author(id, db)
    return author


@router.put("/{id}")
async def update_author(id: int, name: str = None, surname: str = None, patronymic: str = None, confirmed: bool = None,
                        user: SchemeUser = Depends(controller_get_current_user),
                        db: Session = Depends(get_db)):
    author = await controller_update_author(user, id, name, surname, patronymic, confirmed, db)
    return author


@router.delete("/{id}")
async def delete_author(id: int, user: SchemeUser = Depends(controller_get_current_user),
                        db: Session = Depends(get_db)):
    response = await controller_delete_author(id, user, db)
    return response


@router.post("/{id}/identifier", response_model=SchemeAuthorIdentifier)
async def post_author_identifier(id: int, identifier_id: int, identifier_value: str, user: SchemeUser = Depends(controller_get_current_user), db: Session = Depends(get_db)):
    author_identifier = await controller_post_author_identifier(user, id, identifier_id, identifier_value, db)
    return author_identifier


@router.put("/{id}/identifier", response_model=SchemeAuthorIdentifier)
async def update_author_identifier(id: int, identifier_value: str,
                                   user: SchemeUser = Depends(controller_get_current_user),
                                   db: Session = Depends(get_db)):
    author_identifier = await controller_update_author_identifier(user, id, identifier_value, db)
    return author_identifier


@router.delete("/{id}/identifier")
async def delete_author_identifier(id: int, user: SchemeUser = Depends(controller_get_current_user), db: Session = Depends(get_db)):
    author_identifier = await controller_delete_author_identifier(user, id, db)
    return author_identifier


@router.get("/{id}/publications", response_model=SchemePublicationsRouter)
async def get_author_publications(id: int,
                                  page: int = 0, limit: int = 20,
                                  db: Session = Depends(get_db)):
    publications = await controller_get_author_publications(id, page, limit, db)
    return publications


@router.post("/{merged_id}/merge")
async def merge_authors(merged_id: int, base_id: int, user: SchemeUser = Depends(controller_get_current_user),
                        db: Session = Depends(get_db)):
    author = await controller_merge_authors(user, base_id, merged_id, db)
    return author

