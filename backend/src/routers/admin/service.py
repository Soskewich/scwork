from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession as Session
from passlib.hash import bcrypt

from settings_env import settings
from src.model.model import Role, User, Feedback
from src.model.storage import get_count
from src.schemas.schemas import SchemeFeedbackOutput


async def service_create_admin(db: Session):
    admin_role_result = await db.execute(select(Role).filter(Role.name == "Admin"))
    admin_role = admin_role_result.scalars().first()
    if admin_role is None:
        admin_role = Role(name="Admin")
        db.add(admin_role)
        await db.commit()
    admin_result = await db.execute(select(User).filter(User.login == settings.ADMIN_LOGIN))
    admin = admin_result.scalars().first()
    if admin is None:
        admin = User(login=settings.ADMIN_LOGIN, password=bcrypt.hash(settings.ADMIN_PASSWORD), role=admin_role)
        db.add(admin)
        await db.commit()


async def service_admin_check(role_id: int, db: Session):
    role_result = await db.execute(select(Role).filter(Role.id == role_id))
    role = role_result.scalars().first()
    if role is None:
        return False
    if role.name == "Admin":
        return True
    return False


async def service_get_feedbacks(offset: int, limit: int, solved: bool, db: Session):
    query = select(Feedback).filter(Feedback.solved == solved).order_by(desc(Feedback.date))
    feedbacks_result = await db.execute(query.offset(offset).limit(limit))
    feedbacks = feedbacks_result.scalars().all()
    scheme_feedbacks = [SchemeFeedbackOutput.from_orm(feedback) for feedback in feedbacks]
    count = await get_count(query, db)
    return dict(feedbacks=scheme_feedbacks, count=count)
