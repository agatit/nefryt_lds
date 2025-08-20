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
                   Name='Trend2', TrendGroupID=trend_group.ID, UnitID=unit.ID, Color='Red')
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
                       Name='Trend2', TrendGroupID=trend_group.ID, UnitID=unit.ID, Color='Red')
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


def reset_trend_objects():
    global trend_def1, trend_def2, trend_def_list, trend1, trend2, trend3, trend_list, trend_group, unit
    trend_def1 = lds.TrendDef(ID='ID_1', Name='TrendDef1')
    trend_def2 = lds.TrendDef(ID='ID_2', Name='TrendDef2')
    trend_def_list = [trend_def1, trend_def2]
    trend_group = lds.TrendGroup(ID=1, Name='Group1')
    unit = lds.Unit(ID='Unit1', Name='Unit1', Symbol='U')
    trend1 = lds.Trend(ID=1, TrendDefID=trend_def1.ID, RawMin=1, RawMax=10, ScaledMin=0.5, ScaledMax=1.5,
                       Name='Trend1', TrendGroupID=trend_group.ID, UnitID=unit.ID, Color='Black')
    trend2 = lds.Trend(ID=2, TrendDefID=trend_def2.ID, RawMin=2, RawMax=20, ScaledMin=0.2, ScaledMax=1.2,
                       Name='Trend2', TrendGroupID=trend_group.ID, UnitID=unit.ID, Color='Red')
    trend3 = lds.Trend(ID=4, TrendDefID=trend_def1.ID, RawMin=3, RawMax=10, ScaledMin=0.5, ScaledMax=1.5,
                       Name='Trend4', TrendGroupID=trend_group.ID, UnitID=unit.ID, Color='Yellow')
    trend_list = [trend1, trend2, trend3]

    return [trend_def_list, [trend_group], [unit], trend_list]


app.dependency_overrides[get_user_token] = lambda: {"sub": "test_user"}  # type: ignore[attr-defined]
test_client = TestClient(app)


@pytest.mark.parametrize('reset_lds_objects', [reset_trend_objects], indirect=True)
def test_list_trend_params_should_return_ok_response_code_and_empty_list_when_no_trend_params_for_given_trend_id(add_lds_objects):  # noqa
    response = test_client.get("/trend/" + str(trend1.ID) + "/param")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['items']) == 0


