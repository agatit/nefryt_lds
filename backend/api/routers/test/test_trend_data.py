import os
import struct
import sys
from datetime import datetime, timezone
from unittest.mock import patch
from starlette import status
from starlette.testclient import TestClient
from api.routers.utils.security import get_user_token
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))  # noqa: E402
from api.app import app
from database import lds
import pytest

binary_data = os.urandom(200)
trend_def1 = lds.TrendDef(ID='ID_1', Name='TrendDef1')
trend_def2 = lds.TrendDef(ID='ID_2', Name='TrendDef2')
trend_def_list = [trend_def1, trend_def2]
trend_group = lds.TrendGroup(ID=1, Name='Group1')
unit = lds.Unit(ID='Unit1', Name='Unit1', Symbol='U')
trend1 = lds.Trend(ID=1, TrendDefID=trend_def1.ID, RawMin=1, RawMax=10, ScaledMin=0.5, ScaledMax=1.5,
                   Name='Trend1', TrendGroupID=trend_group.ID, UnitID=unit.ID, Color='Black')
trend2 = lds.Trend(ID=2, TrendDefID=trend_def2.ID, RawMin=2, RawMax=20, ScaledMin=0.2, ScaledMax=1.2,
                   Name='Trend2', TrendGroupID=trend_group.ID, UnitID=unit.ID, Color='Red')
trend3 = lds.Trend(ID=3, TrendDefID=trend_def1.ID, RawMin=3, RawMax=10, ScaledMin=0.5, ScaledMax=1.5,
                   Name='Trend4', TrendGroupID=trend_group.ID, UnitID=unit.ID, Color='Yellow')
trend_list = [trend1, trend2, trend3]
trend_data1 = lds.TrendData(TrendID=1, Time=1, Data=binary_data)
trend_data2 = lds.TrendData(TrendID=1, Time=2, Data=binary_data)
trend_data3 = lds.TrendData(TrendID=1, Time=3, Data=binary_data)
trend_data4 = lds.TrendData(TrendID=2, Time=2, Data=binary_data)
trend_data_list = [trend_data1, trend_data2, trend_data3, trend_data4]
trend_param1 = lds.TrendParam(TrendParamDefID='RAW_MAX', TrendID=1, Value='1')
trend_param2 = lds.TrendParam(TrendParamDefID='RAW_MIN', TrendID=1, Value='2')
trend_param3 = lds.TrendParam(TrendParamDefID='SCALED_MIN', TrendID=1, Value='3')
trend_param_list = [trend_param1, trend_param2, trend_param3]
trend_param_def1 = lds.TrendParamDef(ID='RAW_MAX', TrendDefID='ID_1', Name='name', DataType='INT')
trend_param_def2 = lds.TrendParamDef(ID='RAW_MIN', TrendDefID='ID_1', Name='name2', DataType='INT')
trend_param_def3 = lds.TrendParamDef(ID='SCALED_MIN', TrendDefID='ID_1', Name='name3', DataType='FLOAT')
trend_param_def_list = [trend_param_def1, trend_param_def2, trend_param_def3]


def reset_all_trend_objects():
    global trend_def1, trend_def2, trend_def_list, trend1, trend2, trend3, trend_list, \
        trend_data1, trend_data2, trend_data3, trend_data4, trend_data_list, \
        trend_param1, trend_param2, trend_param3, trend_param_list, \
        trend_param_def1, trend_param_def2, trend_param_def3, trend_param_def_list, trend_group, unit
    trend_def1 = lds.TrendDef(ID='ID_1', Name='TrendDef1')
    trend_def2 = lds.TrendDef(ID='ID_2', Name='TrendDef2')
    trend_def_list = [trend_def1, trend_def2]
    trend_group = lds.TrendGroup(ID=1, Name='Group1')
    unit = lds.Unit(ID='Unit1', Name='Unit1', Symbol='U')
    trend1 = lds.Trend(ID=1, TrendDefID=trend_def1.ID, RawMin=1, RawMax=10, ScaledMin=0.5, ScaledMax=1.5,
                       Name='Trend1', TrendGroupID=trend_group.ID, UnitID=unit.ID, Color='Black')
    trend2 = lds.Trend(ID=2, TrendDefID=trend_def2.ID, RawMin=2, RawMax=20, ScaledMin=0.2, ScaledMax=1.2,
                       Name='Trend2', TrendGroupID=trend_group.ID, UnitID=unit.ID, Color='Red')
    trend3 = lds.Trend(ID=3, TrendDefID=trend_def1.ID, RawMin=3, RawMax=10, ScaledMin=0.5, ScaledMax=1.5,
                       Name='Trend4', TrendGroupID=trend_group.ID, UnitID=unit.ID, Color='Yellow')
    trend_list = [trend1, trend2, trend3]
    trend_data1 = lds.TrendData(TrendID=1, Time=1, Data=binary_data)
    trend_data2 = lds.TrendData(TrendID=1, Time=2, Data=binary_data)
    trend_data3 = lds.TrendData(TrendID=1, Time=3, Data=binary_data)
    trend_data4 = lds.TrendData(TrendID=2, Time=2, Data=binary_data)
    trend_data_list = [trend_data1, trend_data2, trend_data3, trend_data4]
    trend_param1 = lds.TrendParam(TrendParamDefID='RAW_MAX', TrendID=1, Value='1')
    trend_param2 = lds.TrendParam(TrendParamDefID='RAW_MIN', TrendID=1, Value='2')
    trend_param3 = lds.TrendParam(TrendParamDefID='SCALED_MIN', TrendID=1, Value='3')
    trend_param_list = [trend_param1, trend_param2, trend_param3]
    trend_param_def1 = lds.TrendParamDef(ID='RAW_MAX', TrendDefID='ID_1', Name='name', DataType='INT')
    trend_param_def2 = lds.TrendParamDef(ID='RAW_MIN', TrendDefID='ID_1', Name='name2', DataType='INT')
    trend_param_def3 = lds.TrendParamDef(ID='SCALED_MIN', TrendDefID='ID_1', Name='name3', DataType='FLOAT')
    trend_param_def_list = [trend_param_def1, trend_param_def2, trend_param_def3]

    return [trend_def_list, [trend_group], [unit], trend_list, trend_data_list, trend_param_list, trend_param_def_list]


