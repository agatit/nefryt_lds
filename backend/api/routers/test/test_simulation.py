import os
import sys
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlmodel import select
from starlette import status
from starlette.testclient import TestClient
from api.schemas import SimulationDataBase
from db import get_engine
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))  # noqa: E402
from api.app import app
from api.routers.utils.security import get_user_token
from database import lds
import pytest

simulation_def1 = lds.SimulationDef(ID='DENSITY', Name='DensitySimulation')
simulation_def2 = lds.SimulationDef(ID='WAVE', Name='WaveSimulation')
simulation_def_list = [simulation_def1, simulation_def2]
trend_def = lds.TrendDef(ID='ID_1', Name='TrendDef1')
trend1 = lds.Trend(ID=1, TrendDefID=trend_def.ID, RawMin=1, RawMax=10, ScaledMin=0.5, ScaledMax=1.5)
trend2 = lds.Trend(ID=2, TrendDefID=trend_def.ID, RawMin=2, RawMax=20, ScaledMin=0.2, ScaledMax=1.2)
simulation1 = lds.Simulation(ID=1, SimulationDefID='DENSITY', TrendID=trend1.ID, Name='Sim1', RefreshTimeSeconds=2,
                             DistanceMeters=500)
simulation2 = lds.Simulation(ID=2, SimulationDefID='WAVE', TrendID=trend1.ID, Name='Sim2', RefreshTimeSeconds=10,
                             DistanceMeters=500)
simulation3 = lds.Simulation(ID=3, SimulationDefID='DENSITY', TrendID=trend2.ID, Name='Sim3', RefreshTimeSeconds=5,
                             DistanceMeters=10)
simulation4 = lds.Simulation(ID=4, SimulationDefID='WAVE', TrendID=trend2.ID, Name='Sim4', RefreshTimeSeconds=5,
                             DistanceMeters=100)
simulation_list = [simulation1, simulation2, simulation3, simulation4]
simulation_param_def1 = lds.SimulationParamDef(ID='LENGTH', SimulationDefID='DENSITY', Name='Pipeline length', DataType='INT')
simulation_param_def2 = lds.SimulationParamDef(ID='WIDTH', SimulationDefID='DENSITY', Name='Pipeline width', DataType='FLOAT')
simulation_param_def3 = lds.SimulationParamDef(ID='LENGTH', SimulationDefID='WAVE', Name='Pipeline length', DataType='INT')
simulation_param_def_list = [simulation_param_def1, simulation_param_def2, simulation_param_def3]
simulation_param1 = lds.SimulationParam(SimulationID=1, SimulationParamDefID='LENGTH', SimulationDefID=simulation1.SimulationDefID,
                                        Value='1500')
simulation_param2 = lds.SimulationParam(SimulationID=1, SimulationParamDefID='WIDTH', SimulationDefID=simulation1.SimulationDefID,
                                        Value='0.75')
simulation_param3 = lds.SimulationParam(SimulationID=3, SimulationParamDefID='LENGTH', SimulationDefID=simulation3.SimulationDefID,
                                        Value='6000')
simulation_param4 = lds.SimulationParam(SimulationID=2, SimulationParamDefID='LENGTH', SimulationDefID=simulation1.SimulationDefID,
                                        Value='1500')
simulation_param_list = [simulation_param1, simulation_param2, simulation_param3, simulation_param4]
simulation_data1 = lds.SimulationData(SimulationID=1, Time=20, Distance=0, Data=1)
simulation_data2 = lds.SimulationData(SimulationID=1, Time=20, Distance=500, Data=2)
simulation_data3 = lds.SimulationData(SimulationID=1, Time=20, Distance=1000, Data=3)
simulation_data4 = lds.SimulationData(SimulationID=2, Time=25, Distance=0, Data=1)
simulation_data5 = lds.SimulationData(SimulationID=2, Time=25, Distance=500, Data=2)
simulation_data_list = [simulation_data1, simulation_data2, simulation_data3, simulation_data4, simulation_data5]


def reset_simulation_def_objects():
    global simulation_def1, simulation_def2, simulation_def_list

    simulation_def1 = lds.SimulationDef(ID='DENSITY', Name='DensitySimulation')
    simulation_def2 = lds.SimulationDef(ID='WAVE', Name='WaveSimulation')
    simulation_def_list = [simulation_def1, simulation_def2]

    return [simulation_def_list]


