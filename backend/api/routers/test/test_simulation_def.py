import os
import sys
from starlette import status
from starlette.testclient import TestClient
from conftest import test_client
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))  # noqa: E402
from api.routers.utils.security import get_user_token
from database import lds
import pytest

simulation_def1 = lds.SimulationDef(ID='DENSITY', Name='DensitySimulation')
simulation_def2 = lds.SimulationDef(ID='WAVE', Name='WaveSimulation')
simulation_def_list = [simulation_def1, simulation_def2]


def reset_simulation_def_objects():
    global simulation_def1, simulation_def2, simulation_def_list

    simulation_def1 = lds.SimulationDef(ID='DENSITY', Name='DensitySimulation')
    simulation_def2 = lds.SimulationDef(ID='WAVE', Name='WaveSimulation')
    simulation_def_list = [simulation_def1, simulation_def2]

    return [simulation_def_list]


def test_list_simulation_defs_should_return_ok_response_code_and_empty_list_when_no_simulation_defs(test_client):
    response = test_client.get("/simulation_def")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['items']) == 0


@pytest.mark.parametrize('add_test_context', [reset_simulation_def_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_simulation_defs_should_return_ok_response_code_and_correct_simulation_defs(test_client):
    response = test_client.get("/simulation_def")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()['items']
    assert len(items) == len(simulation_def_list)
    for expected_simulation_def, returned_simulation_def in zip(simulation_def_list, items):
        assert returned_simulation_def['ID'] == expected_simulation_def.ID.strip()
        assert returned_simulation_def['Name'] == expected_simulation_def.Name


@pytest.mark.parametrize('add_test_context', [reset_simulation_def_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_simulation_defs_should_return_ok_response_code_and_correct_page_data(test_client):
    size = 2
    page = 1
    response = test_client.get(f"/simulation_def?size={size}&page={page}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == size
    assert response.json()['total'] == len(simulation_def_list)
    assert response.json()['pages'] == len(simulation_def_list) // size if len(simulation_def_list) % size == 0 \
        else len(simulation_def_list) // size + 1
    assert response.json()['size'] == size
    assert response.json()['page'] == page


@pytest.mark.parametrize('add_test_context', [reset_simulation_def_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_simulation_defs_should_return_ok_response_code_and_default_page_data(test_client):
    response = test_client.get("/simulation_def")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == len(simulation_def_list)
    assert response.json()['total'] == len(simulation_def_list)
    assert response.json()['pages'] == 1
    assert response.json()['size'] == 50
    assert response.json()['page'] == 1


@pytest.mark.parametrize('add_test_context', [reset_simulation_def_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_simulation_defs_should_return_ok_response_code_and_data_filtered_by_odata_query(test_client):
    odata_filter = f'ID eq \'{simulation_def2.ID}\''
    response = test_client.get(f"/simulation_def?filter={odata_filter}")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()['items']
    assert len(items) == 1
    returned_simulation_def = items[0]
    assert returned_simulation_def['ID'] == simulation_def2.ID.strip()
    assert returned_simulation_def['Name'] == simulation_def2.Name
