import os
import struct
import sys
from datetime import datetime, timezone
from unittest.mock import patch
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from starlette import status
from starlette.testclient import TestClient
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))  # noqa: E402
from api import app
from api.db import get_engine, get_test_engine
from database import lds
import pytest


binary_data = os.urandom(200)
trend_def1 = lds.TrendDef(ID='ID_1', Name='TrendDef1')
trend_def2 = lds.TrendDef(ID='ID_2', Name='TrendDef2')
trend_def_list = [trend_def1, trend_def2]
trend1 = lds.Trend(ID=1, TrendDefID=trend_def1.ID, RawMin=1, RawMax=10, ScaledMin=0.5, ScaledMax=1.5)
trend2 = lds.Trend(ID=2, TrendDefID=trend_def2.ID, RawMin=2, RawMax=20, ScaledMin=0.2, ScaledMax=1.2)
trend_list = [trend1, trend2]
trend_data1 = lds.TrendData(TrendID=1, Time=1, Data=binary_data)
trend_data2 = lds.TrendData(TrendID=1, Time=2, Data=binary_data)
trend_data3 = lds.TrendData(TrendID=1, Time=3, Data=binary_data)
trend_data4 = lds.TrendData(TrendID=2, Time=2, Data=binary_data)
trend_data_list = [trend_data1, trend_data2, trend_data3, trend_data4]
trend_param1 = lds.TrendParam(TrendParamDefID='RAW_MIN', TrendID=1, Value=1)
trend_param2 = lds.TrendParam(TrendParamDefID='RAW_MAX', TrendID=1, Value=2)
trend_param_list = [trend_param1, trend_param2]
trend_param_def1 = lds.TrendParamDef(ID='RAW_MIN', TrendDefID='ID_1', Name='name', DataType='INT')
trend_param_def2 = lds.TrendParamDef(ID='RAW_MAX', TrendDefID='ID_1', Name='name2', DataType='INT')
trend_param_def_list = [trend_param_def1, trend_param_def2]


def reset_all_trend_objects():
    global trend_def1, trend_def2, trend_def_list, trend1, trend2, trend_list, \
        trend_data1, trend_data2, trend_data3, trend_data4, trend_data_list, \
        trend_param1, trend_param2, trend_param_list,\
        trend_param_def1, trend_param_def2, trend_param_def_list
    trend_def1 = lds.TrendDef(ID='ID_1', Name='TrendDef1')
    trend_def2 = lds.TrendDef(ID='ID_2', Name='TrendDef2')
    trend_def_list = [trend_def1, trend_def2]
    trend1 = lds.Trend(ID=1, TrendDefID=trend_def1.ID, RawMin=1, RawMax=10, ScaledMin=0.5, ScaledMax=1.5)
    trend2 = lds.Trend(ID=2, TrendDefID=trend_def2.ID, RawMin=2, RawMax=20, ScaledMin=0.2, ScaledMax=1.2)
    trend_list = [trend1, trend2]
    trend_data1 = lds.TrendData(TrendID=1, Time=1, Data=binary_data)
    trend_data2 = lds.TrendData(TrendID=1, Time=2, Data=binary_data)
    trend_data3 = lds.TrendData(TrendID=1, Time=3, Data=binary_data)
    trend_data4 = lds.TrendData(TrendID=2, Time=2, Data=binary_data)
    trend_data_list = [trend_data1, trend_data2, trend_data3, trend_data4]
    trend_param1 = lds.TrendParam(TrendParamDefID='RAW_MIN', TrendID=1, Value=1)
    trend_param2 = lds.TrendParam(TrendParamDefID='RAW_MAX', TrendID=1, Value=2)
    trend_param_list = [trend_param1, trend_param2]
    trend_param_def1 = lds.TrendParamDef(ID='RAW_MIN', TrendDefID='ID_1', Name='name', DataType='INT')
    trend_param_def2 = lds.TrendParamDef(ID='RAW_MAX', TrendDefID='ID_1', Name='name2', DataType='INT')
    trend_param_def_list = [trend_param_def1, trend_param_def2]

    return [trend_def_list, trend_list, trend_data_list, trend_param_list, trend_param_def_list]


