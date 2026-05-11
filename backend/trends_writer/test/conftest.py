from sqlalchemy.orm import Session
from sqlmodel import SQLModel
import pytest
from _pytest.fixtures import FixtureRequest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from db import get_engine


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