def reset_trend_objects_with_full_child_data():
    global trend_def1, trend_def2, trend_def_list, trend1, trend2, trend3, trend_list, trend_group, unit, trend_data_list
    trend_def1 = lds.TrendDef(ID='ID_1', Name='TrendDef1')
    trend_def2 = lds.TrendDef(ID='ID_2', Name='TrendDef2')
    trend_def_list = [trend_def1, trend_def2]
    trend_group = lds.TrendGroup(ID=1, Name='Group1')
    unit = lds.Unit(ID='Unit1', Name='Unit1', Symbol='U')
    trend1 = lds.Trend(ID=1, TrendDefID=trend_def1.ID, RawMin=1, RawMax=10, ScaledMin=0.5, ScaledMax=1.5,
                       Name='Trend1', TrendGroupID=trend_group.ID, UnitID=unit.ID, Color='Black', TimeDelta=0)
    trend2 = lds.Trend(ID=2, TrendDefID=trend_def2.ID, RawMin=2, RawMax=20, ScaledMin=0.2, ScaledMax=1.2,
                       Name='Trend2', TrendGroupID=trend_group.ID, UnitID=unit.ID, Color='Red', TimeDelta=2)
    trend3 = lds.Trend(ID=3, TrendDefID=trend_def1.ID, RawMin=3, RawMax=10, ScaledMin=0.5, ScaledMax=1.5,
                       Name='Trend4', TrendGroupID=trend_group.ID, UnitID=unit.ID, Color='Yellow', TimeDelta=4)
    trend_list = [trend1, trend2, trend3]
    trend_data_list = [lds.TrendData(TrendID=1, Time=t+40, Data=binary_data) for t in range(1, 11)]
    trend_data_list += [lds.TrendData(TrendID=2, Time=t+40, Data=binary_data) for t in range(1, 9)]
    trend_data_list += [lds.TrendData(TrendID=3, Time=t+40, Data=binary_data) for t in range(1, 7)]

    return [trend_def_list, [trend_group], [unit], trend_list, trend_data_list]


def reset_trend_objects_with_partial_child_data():
    global trend_def1, trend_def2, trend_def_list, trend1, trend2, trend3, trend_list, trend_group, unit, trend_data_list
    trend_def1 = lds.TrendDef(ID='ID_1', Name='TrendDef1')
    trend_def2 = lds.TrendDef(ID='ID_2', Name='TrendDef2')
    trend_def_list = [trend_def1, trend_def2]
    trend_group = lds.TrendGroup(ID=1, Name='Group1')
    unit = lds.Unit(ID='Unit1', Name='Unit1', Symbol='U')
    trend1 = lds.Trend(ID=1, TrendDefID=trend_def1.ID, RawMin=1, RawMax=10, ScaledMin=0.5, ScaledMax=1.5,
                       Name='Trend1', TrendGroupID=trend_group.ID, UnitID=unit.ID, Color='Black', TimeDelta=0)
    trend2 = lds.Trend(ID=2, TrendDefID=trend_def2.ID, RawMin=2, RawMax=20, ScaledMin=0.2, ScaledMax=1.2,
                       Name='Trend2', TrendGroupID=trend_group.ID, UnitID=unit.ID, Color='Red', TimeDelta=2)
    trend3 = lds.Trend(ID=3, TrendDefID=trend_def1.ID, RawMin=3, RawMax=10, ScaledMin=0.5, ScaledMax=1.5,
                       Name='Trend4', TrendGroupID=trend_group.ID, UnitID=unit.ID, Color='Yellow', TimeDelta=4)
    trend_list = [trend1, trend2, trend3]
    trend_data_list = [lds.TrendData(TrendID=1, Time=t+40, Data=binary_data) for t in range(1, 11)]
    trend_data_list += [lds.TrendData(TrendID=2, Time=t+40, Data=binary_data) for t in range(1, 9)]
    trend_data_list += [lds.TrendData(TrendID=3, Time=t+40, Data=binary_data) for t in range(1, 3)]

    return [trend_def_list, [trend_group], [unit], trend_list, trend_data_list]


