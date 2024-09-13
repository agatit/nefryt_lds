import os
import sys
from sqlalchemy.orm import Session
from starlette import status
from starlette.testclient import TestClient
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))  # noqa: E402
from api import app
from api.db import get_engine, get_test_engine
from database import lds
import pytest


trend_def1: lds.TrendDef = lds.TrendDef(ID='ID_1', Name='TrendDef1')
trend_def2: lds.TrendDef = lds.TrendDef(ID='ID_2', Name='TrendDef2')
trend_def_list: list[lds.TrendDef] = [trend_def1, trend_def2]


@pytest.fixture(scope="function")
def add_trend_defs():
    with Session(get_test_engine()) as session:
        session.add_all(trend_def_list)
        session.commit()
        for trend_def in trend_def_list:
            session.refresh(trend_def)


app.dependency_overrides[get_engine] = get_test_engine
test_client = TestClient(app)


def test_list_trend_def_should_return_ok_response_code_and_empty_list_when_no_trend_defs():
    response = test_client.get("/trend_def")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 0


def test_list_trend_def_should_return_ok_response_code_and_correct_trend_defs(add_trend_defs):
    response = test_client.get("/trend_def")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2
    for expected_trend_def, returned_trend_def in zip(trend_def_list, response.json()):
        assert expected_trend_def.ID.strip() == returned_trend_def['ID']
        assert expected_trend_def.Name == returned_trend_def['Name']
