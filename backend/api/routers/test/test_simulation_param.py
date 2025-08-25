import os
import sys
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlmodel import select
from starlette import status
from starlette.testclient import TestClient
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
trend_group = lds.TrendGroup(ID=1, Name='Group1')
unit = lds.Unit(ID='Unit1', Name='Unit1', Symbol='U')
trend1 = lds.Trend(ID=1, TrendDefID=trend_def.ID, RawMin=1, RawMax=10, ScaledMin=0.5, ScaledMax=1.5,
                   Name='Trend1', TrendGroupID=trend_group.ID, UnitID=unit.ID, Color='Black')
trend2 = lds.Trend(ID=2, TrendDefID=trend_def.ID, RawMin=2, RawMax=20, ScaledMin=0.2, ScaledMax=1.2,
                   Name='Trend2', TrendGroupID=trend_group.ID, UnitID=unit.ID, Color='Red')
simulation1 = lds.Simulation(ID=1, SimulationDefID='DENSITY', TrendID=trend1.ID, Name='Sim1', RefreshTimeSeconds=2,
                             ResolutionMeters=500)
simulation2 = lds.Simulation(ID=2, SimulationDefID='WAVE', TrendID=trend1.ID, Name='Sim2', RefreshTimeSeconds=10,
                             ResolutionMeters=500)
simulation3 = lds.Simulation(ID=3, SimulationDefID='DENSITY', TrendID=trend2.ID, Name='Sim3', RefreshTimeSeconds=5,
                             ResolutionMeters=10)
simulation4 = lds.Simulation(ID=4, SimulationDefID='DENSITY', TrendID=trend2.ID, Name='Sim4', RefreshTimeSeconds=5,
                             ResolutionMeters=100)
simulation_list = [simulation1, simulation2, simulation3, simulation4]
simulation_param_def1 = lds.SimulationParamDef(ID='LENGTH', SimulationDefID='DENSITY', Name='Pipeline length', DataType='INT')
simulation_param_def2 = lds.SimulationParamDef(ID='WIDTH', SimulationDefID='DENSITY', Name='Pipeline width', DataType='FLOAT')
simulation_param_def3 = lds.SimulationParamDef(ID='LENGTH', SimulationDefID='WAVE', Name='Pipeline length', DataType='INT')
simulation_param_def_list = [simulation_param_def1, simulation_param_def3, simulation_param_def2]
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
                                 ResolutionMeters=500)
    simulation3 = lds.Simulation(ID=3, SimulationDefID='DENSITY', TrendID=trend2.ID, Name='Sim3', RefreshTimeSeconds=5,
                                 ResolutionMeters=10)
    simulation4 = lds.Simulation(ID=4, SimulationDefID='DENSITY', TrendID=trend2.ID, Name='Sim4', RefreshTimeSeconds=5,
                                 ResolutionMeters=100)
    simulation_list = [simulation1, simulation2, simulation3, simulation4]

    return [simulation_def_list, [trend_def], [trend_group], [unit], [trend1, trend2], simulation_list]


def reset_simulation_param_objects():
    global simulation_def1, simulation_def2, simulation_def_list, trend_def, trend1, trend2, simulation1, \
        simulation2, simulation3, simulation4, simulation_list, simulation_param_def1, simulation_param_def2, \
        simulation_param_def3, simulation_param_list, simulation_param1, simulation_param2, simulation_param3, \
        simulation_param4, simulation_param_def_list, trend_group, unit

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
                                 ResolutionMeters=500)
    simulation3 = lds.Simulation(ID=3, SimulationDefID='DENSITY', TrendID=trend2.ID, Name='Sim3', RefreshTimeSeconds=5,
                                 ResolutionMeters=10)
    simulation4 = lds.Simulation(ID=4, SimulationDefID='DENSITY', TrendID=trend2.ID, Name='Sim4', RefreshTimeSeconds=5,
                                 ResolutionMeters=100)
    simulation_list = [simulation1, simulation2, simulation3, simulation4]
    simulation_param_def1 = lds.SimulationParamDef(ID='LENGTH', SimulationDefID='DENSITY', Name='Pipeline length',
                                                   DataType='INT')
    simulation_param_def2 = lds.SimulationParamDef(ID='WIDTH', SimulationDefID='DENSITY', Name='Pipeline width',
                                                   DataType='FLOAT')
    simulation_param_def3 = lds.SimulationParamDef(ID='LENGTH', SimulationDefID='WAVE', Name='Pipeline length',
                                                   DataType='INT')
    simulation_param_def_list = [simulation_param_def1, simulation_param_def3, simulation_param_def2]
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

    return [simulation_def_list, [trend_def], [trend_group], [unit], [trend1, trend2], simulation_list, simulation_param_def_list,
            simulation_param_list]


