import os
import sys
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from starlette import status
from starlette.testclient import TestClient
from api.routers.utils.security import get_user_token
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))  # noqa: E402
from api.app import app
from db import get_engine
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
                   Name='Trend2', TrendGroupID=trend_group.ID, UnitID=unit.ID, Color='Red', Enabled=False)
trend3 = lds.Trend(ID=4, TrendDefID=trend_def1.ID, RawMin=3, RawMax=10, ScaledMin=0.5, ScaledMax=1.5,
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
                       Name='Trend2', TrendGroupID=trend_group.ID, UnitID=unit.ID, Color='Red', Enabled=False)
    trend3 = lds.Trend(ID=4, TrendDefID=trend_def1.ID, RawMin=3, RawMax=10, ScaledMin=0.5, ScaledMax=1.5,
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


def reset_trend_def_objects():
    global trend_def1, trend_def2, trend_def_list, trend_group, unit

    trend_def1 = lds.TrendDef(ID='ID_1', Name='TrendDef1')
    trend_def2 = lds.TrendDef(ID='ID_2', Name='TrendDef2')
    trend_def_list = [trend_def1, trend_def2]
    trend_group = lds.TrendGroup(ID=1, Name='Group1')
    unit = lds.Unit(ID='Unit1', Name='Unit1', Symbol='U')

    return [trend_def_list, [trend_group], [unit]]


app.dependency_overrides[get_user_token] = lambda: {"sub": "test_user"}  # type: ignore[attr-defined]
test_client = TestClient(app)


def test_list_trends_should_return_ok_response_code_and_empty_list_when_no_trends():
    response = test_client.get("/trend")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['items']) == 0


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_list_trends_should_return_ok_response_code_and_correct_trends(add_lds_objects):
    response = test_client.get("/trend")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()['items']
    assert len(items) == len(trend_list)
    for expected_trend, returned_trend in zip(trend_list, items):
        assert returned_trend['ID'] == expected_trend.ID
        assert returned_trend['TrendDefID'] == expected_trend.TrendDefID.strip()
        assert returned_trend['RawMin'] == expected_trend.RawMin
        assert returned_trend['RawMax'] == expected_trend.RawMax
        assert returned_trend['ScaledMin'] == expected_trend.ScaledMin
        assert returned_trend['ScaledMax'] == expected_trend.ScaledMax
        assert returned_trend['Name'] == expected_trend.Name
        assert returned_trend['UnitID'] == expected_trend.UnitID.strip()
        assert returned_trend['TrendGroupID'] == expected_trend.TrendGroupID
        assert returned_trend['Color'] == expected_trend.Color
        assert returned_trend['TimeDelta'] == 0
        assert returned_trend['TimeExponent'] is None
        assert returned_trend['Format'] is None
        assert returned_trend['Symbol'] is None
        assert returned_trend['NodeID'] is None
        assert returned_trend['Enabled'] == expected_trend.Enabled


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_list_trends_should_return_ok_response_code_and_correct_page_data(add_lds_objects):
    size = 1
    page = 1
    response = test_client.get(f"/trend?size={size}&page={page}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == size
    assert response.json()['total'] == len(trend_list)
    assert response.json()['pages'] == len(trend_list) // size if len(trend_list) % size == 0 \
        else len(trend_list) // size + 1
    assert response.json()['size'] == size
    assert response.json()['page'] == page


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_list_trends_should_return_ok_response_code_and_default_page_data(add_lds_objects):
    response = test_client.get("/trend")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == len(trend_list)
    assert response.json()['total'] == len(trend_list)
    assert response.json()['pages'] == 1
    assert response.json()['size'] == 50
    assert response.json()['page'] == 1


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_list_trends_should_return_ok_response_code_and_data_filtered_by_odata_query(add_lds_objects):
    odata_filter = f'ID gt {trend1.ID} and ID lt {trend3.ID}'
    response = test_client.get(f"/trend?filter={odata_filter}")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()['items']
    assert len(items) == 1
    returned_trend = items[0]
    assert returned_trend['ID'] == trend2.ID
    assert returned_trend['TrendDefID'] == trend2.TrendDefID.strip()
    assert returned_trend['RawMin'] == trend2.RawMin
    assert returned_trend['RawMax'] == trend2.RawMax
    assert returned_trend['ScaledMin'] == trend2.ScaledMin
    assert returned_trend['ScaledMax'] == trend2.ScaledMax
    assert returned_trend['Name'] == trend2.Name
    assert returned_trend['UnitID'] == trend2.UnitID.strip()
    assert returned_trend['TrendGroupID'] == trend2.TrendGroupID
    assert returned_trend['Color'] == trend2.Color
    assert returned_trend['TimeDelta'] == 0
    assert returned_trend['TimeExponent'] is None
    assert returned_trend['Format'] is None
    assert returned_trend['Symbol'] is None
    assert returned_trend['NodeID'] is None
    assert returned_trend['Enabled'] == trend2.Enabled


@pytest.mark.parametrize('reset_lds_objects', [reset_trend_def_objects], indirect=True)
def test_create_trend_should_return_created_response_code_and_created_trend_data(add_lds_objects):
    trend_dict = {'TrendDefID': 'ID_1', 'RawMin': 100,
                  'RawMax': 1000, 'ScaledMin': -1.5, 'ScaledMax': 2.25,
                  'UnitID': unit.ID, 'TrendGroupID': trend_group.ID, 'Color': 'Blue', 'Name': 'New trend'}
    response = test_client.post("/trend", json=trend_dict)
    assert response.status_code == status.HTTP_201_CREATED
    returned_trend = response.json()
    assert returned_trend['ID'] == 1000
    assert returned_trend['TrendDefID'] == trend_dict['TrendDefID']
    assert returned_trend['RawMin'] == trend_dict['RawMin']
    assert returned_trend['RawMax'] == trend_dict['RawMax']
    assert returned_trend['ScaledMin'] == trend_dict['ScaledMin']
    assert returned_trend['ScaledMax'] == trend_dict['ScaledMax']
    assert returned_trend['Name'] == trend_dict['Name']
    assert returned_trend['UnitID'] == trend_dict['UnitID'].strip()
    assert returned_trend['TrendGroupID'] == trend_dict['TrendGroupID']
    assert returned_trend['Color'] == trend_dict['Color']
    assert returned_trend['TimeDelta'] == 0
    assert returned_trend['TimeExponent'] is None
    assert returned_trend['Format'] is None
    assert returned_trend['Symbol'] is None
    assert returned_trend['NodeID'] is None
    assert returned_trend['Enabled'] is True
    with Session(get_engine()) as session:
        trends_count = session.execute(select(func.count()).select_from(lds.Trend)).fetchall()[0][0]
    assert trends_count == 1


@pytest.mark.parametrize('reset_lds_objects', [reset_trend_def_objects], indirect=True)
def test_create_trend_should_return_unprocessable_entity_response_code_when_model_condition_not_met(add_lds_objects):
    trend_dict = {'TrendDefID': 'ID_1', 'RawMin': 100,
                  'RawMax': 100, 'ScaledMin': -1.5, 'ScaledMax': 2.25,
                  'UnitID': unit.ID, 'TrendGroupID': trend_group.ID, 'Color': 'Blue', 'Name': 'New trend'}
    response = test_client.post("/trend", json=trend_dict)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    error = response.json()
    assert error['code'] == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert error['message'] == 'RawMin must be smaller than RawMax'

    trend_dict = {'TrendDefID': 'ID_1', 'RawMin': 100,
                  'RawMax': 1000, 'ScaledMin': -1.5, 'ScaledMax': -2.25,
                  'UnitID': unit.ID, 'TrendGroupID': trend_group.ID, 'Color': 'Blue', 'Name': 'New trend'}
    response = test_client.post("/trend", json=trend_dict)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    error = response.json()
    assert error['code'] == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert error['message'] == 'ScaledMin must be smaller than ScaledMax'


def test_create_trend_should_return_conflict_response_code_and_error_when_no_trend_def_with_given_id():
    trend_dict = {'ID': 1, 'TrendDefID': 'ID_1', 'RawMin': 100,
                  'RawMax': 1000, 'ScaledMin': -1.5, 'ScaledMax': 2.25,
                  'UnitID': unit.ID, 'TrendGroupID': trend_group.ID, 'Color': 'Blue', 'Name': 'New trend'}
    response = test_client.post("/trend", json=trend_dict)
    assert response.status_code == status.HTTP_409_CONFLICT
    error = response.json()
    assert error['code'] == status.HTTP_409_CONFLICT
    assert error['message'] == 'Integrity error when creating trend'


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_delete_trend_by_id_should_return_no_content_response_code_and_remove_trend(add_lds_objects):
    response = test_client.delete("/trend/" + str(trend1.ID))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    with Session(get_engine()) as session:
        trends_count = session.execute(select(func.count()).select_from(lds.Trend)).fetchall()[0][0]
    assert trends_count == len(trend_list) - 1


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
    assert returned_trend['Name'] == trend1.Name
    assert returned_trend['UnitID'] == trend1.UnitID.strip()
    assert returned_trend['TrendGroupID'] == trend1.TrendGroupID
    assert returned_trend['Color'] == trend1.Color
    assert returned_trend['TimeDelta'] == trend1.TimeDelta
    assert returned_trend['TimeExponent'] is None
    assert returned_trend['Format'] is None
    assert returned_trend['Symbol'] is None
    assert returned_trend['NodeID'] is None
    assert returned_trend['Enabled'] == trend1.Enabled


def test_get_trend_by_id_should_return_not_found_response_code_and_error_when_no_trend_with_given_id():
    response = test_client.get("/trend/" + str(trend1.ID))
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No trend with id = ' + str(trend1.ID)


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_update_trend_should_return_ok_response_code_and_trend_of_given_id(add_lds_objects):
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
    assert returned_trend['Name'] == trend2.Name
    assert returned_trend['UnitID'] == trend2.UnitID.strip()
    assert returned_trend['TrendGroupID'] == trend2.TrendGroupID
    assert returned_trend['Color'] == trend2.Color
    assert returned_trend['TimeDelta'] == trend2.TimeDelta
    assert returned_trend['TimeExponent'] is None
    assert returned_trend['Format'] is None
    assert returned_trend['Symbol'] is None
    assert returned_trend['NodeID'] is None
    assert returned_trend['Enabled'] == trend2.Enabled


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_update_trend_should_return_unprocessable_entity_response_code_when_model_condition_not_met(add_lds_objects):
    update_trend_dict = {'RawMax': 0}
    response = test_client.put("/trend/" + str(trend2.ID), json=update_trend_dict)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    error = response.json()
    assert error['code'] == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert error['message'] == 'RawMin must be smaller than RawMax'

    update_trend_dict = {'ScaledMin': 10000}
    response = test_client.put("/trend/" + str(trend2.ID), json=update_trend_dict)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    error = response.json()
    assert error['code'] == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert error['message'] == 'ScaledMin must be smaller than ScaledMax'


def test_update_trend_should_return_not_found_response_code_and_error_when_no_trend_with_given_id():
    update_trend_dict = {'TrendDefID': 'ID_1', 'RawMin': 100, 'RawMax': 1500,
                         'ScaledMin': 1.3, 'ScaledMax': 9.99}
    response = test_client.put("/trend/" + str(trend2.ID), json=update_trend_dict)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No trend with id = ' + str(trend2.ID)


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_enable_trend_should_return_no_content_response_code_and_change_trend_enabled_flag(add_lds_objects):
    response = test_client.put("/trend/" + str(trend1.ID) + "/enable")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    with Session(get_engine()) as session:
        trend = session.execute(select(lds.Trend).where(lds.Trend.ID == trend1.ID)).fetchall()[0][0] # noqa
    assert trend.Enabled is not trend1.Enabled

    response = test_client.put("/trend/" + str(trend1.ID) + "/enable")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    with Session(get_engine()) as session:
        trend = session.execute(select(lds.Trend).where(lds.Trend.ID == trend1.ID)).fetchall()[0][0]  # noqa
    assert trend.Enabled is trend1.Enabled


def test_enable_trend_should_return_not_found_response_code_and_error_when_no_trend_with_given_id():
    response = test_client.put("/trend/" + str(trend1.ID) + "/enable")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No trend with id = ' + str(trend1.ID)