def reset_simulation_objects():
    global simulation_def1, simulation_def2, simulation_def_list, trend_def, trend1, trend2, simulation1, \
        simulation2, simulation3, simulation4, simulation_list

    simulation_def1 = lds.SimulationDef(ID='DENSITY', Name='DensitySimulation')
    simulation_def2 = lds.SimulationDef(ID='WAVE', Name='WaveSimulation')
    simulation_def_list = [simulation_def1, simulation_def2]
    trend_def = lds.TrendDef(ID='ID_1', Name='TrendDef1')
    trend1 = lds.Trend(ID=1, TrendDefID=trend_def.ID, RawMin=1, RawMax=10, ScaledMin=0.5, ScaledMax=1.5)
    trend2 = lds.Trend(ID=2, TrendDefID=trend_def.ID, RawMin=2, RawMax=20, ScaledMin=0.2, ScaledMax=1.2)
    simulation1 = lds.Simulation(ID=1, SimulationDefID='DENSITY', TrendID=trend1.ID, Name='Sim1', RefreshTimeSeconds=2,
                                 DistanceMeters=500)
    simulation2 = lds.Simulation(ID=2, SimulationDefID='WAVE', TrendID=trend1.ID, Name='Sim2', RefreshTimeSeconds=10,
                                 DistanceMeters=500)
    simulation3 = lds.Simulation(ID=3, SimulationDefID='DENSITY', TrendID=trend2.ID, Name='Sim3', RefreshTimeSeconds=5,
                                 DistanceMeters=10)
    simulation4 = lds.Simulation(ID=4, SimulationDefID='WAVE', TrendID=trend2.ID, Name='Sim4', RefreshTimeSeconds=5,
                                 DistanceMeters=100)
    simulation_list = [simulation1, simulation2, simulation3, simulation4]

    return [simulation_def_list, [trend_def], [trend1, trend2], simulation_list]


def reset_simulation_param_objects():
    global simulation_def1, simulation_def2, simulation_def_list, trend_def, trend1, trend2, simulation1, \
        simulation2, simulation3, simulation4, simulation_list, simulation_param_def1, simulation_param_def2, \
        simulation_param_def3, simulation_param_list, simulation_param1, simulation_param2, simulation_param3, \
        simulation_param4, simulation_param_def_list

    simulation_def1 = lds.SimulationDef(ID='DENSITY', Name='DensitySimulation')
    simulation_def2 = lds.SimulationDef(ID='WAVE', Name='WaveSimulation')
    simulation_def_list = [simulation_def1, simulation_def2]
    trend_def = lds.TrendDef(ID='ID_1', Name='TrendDef1')
    trend1 = lds.Trend(ID=1, TrendDefID=trend_def.ID, RawMin=1, RawMax=10, ScaledMin=0.5, ScaledMax=1.5)
    trend2 = lds.Trend(ID=2, TrendDefID=trend_def.ID, RawMin=2, RawMax=20, ScaledMin=0.2, ScaledMax=1.2)
    simulation1 = lds.Simulation(ID=1, SimulationDefID='DENSITY', TrendID=trend1.ID, Name='Sim1', RefreshTimeSeconds=2,
                                 DistanceMeters=500)
    simulation2 = lds.Simulation(ID=2, SimulationDefID='WAVE', TrendID=trend1.ID, Name='Sim2', RefreshTimeSeconds=10,
                                 DistanceMeters=500)
    simulation3 = lds.Simulation(ID=3, SimulationDefID='DENSITY', TrendID=trend2.ID, Name='Sim3', RefreshTimeSeconds=5,
                                 DistanceMeters=10)
    simulation4 = lds.Simulation(ID=4, SimulationDefID='WAVE', TrendID=trend2.ID, Name='Sim4', RefreshTimeSeconds=5,
                                 DistanceMeters=100)
    simulation_list = [simulation1, simulation2, simulation3, simulation4]
    simulation_param_def1 = lds.SimulationParamDef(ID='LENGTH', SimulationDefID='DENSITY', Name='Pipeline length',
                                                   DataType='INT')
    simulation_param_def2 = lds.SimulationParamDef(ID='WIDTH', SimulationDefID='DENSITY', Name='Pipeline width',
                                                   DataType='FLOAT')
    simulation_param_def3 = lds.SimulationParamDef(ID='LENGTH', SimulationDefID='WAVE', Name='Pipeline length',
                                                   DataType='INT')
    simulation_param_def_list = [simulation_param_def1, simulation_param_def2, simulation_param_def3]
    simulation_param1 = lds.SimulationParam(SimulationID=1, SimulationParamDefID='LENGTH',
                                            SimulationDefID=simulation1.SimulationDefID,
                                            Value='1500')
    simulation_param2 = lds.SimulationParam(SimulationID=1, SimulationParamDefID='WIDTH',
                                            SimulationDefID=simulation1.SimulationDefID,
                                            Value='0.75')
    simulation_param3 = lds.SimulationParam(SimulationID=3, SimulationParamDefID='LENGTH',
                                            SimulationDefID=simulation1.SimulationDefID,
                                            Value='6000')
    simulation_param4 = lds.SimulationParam(SimulationID=2, SimulationParamDefID='LENGTH',
                                            SimulationDefID=simulation1.SimulationDefID,
                                            Value='1500')
    simulation_param_list = [simulation_param1, simulation_param2, simulation_param3, simulation_param4]

    return [simulation_def_list, [trend_def], [trend1, trend2], simulation_list, simulation_param_def_list, 
            simulation_param_list]