def reset_trend_def_objects():
    global trend_def1, trend_def2, trend_def_list

    trend_def1 = lds.TrendDef(ID='ID_1', Name='TrendDef1')
    trend_def2 = lds.TrendDef(ID='ID_2', Name='TrendDef2')
    trend_def_list = [trend_def1, trend_def2]

    return [trend_def_list]


def reset_trend_objects():
    global trend_def1, trend_def2, trend_def_list, trend1, trend2, trend_list
    trend_def1 = lds.TrendDef(ID='ID_1', Name='TrendDef1')
    trend_def2 = lds.TrendDef(ID='ID_2', Name='TrendDef2')
    trend_def_list = [trend_def1, trend_def2]
    trend1 = lds.Trend(ID=1, TrendDefID=trend_def1.ID, RawMin=1, RawMax=10, ScaledMin=0.5, ScaledMax=1.5)
    trend2 = lds.Trend(ID=2, TrendDefID=trend_def2.ID, RawMin=2, RawMax=20, ScaledMin=0.2, ScaledMax=1.2)
    trend_list = [trend1, trend2]

    return [trend_def_list, trend_list]


app.dependency_overrides[get_engine] = get_test_engine
test_client = TestClient(app)


def test_list_trends_should_return_ok_response_code_and_empty_list_when_no_trends():
    response = test_client.get("/trend")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 0


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_list_trend_should_return_ok_response_code_and_correct_trends(add_lds_objects):
    response = test_client.get("/trend")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2
    for expected_trend, returned_trend in zip(trend_list, response.json()):
        assert returned_trend['ID'] == expected_trend.ID
        assert returned_trend['TrendDefID'] == expected_trend.TrendDefID.strip()
        assert returned_trend['RawMin'] == expected_trend.RawMin
        assert returned_trend['RawMax'] == expected_trend.RawMax
        assert returned_trend['ScaledMin'] == expected_trend.ScaledMin
        assert returned_trend['ScaledMax'] == expected_trend.ScaledMax


@pytest.mark.parametrize('reset_lds_objects', [reset_trend_def_objects], indirect=True)
def test_create_trend_should_return_created_response_code_and_created_trend_data(add_lds_objects):
    trend_dict = {'ID': 1, 'TrendDefID': 'ID_1', 'RawMin': 100,
                  'RawMax': 1000, 'ScaledMin': -1.5, 'ScaledMax': 2.25}
    response = test_client.post("/trend", json=trend_dict)
    assert response.status_code == status.HTTP_201_CREATED
    returned_trend = response.json()
    assert returned_trend['ID'] == trend_dict['ID']
    assert returned_trend['TrendDefID'] == trend_dict['TrendDefID']
    assert returned_trend['RawMin'] == trend_dict['RawMin']
    assert returned_trend['RawMax'] == trend_dict['RawMax']
    assert returned_trend['ScaledMin'] == trend_dict['ScaledMin']
    assert returned_trend['ScaledMax'] == trend_dict['ScaledMax']
    with Session(get_test_engine()) as session:
        trends_count = session.execute(select(func.count()).select_from(lds.Trend)).fetchall()[0][0]
    assert trends_count == 1


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_create_tren_should_return_conflict_response_code_and_error_when_id_not_unique(add_lds_objects):
    trend_dict = {'ID': trend1.ID, 'TrendDefID': 'ID_1', 'RawMin': 100,
                  'RawMax': 1000, 'ScaledMin': -1.5, 'ScaledMax': 2.25}
    response = test_client.post("/trend", json=trend_dict)
    assert response.status_code == status.HTTP_409_CONFLICT
    error = response.json()
    assert error['code'] == status.HTTP_409_CONFLICT
    assert error['message'] == 'Integrity error when creating trend'


