import os
import sys
from starlette import status
from starlette.testclient import TestClient
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))  # noqa: E402
from api import app
from api.db import get_engine, get_test_engine
from database import lds
import pytest


def reset_trend_def_objects():
    global trend_def1, trend_def2, trend_def_list

    trend_def1 = lds.TrendDef(ID='ID_1', Name='TrendDef1')
    trend_def2 = lds.TrendDef(ID='ID_2', Name='TrendDef2')
    trend_def_list = [trend_def1, trend_def2]

    return trend_def_list


app.dependency_overrides[get_engine] = get_test_engine
test_client = TestClient(app)


def test_list_trend_def_should_return_ok_response_code_and_empty_list_when_no_trend_defs():
    response = test_client.get("/trend_def")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 0


@pytest.mark.parametrize('reset_lds_objects', [reset_trend_def_objects], indirect=True)
def test_list_trend_def_should_return_ok_response_code_and_correct_trend_defs(add_lds_objects):
    response = test_client.get("/trend_def")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2
    for expected_trend_def, returned_trend_def in zip(trend_def_list, response.json()):
        assert expected_trend_def.ID.strip() == returned_trend_def['ID']
        assert expected_trend_def.Name == returned_trend_def['Name']
