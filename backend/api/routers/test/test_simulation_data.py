import os
import sys
from starlette import status
from starlette.testclient import TestClient
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))  # noqa: E402
from api.app import app
from api.routers.utils.security import get_user_token
from database import lds
from api.schemas import base
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
simulation4 = lds.Simulation(ID=4, SimulationDefID='WAVE', TrendID=trend2.ID, Name='Sim4', RefreshTimeSeconds=5,
                             ResolutionMeters=100)
simulation_list = [simulation1, simulation2, simulation3, simulation4]
simulation_param_def1 = lds.SimulationParamDef(ID='LENGTH', SimulationDefID='DENSITY', Name='Pipeline length', DataType='INT')
simulation_param_def2 = lds.SimulationParamDef(ID='WIDTH', SimulationDefID='DENSITY', Name='Pipeline width', DataType='FLOAT')
simulation_param_def3 = lds.SimulationParamDef(ID='LENGTH', SimulationDefID='WAVE', Name='Pipeline length', DataType='INT')
simulation_param_def_list = [simulation_param_def1, simulation_param_def2, simulation_param_def3]
simulation_param1 = lds.SimulationParam(SimulationID=1, SimulationParamDefID='LENGTH', Value='1500')
simulation_param2 = lds.SimulationParam(SimulationID=1, SimulationParamDefID='WIDTH', Value='0.75')
simulation_param3 = lds.SimulationParam(SimulationID=3, SimulationParamDefID='LENGTH', Value='6000')
simulation_param4 = lds.SimulationParam(SimulationID=2, SimulationParamDefID='LENGTH', Value='1500')
simulation_param_list = [simulation_param1, simulation_param2, simulation_param3, simulation_param4]
simulation_data1 = lds.SimulationData(SimulationID=1, Time=20, Distance=0, Data=1)
simulation_data2 = lds.SimulationData(SimulationID=1, Time=20, Distance=500, Data=2)
simulation_data3 = lds.SimulationData(SimulationID=1, Time=20, Distance=1000, Data=3)
simulation_data4 = lds.SimulationData(SimulationID=2, Time=25, Distance=0, Data=1)
simulation_data5 = lds.SimulationData(SimulationID=2, Time=25, Distance=500, Data=2)
simulation_data_list = [simulation_data1, simulation_data2, simulation_data3, simulation_data4, simulation_data5]


def reset_simulation_data_objects():
    global simulation_def1, simulation_def2, simulation_def_list, trend_def, trend1, trend2, simulation1, \
        simulation2, simulation3, simulation4, simulation_list, simulation_param_def1, simulation_param_def2, \
        simulation_param_def3, simulation_param_list, simulation_param1, simulation_param2, simulation_param3, \
        simulation_param4, simulation_param_def_list, simulation_data1, simulation_data2, simulation_data3, \
        simulation_data4, simulation_data5, simulation_data_list, trend_group, unit

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
    simulation4 = lds.Simulation(ID=4, SimulationDefID='WAVE', TrendID=trend2.ID, Name='Sim4', RefreshTimeSeconds=5,
                                 ResolutionMeters=100)
    simulation_list = [simulation1, simulation2, simulation3, simulation4]
    simulation_param_def1 = lds.SimulationParamDef(ID='LENGTH', SimulationDefID='DENSITY', Name='Pipeline length',
                                                   DataType='INT')
    simulation_param_def2 = lds.SimulationParamDef(ID='WIDTH', SimulationDefID='DENSITY', Name='Pipeline width',
                                                   DataType='FLOAT')
    simulation_param_def3 = lds.SimulationParamDef(ID='LENGTH', SimulationDefID='WAVE', Name='Pipeline length',
                                                   DataType='INT')
    simulation_param_def_list = [simulation_param_def1, simulation_param_def2, simulation_param_def3]
    simulation_param1 = lds.SimulationParam(SimulationID=1, SimulationParamDefID='LENGTH', Value='1500')
    simulation_param2 = lds.SimulationParam(SimulationID=1, SimulationParamDefID='WIDTH', Value='0.75')
    simulation_param3 = lds.SimulationParam(SimulationID=3, SimulationParamDefID='LENGTH', Value='6000')
    simulation_param4 = lds.SimulationParam(SimulationID=2, SimulationParamDefID='LENGTH', Value='1500')
    simulation_param_list = [simulation_param1, simulation_param2, simulation_param3, simulation_param4]
    simulation_data1 = lds.SimulationData(SimulationID=1, Time=20, Distance=0, Data=1)
    simulation_data2 = lds.SimulationData(SimulationID=1, Time=20, Distance=500, Data=2)
    simulation_data3 = lds.SimulationData(SimulationID=1, Time=20, Distance=1000, Data=3)
    simulation_data4 = lds.SimulationData(SimulationID=2, Time=25, Distance=0, Data=1)
    simulation_data5 = lds.SimulationData(SimulationID=2, Time=25, Distance=500, Data=2)
    simulation_data_list = [simulation_data1, simulation_data2, simulation_data3, simulation_data4, simulation_data5]

    return [simulation_def_list, [trend_def], [trend_group], [unit], [trend1, trend2], simulation_list, simulation_param_def_list,
            simulation_param_list, simulation_data_list]


app.dependency_overrides[get_user_token] = lambda: {"sub": "test_user"}  # type: ignore[attr-defined]
test_client = TestClient(app)


@pytest.mark.parametrize('reset_lds_objects', [reset_simulation_data_objects], indirect=True)
def test_get_simulation_data_should_return_full_data_for_simulation(add_lds_objects):
    response = test_client.get(f"/simulation/{simulation1.ID}/data")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()['items']
    assert len(items) == 1
    returned_simulation_data = items[0]
    assert returned_simulation_data['SimulationID'] == simulation1.ID
    assert returned_simulation_data['Time'] == simulation_data1.Time
    returned_sim_data_list = returned_simulation_data['Data']
    expected_sim_data_list = [simulation_data1, simulation_data2, simulation_data3]
    for expected_sim_data, returned_sim_data in zip(expected_sim_data_list, returned_sim_data_list):
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
    returned_sim_data_list = returned_simulation_data['Data']
    expected_sim_data_list = [simulation_data4, simulation_data5, base.SimulationData(Distance=1000, Data=None)]
    for expected_sim_data, returned_sim_data in zip(expected_sim_data_list, returned_sim_data_list):
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
