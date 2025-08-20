import os
import sys
from starlette import status
from starlette.testclient import TestClient
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))  # noqa: E402
from api.app import app
from api.routers.utils.security import get_user_token
from database import lds
import pytest

trend_def = lds.TrendDef(ID='ID_1', Name='TrendDef1')
trend_group = lds.TrendGroup(ID=1, Name='Group1')
unit = lds.Unit(ID='Unit1', Name='Unit1', Symbol='U')
trend1 = lds.Trend(ID=1, TrendDefID=trend_def.ID, RawMin=1, RawMax=10, ScaledMin=0.5, ScaledMax=1.5,
                   Name='Trend1', TrendGroupID=trend_group.ID, UnitID=unit.ID, Color='Black')
trend2 = lds.Trend(ID=2, TrendDefID=trend_def.ID, RawMin=2, RawMax=20, ScaledMin=0.2, ScaledMax=1.2,
                   Name='Trend2', TrendGroupID=trend_group.ID, UnitID=unit.ID, Color='Red')
trend3 = lds.Trend(ID=4, TrendDefID=trend_def.ID, RawMin=3, RawMax=10, ScaledMin=0.5, ScaledMax=1.5,
                   Name='Trend4', TrendGroupID=trend_group.ID, UnitID=unit.ID, Color='Yellow')
trend_list = [trend1, trend2, trend3]
profiler_data1 = lds.ProfilerData(ID=1, Time10=0.1, Time100=0.2245, Time1000=0.25, QueueSize=5)
profiler_data2 = lds.ProfilerData(ID=3, Time10=0.2, Time100=0.3, Time1000=0.5, QueueSize=1)
profiler_data3 = lds.ProfilerData(ID=5)
profiler_data_list = [profiler_data1, profiler_data2, profiler_data3]


def reset_profiler_data_objects():
    global trend_def, trend1, trend2, trend3, trend_list, profiler_data1, profiler_data2, \
        profiler_data3, profiler_data_list, trend_group, unit

    trend_def = lds.TrendDef(ID='ID_1', Name='TrendDef1')
    trend_group = lds.TrendGroup(ID=1, Name='Group1')
    unit = lds.Unit(ID='Unit1', Name='Unit1', Symbol='U')
    trend1 = lds.Trend(ID=1, TrendDefID=trend_def.ID, RawMin=1, RawMax=10, ScaledMin=0.5, ScaledMax=1.5,
                       Name='Trend1', TrendGroupID=trend_group.ID, UnitID=unit.ID, Color='Black')
    trend2 = lds.Trend(ID=3, TrendDefID=trend_def.ID, RawMin=2, RawMax=20, ScaledMin=0.2, ScaledMax=1.2,
                       Name='Trend2', TrendGroupID=trend_group.ID, UnitID=unit.ID, Color='Red')
    trend3 = lds.Trend(ID=5, TrendDefID=trend_def.ID, RawMin=3, RawMax=10, ScaledMin=0.5, ScaledMax=1.5,
                       Name='Trend4', TrendGroupID=trend_group.ID, UnitID=unit.ID, Color='Yellow')
    trend_list = [trend1, trend2, trend3]
    profiler_data1 = lds.ProfilerData(ID=1, Time10=0.123456, Time100=0.2, Time1000=0.25, QueueSize=5)
    profiler_data2 = lds.ProfilerData(ID=3, Time10=0.2, Time100=0.3, Time1000=0.5, QueueSize=1)
    profiler_data3 = lds.ProfilerData(ID=5)
    profiler_data_list = [profiler_data1, profiler_data2, profiler_data3]

    return [trend_def], [trend_group], [unit], trend_list, profiler_data_list


app.dependency_overrides[get_user_token] = lambda: {"sub": "test_user"}  # type: ignore[attr-defined]
test_client = TestClient(app)


def test_list_profiler_data_should_return_ok_response_code_and_empty_list_when_no_profiler_data():
    response = test_client.get("/trend_writer")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['items']) == 0


