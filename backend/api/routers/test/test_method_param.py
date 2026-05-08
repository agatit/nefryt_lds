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

method_def1 = lds.MethodDef(ID='COMBINED', Name='CombineOtherResults')
method_def2 = lds.MethodDef(ID='WAVE', Name='WaveHeatmap')
method_def_list = [method_def1, method_def2]
pipeline = lds.Pipeline(ID=1, Name='Pipeline1')
method3 = lds.Method(ID=3, MethodDefID='COMBINED', PipelineID=pipeline.ID, Name='Method1')
method2 = lds.Method(ID=2, MethodDefID='WAVE', PipelineID=pipeline.ID, Name='Method2')
method1 = lds.Method(ID=1, MethodDefID='WAVE', PipelineID=pipeline.ID, Name='Method3')
method_list = [method1, method2, method3]
method_param_def1 = lds.MethodParamDef(ID='WAVE_SPEED', MethodDefID='WAVE', Name='Wave speed', DataType='FLOAT')
method_param_def2 = lds.MethodParamDef(ID='ALARM_VALUE', MethodDefID='WAVE', Name='Alarm value', DataType='FLOAT')
method_param_def3 = lds.MethodParamDef(ID='METHODS', MethodDefID='COMBINED', Name='Methods to combine', DataType='LIST')
method_param_def_list = [method_param_def2, method_param_def3, method_param_def1]
method_param1 = lds.MethodParam(MethodID=1, MethodParamDefID='WAVE_SPEED', Value='100.5')
method_param2 = lds.MethodParam(MethodID=1, MethodParamDefID='ALARM_VALUE', Value='0.1')
method_param3 = lds.MethodParam(MethodID=2, MethodParamDefID='WAVE_SPEED', Value='99.1')
method_param4 = lds.MethodParam(MethodID=3, MethodParamDefID='METHODS', Value='1,2')
method_param_list = [method_param1, method_param2, method_param3, method_param4]

def reset_method_objects():
    global method_def1, method_def2, method_def_list, method1, method2, method3, method_list, pipeline

    method_def1 = lds.MethodDef(ID='COMBINED', Name='CombineOtherResults')
    method_def2 = lds.MethodDef(ID='WAVE', Name='WaveHeatmap')
    method_def_list = [method_def1, method_def2]
    pipeline = lds.Pipeline(ID=1, Name='Pipeline1')
    method1 = lds.Method(ID=1, MethodDefID='COMBINED', PipelineID=pipeline.ID, Name='Method1')
    method2 = lds.Method(ID=2, MethodDefID='WAVE', PipelineID=pipeline.ID, Name='Method2')
    method3 = lds.Method(ID=3, MethodDefID='WAVE', PipelineID=pipeline.ID, Name='Method3')
    method_list = [method1, method2, method3]

    return [method_def_list, [pipeline], method_list]


def reset_method_param_objects():
    global method_def1, method_def2, method_def_list,  method1, method2, method3, method_list, \
        method_param_def1, method_param_def2, method_param_def3, method_param_list, \
        method_param1, method_param2, method_param3, method_param4, method_param_def_list, pipeline

    method_def1 = lds.MethodDef(ID='COMBINED', Name='CombineOtherResults')
    method_def2 = lds.MethodDef(ID='WAVE', Name='WaveHeatmap')
    method_def_list = [method_def1, method_def2]
    pipeline = lds.Pipeline(ID=1, Name='Pipeline1')
    method3 = lds.Method(ID=3, MethodDefID='COMBINED', PipelineID=pipeline.ID, Name='Method1')
    method2 = lds.Method(ID=2, MethodDefID='WAVE', PipelineID=pipeline.ID, Name='Method2')
    method1 = lds.Method(ID=1, MethodDefID='WAVE', PipelineID=pipeline.ID, Name='Method3')
    method_list = [method1, method2, method3]
    method_param_def1 = lds.MethodParamDef(ID='WAVE_SPEED', MethodDefID='WAVE', Name='Wave speed', DataType='FLOAT')
    method_param_def2 = lds.MethodParamDef(ID='ALARM_VALUE', MethodDefID='WAVE', Name='Alarm value', DataType='FLOAT')
    method_param_def3 = lds.MethodParamDef(ID='METHODS', MethodDefID='COMBINED', Name='Methods to combine', DataType='LIST')
    method_param_def_list = [method_param_def2, method_param_def3, method_param_def1]
    method_param1 = lds.MethodParam(MethodID=1, MethodParamDefID='WAVE_SPEED', Value='100.5')
    method_param2 = lds.MethodParam(MethodID=1, MethodParamDefID='ALARM_VALUE', Value='0.1')
    method_param3 = lds.MethodParam(MethodID=2, MethodParamDefID='WAVE_SPEED', Value='99.1')
    method_param4 = lds.MethodParam(MethodID=3, MethodParamDefID='METHODS', Value='1,2')
    method_param_list = [method_param1, method_param2, method_param3, method_param4]

    return [method_def_list, [pipeline], method_list, method_param_def_list, method_param_list]


