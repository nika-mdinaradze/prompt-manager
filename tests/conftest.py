import uuid
from typing import Any, AsyncGenerator

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.db import Base, get_db
from src.main import app as _app

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(DATABASE_URL, echo=True)
async_session_testing = async_sessionmaker(
    bind=test_engine, expire_on_commit=False, class_=AsyncSession
)


@pytest_asyncio.fixture(scope="function")
async def app() -> AsyncGenerator[FastAPI, Any]:
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield _app
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def db_session(app: FastAPI) -> AsyncGenerator[AsyncSession, Any]:
    async with async_session_testing() as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def client(
    app: FastAPI, db_session: AsyncSession
) -> AsyncGenerator[AsyncClient, Any]:
    async def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1"
    ) as client:
        yield client


@pytest.fixture(scope="function")
def prompt_payload():
    payload = {
        "text": uuid.uuid4().hex,
        "variables": {uuid.uuid4().hex: uuid.uuid4().hex},
        "created_by": uuid.uuid4().hex,
    }
    return payload
