import os
import sys
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlmodel import select
from starlette import status
from starlette.testclient import TestClient
from conftest import test_client
from db import get_engine
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))  # noqa: E402
from api.routers.utils.security import get_user_token
from database import lds
import pytest

simulation_def1 = lds.SimulationDef(ID='DENSITY', Name='DensitySimulation')
simulation_def2 = lds.SimulationDef(ID='WAVE', Name='WaveSimulation')
simulation_def_list = [simulation_def1, simulation_def2]
trend_def = lds.TrendDef(ID='ID_1', Name='TrendDef1')
trend_group = lds.TrendGroup(ID=1, Name='Group1')
unit = lds.Unit(ID='Unit1', Name='Unit1', Symbol='U')
trend1 = lds.Trend(ID=1, TrendDefID=trend_def.ID, RawMin=1, RawMax=10, ScaledMin=0.5, ScaledMax=1.5,
                   Name='Trend1', TrendGroupID=trend_group.ID, UnitID=unit.ID, Color='Black')
trend2 = lds.Trend(ID=2, TrendDefID=trend_def.ID, RawMin=2, RawMax=20, ScaledMin=0.2, ScaledMax=1.2,
                   Name='Trend2', TrendGroupID=trend_group.ID, UnitID=unit.ID, Color='Red')
simulation1 = lds.Simulation(ID=1, SimulationDefID='DENSITY', TrendID=trend1.ID, Name='Sim1', RefreshTimeSeconds=2,
                             ResolutionMeters=500)
simulation2 = lds.Simulation(ID=2, SimulationDefID='WAVE', TrendID=trend1.ID, Name='Sim2', RefreshTimeSeconds=10,
                             ResolutionMeters=500, Enabled=False)
simulation3 = lds.Simulation(ID=3, SimulationDefID='DENSITY', TrendID=trend2.ID, Name='Sim3', RefreshTimeSeconds=5,
                             ResolutionMeters=10, Enabled=False)
simulation4 = lds.Simulation(ID=4, SimulationDefID='WAVE', TrendID=trend2.ID, Name='Sim4', RefreshTimeSeconds=5,
                             ResolutionMeters=100)
simulation_list = [simulation1, simulation2, simulation3, simulation4]


def reset_simulation_objects():
    global simulation_def1, simulation_def2, simulation_def_list, trend_def, trend1, trend2, simulation1, \
        simulation2, simulation3, simulation4, simulation_list, trend_group, unit

    simulation_def1 = lds.SimulationDef(ID='DENSITY', Name='DensitySimulation')
    simulation_def2 = lds.SimulationDef(ID='WAVE', Name='WaveSimulation')
    simulation_def_list = [simulation_def1, simulation_def2]
    trend_def = lds.TrendDef(ID='ID_1', Name='TrendDef1')
    trend_group = lds.TrendGroup(ID=1, Name='Group1')
    unit = lds.Unit(ID='Unit1', Name='Unit1', Symbol='U')
    trend1 = lds.Trend(ID=1, TrendDefID=trend_def.ID, RawMin=1, RawMax=10, ScaledMin=0.5, ScaledMax=1.5,
                       Name='Trend1', TrendGroupID=trend_group.ID, UnitID=unit.ID, Color='Black')
    trend2 = lds.Trend(ID=2, TrendDefID=trend_def.ID, RawMin=2, RawMax=20, ScaledMin=0.2, ScaledMax=1.2,
                       Name='Trend2', TrendGroupID=trend_group.ID, UnitID=unit.ID, Color='Red')
    simulation1 = lds.Simulation(ID=1, SimulationDefID='DENSITY', TrendID=trend1.ID, Name='Sim1', RefreshTimeSeconds=2,
                                 ResolutionMeters=500)
    simulation2 = lds.Simulation(ID=2, SimulationDefID='WAVE', TrendID=trend1.ID, Name='Sim2', RefreshTimeSeconds=10,
                                 ResolutionMeters=500, Enabled=False)
    simulation3 = lds.Simulation(ID=3, SimulationDefID='DENSITY', TrendID=trend2.ID, Name='Sim3', RefreshTimeSeconds=5,
                                 ResolutionMeters=10, Enabled=False)
    simulation4 = lds.Simulation(ID=4, SimulationDefID='WAVE', TrendID=trend2.ID, Name='Sim4', RefreshTimeSeconds=5,
                                 ResolutionMeters=100)
    simulation_list = [simulation1, simulation2, simulation3, simulation4]

    return [simulation_def_list, [trend_def], [trend_group], [unit], [trend1, trend2], simulation_list]