app.dependency_overrides[get_user_token] = lambda: {"sub": "test_user"}  # type: ignore[attr-defined]
test_client = TestClient(app)


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_objects], indirect=True)
def test_list_simulation_param_defs_should_return_ok_response_code_and_empty_list_when_no_simulation_param_defs(add_lds_objects):
    response = test_client.get("/simulation/param/def")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['items']) == 0


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_param_objects], indirect=True)
def test_list_simulation_param_defs_should_return_ok_response_code_and_correct_simulation_param_defs(add_lds_objects):
    response = test_client.get("/simulation/param/def")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()['items']
    assert len(items) == len(simulation_param_def_list)
    print(items)
    for expected_simulation_param_def, returned_simulation_param_def in zip(simulation_param_def_list, items):
        assert returned_simulation_param_def['ID'] == expected_simulation_param_def.ID.strip()
        assert returned_simulation_param_def['SimulationDefID'] == expected_simulation_param_def.SimulationDefID.strip()
        assert returned_simulation_param_def['Name'] == expected_simulation_param_def.Name
        assert returned_simulation_param_def['DataType'] == expected_simulation_param_def.DataType


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_param_objects], indirect=True)
def test_list_simulation_param_defs_should_return_ok_response_code_and_correct_page_data(add_lds_objects):
    size = 2
    page = 2
    response = test_client.get(f"/simulation/param/def?size={size}&page={page}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == len(simulation_param_def_list) - size
    assert response.json()['total'] == len(simulation_param_def_list)
    assert response.json()['pages'] == len(simulation_param_def_list) // size if len(simulation_param_def_list) % size == 0 \
        else len(simulation_param_def_list) // size + 1
    assert response.json()['size'] == size
    assert response.json()['page'] == page


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_param_objects], indirect=True)
def test_list_simulation_param_defs_should_return_ok_response_code_and_default_page_data(add_lds_objects):
    response = test_client.get("/simulation/param/def")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == len(simulation_param_def_list)
    assert response.json()['total'] == len(simulation_param_def_list)
    assert response.json()['pages'] == 1
    assert response.json()['size'] == 50
    assert response.json()['page'] == 1


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_param_objects], indirect=True)
def test_list_simulation_param_defs_should_return_ok_response_code_and_data_filtered_by_odata_query(add_lds_objects):
    odata_filter = f'DataType ne \'{simulation_param_def1.DataType}\''
    response = test_client.get(f"/simulation/param/def?filter={odata_filter}")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()['items']
    assert len(items) == 1
    returned_simulation_param_def = items[0]
    assert returned_simulation_param_def['ID'] == simulation_param_def2.ID.strip()
    assert returned_simulation_param_def['SimulationDefID'] == simulation_param_def2.SimulationDefID.strip()
    assert returned_simulation_param_def['Name'] == simulation_param_def2.Name
    assert returned_simulation_param_def['DataType'] == simulation_param_def2.DataType


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
    expected_simulation_param_def_list = [simulation_param_def1, simulation_param_def2]
    for expected_simulation_param_def, expected_simulation_param, returned_simulation_param in (
            zip(expected_simulation_param_def_list, simulation_param_list, items)):
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


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_objects], indirect=True)
def test_list_required_simulation_params_by_simulation_id_should_return_ok_response_code_and_empty_list_when_no_simulation_params_for_given_simulation_id(add_lds_objects):  # noqa
    response = test_client.get("/simulation/" + str(simulation2.ID) + "/param/all")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['items']) == 0


