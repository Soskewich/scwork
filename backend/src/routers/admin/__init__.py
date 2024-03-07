from datetime import date

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession as Session

from src.model.database import get_db
from src.routers.admin.controller import controller_get_feedbacks, controller_fill_authors, \
    controller_fill_scopus, controller_fill_white_list, controller_jcr_list_fill, controller_whitelist_jcr_citescore, \
    controller_vak_journals_rank, controller_rsci_journals_rank, controller_fill_from_openalex, \
    controller_fill_elibrary, controller_fill_author_departments, controller_vak_list_fill
from src.routers.user import controller_get_current_user
from src.schemas.routers import SchemeFeedbacksGetRouter
from src.schemas.schemas import SchemeUser

router = APIRouter(
    prefix="/api/admin",
    tags=["admin"],
    responses={404: {"description": "Not found"}}
)


@router.get("/feedbacks", response_model=SchemeFeedbacksGetRouter)
async def get_feedbacks(page: int = 0, limit: int = 20, solved: bool = False,
                        user: SchemeUser = Depends(controller_get_current_user), db: Session = Depends(get_db)):
    feedbacks = await controller_get_feedbacks(page, limit, solved, user, db)
    return feedbacks


@router.post('/upload/authors')
async def authors_fill(file: UploadFile = File(...),
                       user: SchemeUser = Depends(controller_get_current_user), db: Session = Depends(get_db)):
    message = await controller_fill_authors(file, user, db)
    return message


@router.post('/upload/author_department')
async def authors_fill(file: UploadFile = File(...),
                       user: SchemeUser = Depends(controller_get_current_user), db: Session = Depends(get_db)):
    message = await controller_fill_author_departments(file, user, db)
    return message


@router.post("/upload/white_list_upgraded")
async def jcr_fill(rating_date: date = date.today(), file: UploadFile = File(...),
                      user: SchemeUser = Depends(controller_get_current_user), db: Session = Depends(get_db)):
    message = await controller_whitelist_jcr_citescore(rating_date, file, user, db)
    return message


@router.post("/upload/vak_with_rank")
async def vak_fill(rating_date: date = date.today(), file: UploadFile = File(...),
                      user: SchemeUser = Depends(controller_get_current_user), db: Session = Depends(get_db)):
    message = await controller_vak_journals_rank(rating_date, file, user, db)
    return message


@router.post("/upload/rsci_journals_rank")
async def rsci_fill(rating_date: date = date.today(), file: UploadFile = File(...),
                      user: SchemeUser = Depends(controller_get_current_user), db: Session = Depends(get_db)):
    message = await controller_rsci_journals_rank(rating_date, file, user, db)
    return message


@router.post("/upload/scopus")
async def scopus_fill(rating_date: date = date.today(), file: UploadFile = File(...),
                      user: SchemeUser = Depends(controller_get_current_user), db: Session = Depends(get_db)):
    message = await controller_fill_scopus(rating_date, file, user, db)
    return message


@router.post('/upload/elibrary')
async def elibrary_fill(file: UploadFile = File(...),
                        user: SchemeUser = Depends(controller_get_current_user), db: Session = Depends(get_db)):
    message = await controller_fill_elibrary(file, user, db)
    return message


@router.post("/upload/white_list")
async def white_list_fill(rating_date: date = date.today(), file: UploadFile = File(...),
                          user: SchemeUser = Depends(controller_get_current_user), db: Session = Depends(get_db)):
    message = await controller_fill_white_list(rating_date, file, user, db)
    return message


@router.post("/upload/jcr")
async def jcr_fill(rating_date: date = date.today(), file: UploadFile = File(...),
                      user: SchemeUser = Depends(controller_get_current_user), db: Session = Depends(get_db)):
    message = await controller_jcr_list_fill(rating_date, file, user, db)
    return message


@router.post("/update/openalex")
async def openalex_update(user: SchemeUser = Depends(controller_get_current_user), db: Session = Depends(get_db)):
    message = await controller_fill_from_openalex(user, db)
    return message


@router.post("/update/vak_list")
async def vak_list_update(user: SchemeUser = Depends(controller_get_current_user),
                          file: UploadFile = File(...), db: Session = Depends(get_db)):
    message = await controller_vak_list_fill(file, user, db)
    return message