def test_list_simulations_should_return_ok_response_code_and_empty_list_when_no_simulations(test_client):
    response = test_client.get("/simulation")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['items']) == 0


@pytest.mark.parametrize('add_test_context', [reset_simulation_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_simulations_should_return_ok_response_code_and_correct_simulations(test_client):
    response = test_client.get("/simulation")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()['items']
    assert len(items) == len(simulation_list)
    for expected_simulation, returned_simulation in zip(simulation_list, items):
        assert returned_simulation['ID'] == expected_simulation.ID
        assert returned_simulation['SimulationDefID'] == expected_simulation.SimulationDefID.strip()
        assert returned_simulation['TrendID'] == expected_simulation.TrendID
        assert returned_simulation['Name'] == expected_simulation.Name
        assert returned_simulation['RefreshTimeSeconds'] == expected_simulation.RefreshTimeSeconds
        assert returned_simulation['ResolutionMeters'] == expected_simulation.ResolutionMeters
        assert returned_simulation['Enabled'] == expected_simulation.Enabled


@pytest.mark.parametrize('add_test_context', [reset_simulation_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_simulations_should_return_ok_response_code_and_correct_page_data(test_client):
    size = 1
    page = 1
    response = test_client.get(f"/simulation?size={size}&page={page}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == size
    assert response.json()['total'] == len(simulation_list)
    assert response.json()['pages'] == len(simulation_list) // size if len(simulation_list) % size == 0 \
        else len(simulation_list) // size + 1
    assert response.json()['size'] == size
    assert response.json()['page'] == page


@pytest.mark.parametrize('add_test_context', [reset_simulation_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_simulations_should_return_ok_response_code_and_default_page_data(test_client):
    response = test_client.get("/simulation")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == len(simulation_list)
    assert response.json()['total'] == len(simulation_list)
    assert response.json()['pages'] == 1
    assert response.json()['size'] == 50
    assert response.json()['page'] == 1


@pytest.mark.parametrize('add_test_context', [reset_simulation_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_simulations_should_return_ok_response_code_and_data_filtered_by_odata_query(test_client):
    odata_filter = f'TrendID ne {trend1.ID}'
    response = test_client.get(f"/simulation?filter={odata_filter}")
    assert response.status_code == status.HTTP_200_OK
    returned_simulations = response.json()['items']
    assert len(returned_simulations) == 2
    expected_simulations = [simulation3, simulation4]
    for returned_simulation, expected_simulation in zip(returned_simulations, expected_simulations):
        assert returned_simulation['ID'] == expected_simulation.ID
        assert returned_simulation['SimulationDefID'] == expected_simulation.SimulationDefID.strip()
        assert returned_simulation['TrendID'] == expected_simulation.TrendID
        assert returned_simulation['Name'] == expected_simulation.Name
        assert returned_simulation['RefreshTimeSeconds'] == expected_simulation.RefreshTimeSeconds
        assert returned_simulation['ResolutionMeters'] == expected_simulation.ResolutionMeters
        assert returned_simulation['Enabled'] == expected_simulation.Enabled


@pytest.mark.parametrize('add_test_context', [reset_simulation_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_create_simulation_should_return_created_response_code_and_created_simulation_data(test_client):
    simulation_dict = {'SimulationDefID': simulation_def1.ID, 'TrendID': trend2.ID,
                       'RefreshTimeSeconds': 5, 'ResolutionMeters': 100, 'Name': 'Sim'}
    response = test_client.post("/simulation", json=simulation_dict)
    assert response.status_code == status.HTTP_201_CREATED
    returned_simulation = response.json()
    assert returned_simulation['ID'] == simulation4.ID+1
    assert returned_simulation['SimulationDefID'] == simulation_dict['SimulationDefID'].strip()
    assert returned_simulation['TrendID'] == simulation_dict['TrendID']
    assert returned_simulation['Name'] == simulation_dict['Name']
    assert returned_simulation['RefreshTimeSeconds'] == simulation_dict['RefreshTimeSeconds']
    assert returned_simulation['ResolutionMeters'] == simulation_dict['ResolutionMeters']
    assert returned_simulation['Enabled'] == simulation4.Enabled
    with Session(get_engine()) as session:
        simulations_count = session.execute(select(func.count()).select_from(lds.Simulation)).fetchall()[0][0]
    assert simulations_count == len(simulation_list)+1


@pytest.mark.parametrize('add_test_context', [reset_simulation_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_create_simulation_should_return_conflict_response_code_and_error_when_no_simulation_def_with_given_id(test_client):
    simulation_dict = {'SimulationDefID': 'ABC', 'TrendID': trend2.ID,
                       'RefreshTimeSeconds': 5, 'ResolutionMeters': 100, 'Name': 'Sim'}
    response = test_client.post("/simulation", json=simulation_dict)
    assert response.status_code == status.HTTP_409_CONFLICT
    error = response.json()
    assert error['code'] == status.HTTP_409_CONFLICT
    assert error['message'] == 'Integrity error when creating simulation'


@pytest.mark.parametrize('add_test_context', [reset_simulation_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_create_simulation_should_return_conflict_response_code_and_error_when_no_trend_with_given_id(test_client):
    simulation_dict = {'SimulationDefID': simulation_def1.ID, 'TrendID': trend2.ID+1,
                       'RefreshTimeSeconds': 5, 'ResolutionMeters': 100, 'Name': 'Sim'}
    response = test_client.post("/simulation", json=simulation_dict)
    assert response.status_code == status.HTTP_409_CONFLICT
    error = response.json()
    assert error['code'] == status.HTTP_409_CONFLICT
    assert error['message'] == 'Integrity error when creating simulation'


@pytest.mark.parametrize('add_test_context', [reset_simulation_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_delete_simulation_by_id_should_return_no_content_response_code_and_remove_simulation(test_client):
    response = test_client.delete("/simulation/" + str(simulation1.ID))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    with Session(get_engine()) as session:
        simulations_count = session.execute(select(func.count()).select_from(lds.Simulation)).fetchall()[0][0]
    assert simulations_count == len(simulation_list) - 1


def test_delete_simulation_by_id_should_return_not_found_response_code_and_error_when_no_simulation_with_given_id(test_client):
    response = test_client.delete("/simulation/" + str(simulation3.ID))
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No simulation with id = ' + str(simulation3.ID)


@pytest.mark.parametrize('add_test_context', [reset_simulation_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_get_simulation_by_id_should_return_ok_response_code_and_simulation_of_given_id(test_client):
    response = test_client.get("/simulation/" + str(simulation3.ID))
    assert response.status_code == status.HTTP_200_OK
    returned_simulation = response.json()
    assert returned_simulation['ID'] == simulation3.ID
    assert returned_simulation['SimulationDefID'] == simulation3.SimulationDefID.strip()
    assert returned_simulation['TrendID'] == simulation3.TrendID
    assert returned_simulation['Name'] == simulation3.Name
    assert returned_simulation['RefreshTimeSeconds'] == simulation3.RefreshTimeSeconds
    assert returned_simulation['ResolutionMeters'] == simulation3.ResolutionMeters
    assert returned_simulation['Enabled'] == simulation3.Enabled


def test_get_simulation_by_id_should_return_not_found_response_code_and_error_when_no_simulation_with_given_id(test_client):
    response = test_client.get("/simulation/" + str(simulation2.ID))
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No simulation with id = ' + str(simulation2.ID)


@pytest.mark.parametrize('add_test_context', [reset_simulation_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_update_simulation_by_id_should_return_ok_response_code_and_simulation_of_given_id(test_client):
    update_simulation_dict = {'SimulationDefID': 'WAVE', 'RefreshTimeSeconds': 45, 'ResolutionMeters': 111}
    response = test_client.put("/simulation/" + str(simulation2.ID), json=update_simulation_dict)
    assert response.status_code == status.HTTP_200_OK
    returned_simulation = response.json()
    assert returned_simulation['ID'] == simulation2.ID
    assert returned_simulation['SimulationDefID'] == update_simulation_dict['SimulationDefID']
    assert returned_simulation['TrendID'] == simulation2.TrendID
    assert returned_simulation['Name'] == simulation2.Name
    assert returned_simulation['RefreshTimeSeconds'] == update_simulation_dict['RefreshTimeSeconds']
    assert returned_simulation['ResolutionMeters'] == update_simulation_dict['ResolutionMeters']
    assert returned_simulation['Enabled'] == simulation2.Enabled


@pytest.mark.parametrize('add_test_context', [reset_simulation_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_update_simulation_by_id_should_return_conflict_response_code_and_error_when_no_simulation_def_with_given_id(test_client):
    update_simulation_dict = {'SimulationDefID': 'ABC', 'RefreshTimeSeconds': 45, 'ResolutionMeters': 111}
    response = test_client.put("/simulation/" + str(simulation3.ID), json=update_simulation_dict)
    assert response.status_code == status.HTTP_409_CONFLICT
    error = response.json()
    assert error['code'] == status.HTTP_409_CONFLICT
    assert error['message'] == 'Integrity error when updating simulation with id = ' + str(simulation3.ID)


@pytest.mark.parametrize('add_test_context', [reset_simulation_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_update_simulation_by_id_should_return_conflict_response_code_and_error_when_no_trend_with_given_id(test_client):
    update_simulation_dict = {'TrendID': trend2.ID+10, 'RefreshTimeSeconds': 45, 'ResolutionMeters': 111}
    response = test_client.put("/simulation/" + str(simulation3.ID), json=update_simulation_dict)
    assert response.status_code == status.HTTP_409_CONFLICT
    error = response.json()
    assert error['code'] == status.HTTP_409_CONFLICT
    assert error['message'] == 'Integrity error when updating simulation with id = ' + str(simulation3.ID)


def test_update_simulation_by_id_should_return_not_found_response_code_and_error_when_no_simulation_with_given_id(test_client):
    update_simulation_dict = {'SimulationDefID': 'WAVE', 'RefreshTimeSeconds': 45, 'ResolutionMeters': 111}
    response = test_client.put("/simulation/" + str(simulation3.ID), json=update_simulation_dict)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No simulation with id = ' + str(simulation3.ID)


@pytest.mark.parametrize('add_test_context', [reset_simulation_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_enable_simulation_should_return_no_content_response_code_and_change_simulation_enabled_flag(test_client):
    response = test_client.put("/simulation/" + str(simulation1.ID) + "/enable")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    with Session(get_engine()) as session:
        simulation = session.execute(select(lds.Simulation).where(lds.Simulation.ID == simulation1.ID)).fetchall()[0][0] # noqa
    assert simulation.Enabled is not simulation1.Enabled

    response = test_client.put("/simulation/" + str(simulation1.ID) + "/enable")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    with Session(get_engine()) as session:
        simulation = session.execute(select(lds.Simulation).where(lds.Simulation.ID == simulation1.ID)).fetchall()[0][0]  # noqa
    assert simulation.Enabled is simulation1.Enabled


def test_enable_trend_should_return_not_found_response_code_and_error_when_no_trend_with_given_id(test_client):
    response = test_client.put("/simulation/" + str(simulation3.ID) + "/enable")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No simulation with id = ' + str(simulation3.ID)