def test_list_required_simulation_params_by_simulation_id_should_return_not_found_response_code_and_error_when_no_simulation_with_given_id():
    response = test_client.get("/simulation/" + str(simulation2.ID) + "/param/all")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No simulation with id = ' + str(simulation2.ID)


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_param_objects], indirect=True)
def test_list_required_simulation_params_by_simulation_id_should_return_ok_response_code_and_correct_simulation_params_for_given_simulation_id(add_lds_objects):
    response = test_client.get("/simulation/" + str(simulation4.ID) + "/param/all")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()['items']
    assert len(items) == 2
    expected_simulation_param_def_list = [simulation_param_def1, simulation_param_def2]
    for expected_simulation_param_def, expected_simulation_param, returned_simulation_param in (
            zip(expected_simulation_param_def_list, simulation_param_list, items)):
        assert returned_simulation_param['SimulationID'] == simulation4.ID
        assert returned_simulation_param['SimulationParamDefID'] == expected_simulation_param.SimulationParamDefID.strip()
        assert returned_simulation_param['Value'] is None
        assert returned_simulation_param['DataType'] == expected_simulation_param_def.DataType
        assert returned_simulation_param['Name'] == expected_simulation_param_def.Name


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_param_objects], indirect=True)
def test_list_required_simulation_params_by_simulation_id_should_return_ok_response_code_and_correct_page_data(add_lds_objects):
    size = 1
    page = 2
    response = test_client.get("/simulation/" + str(simulation4.ID) + f"/param/all?size={size}&page={page}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == size
    assert response.json()['total'] == 2
    assert response.json()['pages'] == 2 // size if 2 % size == 0 \
        else 2 // size + 1
    assert response.json()['size'] == size
    assert response.json()['page'] == page


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_param_objects], indirect=True)
def test_list_required_simulation_params_by_simulation_id_should_return_ok_response_code_and_default_page_data(add_lds_objects):
    response = test_client.get("/simulation/" + str(simulation4.ID) + "/param/all")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == 2
    assert response.json()['total'] == 2
    assert response.json()['pages'] == 1
    assert response.json()['size'] == 50
    assert response.json()['page'] == 1


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_param_objects], indirect=True)
def test_list_required_simulation_params_by_simulation_id_should_return_ok_response_code_and_data_filtered_by_odata_query(add_lds_objects):
    odata_filter = f'ID eq \'{simulation_param2.SimulationParamDefID.strip()}\''
    response = test_client.get("/simulation/" + str(simulation4.ID) + f"/param/all?filter={odata_filter}")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()['items']
    assert len(items) == 1
    returned_simulation_param = items[0]
    assert returned_simulation_param['SimulationID'] == simulation4.ID
    assert returned_simulation_param['SimulationParamDefID'] == simulation_param2.SimulationParamDefID.strip()
    assert returned_simulation_param['Value'] is None
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
    update_simulation_param_value = '1234'
    response = test_client.put("/simulation/" + str(simulation1.ID) + "/param/" + simulation_param2.SimulationParamDefID.strip(),
                               json=update_simulation_param_value)
    assert response.status_code == status.HTTP_200_OK
    returned_simulation_param = response.json()
    assert returned_simulation_param['SimulationID'] == simulation_param2.SimulationID
    assert returned_simulation_param['SimulationParamDefID'] == simulation_param2.SimulationParamDefID.strip()
    assert returned_simulation_param['Value'] == update_simulation_param_value
    assert returned_simulation_param['DataType'] == simulation_param_def2.DataType
    assert returned_simulation_param['Name'] == simulation_param_def2.Name


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_param_objects], indirect=True)
def test_update_simulation_param_should_return_not_found_response_code_and_error_when_no_simulation_param_with_given_id(add_lds_objects):
    update_simulation_param_value = '888'
    response = test_client.put("/simulation/" + str(simulation2.ID) + "/param/" + simulation_param2.SimulationParamDefID.strip(),
                               json=update_simulation_param_value)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == (f"No simulation param for simulation with id = {simulation2.ID} "
                                    f"and simulation param def with id = {simulation_param2.SimulationParamDefID.strip()}")


def test_update_simulation_param_should_return_not_found_response_code_and_error_when_no_simulation_with_given_id():
    update_simulation_param_value = '888'
    response = test_client.put(
        "/simulation/" + str(simulation1.ID) + "/param/" + simulation_param1.SimulationParamDefID.strip(),
        json=update_simulation_param_value)
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
