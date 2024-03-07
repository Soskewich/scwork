import asyncio
import os
import httpx
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from settings_env import settings
from src.model.database import Base
from src.model.database import get_db
from main import app
from src.routers.admin.service import service_create_admin

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URL = 'sqlite+aiosqlite:///' + os.path.join(basedir, 'data.sqlite')

engine_local = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
)

TestingSessionLocal = sessionmaker(class_=AsyncSession, bind=engine_local)


def get_cookies(set_cookie_header: str) -> httpx.Cookies:
    cookies = httpx.Cookies()
    entries = set_cookie_header.split(", ")
    chunks = entries[0].split("; ")
    chunk = next(c for c in chunks)
    k, v = chunk.split("=")
    cookies.set(k, v)
    return cookies


async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session


async def init_base():
    async with engine_local.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        db = TestingSessionLocal()
        await service_create_admin(db)


loop = asyncio.new_event_loop()
loop.run_until_complete(init_base())
loop.close()

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session")
def client():
    assert settings.MODE == "TEST"
    print(f"{settings.ADMIN_LOGIN=}")
    with TestClient(app, base_url='http://localhost') as c:
        yield c


def test_author_crud(client):
    response = client.post(
        "/api/user/token",
        data={"username": settings.ADMIN_LOGIN, "password": settings.ADMIN_PASSWORD},
        headers={"content-type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200, response.text

    cookies = get_cookies(response.headers['set-cookie'])
    client.cookies = cookies

    response = client.post(
        "/api/author",
        params={"name": "Иван", "surname": "Иванов", "patronymic": "Иванович", "confirmed": "false"}
    )
    assert response.status_code == 200, response.text

    author_id = response.json()['id']

    response = client.get(
        f"/api/author/{author_id}"
    )
    expected_json = {
        "author": {
            'id': author_id,
            'name': "Иван",
            "surname": "Иванов",
            "patronymic": "Иванович",
            "confirmed": False,
            'author_identifiers': [],
            'author_departments': []
        },
    }
    assert response.status_code == 200, response.text
    assert response.json() == expected_json, response.json()

    response = client.put(
        f"/api/author/{author_id}",
        params={"name": "Василий", "surname": "Васильев", "patronymic": "Васильевич", "confirmed": "true"}
    )

    assert response.status_code == 200, response.text

    expected_json['author']['name'] = "Василий"
    expected_json['author']['surname'] = "Васильев"
    expected_json['author']['patronymic'] = "Васильевич"
    expected_json['author']['confirmed'] = True

    response = client.get(
        f"/api/author/{author_id}"
    )

    assert response.status_code == 200, response.text
    assert response.json() == expected_json, response.json()

    response = client.delete(
        f'/api/author/{author_id}'
    )

    assert response.status_code == 200, response.text

    response = client.get(
        f'/api/author/{author_id}'
    )

    assert response.status_code == 404, response.text