def reset_simulation_data_objects():
    global simulation_def1, simulation_def2, simulation_def_list, trend_def, trend1, trend2, simulation1, \
        simulation2, simulation3, simulation4, simulation_list, simulation_param_def1, simulation_param_def2, \
        simulation_param_def3, simulation_param_list, simulation_param1, simulation_param2, simulation_param3, \
        simulation_param4, simulation_param_def_list, simulation_data1, simulation_data2, simulation_data3, \
        simulation_data4, simulation_data5, simulation_data_list

    simulation_def1 = lds.SimulationDef(ID='DENSITY', Name='DensitySimulation')
    simulation_def2 = lds.SimulationDef(ID='WAVE', Name='WaveSimulation')
    simulation_def_list = [simulation_def1, simulation_def2]
    trend_def = lds.TrendDef(ID='ID_1', Name='TrendDef1')
    trend1 = lds.Trend(ID=1, TrendDefID=trend_def.ID, RawMin=1, RawMax=10, ScaledMin=0.5, ScaledMax=1.5)
    trend2 = lds.Trend(ID=2, TrendDefID=trend_def.ID, RawMin=2, RawMax=20, ScaledMin=0.2, ScaledMax=1.2)
    simulation1 = lds.Simulation(ID=1, SimulationDefID='DENSITY', TrendID=trend1.ID, Name='Sim1', RefreshTimeSeconds=2,
                                 DistanceMeters=500)
    simulation2 = lds.Simulation(ID=2, SimulationDefID='WAVE', TrendID=trend1.ID, Name='Sim2', RefreshTimeSeconds=10,
                                 DistanceMeters=500)
    simulation3 = lds.Simulation(ID=3, SimulationDefID='DENSITY', TrendID=trend2.ID, Name='Sim3', RefreshTimeSeconds=5,
                                 DistanceMeters=10)
    simulation4 = lds.Simulation(ID=4, SimulationDefID='WAVE', TrendID=trend2.ID, Name='Sim4', RefreshTimeSeconds=5,
                                 DistanceMeters=100)
    simulation_list = [simulation1, simulation2, simulation3, simulation4]
    simulation_param_def1 = lds.SimulationParamDef(ID='LENGTH', SimulationDefID='DENSITY', Name='Pipeline length',
                                                   DataType='INT')
    simulation_param_def2 = lds.SimulationParamDef(ID='WIDTH', SimulationDefID='DENSITY', Name='Pipeline width',
                                                   DataType='FLOAT')
    simulation_param_def3 = lds.SimulationParamDef(ID='LENGTH', SimulationDefID='WAVE', Name='Pipeline length',
                                                   DataType='INT')
    simulation_param_def_list = [simulation_param_def1, simulation_param_def2, simulation_param_def3]
    simulation_param1 = lds.SimulationParam(SimulationID=1, SimulationParamDefID='LENGTH',
                                            SimulationDefID=simulation1.SimulationDefID,
                                            Value='1500')
    simulation_param2 = lds.SimulationParam(SimulationID=1, SimulationParamDefID='WIDTH',
                                            SimulationDefID=simulation1.SimulationDefID,
                                            Value='0.75')
    simulation_param3 = lds.SimulationParam(SimulationID=3, SimulationParamDefID='LENGTH',
                                            SimulationDefID=simulation1.SimulationDefID,
                                            Value='6000')
    simulation_param4 = lds.SimulationParam(SimulationID=2, SimulationParamDefID='LENGTH',
                                            SimulationDefID=simulation1.SimulationDefID,
                                            Value='1500')
    simulation_param_list = [simulation_param1, simulation_param2, simulation_param3, simulation_param4]
    simulation_data1 = lds.SimulationData(SimulationID=1, Time=20, Distance=0, Data=1)
    simulation_data2 = lds.SimulationData(SimulationID=1, Time=20, Distance=500, Data=2)
    simulation_data3 = lds.SimulationData(SimulationID=1, Time=20, Distance=1000, Data=3)
    simulation_data4 = lds.SimulationData(SimulationID=2, Time=25, Distance=0, Data=1)
    simulation_data5 = lds.SimulationData(SimulationID=2, Time=25, Distance=500, Data=2)
    simulation_data_list = [simulation_data1, simulation_data2, simulation_data3, simulation_data4, simulation_data5]

    return [simulation_def_list, [trend_def], [trend1, trend2], simulation_list, simulation_param_def_list,
            simulation_param_list, simulation_data_list]


app.dependency_overrides[get_user_token] = lambda: {"sub": "test_user"}  # type: ignore[attr-defined]
test_client = TestClient(app)


