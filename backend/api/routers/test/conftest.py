from sqlalchemy.orm import Session
from sqlmodel import SQLModel
from starlette.testclient import TestClient
from fastapi import FastAPI
import pytest
from _pytest.fixtures import FixtureRequest
import pytest_asyncio
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from api.app import init_app
from api.routers.utils import get_user_token
from db import get_engine


@pytest_asyncio.fixture(scope="session")
async def test_client():
    app = await init_app()
    app.dependency_overrides[get_user_token] = lambda: {"sub": "test_user"}
    test_client = TestClient(app)
    return test_client


@pytest.fixture(scope="function")
def add_test_context(
    request: FixtureRequest
) -> None:
    _insert_context(request.param())


def _insert_context(
    test_entities: list[list[SQLModel]],
) -> None:
    with Session(get_engine()) as session:
        entities_flat: list[SQLModel] = []
        for entities_list in test_entities:
            session.add_all(entities_list)
            entities_flat.extend(entities_list)
            session.commit()
        for entity in entities_flat:
            session.refresh(entity)
