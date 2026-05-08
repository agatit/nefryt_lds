import os
import sys
from starlette import status
from starlette.testclient import TestClient
from conftest import test_client
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))  # noqa: E402
from api.routers.utils.security import get_user_token
from database import lds
import pytest

method_def1 = lds.MethodDef(ID='COMBINED', Name='CombineOtherResults')
method_def2 = lds.MethodDef(ID='WAVE', Name='WaveHeatmap')
method_def_list = [method_def1, method_def2]


def reset_method_def_objects():
    global method_def1, method_def2, method_def_list

    method_def1 = lds.MethodDef(ID='COMBINED', Name='CombineOtherResults')
    method_def2 = lds.MethodDef(ID='WAVE', Name='WaveHeatmap')
    method_def_list = [method_def1, method_def2]

    return [method_def_list]


def test_list_method_defs_should_return_ok_response_code_and_empty_list_when_no_method_defs(test_client):
    response = test_client.get("/method_def")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['items']) == 0


@pytest.mark.parametrize('add_test_context', [reset_method_def_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_method_defs_should_return_ok_response_code_and_correct_method_defs(test_client):
    response = test_client.get("/method_def")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()['items']
    assert len(items) == len(method_def_list)
    for expected_method_def, returned_method_def in zip(method_def_list, items):
        assert returned_method_def['ID'] == expected_method_def.ID.strip()
        assert returned_method_def['Name'] == expected_method_def.Name


@pytest.mark.parametrize('add_test_context', [reset_method_def_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_method_defs_should_return_ok_response_code_and_correct_page_data(test_client):
    size = 1
    page = 2
    response = test_client.get(f"/method_def?size={size}&page={page}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == size
    assert response.json()['total'] == len(method_def_list)
    assert response.json()['pages'] == len(method_def_list) // size if len(method_def_list) % size == 0 \
        else len(method_def_list) // size + 1
    assert response.json()['size'] == size
    assert response.json()['page'] == page


@pytest.mark.parametrize('add_test_context', [reset_method_def_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_method_defs_should_return_ok_response_code_and_default_page_data(test_client):
    response = test_client.get("/method_def")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == len(method_def_list)
    assert response.json()['total'] == len(method_def_list)
    assert response.json()['pages'] == 1
    assert response.json()['size'] == 50
    assert response.json()['page'] == 1


@pytest.mark.parametrize('add_test_context', [reset_method_def_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_method_defs_should_return_ok_response_code_and_data_filtered_by_odata_query(test_client):
    odata_filter = f'ID eq \'{method_def2.ID}\''
    response = test_client.get(f"/method_def?filter={odata_filter}")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()['items']
    assert len(items) == 1
    returned_method_def = items[0]
    assert returned_method_def['ID'] == method_def2.ID.strip()
    assert returned_method_def['Name'] == method_def2.Name