def test_list_simulation_defs_should_return_ok_response_code_and_empty_list_when_no_simulation_defs():
    response = test_client.get("/simulation/defs")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['items']) == 0


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_def_objects], indirect=True)
def test_list_simulation_defs_should_return_ok_response_code_and_correct_simulation_defs(add_lds_objects):
    response = test_client.get("/simulation/defs")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()['items']
    assert len(items) == len(simulation_def_list)
    for expected_simulation_def, returned_simulation_def in zip(simulation_def_list, items):
        assert returned_simulation_def['ID'] == expected_simulation_def.ID.strip()
        assert returned_simulation_def['Name'] == expected_simulation_def.Name


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_def_objects], indirect=True)
def test_list_simulation_defs_should_return_ok_response_code_and_correct_page_data(add_lds_objects):
    size = 2
    page = 1
    response = test_client.get(f"/simulation/defs?size={size}&page={page}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == size
    assert response.json()['total'] == len(simulation_def_list)
    assert response.json()['pages'] == len(simulation_def_list) // size if len(simulation_def_list) % size == 0 \
        else len(simulation_def_list) // size + 1
    assert response.json()['size'] == size
    assert response.json()['page'] == page


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_def_objects], indirect=True)
def test_list_simulation_defs_should_return_ok_response_code_and_default_page_data(add_lds_objects):
    response = test_client.get("/simulation/defs")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == len(simulation_def_list)
    assert response.json()['total'] == len(simulation_def_list)
    assert response.json()['pages'] == 1
    assert response.json()['size'] == 50
    assert response.json()['page'] == 1


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_def_objects], indirect=True)
def test_list_simulation_defs_should_return_ok_response_code_and_data_filtered_by_odata_query(add_lds_objects):
    odata_filter = f'ID eq \'{simulation_def2.ID}\''
    response = test_client.get(f"/simulation/defs?filter={odata_filter}")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()['items']
    assert len(items) == 1
    returned_simulation_def = items[0]
    assert returned_simulation_def['ID'] == simulation_def2.ID.strip()
    assert returned_simulation_def['Name'] == simulation_def2.Name


def test_list_simulations_should_return_ok_response_code_and_empty_list_when_no_simulations():
    response = test_client.get("/simulation")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['items']) == 0


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_objects], indirect=True)
def test_list_simulations_should_return_ok_response_code_and_correct_simulations(add_lds_objects):
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
        assert returned_simulation['DistanceMeters'] == expected_simulation.DistanceMeters


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_objects], indirect=True)
def test_list_simulations_should_return_ok_response_code_and_correct_page_data(add_lds_objects):
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


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_objects], indirect=True)
def test_list_simulations_should_return_ok_response_code_and_default_page_data(add_lds_objects):
    response = test_client.get("/simulation")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == len(simulation_list)
    assert response.json()['total'] == len(simulation_list)
    assert response.json()['pages'] == 1
    assert response.json()['size'] == 50
    assert response.json()['page'] == 1


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_objects], indirect=True)
def test_list_simulations_should_return_ok_response_code_and_data_filtered_by_odata_query(add_lds_objects):
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
        assert returned_simulation['DistanceMeters'] == expected_simulation.DistanceMeters


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_objects], indirect=True)
def test_create_simulation_should_return_created_response_code_and_created_simulation_data(add_lds_objects):
    simulation_dict = {'SimulationDefID': simulation_def1.ID, 'TrendID': trend2.ID, 'RefreshTimeSeconds': 5, 'DistanceMeters': 100}
    response = test_client.post("/simulation", json=simulation_dict)
    assert response.status_code == status.HTTP_201_CREATED
    returned_simulation = response.json()
    assert returned_simulation['ID'] == simulation4.ID+1
    assert returned_simulation['SimulationDefID'] == simulation_dict['SimulationDefID'].strip()
    assert returned_simulation['TrendID'] == simulation_dict['TrendID']
    assert returned_simulation['Name'] is None
    assert returned_simulation['RefreshTimeSeconds'] == simulation_dict['RefreshTimeSeconds']
    assert returned_simulation['DistanceMeters'] == simulation_dict['DistanceMeters']
    with Session(get_engine()) as session:
        simulations_count = session.execute(select(func.count()).select_from(lds.Simulation)).fetchall()[0][0]
    assert simulations_count == len(simulation_list)+1


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_objects], indirect=True)
def test_create_simulation_should_return_conflict_response_code_and_error_when_no_simulation_def_with_given_id(add_lds_objects):
    simulation_dict = {'SimulationDefID': 'ABC', 'TrendID': trend2.ID, 'RefreshTimeSeconds': 5, 'DistanceMeters': 100}
    response = test_client.post("/simulation", json=simulation_dict)
    assert response.status_code == status.HTTP_409_CONFLICT
    error = response.json()
    assert error['code'] == status.HTTP_409_CONFLICT
    assert error['message'] == 'Integrity error when creating simulation'


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_objects], indirect=True)
def test_create_simulation_should_return_conflict_response_code_and_error_when_no_trend_with_given_id(add_lds_objects):
    simulation_dict = {'SimulationDefID': simulation_def1.ID, 'TrendID': trend2.ID+1, 'RefreshTimeSeconds': 5, 'DistanceMeters': 100}
    response = test_client.post("/simulation", json=simulation_dict)
    assert response.status_code == status.HTTP_409_CONFLICT
    error = response.json()
    assert error['code'] == status.HTTP_409_CONFLICT
    assert error['message'] == 'Integrity error when creating simulation'


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_objects], indirect=True)
def test_delete_simulation_by_id_should_return_no_content_response_code_and_remove_simulation(add_lds_objects):
    response = test_client.delete("/simulation/" + str(simulation1.ID))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    with Session(get_engine()) as session:
        simulations_count = session.execute(select(func.count()).select_from(lds.Simulation)).fetchall()[0][0]
    assert simulations_count == len(simulation_list) - 1