def test_create_trend_should_return_conflict_response_code_and_error_when_no_trend_def_with_given_id():
    trend_dict = {'ID': 1, 'TrendDefID': 'ID_1', 'RawMin': 100,
                  'RawMax': 1000, 'ScaledMin': -1.5, 'ScaledMax': 2.25}
    response = test_client.post("/trend", json=trend_dict)
    assert response.status_code == status.HTTP_409_CONFLICT
    error = response.json()
    assert error['code'] == status.HTTP_409_CONFLICT
    assert error['message'] == 'Integrity error when creating trend'


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_get_trend_data_should_return_ok_response_code_and_correct_trend_data_when_samples_count_is_equal_to_time_delta(add_lds_objects):  # noqa
    samples = 3
    response = test_client.get("/trend/" + str(trend1.ID) + "/data/" + str(trend_data1.Time) +
                               "/" + str(trend_data3.Time) + "/" + str(samples))
    assert response.status_code == status.HTTP_200_OK
    returned_trend_datas = response.json()
    for returned_trend_data, expected_trend_data in zip(returned_trend_datas, trend_data_list[:3]):
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
    returned_trend_datas = response.json()
    for count, returned_trend_data in enumerate(returned_trend_datas):
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
    returned_trend_datas = response.json()
    for count, returned_trend_data in enumerate(returned_trend_datas):
        timestamp_ms = calculate_expected_timestamp_ms(count, trend_data1.Time, trend_data3.Time, samples)
        trend_data_num = calculate_expected_trend_data_number(count, trend_data1.Time, trend_data3.Time, samples)
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
    returned_trend_datas = response.json()
    for count, returned_trend_data in enumerate(returned_trend_datas):
        timestamp_ms = calculate_expected_timestamp_ms(count, trend_data1.Time, trend_data3.Time + 1, samples)
        assert returned_trend_data['Timestamp'] == count + 1
        assert returned_trend_data['TimestampMs'] == timestamp_ms
        assert returned_trend_data['Data'][0]['ID'] == trend1.ID
        if count == len(returned_trend_datas) - 1:
            assert returned_trend_data['Data'][0]['Value'] is None
        else:
            assert returned_trend_data['Data'][0]['Value'] == calculate_expected_value(trend1, timestamp_ms)


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_get_trend_data_should_return_ok_response_code_and_correct_trend_data_when_not_all_trends_exists(add_lds_objects):  # noqa
    samples = 2
    response = test_client.get("/trend/" + str(trend2.ID) + ",10/data/" + str(trend_data4.Time) +
                               "/" + str(trend_data4.Time) + "/" + str(samples))
    assert response.status_code == status.HTTP_200_OK
    returned_trend_datas = response.json()
    for count, returned_trend_data in enumerate(returned_trend_datas):
        timestamp_ms = calculate_expected_timestamp_ms(count, trend_data4.Time, trend_data4.Time, samples)
        assert returned_trend_data['Timestamp'] == 2
        assert returned_trend_data['TimestampMs'] == timestamp_ms
        assert returned_trend_data['Data'][0]['ID'] == trend2.ID
        assert returned_trend_data['Data'][0]['Value'] == calculate_expected_value(trend2, timestamp_ms)


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
    with patch('api.routers.trend.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(1970, 1, 1, second=3, tzinfo=timezone.utc)

        samples = 3
        response = test_client.get("/trend/" + str(trend1.ID) + "/current_data/" +
                                   str(trend_data3.Time - trend_data1.Time) + "/" + str(samples))
        assert response.status_code == status.HTTP_200_OK
        returned_trend_datas = response.json()
        for returned_trend_data, expected_trend_data in zip(returned_trend_datas, trend_data_list[:3]):
            assert returned_trend_data['Timestamp'] == expected_trend_data.Time
            assert returned_trend_data['TimestampMs'] == 0
            assert returned_trend_data['Data'][0]['ID'] == expected_trend_data.TrendID
            assert returned_trend_data['Data'][0]['Value'] == calculate_expected_value(trend1, 0)


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_get_trend_current_data_should_return_ok_response_code_and_correct_trend_data_when_samples_count_is_higher_than_time_delta(add_lds_objects):  # noqa
    with patch('api.routers.trend.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(1970, 1, 1, second=3, tzinfo=timezone.utc)

        samples = 9
        response = test_client.get("/trend/" + str(trend1.ID) + "/current_data/" +
                                   str(trend_data3.Time - trend_data1.Time) + "/" + str(samples))
        assert response.status_code == status.HTTP_200_OK
        returned_trend_datas = response.json()
        for count, returned_trend_data in enumerate(returned_trend_datas):
            timestamp_ms = calculate_expected_timestamp_ms(count, trend_data1.Time, trend_data3.Time, samples)
            trend_data_num = calculate_expected_trend_data_number(count, trend_data1.Time, trend_data3.Time, samples)
            assert returned_trend_data['Timestamp'] == trend_data_list[trend_data_num].Time
            assert returned_trend_data['TimestampMs'] == timestamp_ms
            assert returned_trend_data['Data'][0]['ID'] == trend_data_list[trend_data_num].TrendID
            assert returned_trend_data['Data'][0]['Value'] == calculate_expected_value(trend1, timestamp_ms)


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_get_trend_current_data_should_return_ok_response_code_and_correct_trend_data_when_samples_count_is_lower_than_time_delta(add_lds_objects):  # noqa
    with patch('api.routers.trend.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(1970, 1, 1, second=3, tzinfo=timezone.utc)

        samples = 2
        response = test_client.get("/trend/" + str(trend1.ID) + "/current_data/" +
                                   str(trend_data3.Time - trend_data1.Time) + "/" + str(samples))
        assert response.status_code == status.HTTP_200_OK
        returned_trend_datas = response.json()
        for count, returned_trend_data in enumerate(returned_trend_datas):
            timestamp_ms = calculate_expected_timestamp_ms(count, trend_data1.Time, trend_data3.Time, samples)
            trend_data_num = calculate_expected_trend_data_number(count, trend_data1.Time, trend_data3.Time, samples)
            assert returned_trend_data['Timestamp'] == trend_data_list[trend_data_num].Time
            assert returned_trend_data['TimestampMs'] == timestamp_ms
            assert returned_trend_data['Data'][0]['ID'] == trend_data_list[trend_data_num].TrendID
            assert returned_trend_data['Data'][0]['Value'] == calculate_expected_value(trend1, timestamp_ms)


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_get_trend_current_data_should_return_ok_response_code_and_correct_trend_data_when_not_all_trend_datas_exists(add_lds_objects):  # noqa
    with patch('api.routers.trend.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(1970, 1, 1, second=4, tzinfo=timezone.utc)

        samples = 4
        response = test_client.get("/trend/" + str(trend1.ID) + "/current_data/" +
                                   str(trend_data3.Time+1 - trend_data1.Time) + "/" + str(samples))
        assert response.status_code == status.HTTP_200_OK
        returned_trend_datas = response.json()
        for count, returned_trend_data in enumerate(returned_trend_datas):
            timestamp_ms = calculate_expected_timestamp_ms(count, trend_data1.Time, trend_data3.Time + 1, samples)
            assert returned_trend_data['Timestamp'] == count + 1
            assert returned_trend_data['TimestampMs'] == timestamp_ms
            assert returned_trend_data['Data'][0]['ID'] == trend1.ID
            if count == len(returned_trend_datas) - 1:
                assert returned_trend_data['Data'][0]['Value'] is None
            else:
                assert returned_trend_data['Data'][0]['Value'] == calculate_expected_value(trend1, timestamp_ms)


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_get_trend_current_data_should_return_ok_response_code_and_correct_trend_data_when_not_all_trends_exists(add_lds_objects):  # noqa
    with patch('api.routers.trend.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(1970, 1, 1, second=2, tzinfo=timezone.utc)

        samples = 2
        response = test_client.get("/trend/" + str(trend2.ID) + ",10/current_data/" +
                                   str(trend_data4.Time - trend_data4.Time) + "/" + str(samples))
        assert response.status_code == status.HTTP_200_OK
        returned_trend_datas = response.json()
        for count, returned_trend_data in enumerate(returned_trend_datas):
            timestamp_ms = calculate_expected_timestamp_ms(count, trend_data4.Time, trend_data4.Time, samples)
            assert returned_trend_data['Timestamp'] == 2
            assert returned_trend_data['TimestampMs'] == timestamp_ms
            assert returned_trend_data['Data'][0]['ID'] == trend2.ID
            assert returned_trend_data['Data'][0]['Value'] == calculate_expected_value(trend2, timestamp_ms)


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_get_trend_current_data_should_return_not_found_response_code_and_error_when_no_trend_data_exists(add_lds_objects):  # noqa
    with patch('api.routers.trend.datetime') as mock_datetime:
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


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_delete_trend_by_id_should_return_no_content_response_code_and_remove_trend(add_lds_objects):
    response = test_client.delete("/trend/" + str(trend1.ID))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    with Session(get_test_engine()) as session:
        trends_count = session.execute(select(func.count()).select_from(lds.Trend)).fetchall()[0][0]
    assert trends_count == 1


def test_delete_trend_by_id_should_return_not_found_response_code_and_error_when_no_trend_with_given_id():
    response = test_client.delete("/trend/" + str(trend1.ID))
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No trend with id = ' + str(trend1.ID)


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_get_trend_by_id_should_return_ok_response_code_and_trend_of_given_id(add_lds_objects):
    response = test_client.get("/trend/" + str(trend1.ID))
    assert response.status_code == status.HTTP_200_OK
    returned_trend = response.json()
    assert returned_trend['ID'] == trend1.ID
    assert returned_trend['TrendDefID'] == trend1.TrendDefID.strip()
    assert returned_trend['RawMin'] == trend1.RawMin
    assert returned_trend['RawMax'] == trend1.RawMax
    assert returned_trend['ScaledMin'] == trend1.ScaledMin
    assert returned_trend['ScaledMax'] == trend1.ScaledMax


def test_get_trend_by_id_should_return_not_found_response_code_and_error_when_no_trend_with_given_id():
    response = test_client.get("/trend/" + str(trend1.ID))
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No trend with id = ' + str(trend1.ID)


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_update_trend_by_id_should_return_ok_response_code_and_trend_of_given_id(add_lds_objects):
    update_trend_dict = {'TrendDefID': 'ID_1', 'RawMin': 100, 'RawMax': 1500,
                         'ScaledMin': 1.3, 'ScaledMax': 9.99}
    response = test_client.put("/trend/" + str(trend2.ID), json=update_trend_dict)
    assert response.status_code == status.HTTP_200_OK
    returned_trend = response.json()
    assert returned_trend['ID'] == trend2.ID
    assert returned_trend['TrendDefID'] == update_trend_dict['TrendDefID']
    assert returned_trend['RawMin'] == update_trend_dict['RawMin']
    assert returned_trend['RawMax'] == update_trend_dict['RawMax']
    assert returned_trend['ScaledMin'] == update_trend_dict['ScaledMin']
    assert returned_trend['ScaledMax'] == update_trend_dict['ScaledMax']


def test_update_trend_by_id_should_return_not_found_response_code_and_error_when_no_trend_with_given_id():
    update_trend_dict = {'TrendDefID': 'ID_1', 'RawMin': 100, 'RawMax': 1500,
                         'ScaledMin': 1.3, 'ScaledMax': 9.99}
    response = test_client.put("/trend/" + str(trend2.ID), json=update_trend_dict)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No trend with id = ' + str(trend2.ID)


@pytest.mark.parametrize('reset_lds_objects', [reset_trend_objects], indirect=True)
def test_list_trend_params_should_return_ok_response_code_and_empty_list_when_no_trend_params_for_given_trend_id(add_lds_objects): # noqa
    response = test_client.get("/trend/" + str(trend1.ID) + "/param")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 0


def test_list_trend_params_should_return_ok_response_code_and_error_when_no_trend_with_given_id():
    response = test_client.get("/trend/" + str(trend1.ID) + "/param")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No trend with id = ' + str(trend1.ID)


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_list_trend_params_should_return_ok_response_code_and_correct_trend_params_for_given_trend_id(add_lds_objects):
    response = test_client.get("/trend/" + str(trend1.ID) + "/param")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2
    for expected_trend_param_def, expected_trend_param, returned_trend_param in (
            zip(trend_param_def_list, trend_param_list, reversed(response.json()))):
        assert returned_trend_param['TrendID'] == expected_trend_param.TrendID
        assert returned_trend_param['Value'] == expected_trend_param.Value
        assert returned_trend_param['TrendParamDefID'] == expected_trend_param.TrendParamDefID.strip()
        assert returned_trend_param['DataType'] == expected_trend_param_def.DataType
        assert returned_trend_param['Name'] == expected_trend_param_def.Name.strip()


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_get_trend_param_by_id_should_return_ok_response_code_and_trend_param_of_given_trend_and_trend_param_id(add_lds_objects): # noqa
    response = test_client.get("/trend/" + str(trend1.ID) + "/param/" + trend_param1.TrendParamDefID)
    assert response.status_code == status.HTTP_200_OK
    returned_trend_param = response.json()
    assert returned_trend_param['TrendID'] == trend_param1.TrendID
    assert returned_trend_param['Value'] == trend_param1.Value
    assert returned_trend_param['TrendParamDefID'] == trend_param1.TrendParamDefID.strip()
    assert returned_trend_param['DataType'] == trend_param_def1.DataType
    assert returned_trend_param['Name'] == trend_param_def1.Name.strip()


def test_get_trend_param_by_id_should_return_not_found_response_code_and_error_when_no_trend_param_with_given_id():
    response = test_client.get("/trend/" + str(trend1.ID) + "/param/" + trend_param1.TrendParamDefID)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == (f"No trend param for trend with id = {trend1.ID} "
                                f"and trendParamDef with id = {trend_param1.TrendParamDefID.strip()}")


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_update_trend_param_should_return_ok_response_code_and_trend_param_of_given_id(add_lds_objects):
    update_trend_param_value = '1444'
    response = test_client.put("/trend/" + str(trend1.ID) + "/param/" + trend_param1.TrendParamDefID,
                               json=update_trend_param_value)
    assert response.status_code == status.HTTP_200_OK
    returned_trend_param = response.json()
    assert returned_trend_param['TrendID'] == trend_param1.TrendID
    assert returned_trend_param['Value'] == update_trend_param_value
    assert returned_trend_param['TrendParamDefID'] == trend_param1.TrendParamDefID.strip()
    assert returned_trend_param['DataType'] == trend_param_def1.DataType
    assert returned_trend_param['Name'] == trend_param_def1.Name.strip()


def test_update_trend_param_should_return_not_found_response_code_and_error_when_no_trend_param_with_given_id():
    update_trend_param_value = '1444'
    response = test_client.put("/trend/" + str(trend1.ID) + "/param/" + trend_param1.TrendParamDefID,
                               json=update_trend_param_value)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == (f"No trend param for trend with id = {trend1.ID} "
                                f"and trendParamDef with id = {trend_param1.TrendParamDefID.strip()}")


def calculate_expected_value(trend: lds.Trend, timestamp_ms: int) -> float:
    one_second_data = struct.unpack("H" * 100, binary_data)
    return ((trend.ScaledMax - trend.ScaledMin) * (one_second_data[-timestamp_ms // 10 - 1] - trend.RawMin)
            / (trend.RawMax - trend.RawMin) + trend.ScaledMin)


def calculate_expected_timestamp_ms(count: int, time1: int, time2: int, samples: int) -> int:
    return (count * (((time2 - time1 + 1) * 100) // samples)) % 100 * 10


def calculate_expected_trend_data_number(count: int, time1: int, time2: int, samples: int) -> int:
    return ((count * (((time2 - time1 + 1) * 100) // samples)) // 100
            % (time2 - time1 + 1))
