import os
import sys
from starlette import status
from starlette.testclient import TestClient
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))  # noqa: E402
from api.app import app
from api.routers.security import get_user_token
from database import lds
import pytest

trend_def1 = lds.TrendDef(ID='ID_1', Name='TrendDef1')
trend_def2 = lds.TrendDef(ID='ID_2', Name='TrendDef2')
trend_def_list = [trend_def1, trend_def2]


def reset_trend_def_objects():
    global trend_def1, trend_def2, trend_def_list

    trend_def1 = lds.TrendDef(ID='ID_1', Name='TrendDef1')
    trend_def2 = lds.TrendDef(ID='ID_2', Name='TrendDef2')
    trend_def_list = [trend_def1, trend_def2]

    return [trend_def_list]


app.dependency_overrides[get_user_token] = lambda: {"sub": "test_user"}  # type: ignore[attr-defined]
test_client = TestClient(app)


def test_list_trend_defs_should_return_ok_response_code_and_empty_list_when_no_trend_defs():
    response = test_client.get("/trend_def")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['items']) == 0


@pytest.mark.parametrize('reset_lds_objects', [reset_trend_def_objects], indirect=True)
def test_list_trend_defs_should_return_ok_response_code_and_correct_trend_defs(add_lds_objects):
    response = test_client.get("/trend_def")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()['items']
    assert len(items) == len(trend_def_list)
    for expected_trend_def, returned_trend_def in zip(trend_def_list, items):
        assert returned_trend_def['ID'] == expected_trend_def.ID.strip()
        assert returned_trend_def['Name'] == expected_trend_def.Name


@pytest.mark.parametrize('reset_lds_objects', [reset_trend_def_objects], indirect=True)
def test_list_trend_defs_should_return_ok_response_code_and_correct_page_data(add_lds_objects):
    size = 2
    page = 3
    response = test_client.get(f"/trend_def?size={size}&page={page}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == 0
    assert response.json()['total'] == len(trend_def_list)
    assert response.json()['pages'] == len(trend_def_list) // size if len(trend_def_list) % size == 0 \
        else len(trend_def_list) // size + 1
    assert response.json()['size'] == size
    assert response.json()['page'] == page


@pytest.mark.parametrize('reset_lds_objects', [reset_trend_def_objects], indirect=True)
def test_list_trend_defs_should_return_ok_response_code_and_default_page_data(add_lds_objects):
    response = test_client.get("/trend_def")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == len(trend_def_list)
    assert response.json()['total'] == len(trend_def_list)
    assert response.json()['pages'] == 1
    assert response.json()['size'] == 50
    assert response.json()['page'] == 1


@pytest.mark.parametrize('reset_lds_objects', [reset_trend_def_objects], indirect=True)
def test_list_trend_defs_should_return_ok_response_code_and_data_filtered_by_odata_query(add_lds_objects):
    odata_filter = f'ID ne \'{trend_def2.ID}\''
    response = test_client.get(f"/trend_def?filter={odata_filter}")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()['items']
    assert len(items) == 1
    returned_trend_def = items[0]
    assert returned_trend_def['ID'] == trend_def1.ID.strip()
    assert returned_trend_def['Name'] == trend_def1.Name
