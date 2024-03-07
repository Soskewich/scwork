from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession as Session

from src.routers.feedback.service import service_post_feedback
from src.schemas.routers import SchemeFeedbackPostRouter


async def controller_post_feedback(feedback: SchemeFeedbackPostRouter, db: Session):
    message = await service_post_feedback(feedback, db)
    if message:
        return message
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
