from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession as Session

from src.model.database import get_db
from src.routers.publication.controller import controller_get_publications, controller_get_publication_by_id, \
    controller_get_publication_types, controller_post_author_publication, controller_delete_author_publication, \
    controller_get_publications_excel
from src.routers.publication.schema import Publication_params
from src.routers.user import controller_get_current_user
from src.schemas.routers import SchemePublicationsRouter, SchemePublicationRouter, SchemePublicationTypesRouter
from src.schemas.schemas import SchemeUser, SchemeAuthorPublication

router = APIRouter(
    prefix="/api/publication",
    tags=["publication"],
    responses={404: {"description": "Not found"}}
)


@router.get("/publication_types", response_model=SchemePublicationTypesRouter)
async def get_publication_types(db: Session = Depends(get_db)):
    publication_types = await controller_get_publication_types(db)
    return publication_types


@router.get("", response_model=SchemePublicationsRouter)
async def get_publications(params: Publication_params = Depends(), db: Session = Depends(get_db)):
    publications = await controller_get_publications(params, db)
    return publications


@router.get("/excel")
async def get_publication_excel(params: Publication_params = Depends(), db: Session = Depends(get_db)):
    excel = await controller_get_publications_excel(params, db)
    return excel


@router.get("/{id}", response_model=SchemePublicationRouter)
async def get_publication_by_id(id: int, db: Session = Depends(get_db)):
    publication = await controller_get_publication_by_id(id, db)
    return publication


@router.post("/{id}/author")
async def post_author_publication(id: int, author_id: int,
                                  user: SchemeUser = Depends(controller_get_current_user),
                                  db: Session = Depends(get_db)):
    author_publication = await controller_post_author_publication(user, id, author_id, db)
    return author_publication


@router.delete("/{id}/author")
async def delete_author_publication(id: int, author_id: int, user:
                                    SchemeUser = Depends(controller_get_current_user),
                                    db: Session = Depends(get_db)):
    author_identifier = await controller_delete_author_publication(user, id, author_id, db)
    return author_identifier
