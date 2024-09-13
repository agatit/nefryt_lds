import os
import sys
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))  # noqa: E402
from api.db import clear_test_db


@pytest.fixture(autouse=True)
def reset_db_status():
    clear_test_db()