def test_delete_simulation_by_id_should_return_not_found_response_code_and_error_when_no_simulation_with_given_id():
    response = test_client.delete("/simulation/" + str(simulation3.ID))
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No simulation with id = ' + str(simulation3.ID)


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_objects], indirect=True)
def test_get_simulation_by_id_should_return_ok_response_code_and_simulation_of_given_id(add_lds_objects):
    response = test_client.get("/simulation/" + str(simulation3.ID))
    assert response.status_code == status.HTTP_200_OK
    returned_simulation = response.json()
    assert returned_simulation['ID'] == simulation3.ID
    assert returned_simulation['SimulationDefID'] == simulation3.SimulationDefID.strip()
    assert returned_simulation['TrendID'] == simulation3.TrendID
    assert returned_simulation['Name'] == simulation3.Name
    assert returned_simulation['RefreshTimeSeconds'] == simulation3.RefreshTimeSeconds
    assert returned_simulation['DistanceMeters'] == simulation3.DistanceMeters


def test_get_simulation_by_id_should_return_not_found_response_code_and_error_when_no_simulation_with_given_id():
    response = test_client.get("/simulation/" + str(simulation2.ID))
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No simulation with id = ' + str(simulation2.ID)


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_objects], indirect=True)
def test_update_simulation_by_id_should_return_ok_response_code_and_simulation_of_given_id(add_lds_objects):
    update_simulation_dict = {'SimulationDefID': 'WAVE', 'RefreshTimeSeconds': 45, 'DistanceMeters': 111}
    response = test_client.put("/simulation/" + str(simulation2.ID), json=update_simulation_dict)
    assert response.status_code == status.HTTP_200_OK
    returned_simulation = response.json()
    assert returned_simulation['ID'] == simulation2.ID
    assert returned_simulation['SimulationDefID'] == update_simulation_dict['SimulationDefID']
    assert returned_simulation['TrendID'] == simulation2.TrendID
    assert returned_simulation['Name'] == simulation2.Name
    assert returned_simulation['RefreshTimeSeconds'] == update_simulation_dict['RefreshTimeSeconds']
    assert returned_simulation['DistanceMeters'] == update_simulation_dict['DistanceMeters']


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_objects], indirect=True)
def test_update_simulation_by_id_should_return_conflict_response_code_and_error_when_no_simulation_def_with_given_id(add_lds_objects):
    update_simulation_dict = {'SimulationDefID': 'ABC', 'RefreshTimeSeconds': 45, 'DistanceMeters': 111}
    response = test_client.put("/simulation/" + str(simulation3.ID), json=update_simulation_dict)
    assert response.status_code == status.HTTP_409_CONFLICT
    error = response.json()
    assert error['code'] == status.HTTP_409_CONFLICT
    assert error['message'] == 'Integrity error when updating simulation with id = ' + str(simulation3.ID)


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_objects], indirect=True)
def test_update_simulation_by_id_should_return_conflict_response_code_and_error_when_no_simulation_def_with_given_id(add_lds_objects):
    update_simulation_dict = {'TrendID': trend2.ID+10, 'RefreshTimeSeconds': 45, 'DistanceMeters': 111}
    response = test_client.put("/simulation/" + str(simulation3.ID), json=update_simulation_dict)
    assert response.status_code == status.HTTP_409_CONFLICT
    error = response.json()
    assert error['code'] == status.HTTP_409_CONFLICT
    assert error['message'] == 'Integrity error when updating simulation with id = ' + str(simulation3.ID)