@pytest.mark.parametrize('reset_lds_objects', [reset_profiler_data_objects], indirect=True)
def test_list_profiler_data_should_return_ok_response_code_and_correct_profiler_data(add_lds_objects):
    response = test_client.get("/trend_writer")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()['items']
    assert len(items) == len(profiler_data_list)
    for expected_profiler_data, returned_profiler_data in zip(profiler_data_list, items):
        assert returned_profiler_data['ID'] == expected_profiler_data.ID
        if expected_profiler_data.Time10 is None:
            assert returned_profiler_data['Time10'] is None
        else:
            assert returned_profiler_data['Time10'] == float(expected_profiler_data.Time10)
        if expected_profiler_data.Time100 is None:
            assert returned_profiler_data['Time100'] is None
        else:
            assert returned_profiler_data['Time100'] == float(expected_profiler_data.Time100)
        if expected_profiler_data.Time1000 is None:
            assert returned_profiler_data['Time1000'] is None
        else:
            assert returned_profiler_data['Time1000'] == float(expected_profiler_data.Time1000)
        assert returned_profiler_data['QueueSize'] == expected_profiler_data.QueueSize


@pytest.mark.parametrize('reset_lds_objects', [reset_profiler_data_objects], indirect=True)
def test_list_profiler_data_should_return_ok_response_code_and_correct_page_data(add_lds_objects):
    size = 2
    page = 1
    response = test_client.get(f"/trend_writer?size={size}&page={page}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == size
    assert response.json()['total'] == len(profiler_data_list)
    assert response.json()['pages'] == len(profiler_data_list) // size if len(profiler_data_list) % size == 0 \
        else len(profiler_data_list) // size + 1
    assert response.json()['size'] == size
    assert response.json()['page'] == page


@pytest.mark.parametrize('reset_lds_objects', [reset_profiler_data_objects], indirect=True)
def test_list_profiler_data_should_return_ok_response_code_and_default_page_data(add_lds_objects):
    response = test_client.get("/trend_writer")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == len(profiler_data_list)
    assert response.json()['total'] == len(profiler_data_list)
    assert response.json()['pages'] == 1
    assert response.json()['size'] == 50
    assert response.json()['page'] == 1


@pytest.mark.parametrize('reset_lds_objects', [reset_profiler_data_objects], indirect=True)
def test_get_general_profiler_data_should_return_ok_response_code_and_correct_general_profiler_data(add_lds_objects):
    response = test_client.get("/trend_writer/general")
    assert response.status_code == status.HTTP_200_OK
    returned_general_data = response.json()
    assert returned_general_data['ActiveTrends'] == 2
    assert returned_general_data['Time10'] == (float(profiler_data2.Time10) + float(profiler_data1.Time10))/2
    assert returned_general_data['Time100'] == (float(profiler_data2.Time100) + round(float(profiler_data1.Time100), 5))/2
    assert returned_general_data['Time1000'] == (float(profiler_data2.Time1000) + float(profiler_data1.Time1000))/2
    assert returned_general_data['QueueSize'] == (profiler_data2.QueueSize + profiler_data1.QueueSize)/2


def test_get_general_profiler_data_should_return_bad_request_response_code_and_error_when_no_profiler_data_stored():
    response = test_client.get("/trend_writer/general")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    error = response.json()
    assert error['code'] == status.HTTP_400_BAD_REQUEST
    assert error['message'] == 'No stored profiler data to calculate general data'
    

@pytest.mark.parametrize('reset_lds_objects', [reset_profiler_data_objects], indirect=True)
def test_get_profiler_data_by_id_should_return_ok_response_code_and_profiler_data_of_given_id(add_lds_objects):
    response = test_client.get("/trend_writer/" + str(profiler_data2.ID))
    assert response.status_code == status.HTTP_200_OK
    returned_profiler_data = response.json()
    assert returned_profiler_data['ID'] == profiler_data2.ID
    assert returned_profiler_data['Time10'] == float(profiler_data2.Time10)
    assert returned_profiler_data['Time100'] == float(profiler_data2.Time100)
    assert returned_profiler_data['Time1000'] == float(profiler_data2.Time1000)
    assert returned_profiler_data['QueueSize'] == profiler_data2.QueueSize


def test_get_profiler_data_by_id_should_return_not_found_response_code_and_error_when_no_profiler_data_with_given_id():
    response = test_client.get("/trend_writer/"+ str(profiler_data2.ID))
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No profiler data for trend with id = ' + str(profiler_data2.ID)