def test_list_trend_params_should_return_not_found_response_code_and_error_when_no_trend_with_given_id():
    response = test_client.get("/trend/" + str(trend1.ID) + "/param")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No trend with id = ' + str(trend1.ID)


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_list_trend_params_should_return_ok_response_code_and_correct_trend_params_for_given_trend_id(add_lds_objects):
    response = test_client.get("/trend/" + str(trend1.ID) + "/param")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()['items']
    assert len(items) == len(trend_param_list)
    for expected_trend_param_def, expected_trend_param, returned_trend_param in (
            zip(trend_param_def_list, trend_param_list, items)):
        assert returned_trend_param['TrendID'] == expected_trend_param.TrendID
        assert returned_trend_param['Value'] == expected_trend_param.Value
        assert returned_trend_param['TrendParamDefID'] == expected_trend_param.TrendParamDefID.strip()
        assert returned_trend_param['DataType'] == expected_trend_param_def.DataType.strip()
        assert returned_trend_param['Name'] == expected_trend_param_def.Name.strip()


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_list_trend_params_should_return_ok_response_code_and_correct_page_data(add_lds_objects):
    size = 3
    page = 1
    response = test_client.get("/trend/" + str(trend1.ID) + f"/param?size={size}&page={page}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == len(trend_param_list)
    assert response.json()['total'] == len(trend_param_list)
    assert response.json()['pages'] == len(trend_param_list) // size if len(trend_param_list) % size == 0 \
        else len(trend_param_list) // size + 1
    assert response.json()['size'] == size
    assert response.json()['page'] == page


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_list_trend_params_should_return_ok_response_code_and_default_page_data(add_lds_objects):
    response = test_client.get("/trend/" + str(trend1.ID) + "/param")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == len(trend_param_list)
    assert response.json()['total'] == len(trend_param_list)
    assert response.json()['pages'] == 1
    assert response.json()['size'] == 50
    assert response.json()['page'] == 1


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_list_trend_params_should_return_ok_response_code_and_data_filtered_by_odata_query(add_lds_objects):
    odata_filter = f'Value eq {trend_param3.Value}'
    response = test_client.get("/trend/" + str(trend1.ID) + f"/param?filter={odata_filter}")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()['items']
    assert len(items) == 1
    returned_trend_param = items[0]
    assert returned_trend_param['TrendID'] == trend_param3.TrendID
    assert returned_trend_param['Value'] == trend_param3.Value
    assert returned_trend_param['TrendParamDefID'] == trend_param3.TrendParamDefID.strip()
    assert returned_trend_param['DataType'] == trend_param_def3.DataType.strip()
    assert returned_trend_param['Name'] == trend_param_def3.Name.strip()


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_create_trend_param_should_return_created_response_code_and_created_trend_param_data(add_lds_objects):
    trend_param_dict = {'TrendParamDefID': trend_param_def1.ID.strip(), 'Value': '1111'}
    response = test_client.post("/trend/" + str(trend3.ID) + "/param", json=trend_param_dict)
    assert response.status_code == status.HTTP_201_CREATED
    returned_trend_param = response.json()
    assert returned_trend_param['TrendID'] == trend3.ID
    assert returned_trend_param['Value'] == trend_param_dict['Value']
    assert returned_trend_param['TrendParamDefID'] == trend_param_dict['TrendParamDefID']
    assert returned_trend_param['DataType'] == trend_param_def1.DataType.strip()
    assert returned_trend_param['Name'] == trend_param_def1.Name.strip()
    with Session(get_engine()) as session:
        trend_params_count = session.execute(select(func.count()).select_from(lds.TrendParam)).fetchall()[0][0]
    assert trend_params_count == len(trend_param_list) + 1


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_create_trend_param_should_return_conflict_response_code_and_error_when_key_not_unique(add_lds_objects):
    trend_param_dict = {'TrendParamDefID': trend_param_def3.ID, 'Value': '1111'}
    response = test_client.post("/trend/" + str(trend1.ID) + "/param", json=trend_param_dict)
    assert response.status_code == status.HTTP_409_CONFLICT
    error = response.json()
    assert error['code'] == status.HTTP_409_CONFLICT
    assert error['message'] == 'Integrity error when creating trend param'


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_create_trend_param_should_return_conflict_response_code_and_error_when_no_trend_with_given_id(add_lds_objects):
    trend_param_dict = {'TrendParamDefID': trend_param_def3.ID, 'Value': '1111'}
    response = test_client.post("/trend/100/param", json=trend_param_dict)
    assert response.status_code == status.HTTP_409_CONFLICT
    error = response.json()
    assert error['code'] == status.HTTP_409_CONFLICT
    assert error['message'] == 'No trend with id = 100'


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_create_trend_param_should_return_conflict_response_code_and_error_when_no_trend_param_def_with_given_id(add_lds_objects):
    trend_param_dict = {'TrendParamDefID': 'DEF', 'Value': '1111'}
    response = test_client.post(f"/trend/{trend1.ID}/param", json=trend_param_dict)
    assert response.status_code == status.HTTP_409_CONFLICT
    error = response.json()
    assert error['code'] == status.HTTP_409_CONFLICT
    assert error['message'] == 'No TrendParamDef with id = DEF'


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_delete_trend_param_by_id_should_return_no_content_response_code_and_remove_trend_param(add_lds_objects):
    response = test_client.delete("/trend/" + str(trend1.ID) + "/param/" + trend_param1.TrendParamDefID)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    with Session(get_engine()) as session:
        trend_params_count = session.execute(select(func.count()).select_from(lds.TrendParam)).fetchall()[0][0]
    assert trend_params_count == len(trend_param_list) - 1


def test_delete_trend_param_by_id_should_return_not_found_response_code_and_error_when_no_trend_param_with_given_id():
    response = test_client.delete("/trend/" + str(trend1.ID) + "/param/" + trend_param1.TrendParamDefID)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert (error['message'] == 'No trend param with id = ' + trend_param1.TrendParamDefID +
            ' for trend with id = ' + str(trend1.ID))


@pytest.mark.parametrize('reset_lds_objects', [reset_all_trend_objects], indirect=True)
def test_get_trend_param_by_id_should_return_ok_response_code_and_trend_param_of_given_trend_and_trend_param_id(add_lds_objects):  # noqa
    response = test_client.get("/trend/" + str(trend1.ID) + "/param/" + trend_param1.TrendParamDefID)
    assert response.status_code == status.HTTP_200_OK
    returned_trend_param = response.json()
    assert returned_trend_param['TrendID'] == trend_param1.TrendID
    assert returned_trend_param['Value'] == trend_param1.Value
    assert returned_trend_param['TrendParamDefID'] == trend_param1.TrendParamDefID.strip()
    assert returned_trend_param['DataType'] == trend_param_def1.DataType.strip()
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
    response = test_client.put("/trend/" + str(trend1.ID) + "/param/" + trend_param1.TrendParamDefID.strip(),
                               json=update_trend_param_value)
    assert response.status_code == status.HTTP_200_OK
    returned_trend_param = response.json()
    assert returned_trend_param['TrendID'] == trend_param1.TrendID
    assert returned_trend_param['Value'] == update_trend_param_value
    assert returned_trend_param['TrendParamDefID'] == trend_param1.TrendParamDefID.strip()
    assert returned_trend_param['DataType'] == trend_param_def1.DataType.strip()
    assert returned_trend_param['Name'] == trend_param_def1.Name.strip()


def test_update_trend_param_should_return_not_found_response_code_and_error_when_no_trend_param_with_given_id():
    update_trend_param_value = '1444'
    response = test_client.put("/trend/" + str(trend1.ID) + "/param/" + trend_param1.TrendParamDefID.strip(),
                               json=update_trend_param_value)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == (f"No trend param for trend with id = {trend1.ID} "
                                f"and trendParamDef with id = {trend_param1.TrendParamDefID.strip()}")
