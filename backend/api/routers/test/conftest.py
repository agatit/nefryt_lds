import logging
import os
import sys
import pytest
from sqlalchemy.orm import Session
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))  # noqa: E402
from api.db import clear_test_db, test_engine


# has to reset objects manually because of session.refresh() which happens inside of add_events
@pytest.fixture(scope="function")
def reset_lds_objects(request):
    return request.param()


@pytest.fixture(scope="function")
def add_lds_objects(reset_lds_objects):
    lds_objects = reset_lds_objects
    with Session(test_engine) as session:
        session.add_all(lds_objects)
        session.commit()
        for lds_object in lds_objects:
            session.refresh(lds_object)


@pytest.fixture(autouse=True)
def reset_db_status():
    clear_test_db()


logging.disable(logging.CRITICAL)