def test_update_simulation_by_id_should_return_not_found_response_code_and_error_when_no_simulation_with_given_id():
    update_simulation_dict = {'SimulationDefID': 'WAVE', 'RefreshTimeSeconds': 45, 'DistanceMeters': 111}
    response = test_client.put("/simulation/" + str(simulation3.ID), json=update_simulation_dict)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No simulation with id = ' + str(simulation3.ID)


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_param_objects], indirect=True)
def test_list_simulation_params_by_simulation_id_should_return_ok_response_code_and_empty_list_when_no_simulation_params_for_given_simulation_id(add_lds_objects):  # noqa
    response = test_client.get("/simulation/" + str(simulation2.ID) + "/param")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['items']) == 0


def test_list_simulation_params_by_simulation_id_should_return_not_found_response_code_and_error_when_no_simulation_with_given_id():
    response = test_client.get("/simulation/" + str(simulation2.ID) + "/param")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No simulation with id = ' + str(simulation2.ID)


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_param_objects], indirect=True)
def test_list_simulation_params_by_simulation_id_should_return_ok_response_code_and_correct_simulation_params_for_given_simulation_id(add_lds_objects):
    response = test_client.get("/simulation/" + str(simulation1.ID) + "/param")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()['items']
    assert len(items) == 2
    for expected_simulation_param_def, expected_simulation_param, returned_simulation_param in (
            zip(simulation_param_def_list, simulation_param_list, items)):
        assert returned_simulation_param['SimulationID'] == expected_simulation_param.SimulationID
        assert returned_simulation_param['SimulationParamDefID'] == expected_simulation_param.SimulationParamDefID.strip()
        assert returned_simulation_param['Value'] == expected_simulation_param.Value
        assert returned_simulation_param['DataType'] == expected_simulation_param_def.DataType
        assert returned_simulation_param['Name'] == expected_simulation_param_def.Name


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_param_objects], indirect=True)
def test_list_simulation_params_by_simulation_id_should_return_ok_response_code_and_correct_page_data(add_lds_objects):
    size = 1
    page = 2
    response = test_client.get("/simulation/" + str(simulation1.ID) + f"/param?size={size}&page={page}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == size
    assert response.json()['total'] == 2
    assert response.json()['pages'] == 2 // size if 2 % size == 0 \
        else 2 // size + 1
    assert response.json()['size'] == size
    assert response.json()['page'] == page


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_param_objects], indirect=True)
def test_list_simulation_params_by_simulation_id_should_return_ok_response_code_and_default_page_data(add_lds_objects):
    response = test_client.get("/simulation/" + str(simulation1.ID) + "/param")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == 2
    assert response.json()['total'] == 2
    assert response.json()['pages'] == 1
    assert response.json()['size'] == 50
    assert response.json()['page'] == 1


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_param_objects], indirect=True)
def test_list_simulation_params_by_simulation_id_should_return_ok_response_code_and_data_filtered_by_odata_query(add_lds_objects):
    odata_filter = f'SimulationParamDefID eq \'{simulation_param2.SimulationParamDefID.strip()}\''
    response = test_client.get("/simulation/" + str(simulation1.ID) + f"/param?filter={odata_filter}")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()['items']
    assert len(items) == 1
    returned_simulation_param = items[0]
    assert returned_simulation_param['SimulationID'] == simulation_param2.SimulationID
    assert returned_simulation_param['SimulationParamDefID'] == simulation_param2.SimulationParamDefID.strip()
    assert returned_simulation_param['Value'] == simulation_param2.Value
    assert returned_simulation_param['DataType'] == simulation_param_def2.DataType
    assert returned_simulation_param['Name'] == simulation_param_def2.Name


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_param_objects], indirect=True)
def test_get_simulation_param_by_simulation_param_def_id_should_return_ok_response_code_and_trend_param_of_given_trend_and_trend_param_id(add_lds_objects):  # noqa
    response = test_client.get("/simulation/" + str(simulation1.ID) + "/param/" + simulation_param1.SimulationParamDefID.strip())
    assert response.status_code == status.HTTP_200_OK
    returned_simulation_param = response.json()
    assert returned_simulation_param['SimulationID'] == simulation_param1.SimulationID
    assert returned_simulation_param['SimulationParamDefID'] == simulation_param1.SimulationParamDefID.strip()
    assert returned_simulation_param['Value'] == simulation_param1.Value
    assert returned_simulation_param['DataType'] == simulation_param_def1.DataType
    assert returned_simulation_param['Name'] == simulation_param_def1.Name


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_param_objects], indirect=True)
def test_get_simulation_param_by_simulation_param_def_id_should_return_not_found_response_code_and_error_when_no_trend_param_with_given_id(add_lds_objects):
    response = test_client.get("/simulation/" + str(simulation2.ID) + "/param/" + simulation_param1.SimulationParamDefID.strip())
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == (f"No simulation param for simulation with id = {simulation2.ID} "
                                f"and simulation param def with id = {simulation_param1.SimulationParamDefID.strip()}")


