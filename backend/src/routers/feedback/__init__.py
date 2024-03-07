from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession as Session

from src.model.database import get_db
from src.routers.feedback.controller import controller_post_feedback
from src.schemas.routers import SchemeFeedbackPostRouter

router = APIRouter(
    prefix="/api/feedback",
    tags=["feedback"],
    responses={404: {"description": "Not found"}}
)


@router.post('')
async def post_feedback(feedback: SchemeFeedbackPostRouter, db: Session = Depends(get_db)):
    message = await controller_post_feedback(feedback, db)
    return message
