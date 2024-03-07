from sqlalchemy.ext.asyncio import AsyncSession as Session
from datetime import date
from src.model.model import Feedback
from src.schemas.routers import SchemeFeedbackPostRouter
from settings_env import settings
from src.utils.aiohttp import SingletonAiohttp


async def service_post_feedback(feedback: SchemeFeedbackPostRouter, db: Session):
    r = await SingletonAiohttp.post_query_url(f"https://www.google.com/recaptcha/api/siteverify", data={
        'secret': settings.RECAPTCHA_SECRET_KEY,
        'response': feedback.token
    })
    if r['success']:
        feedback_model = Feedback(
            name=feedback.feedback.name,
            mail=feedback.feedback.mail,
            message=feedback.feedback.message,
            date=date.today(),
            solved=False
        )
        db.add(feedback_model)
        await db.commit()
        return dict(message='OK')
    else:
        return False