def test_get_simulation_param_by_simulation_param_def_id_should_return_not_found_response_code_and_error_when_no_simulation_with_given_id():
    response = test_client.get("/simulation/" + str(simulation1.ID) + "/param/" + simulation_param1.SimulationParamDefID.strip())
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No simulation with id = ' + str(simulation1.ID)


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_param_objects], indirect=True)
def test_update_simulation_param_should_return_ok_response_code_and_simulation_param_of_given_id(add_lds_objects):
    update_simulation_param_dict = {'Value': '888', 'SimulationID': simulation3.ID}
    response = test_client.put("/simulation/" + str(simulation1.ID) + "/param/" + simulation_param2.SimulationParamDefID.strip(),
                               json=update_simulation_param_dict)
    assert response.status_code == status.HTTP_200_OK
    returned_simulation_param = response.json()
    assert returned_simulation_param['SimulationID'] == update_simulation_param_dict['SimulationID']
    assert returned_simulation_param['SimulationParamDefID'] == simulation_param2.SimulationParamDefID.strip()
    assert returned_simulation_param['Value'] == update_simulation_param_dict['Value']
    assert returned_simulation_param['DataType'] == simulation_param_def2.DataType
    assert returned_simulation_param['Name'] == simulation_param_def2.Name


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_param_objects], indirect=True)
def test_update_simulation_param_should_return_not_found_response_code_and_error_when_no_simulation_param_with_given_id(add_lds_objects):
    update_simulation_param_dict = {'Value': '888', 'SimulationID': simulation1.ID}
    response = test_client.put("/simulation/" + str(simulation2.ID) + "/param/" + simulation_param2.SimulationParamDefID.strip(),
                               json=update_simulation_param_dict)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == (f"No simulation param for simulation with id = {simulation2.ID} "
                                    f"and simulation param def with id = {simulation_param2.SimulationParamDefID.strip()}")


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_param_objects], indirect=True)
def test_update_simulation_param_should_return_conflict_response_code_and_error_when_no_simulation_with_given_id(add_lds_objects):
    update_simulation_param_dict = {'Value': '888', 'SimulationID': simulation1.ID+10}
    response = test_client.put("/simulation/" + str(simulation1.ID) + "/param/" + simulation_param1.SimulationParamDefID.strip(),
                               json=update_simulation_param_dict)
    assert response.status_code == status.HTTP_409_CONFLICT
    error = response.json()
    assert error['code'] == status.HTTP_409_CONFLICT
    assert error['message'] == f'No simulation with id = {simulation1.ID+10} given in update data'


def test_update_simulation_param_should_return_not_found_response_code_and_error_when_no_simulation_with_given_id():
    update_simulation_param_dict = {'Value': '888', 'SimulationID': simulation2.ID}
    response = test_client.put(
        "/simulation/" + str(simulation1.ID) + "/param/" + simulation_param1.SimulationParamDefID.strip(),
        json=update_simulation_param_dict)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No simulation with id = ' + str(simulation1.ID)


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_param_objects], indirect=True)
def test_create_simulation_param_should_return_created_response_code_and_created_simulation_param(add_lds_objects):
    simulation_param_dict = {'SimulationParamDefID': simulation_param_def2.ID.strip(), 'Value': '1111'}
    response = test_client.post("/simulation/" + str(simulation3.ID) + "/param", json=simulation_param_dict)
    assert response.status_code == status.HTTP_201_CREATED
    returned_simulation_param = response.json()
    assert returned_simulation_param['SimulationID'] == simulation3.ID
    assert returned_simulation_param['SimulationParamDefID'] == simulation_param_dict['SimulationParamDefID'].strip()
    assert returned_simulation_param['Value'] == simulation_param_dict['Value']
    assert returned_simulation_param['DataType'] == simulation_param_def2.DataType
    assert returned_simulation_param['Name'] == simulation_param_def2.Name
    with Session(get_engine()) as session:
        simulation_params_count = session.execute(select(func.count()).select_from(lds.SimulationParam)).fetchall()[0][0]
    assert simulation_params_count == len(simulation_param_list)+1


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_param_objects], indirect=True)
def test_create_simulation_should_return_conflict_response_code_and_error_when_param_with_given_key_exists(add_lds_objects):
    simulation_param_dict = {'SimulationParamDefID': simulation_param_def2.ID.strip(), 'Value': '1111'}
    response = test_client.post("/simulation/" + str(simulation1.ID) + "/param", json=simulation_param_dict)
    assert response.status_code == status.HTTP_409_CONFLICT
    error = response.json()
    assert error['code'] == status.HTTP_409_CONFLICT
    assert error['message'] == 'Integrity error when creating simulation param'