app.dependency_overrides[get_user_token] = lambda: {"sub": "test_user"}  # type: ignore[attr-defined]
test_client = TestClient(app)


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_get_trend_data_should_return_ok_response_code_and_correct_trend_data_when_samples_count_is_equal_to_time_delta(add_lds_objects):  # noqa
    samples = 3
    response = test_client.get("/trend/" + str(trend1.ID) + "/data/" + str(trend_data1.Time) +
                               "/" + str(trend_data3.Time) + "/" + str(samples))
    assert response.status_code == status.HTTP_200_OK
    returned_trend_data_list = response.json()['items']
    for returned_trend_data, expected_trend_data in zip(returned_trend_data_list, trend_data_list[:3]):
        assert returned_trend_data['Timestamp'] == expected_trend_data.Time
        assert returned_trend_data['TimestampMs'] == 0
        assert returned_trend_data['Data'][0]['ID'] == expected_trend_data.TrendID
        assert returned_trend_data['Data'][0]['Value'] == calculate_expected_value(trend1, 0)


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_get_trend_data_should_return_ok_response_code_and_correct_trend_data_when_samples_count_is_higher_than_time_delta(add_lds_objects):  # noqa
    samples = 9
    response = test_client.get("/trend/" + str(trend1.ID) + "/data/" + str(trend_data1.Time) +
                               "/" + str(trend_data3.Time) + "/" + str(samples))
    assert response.status_code == status.HTTP_200_OK
    returned_trend_data_list = response.json()['items']
    for count, returned_trend_data in enumerate(returned_trend_data_list):
        timestamp_ms = calculate_expected_timestamp_ms(count, trend_data1.Time, trend_data3.Time, samples)
        trend_data_num = calculate_expected_trend_data_number(count, trend_data1.Time, trend_data3.Time, samples)
        assert returned_trend_data['Timestamp'] == trend_data_list[trend_data_num].Time
        assert returned_trend_data['TimestampMs'] == timestamp_ms
        assert returned_trend_data['Data'][0]['ID'] == trend_data_list[trend_data_num].TrendID
        assert returned_trend_data['Data'][0]['Value'] == calculate_expected_value(trend1, timestamp_ms)


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_get_trend_data_should_return_ok_response_code_and_correct_trend_data_when_samples_count_is_lower_than_time_delta(add_lds_objects):  # noqa
    samples = 2
    response = test_client.get("/trend/" + str(trend1.ID) + "/data/" + str(trend_data1.Time) +
                               "/" + str(trend_data3.Time) + "/" + str(samples))
    assert response.status_code == status.HTTP_200_OK
    returned_trend_data_list = response.json()['items']
    for count, returned_trend_data in enumerate(returned_trend_data_list):
        timestamp_ms = calculate_expected_timestamp_ms(count, trend_data1.Time, trend_data3.Time, samples)
        trend_data_num = calculate_expected_trend_data_number(count, trend_data1.Time, trend_data3.Time, samples)
        assert returned_trend_data['Timestamp'] == trend_data_list[trend_data_num].Time
        assert returned_trend_data['TimestampMs'] == timestamp_ms
        assert returned_trend_data['Data'][0]['ID'] == trend_data_list[trend_data_num].TrendID
        assert returned_trend_data['Data'][0]['Value'] == calculate_expected_value(trend1, timestamp_ms)


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_get_trend_data_should_return_ok_response_code_and_correct_trend_data_when_begin_and_end_not_integer(add_lds_objects):  # noqa
    samples = 5
    response = test_client.get("/trend/" + str(trend1.ID) + "/data/" + str(trend_data1.Time+0.5) +
                               "/" + str(trend_data3.Time+0.5) + "/" + str(samples))
    assert response.status_code == status.HTTP_200_OK
    returned_trend_data_list = response.json()['items']
    for count, returned_trend_data in enumerate(returned_trend_data_list):
        timestamp_ms = calculate_expected_timestamp_ms(count, trend_data1.Time+0.5, trend_data3.Time+0.5, samples)
        trend_data_num = calculate_expected_trend_data_number(count, trend_data1.Time+0.5, trend_data3.Time+0.5, samples)
        assert returned_trend_data['Timestamp'] == trend_data_list[trend_data_num].Time
        assert returned_trend_data['TimestampMs'] == timestamp_ms
        assert returned_trend_data['Data'][0]['ID'] == trend_data_list[trend_data_num].TrendID
        assert returned_trend_data['Data'][0]['Value'] == calculate_expected_value(trend1, timestamp_ms)


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_get_trend_data_should_return_ok_response_code_and_correct_trend_data_when_not_all_trend_datas_exists(add_lds_objects):  # noqa
    samples = 4
    response = test_client.get("/trend/" + str(trend1.ID) + "/data/" + str(trend_data1.Time) +
                               "/" + str(trend_data3.Time + 1) + "/" + str(samples))
    assert response.status_code == status.HTTP_200_OK
    returned_trend_data_list = response.json()['items']
    for count, returned_trend_data in enumerate(returned_trend_data_list):
        timestamp_ms = calculate_expected_timestamp_ms(count, trend_data1.Time, trend_data3.Time + 1, samples)
        assert returned_trend_data['Timestamp'] == count + 1
        assert returned_trend_data['TimestampMs'] == timestamp_ms
        assert returned_trend_data['Data'][0]['ID'] == trend1.ID
        if count == len(returned_trend_data_list) - 1:
            assert returned_trend_data['Data'][0]['Value'] is None
        else:
            assert returned_trend_data['Data'][0]['Value'] == calculate_expected_value(trend1, timestamp_ms)


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_get_trend_data_should_return_ok_response_code_and_correct_trend_data_when_not_all_trends_exists(add_lds_objects):  # noqa
    samples = 2
    response = test_client.get("/trend/" + str(trend2.ID) + ",10/data/" + str(trend_data4.Time) +
                               "/" + str(trend_data4.Time) + "/" + str(samples))
    assert response.status_code == status.HTTP_200_OK
    returned_trend_data_list = response.json()['items']
    for count, returned_trend_data in enumerate(returned_trend_data_list):
        timestamp_ms = calculate_expected_timestamp_ms(count, trend_data4.Time, trend_data4.Time, samples)
        assert returned_trend_data['Timestamp'] == 2
        assert returned_trend_data['TimestampMs'] == timestamp_ms
        assert returned_trend_data['Data'][0]['ID'] == trend2.ID
        assert returned_trend_data['Data'][0]['Value'] == calculate_expected_value(trend2, timestamp_ms)


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_get_trend_data_should_return_ok_response_code_and_correct_page_data(add_lds_objects):
    samples = 3
    size = 2
    page = 2
    response = test_client.get("/trend/" + str(trend1.ID) + "/data/" + str(trend_data1.Time) +
                               "/" + str(trend_data3.Time) + "/" + str(samples) + f'?size={size}&page={page}')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == 1
    assert response.json()['total'] == samples
    assert response.json()['pages'] == samples // size if samples % size == 0 else samples // size + 1
    assert response.json()['size'] == size
    assert response.json()['page'] == page


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_get_trend_data_should_return_ok_response_code_and_default_page_data(add_lds_objects):
    samples = 3
    response = test_client.get("/trend/" + str(trend1.ID) + "/data/" + str(trend_data1.Time) +
                               "/" + str(trend_data3.Time) + "/" + str(samples))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == samples
    assert response.json()['total'] == samples
    assert response.json()['pages'] == 1
    assert response.json()['size'] == 50
    assert response.json()['page'] == 1


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_get_trend_data_should_return_ok_response_code_and_only_null_values_when_page_data_not_include_any_trend_datas(add_lds_objects): # noqa
    samples = 10
    size = 2
    page = 5
    response = test_client.get("/trend/" + str(trend1.ID) + "/data/" + str(trend_data1.Time) +
                               "/" + str(trend_data3.Time + samples) + "/" + str(samples) + f'?size={size}&page={page}')
    assert response.status_code == status.HTTP_200_OK
    returned_trend_data_list = response.json()['items']
    for count, returned_trend_data in enumerate(returned_trend_data_list):
        trend_data_num = calculate_expected_trend_data_number(count, trend_data1.Time, trend_data3.Time, samples)
        for data in returned_trend_data['Data']:
            assert data['ID'] == trend_data_list[trend_data_num].TrendID
            assert data['Value'] is None


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_get_trend_data_should_return_not_found_response_code_and_error_when_no_trend_data_exists(add_lds_objects):  # noqa
    samples = 2
    response = test_client.get("/trend/10/data/" + str(trend_data4.Time) +
                               "/" + str(trend_data4.Time) + "/" + str(samples))
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No data'
    response = test_client.get("/trend/" + str(trend2.ID) + "/data/" + str(trend_data4.Time + 100) +
                               "/" + str(trend_data4.Time + 1000) + "/" + str(samples))
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No data'


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_get_trend_current_data_should_return_ok_response_code_and_correct_trend_data_when_samples_count_is_equal_to_time_delta(add_lds_objects):  # noqa
    with patch('api.routers.trend_data.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(1970, 1, 1, second=3, tzinfo=timezone.utc)
        samples = 3
        response = test_client.get("/trend/" + str(trend1.ID) + "/current_data/" +
                                   str(trend_data3.Time - trend_data1.Time) + "/" + str(samples))
        assert response.status_code == status.HTTP_200_OK
        returned_trend_data_list = response.json()['items'][0]['Data']
        for returned_trend_data, expected_trend_data in zip(returned_trend_data_list, trend_data_list[:3]):
            assert returned_trend_data['Timestamp'] == expected_trend_data.Time
            assert returned_trend_data['TimestampMs'] == 0
            assert returned_trend_data['Data'][0]['ID'] == expected_trend_data.TrendID
            assert returned_trend_data['Data'][0]['Value'] == calculate_expected_value(trend1, 0)


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_get_trend_current_data_should_return_ok_response_code_and_correct_trend_data_when_samples_count_is_higher_than_time_delta(add_lds_objects):  # noqa
    with patch('api.routers.trend_data.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(1970, 1, 1, second=3, tzinfo=timezone.utc)
        samples = 9
        response = test_client.get("/trend/" + str(trend1.ID) + "/current_data/" +
                                   str(trend_data3.Time - trend_data1.Time) + "/" + str(samples))
        assert response.status_code == status.HTTP_200_OK
        returned_trend_data_list = response.json()['items'][0]['Data']
        for count, returned_trend_data in enumerate(returned_trend_data_list):
            timestamp_ms = calculate_expected_timestamp_ms(count, trend_data1.Time, trend_data3.Time, samples)
            trend_data_num = calculate_expected_trend_data_number(count, trend_data1.Time, trend_data3.Time, samples)
            assert returned_trend_data['Timestamp'] == trend_data_list[trend_data_num].Time
            assert returned_trend_data['TimestampMs'] == timestamp_ms
            assert returned_trend_data['Data'][0]['ID'] == trend_data_list[trend_data_num].TrendID
            assert returned_trend_data['Data'][0]['Value'] == calculate_expected_value(trend1, timestamp_ms)


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_get_trend_current_data_should_return_ok_response_code_and_correct_trend_data_when_samples_count_is_lower_than_time_delta(add_lds_objects):  # noqa
    with patch('api.routers.trend_data.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(1970, 1, 1, second=3, tzinfo=timezone.utc)
        samples = 2
        response = test_client.get("/trend/" + str(trend1.ID) + "/current_data/" +
                                   str(trend_data3.Time - trend_data1.Time) + "/" + str(samples))
        assert response.status_code == status.HTTP_200_OK
        returned_trend_data_list = response.json()['items'][0]['Data']
        for count, returned_trend_data in enumerate(returned_trend_data_list):
            timestamp_ms = calculate_expected_timestamp_ms(count, trend_data1.Time, trend_data3.Time, samples)
            trend_data_num = calculate_expected_trend_data_number(count, trend_data1.Time, trend_data3.Time, samples)
            assert returned_trend_data['Timestamp'] == trend_data_list[trend_data_num].Time
            assert returned_trend_data['TimestampMs'] == timestamp_ms
            assert returned_trend_data['Data'][0]['ID'] == trend_data_list[trend_data_num].TrendID
            assert returned_trend_data['Data'][0]['Value'] == calculate_expected_value(trend1, timestamp_ms)


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_get_trend_current_data_should_return_ok_response_code_and_correct_trend_data_when_begin_and_end_not_integer(add_lds_objects):  # noqa
    with patch('api.routers.trend_data.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(1970, 1, 1, second=3, tzinfo=timezone.utc)
        samples = 5
        response = test_client.get("/trend/" + str(trend1.ID) + "/current_data/" +
                                   str(trend_data3.Time - trend_data1.Time - 0.5) + "/" + str(samples))
        assert response.status_code == status.HTTP_200_OK
        returned_trend_data_list = response.json()['items'][0]['Data']
        for count, returned_trend_data in enumerate(returned_trend_data_list):
            timestamp_ms = calculate_expected_timestamp_ms(count, trend_data1.Time + 0.5, trend_data3.Time, samples)
            trend_data_num = calculate_expected_trend_data_number(count, trend_data1.Time + 0.5, trend_data3.Time, samples)
            assert returned_trend_data['Timestamp'] == trend_data_list[trend_data_num].Time
            assert returned_trend_data['TimestampMs'] == timestamp_ms
            assert returned_trend_data['Data'][0]['ID'] == trend_data_list[trend_data_num].TrendID
            assert returned_trend_data['Data'][0]['Value'] == calculate_expected_value(trend1, timestamp_ms)


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_get_trend_current_data_should_return_ok_response_code_and_correct_trend_data_when_not_all_trend_datas_exists(add_lds_objects):  # noqa
    with patch('api.routers.trend_data.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(1970, 1, 1, second=4, tzinfo=timezone.utc)
        samples = 4
        response = test_client.get("/trend/" + str(trend1.ID) + "/current_data/" +
                                   str(trend_data3.Time + 1 - trend_data1.Time) + "/" + str(samples))
        assert response.status_code == status.HTTP_200_OK
        returned_trend_data_list = response.json()['items'][0]['Data']
        for count, returned_trend_data in enumerate(returned_trend_data_list):
            timestamp_ms = calculate_expected_timestamp_ms(count, trend_data1.Time, trend_data3.Time + 1, samples)
            assert returned_trend_data['Timestamp'] == count + 1
            assert returned_trend_data['TimestampMs'] == timestamp_ms
            assert returned_trend_data['Data'][0]['ID'] == trend1.ID
            if count == len(returned_trend_data_list) - 1:
                assert returned_trend_data['Data'][0]['Value'] is None
            else:
                assert returned_trend_data['Data'][0]['Value'] == calculate_expected_value(trend1, timestamp_ms)


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_get_trend_current_data_should_return_ok_response_code_and_correct_trend_data_when_not_all_trends_exists(add_lds_objects):  # noqa
    with patch('api.routers.trend_data.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(1970, 1, 1, second=2, tzinfo=timezone.utc)
        samples = 2
        response = test_client.get("/trend/" + str(trend2.ID) + ",10/current_data/" +
                                   str(trend_data4.Time - trend_data4.Time) + "/" + str(samples))
        assert response.status_code == status.HTTP_200_OK
        returned_trend_data_list = response.json()['items'][0]['Data']
        for count, returned_trend_data in enumerate(returned_trend_data_list):
            timestamp_ms = calculate_expected_timestamp_ms(count, trend_data4.Time, trend_data4.Time, samples)
            assert returned_trend_data['Timestamp'] == 2
            assert returned_trend_data['TimestampMs'] == timestamp_ms
            assert returned_trend_data['Data'][0]['ID'] == trend2.ID
            assert returned_trend_data['Data'][0]['Value'] == calculate_expected_value(trend2, timestamp_ms)


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_get_trend_current_data_should_return_ok_response_code_and_correct_page_data(add_lds_objects):
    with patch('api.routers.trend_data.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(1970, 1, 1, second=3, tzinfo=timezone.utc)
        samples = 3
        size = 2
        page = 1
        response = test_client.get("/trend/" + str(trend1.ID) + "/current_data/"
                                   + str(trend_data3.Time - trend_data1.Time)
                                   + "/" + str(samples) + f'?size={size}&page={page}')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 5
        assert len(response.json()['items']) == 1
        assert len(response.json()['items'][0]['Data']) == size
        assert response.json()['total'] == samples
        assert response.json()['pages'] == samples // size if samples % size == 0 else samples // size + 1
        assert response.json()['size'] == size
        assert response.json()['page'] == page


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_get_trend_current_data_should_return_ok_response_code_and_default_page_data(add_lds_objects):
    with patch('api.routers.trend_data.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(1970, 1, 1, second=3, tzinfo=timezone.utc)
        samples = 3
        response = test_client.get("/trend/" + str(trend1.ID) + "/current_data/"
                                   + str(trend_data3.Time - trend_data1.Time) + "/" + str(samples))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == 1
    assert len(response.json()['items'][0]['Data']) == samples
    assert response.json()['total'] == samples
    assert response.json()['pages'] == 1
    assert response.json()['size'] == 50
    assert response.json()['page'] == 1


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_get_trend_current_data_should_return_not_found_response_code_and_error_when_no_trend_data_exists(add_lds_objects):  # noqa
    with patch('api.routers.trend_data.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(1970, 1, 1, second=3, tzinfo=timezone.utc)
        samples = 2
        response = test_client.get("/trend/10/current_data/" +
                                   str(trend_data4.Time - trend_data4.Time) + "/" + str(samples))
        assert response.status_code == status.HTTP_404_NOT_FOUND
        error = response.json()
        assert error['code'] == status.HTTP_404_NOT_FOUND
        assert error['message'] == 'No data'
        mock_datetime.now.return_value = datetime(1980, 1, 1, tzinfo=timezone.utc)
        response = test_client.get("/trend/" + str(trend2.ID) + "/current_data/" +
                                   str(trend_data3.Time + 100 - trend_data1.Time) + "/" + str(samples))
        assert response.status_code == status.HTTP_404_NOT_FOUND
        error = response.json()
        assert error['code'] == status.HTTP_404_NOT_FOUND
        assert error['message'] == 'No data'


@pytest.mark.parametrize('reset_lds_objects', [reset_trend_objects_with_full_child_data], indirect=True)
def test_get_trend_current_data_should_return_correct_last_timestamp_value_when_all_trends_have_current_data(add_lds_objects):  # noqa
    with patch('api.routers.trend_data.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(1970, 1, 1, second=50, tzinfo=timezone.utc)
        response = test_client.get("/trend/1,2,3/current_data/5/1")
        assert response.status_code == status.HTTP_200_OK
        returned_trend_data_list = response.json()['items'][0]['Data']
        assert len(returned_trend_data_list) == 1
        assert response.json()['items'][0]['LastTimestamp'] == 46


@pytest.mark.parametrize('reset_lds_objects', [reset_trend_objects_with_partial_child_data], indirect=True)
def test_get_trend_current_data_should_return_correct_last_timestamp_value_when_not_all_trends_have_current_data(add_lds_objects):  # noqa
    with patch('api.routers.trend_data.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(1970, 1, 1, second=50, tzinfo=timezone.utc)
        response = test_client.get("/trend/1,2,3/current_data/5/3")
        assert response.status_code == status.HTTP_200_OK
        returned_trend_data_list = response.json()['items'][0]['Data']
        assert len(returned_trend_data_list) == 3
        assert response.json()['items'][0]['LastTimestamp'] == 48


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_get_single_trend_data_should_return_ok_response_code_and_correct_trend_data_when_samples_count_is_equal_to_time_delta(add_lds_objects):  # noqa
    samples = 3
    response = test_client.get("/trend/" + str(trend1.ID) + "/single_data/" + str(trend_data1.Time) +
                               "/" + str(trend_data3.Time) + "/" + str(samples))
    assert response.status_code == status.HTTP_200_OK
    returned_trend_data_list = response.json()['items']
    for returned_trend_data, expected_trend_data in zip(returned_trend_data_list, trend_data_list[:3]):
        assert returned_trend_data['Timestamp'] == expected_trend_data.Time
        assert returned_trend_data['TimestampMs'] == 0
        assert returned_trend_data['Value'] == calculate_expected_value(trend1, 0)


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_get_single_trend_data_should_return_ok_response_code_and_correct_trend_data_when_samples_count_is_higher_than_time_delta(add_lds_objects):  # noqa
    samples = 9
    response = test_client.get("/trend/" + str(trend1.ID) + "/single_data/" + str(trend_data1.Time) +
                               "/" + str(trend_data3.Time) + "/" + str(samples))
    assert response.status_code == status.HTTP_200_OK
    returned_trend_data_list = response.json()['items']
    for count, returned_trend_data in enumerate(returned_trend_data_list):
        timestamp_ms = calculate_expected_timestamp_ms(count, trend_data1.Time, trend_data3.Time, samples)
        trend_data_num = calculate_expected_trend_data_number(count, trend_data1.Time, trend_data3.Time, samples)
        assert returned_trend_data['Timestamp'] == trend_data_list[trend_data_num].Time
        assert returned_trend_data['TimestampMs'] == timestamp_ms
        assert returned_trend_data['Value'] == calculate_expected_value(trend1, timestamp_ms)


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_get_single_trend_data_should_return_ok_response_code_and_correct_trend_data_when_samples_count_is_lower_than_time_delta(add_lds_objects):  # noqa
    samples = 2
    response = test_client.get("/trend/" + str(trend1.ID) + "/single_data/" + str(trend_data1.Time) +
                               "/" + str(trend_data3.Time) + "/" + str(samples))
    assert response.status_code == status.HTTP_200_OK
    returned_trend_data_list = response.json()['items']
    for count, returned_trend_data in enumerate(returned_trend_data_list):
        timestamp_ms = calculate_expected_timestamp_ms(count, trend_data1.Time, trend_data3.Time, samples)
        trend_data_num = calculate_expected_trend_data_number(count, trend_data1.Time, trend_data3.Time, samples)
        assert returned_trend_data['Timestamp'] == trend_data_list[trend_data_num].Time
        assert returned_trend_data['TimestampMs'] == timestamp_ms
        assert returned_trend_data['Value'] == calculate_expected_value(trend1, timestamp_ms)


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_get_single_trend_data_should_return_ok_response_code_and_correct_trend_data_when_begin_and_end_not_integer(add_lds_objects):  # noqa
    samples = 8
    response = test_client.get("/trend/" + str(trend1.ID) + "/single_data/" + str(trend_data1.Time+0.5) +
                               "/" + str(trend_data3.Time+0.5) + "/" + str(samples))
    assert response.status_code == status.HTTP_200_OK
    returned_trend_data_list = response.json()['items']
    for count, returned_trend_data in enumerate(returned_trend_data_list):
        timestamp_ms = calculate_expected_timestamp_ms(count, trend_data1.Time+0.5, trend_data3.Time+0.5, samples)
        trend_data_num = calculate_expected_trend_data_number(count, trend_data1.Time+0.5, trend_data3.Time+0.5, samples)
        assert returned_trend_data['Timestamp'] == trend_data_list[trend_data_num].Time
        assert returned_trend_data['TimestampMs'] == timestamp_ms
        assert returned_trend_data['Value'] == calculate_expected_value(trend1, timestamp_ms)


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_get_single_trend_data_should_return_ok_response_code_and_correct_trend_data_when_not_all_trend_datas_exists(add_lds_objects):  # noqa
    samples = 4
    response = test_client.get("/trend/" + str(trend1.ID) + "/single_data/" + str(trend_data1.Time) +
                               "/" + str(trend_data3.Time + 1) + "/" + str(samples))
    assert response.status_code == status.HTTP_200_OK
    returned_trend_data_list = response.json()['items']
    assert len(returned_trend_data_list) == 3
    for count, returned_trend_data in enumerate(returned_trend_data_list):
        timestamp_ms = calculate_expected_timestamp_ms(count, trend_data1.Time, trend_data3.Time + 1, samples)
        assert returned_trend_data['Timestamp'] == count + 1
        assert returned_trend_data['TimestampMs'] == timestamp_ms
        assert returned_trend_data['Value'] == calculate_expected_value(trend1, timestamp_ms)


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_get_single_trend_data_should_return_ok_response_code_and_correct_trend_data_when_not_all_trend_datas_exists(add_lds_objects):  # noqa
    samples = 4
    response = test_client.get("/trend/" + str(trend1.ID) + "/single_data/" + str(trend_data1.Time) +
                               "/" + str(trend_data3.Time + 1) + "/" + str(samples))
    assert response.status_code == status.HTTP_200_OK
    returned_trend_data_list = response.json()['items']
    assert len(returned_trend_data_list) == 3
    for count, returned_trend_data in enumerate(returned_trend_data_list):
        timestamp_ms = calculate_expected_timestamp_ms(count, trend_data1.Time, trend_data3.Time + 1, samples)
        assert returned_trend_data['Timestamp'] == count + 1
        assert returned_trend_data['TimestampMs'] == timestamp_ms
        assert returned_trend_data['Value'] == calculate_expected_value(trend1, timestamp_ms)


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_get_single_trend_data_should_return_ok_response_code_and_correct_page_data(add_lds_objects):
    samples = 3
    size = 2
    page = 2
    response = test_client.get("/trend/" + str(trend1.ID) + "/single_data/" + str(trend_data1.Time) +
                               "/" + str(trend_data3.Time) + "/" + str(samples) + f'?size={size}&page={page}')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == 1
    assert response.json()['total'] == samples
    assert response.json()['pages'] == samples // size if samples % size == 0 else samples // size + 1
    assert response.json()['size'] == size
    assert response.json()['page'] == page


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_get_single_trend_data_should_return_ok_response_code_and_default_page_data(add_lds_objects):
    samples = 3
    response = test_client.get("/trend/" + str(trend1.ID) + "/single_data/" + str(trend_data1.Time) +
                               "/" + str(trend_data3.Time) + "/" + str(samples))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == samples
    assert response.json()['total'] == samples
    assert response.json()['pages'] == 1
    assert response.json()['size'] == 50
    assert response.json()['page'] == 1


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_get_single_trend_data_should_return_ok_response_code_and_no_items_when_page_data_not_include_any_trend_datas(add_lds_objects): # noqa
    samples = 10
    size = 2
    page = 5
    response = test_client.get("/trend/" + str(trend1.ID) + "/single_data/" + str(trend_data1.Time - 3) +
                               "/" + str(trend_data3.Time + 3) + "/" + str(samples) + f'?size={size}&page={page}')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == 0
    assert response.json()['total'] == samples
    assert response.json()['pages'] == samples // size if samples % size == 0 else samples // size + 1
    assert response.json()['size'] == size
    assert response.json()['page'] == page
    page = 1
    response = test_client.get("/trend/" + str(trend1.ID) + "/single_data/" + str(trend_data1.Time - 3) +
                               "/" + str(trend_data3.Time + 3) + "/" + str(
        samples) + f'?size={size}&page={page}')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == 0
    assert response.json()['total'] == samples
    assert response.json()['pages'] == samples // size if samples % size == 0 else samples // size + 1
    assert response.json()['size'] == size
    assert response.json()['page'] == page


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_get_single_trend_data_should_return_ok_response_code_and_part_items_list_when_page_data_include_part_data(add_lds_objects): # noqa
    samples = 9
    size = 2
    page = 2
    response = test_client.get("/trend/" + str(trend1.ID) + "/single_data/" + str(trend_data1.Time - 3) +
                               "/" + str(trend_data3.Time + 3) + "/" + str(samples) + f'?size={size}&page={page}')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == 1
    assert response.json()['total'] == samples
    assert response.json()['pages'] == samples // size if samples % size == 0 else samples // size + 1
    assert response.json()['size'] == size
    assert response.json()['page'] == page
    samples = 8
    page = 3
    response = test_client.get("/trend/" + str(trend1.ID) + "/single_data/" + str(trend_data1.Time - 2) +
                               "/" + str(trend_data3.Time + 3) + "/" + str(samples) + f'?size={size}&page={page}')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == 1
    assert response.json()['total'] == samples
    assert response.json()['pages'] == samples // size if samples % size == 0 else samples // size + 1
    assert response.json()['size'] == size
    assert response.json()['page'] == page


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_get_single_trend_data_should_return_not_found_response_code_and_error_when_no_trend_data_exists(add_lds_objects):  # noqa
    samples = 2
    response = test_client.get("/trend/10/single_data/" + str(trend_data4.Time) +
                               "/" + str(trend_data4.Time) + "/" + str(samples))
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No data'
    response = test_client.get("/trend/" + str(trend2.ID) + "/single_data/" + str(trend_data4.Time + 100) +
                               "/" + str(trend_data4.Time + 1000) + "/" + str(samples))
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No data'


def calculate_expected_value(trend: lds.Trend, timestamp_ms: int) -> float:
    one_second_data = struct.unpack("H" * 100, binary_data)
    return ((trend.ScaledMax - trend.ScaledMin) * (one_second_data[-1 - timestamp_ms // 10] - trend.RawMin)
            / (trend.RawMax - trend.RawMin) + trend.ScaledMin)


def calculate_expected_timestamp_ms(count: int, time1: float, time2: float, samples: int) -> int:
    return int(100 * (time1 - int(time1)) + (count * ((time2 - time1) * 100) // (samples-1))) % 100 * 10


def calculate_expected_trend_data_number(count: int, time1: float, time2: float, samples: int) -> int:
    return int(100 * (time1 - int(time1)) + (count * ((time2 - time1) * 100) // (samples-1))) // 100