@pytest.mark.parametrize('add_test_context', [reset_method_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_method_param_defs_should_return_ok_response_code_and_empty_list_when_no_method_param_defs(test_client):
    response = test_client.get("/method/param/def")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['items']) == 0


@pytest.mark.parametrize('add_test_context', [reset_method_param_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_method_param_defs_should_return_ok_response_code_and_correct_method_param_defs(test_client):
    response = test_client.get("/method/param/def")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()['items']
    assert len(items) == len(method_param_def_list)
    for expected_method_param_def, returned_method_param_def in zip(method_param_def_list, items):
        assert returned_method_param_def['ID'] == expected_method_param_def.ID.strip()
        assert returned_method_param_def['MethodDefID'] == expected_method_param_def.MethodDefID.strip()
        assert returned_method_param_def['Name'] == expected_method_param_def.Name
        assert returned_method_param_def['DataType'] == expected_method_param_def.DataType.strip()


@pytest.mark.parametrize('add_test_context', [reset_method_param_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_method_param_defs_should_return_ok_response_code_and_correct_page_data(test_client):
    size = 1
    page = 2
    response = test_client.get(f"/method/param/def?size={size}&page={page}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == size
    assert response.json()['total'] == len(method_param_def_list)
    assert response.json()['pages'] == len(method_param_def_list) // size if len(method_param_def_list) % size == 0 \
        else len(method_param_def_list) // size + 1
    assert response.json()['size'] == size
    assert response.json()['page'] == page


@pytest.mark.parametrize('add_test_context', [reset_method_param_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_method_param_defs_should_return_ok_response_code_and_default_page_data(test_client):
    response = test_client.get("/method/param/def")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == len(method_param_def_list)
    assert response.json()['total'] == len(method_param_def_list)
    assert response.json()['pages'] == 1
    assert response.json()['size'] == 50
    assert response.json()['page'] == 1


@pytest.mark.parametrize('add_test_context', [reset_method_param_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_method_param_defs_should_return_ok_response_code_and_data_filtered_by_odata_query(test_client):
    odata_filter = f'DataType ne \'{method_param_def3.DataType}\''
    response = test_client.get(f"/method/param/def?filter={odata_filter}")
    assert response.status_code == status.HTTP_200_OK
    returned_method_param_defs = response.json()['items']
    expected_method_param_defs = [method_param_def2, method_param_def1]
    assert len(returned_method_param_defs) == len(expected_method_param_defs)
    for returned_method_param_def, expected_method_param_def in zip(returned_method_param_defs,expected_method_param_defs):
        assert returned_method_param_def['ID'] == expected_method_param_def.ID.strip()
        assert returned_method_param_def['MethodDefID'] == expected_method_param_def.MethodDefID.strip()
        assert returned_method_param_def['Name'] == expected_method_param_def.Name
        assert returned_method_param_def['DataType'] == expected_method_param_def.DataType.strip()


@pytest.mark.parametrize('add_test_context', [reset_method_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_method_params_by_method_id_should_return_ok_response_code_and_empty_list_when_no_method_params_for_given_method_id(test_client):  # noqa
    response = test_client.get("/method/" + str(method2.ID) + "/param")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['items']) == 0


def test_list_method_params_by_method_id_should_return_not_found_response_code_and_error_when_no_method_with_given_id(test_client):
    response = test_client.get("/method/" + str(method2.ID) + "/param")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No method with id = ' + str(method2.ID)


@pytest.mark.parametrize('add_test_context', [reset_method_param_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_method_params_by_method_id_should_return_ok_response_code_and_correct_method_params_for_given_method_id(test_client):
    response = test_client.get("/method/" + str(method1.ID) + "/param")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()['items']
    assert len(items) == 2
    expected_method_param_def_list = [method_param_def2, method_param_def1]
    expected_method_param_list = [method_param2, method_param1]
    for expected_method_param_def, expected_method_param, returned_method_param in (
            zip(expected_method_param_def_list, expected_method_param_list, items)):
        assert returned_method_param['MethodID'] == expected_method_param.MethodID
        assert returned_method_param['MethodParamDefID'] == expected_method_param.MethodParamDefID.strip()
        assert returned_method_param['Value'] == expected_method_param.Value
        assert returned_method_param['DataType'] == expected_method_param_def.DataType.strip()
        assert returned_method_param['Name'] == expected_method_param_def.Name


@pytest.mark.parametrize('add_test_context', [reset_method_param_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_method_params_by_method_id_should_return_ok_response_code_and_correct_page_data(test_client):
    size = 3
    page = 1
    response = test_client.get("/method/" + str(method1.ID) + f"/param?size={size}&page={page}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == 2
    assert response.json()['total'] == 2
    assert response.json()['pages'] == 2 // size if 2 % size == 0 \
        else 2 // size + 1
    assert response.json()['size'] == size
    assert response.json()['page'] == page


@pytest.mark.parametrize('add_test_context', [reset_method_param_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_method_params_by_method_id_should_return_ok_response_code_and_default_page_data(test_client):
    response = test_client.get("/method/" + str(method1.ID) + "/param")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == 2
    assert response.json()['total'] == 2
    assert response.json()['pages'] == 1
    assert response.json()['size'] == 50
    assert response.json()['page'] == 1


@pytest.mark.parametrize('add_test_context', [reset_method_param_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_method_params_by_method_id_should_return_ok_response_code_and_data_filtered_by_odata_query(test_client):
    odata_filter = f'MethodParamDefID eq \'{method_param2.MethodParamDefID.strip()}\''
    response = test_client.get("/method/" + str(method1.ID) + f"/param?filter={odata_filter}")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()['items']
    assert len(items) == 1
    returned_method_param = items[0]
    assert returned_method_param['MethodID'] == method_param2.MethodID
    assert returned_method_param['MethodParamDefID'] == method_param2.MethodParamDefID.strip()
    assert returned_method_param['Value'] == method_param2.Value
    assert returned_method_param['DataType'] == method_param_def2.DataType.strip()
    assert returned_method_param['Name'] == method_param_def2.Name


@pytest.mark.parametrize('add_test_context', [reset_method_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_required_method_params_by_method_id_should_return_ok_response_code_and_empty_list_when_no_method_params_for_given_method_id(test_client):  # noqa
    response = test_client.get("/method/" + str(method2.ID) + "/param/all")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['items']) == 0


def test_list_required_method_params_by_method_id_should_return_not_found_response_code_and_error_when_no_method_with_given_id(test_client):
    response = test_client.get("/method/" + str(method2.ID) + "/param/all")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No method with id = ' + str(method2.ID)


@pytest.mark.parametrize('add_test_context', [reset_method_param_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_required_method_params_by_method_id_should_return_ok_response_code_and_correct_method_params_for_given_method_id(test_client):
    response = test_client.get("/method/" + str(method2.ID) + "/param/all")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()['items']
    assert len(items) == 2
    returned_method_params = items
    expected_method_param_values = [None, method_param3.Value]
    expected_method_param_defs = [method_param_def2, method_param_def1]
    for returned_method_param, expected_method_param_value, expected_method_param_def in \
        zip(returned_method_params, expected_method_param_values, expected_method_param_defs):
        assert returned_method_param['MethodID'] == method2.ID
        assert returned_method_param['MethodParamDefID'] == expected_method_param_def.ID.strip()
        assert returned_method_param['Value'] == expected_method_param_value
        assert returned_method_param['DataType'] == expected_method_param_def.DataType.strip()
        assert returned_method_param['Name'] == expected_method_param_def.Name


@pytest.mark.parametrize('add_test_context', [reset_method_param_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_required_method_params_by_method_id_should_return_ok_response_code_and_correct_page_data(test_client):
    size = 1
    page = 1
    response = test_client.get("/method/" + str(method1.ID) + f"/param/all?size={size}&page={page}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == size
    assert response.json()['total'] == 2
    assert response.json()['pages'] == 2 // size if 2 % size == 0 \
        else 2 // size + 1
    assert response.json()['size'] == size
    assert response.json()['page'] == page


@pytest.mark.parametrize('add_test_context', [reset_method_param_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_required_method_params_by_method_id_should_return_ok_response_code_and_default_page_data(test_client):
    response = test_client.get("/method/" + str(method3.ID) + "/param/all")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == 1
    assert response.json()['total'] == 1
    assert response.json()['pages'] == 1
    assert response.json()['size'] == 50
    assert response.json()['page'] == 1


@pytest.mark.parametrize('add_test_context', [reset_method_param_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_required_method_params_by_method_id_should_return_ok_response_code_and_data_filtered_by_odata_query(test_client):
    odata_filter = f'ID eq \'{method_param2.MethodParamDefID.strip()}\''
    response = test_client.get("/method/" + str(method2.ID) + f"/param/all?filter={odata_filter}")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()['items']
    assert len(items) == 1
    returned_method_param = items[0]
    assert returned_method_param['MethodID'] == method2.ID
    assert returned_method_param['MethodParamDefID'] == method_param2.MethodParamDefID.strip()
    assert returned_method_param['Value'] is None
    assert returned_method_param['DataType'] == method_param_def2.DataType.strip()
    assert returned_method_param['Name'] == method_param_def2.Name


@pytest.mark.parametrize('add_test_context', [reset_method_param_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_get_method_param_by_method_param_def_id_should_return_ok_response_code_and_trend_param_of_given_trend_and_trend_param_id(test_client):  # noqa
    response = test_client.get("/method/" + str(method1.ID) + "/param/" + method_param1.MethodParamDefID.strip())
    assert response.status_code == status.HTTP_200_OK
    returned_method_param = response.json()
    assert returned_method_param['MethodID'] == method_param1.MethodID
    assert returned_method_param['MethodParamDefID'] == method_param1.MethodParamDefID.strip()
    assert returned_method_param['Value'] == method_param1.Value
    assert returned_method_param['DataType'] == method_param_def1.DataType.strip()
    assert returned_method_param['Name'] == method_param_def1.Name


@pytest.mark.parametrize('add_test_context', [reset_method_param_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_get_method_param_by_method_param_def_id_should_return_not_found_response_code_and_error_when_no_trend_param_with_given_id(test_client):
    response = test_client.get("/method/" + str(method2.ID) + "/param/" + method_param_def2.ID.strip())
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == (f"No method param for method with id = {method2.ID} "
                                f"and method param def with id = {method_param_def2.ID.strip()}")


def test_get_method_param_by_method_param_def_id_should_return_not_found_response_code_and_error_when_no_method_with_given_id(test_client):
    response = test_client.get("/method/" + str(method3.ID) + "/param/" + method_param1.MethodParamDefID.strip())
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No method with id = ' + str(method3.ID)


@pytest.mark.parametrize('add_test_context', [reset_method_param_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_update_method_param_should_return_ok_response_code_and_method_param_of_given_id(test_client):
    update_method_param_value = '105.1'
    response = test_client.put("/method/" + str(method1.ID) + "/param/" + method_param1.MethodParamDefID.strip(),
                               json=update_method_param_value)
    assert response.status_code == status.HTTP_200_OK
    returned_method_param = response.json()
    assert returned_method_param['MethodID'] == method_param1.MethodID
    assert returned_method_param['MethodParamDefID'] == method_param1.MethodParamDefID.strip()
    assert returned_method_param['Value'] == update_method_param_value
    assert returned_method_param['DataType'] == method_param_def1.DataType.strip()
    assert returned_method_param['Name'] == method_param_def1.Name


@pytest.mark.parametrize('add_test_context', [reset_method_param_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_update_method_param_should_return_not_found_response_code_and_error_when_no_method_param_with_given_id(test_client):
    update_method_param_value = '2,3'
    response = test_client.put("/method/" + str(method1.ID) + "/param/" + method_param4.MethodParamDefID.strip(),
                               json=update_method_param_value)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == (f"No method param for method with id = {method1.ID} "
                                    f"and method param def with id = {method_param4.MethodParamDefID.strip()}")


def test_update_method_param_should_return_not_found_response_code_and_error_when_no_method_with_given_id(test_client):
    update_method_param_value = '105.5'
    response = test_client.put(
        "/method/" + str(method1.ID) + "/param/" + method_param1.MethodParamDefID.strip(),
        json=update_method_param_value)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No method with id = ' + str(method1.ID)


@pytest.mark.parametrize('add_test_context', [reset_method_param_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_create_method_param_should_return_created_response_code_and_created_method_param(test_client):
    method_param_dict = {'MethodParamDefID': method_param_def2.ID.strip(), 'Value': '0.234'}
    response = test_client.post("/method/" + str(method2.ID) + "/param", json=method_param_dict)
    assert response.status_code == status.HTTP_201_CREATED
    returned_method_param = response.json()
    assert returned_method_param['MethodID'] == method2.ID
    assert returned_method_param['MethodParamDefID'] == method_param_dict['MethodParamDefID'].strip()
    assert returned_method_param['Value'] == method_param_dict['Value']
    assert returned_method_param['DataType'] == method_param_def2.DataType.strip()
    assert returned_method_param['Name'] == method_param_def2.Name
    with Session(get_engine()) as session:
        method_params_count = session.execute(select(func.count()).select_from(lds.MethodParam)).fetchall()[0][0]
    assert method_params_count == len(method_param_list)+1


@pytest.mark.parametrize('add_test_context', [reset_method_param_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_create_method_should_return_conflict_response_code_and_error_when_param_with_given_key_exists(test_client):
    method_param_dict = {'MethodParamDefID': method_param_def1.ID.strip(), 'Value': '111.1'}
    response = test_client.post("/method/" + str(method1.ID) + "/param", json=method_param_dict)
    assert response.status_code == status.HTTP_409_CONFLICT
    error = response.json()
    assert error['code'] == status.HTTP_409_CONFLICT
    assert error['message'] == 'Integrity error when creating method param'


def test_create_method_should_return_not_found_response_code_and_error_when_no_method_with_given_id(test_client):
    method_param_dict = {'MethodParamDefID': method_param_def2.ID.strip(), 'Value': '0.15'}
    response = test_client.post("/method/" + str(method1.ID) + "/param", json=method_param_dict)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No method with id = ' + str(method1.ID)


@pytest.mark.parametrize('add_test_context', [reset_method_param_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_create_method_should_return_conflict_response_code_and_error_when_no_param_def_method_id_pair_exists(test_client):
    method_param_dict = {'MethodParamDefID': method_param_def1.ID.strip(), 'Value': '88.8'}
    response = test_client.post("/method/" + str(method3.ID) + "/param", json=method_param_dict)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == f'No method param def with id = {method_param_def1.ID.strip()}'


@pytest.mark.parametrize('add_test_context', [reset_method_param_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_delete_method_param_by_id_should_return_no_content_response_code_and_remove_method_param(test_client):
    response = test_client.delete("/method/" + str(method2.ID) + "/param/" + method_param_def1.ID.strip())
    assert response.status_code == status.HTTP_204_NO_CONTENT
    with Session(get_engine()) as session:
        methods_count = session.execute(select(func.count()).select_from(lds.MethodParam)).fetchall()[0][0]
    assert methods_count == len(method_param_list) - 1


@pytest.mark.parametrize('add_test_context', [reset_method_param_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_delete_method_param_by_id_should_return_not_found_response_code_and_error_when_no_method_param_for_given_ids(test_client):
    response = test_client.delete("/method/" + str(method2.ID) + "/param/" + method_param_def2.ID.strip())
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == ('No method param for method with id = ' + str(method2.ID)
                                + ' and method param def with id = ' + method_param_def2.ID.strip())


def test_delete_method_param_by_id_should_return_not_found_response_code_and_error_when_no_method_with_given_id(test_client):
    response = test_client.delete("/method/" + str(method2.ID) + "/param/" + method_param_def1.ID.strip())
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No method with id = ' + str(method2.ID)