def test_create_simulation_should_return_not_found_response_code_and_error_when_no_simulation_with_given_id():
    simulation_param_dict = {'SimulationParamDefID': simulation_param_def2.ID.strip(), 'Value': '1111'}
    response = test_client.post("/simulation/" + str(simulation1.ID) + "/param", json=simulation_param_dict)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No simulation with id = ' + str(simulation1.ID)


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_param_objects], indirect=True)
def test_delete_simulation_param_by_id_should_return_no_content_response_code_and_remove_simulation_param(add_lds_objects):
    response = test_client.delete("/simulation/" + str(simulation1.ID) + "/param/" + simulation_param_def1.ID.strip())
    assert response.status_code == status.HTTP_204_NO_CONTENT
    with Session(get_engine()) as session:
        simulations_count = session.execute(select(func.count()).select_from(lds.SimulationParam)).fetchall()[0][0]
    assert simulations_count == len(simulation_list) - 1


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_param_objects], indirect=True)
def test_delete_simulation_param_by_id_should_return_not_found_response_code_and_error_when_no_simulation_param_for_given_ids(add_lds_objects):
    response = test_client.delete("/simulation/" + str(simulation3.ID) + "/param/" + simulation_param_def2.ID.strip())
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == ('No simulation param for simulation with id = ' + str(simulation3.ID)
                                + ' and simulation param def with id = ' + simulation_param_def2.ID.strip())


def test_delete_simulation_param_by_id_should_return_not_found_response_code_and_error_when_no_simulation_with_given_id():
    response = test_client.delete("/simulation/" + str(simulation2.ID) + "/param/" + simulation_param_def1.ID.strip())
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No simulation with id = ' + str(simulation2.ID)


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_data_objects], indirect=True)
def test_get_simulation_data_should_return_full_data_for_simulation(add_lds_objects):
    response = test_client.get(f"/simulation/{simulation1.ID}/data")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()['items']
    assert len(items) == 1
    returned_simulation_data = items[0]
    assert returned_simulation_data['SimulationID'] == simulation1.ID
    assert returned_simulation_data['Time'] == simulation_data1.Time
    returned_sim_datas = returned_simulation_data['Data']
    expected_sim_datas = [simulation_data1, simulation_data2, simulation_data3]
    for expected_sim_data, returned_sim_data in zip(expected_sim_datas, returned_sim_datas):
        assert returned_sim_data['Distance'] == expected_sim_data.Distance
        assert returned_sim_data['Data'] == expected_sim_data.Data


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_data_objects], indirect=True)
def test_get_simulation_data_should_return_completed_data_for_simulation(add_lds_objects):
    response = test_client.get(f"/simulation/{simulation2.ID}/data")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()['items']
    assert len(items) == 1
    returned_simulation_data = items[0]
    assert returned_simulation_data['SimulationID'] == simulation2.ID
    assert returned_simulation_data['Time'] == simulation_data4.Time
    returned_sim_datas = returned_simulation_data['Data']
    expected_sim_datas = [simulation_data4, simulation_data5, SimulationDataBase(Distance=1000, Data=None)]
    for expected_sim_data, returned_sim_data in zip(expected_sim_datas, returned_sim_datas):
        assert returned_sim_data['Distance'] == expected_sim_data.Distance
        assert returned_sim_data['Data'] == expected_sim_data.Data


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_data_objects], indirect=True)
def test_get_simulation_data_should_return_not_found_response_code_and_error_when_no_data_for_simulation(add_lds_objects):
    response = test_client.get(f"/simulation/{simulation3.ID}/data")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No simulation data for simulation with id = ' + str(simulation3.ID)


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_data_objects], indirect=True)
def test_get_simulation_data_should_return_not_found_response_code_and_error_when_no_length_param_for_simulation(add_lds_objects):
    response = test_client.get(f"/simulation/{simulation4.ID}/data")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No simulation param with id = \'LENGTH\' for simulation with id = ' + str(simulation4.ID)


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_data_objects], indirect=True)
def test_get_simulation_data_should_return_not_found_response_code_and_error_when_no_simulation_with_given_id(add_lds_objects):
    response = test_client.get(f"/simulation/{simulation4.ID + 1}/data")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No simulation with id = ' + str(simulation4.ID + 1)


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_data_objects], indirect=True)
def test_get_simulation_data_should_return_ok_response_code_and_correct_page_data(add_lds_objects):
    size = 2
    page = 2
    response = test_client.get(f"/simulation/{simulation2.ID}/data?size={size}&page={page}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == 1
    assert response.json()['total'] == 3
    assert response.json()['pages'] == len(simulation_def_list) // size if len(simulation_def_list) % size == 0 \
        else len(simulation_def_list) // size + 1
    assert response.json()['size'] == size
    assert response.json()['page'] == page


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_data_objects], indirect=True)
def test_get_simulation_data_should_return_ok_response_code_and_default_page_data(add_lds_objects):
    response = test_client.get(f"/simulation/{simulation2.ID}/data")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == 1
    assert response.json()['total'] == 3
    assert response.json()['pages'] == 1
    assert response.json()['size'] == 50
    assert response.json()['page'] == 1
