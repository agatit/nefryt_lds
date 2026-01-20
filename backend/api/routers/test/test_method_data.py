import os
import random
import sys
from starlette import status
from starlette.testclient import TestClient
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))  # noqa: E402
from api.app import app
from api.routers.utils.security import get_user_token
from database import lds
import pytest

method_def = lds.MethodDef(ID='WAVE', Name='WaveHeatmap')
pipeline = lds.Pipeline(ID=1, Name='Pipeline1')
method2 = lds.Method(ID=2, MethodDefID='WAVE', PipelineID=pipeline.ID, Name='Method2')
method1 = lds.Method(ID=1, MethodDefID='WAVE', PipelineID=pipeline.ID, Name='Method3')
method3 = lds.Method(ID=3, MethodDefID='WAVE', PipelineID=pipeline.ID, Name='Method1')
method_list = [method1, method2, method3]
method_param_def1 = lds.MethodParamDef(ID='WAVE_SPEED', MethodDefID='WAVE', Name='Wave speed', DataType='FLOAT')
method_param_def2 = lds.MethodParamDef(ID='ALARM_VALUE', MethodDefID='WAVE', Name='Alarm value', DataType='FLOAT')
method_param_def_list = [method_param_def2, method_param_def1]
method_param1 = lds.MethodParam(MethodID=1, MethodParamDefID='WAVE_SPEED', Value='100.5')
method_param2 = lds.MethodParam(MethodID=1, MethodParamDefID='ALARM_VALUE', Value='0.1')
method_param3 = lds.MethodParam(MethodID=2, MethodParamDefID='WAVE_SPEED', Value='99.1')
method_param_list = [method_param1, method_param2, method_param3]
method_data_list = []
for pos in range(5,20,5):
    for time in range(100, 103):
        method_data_list.append(lds.MethodData(MethodID=method1.ID, Position=pos, Time=time, Value=random.random()))
        method_data_list.append(lds.MethodData(MethodID=method2.ID, Position=pos, Time=time))


def reset_method_data_objects():
    global method_def, pipeline, method1, method2, method3, method_list, method_param_def1, method_param_def2, \
        method_param_list, method_param1, method_param2, method_param3, method_param_def_list, method_data_list, \
        pos, time

    method_def = lds.MethodDef(ID='WAVE', Name='WaveHeatmap')
    pipeline = lds.Pipeline(ID=1, Name='Pipeline1')
    method2 = lds.Method(ID=2, MethodDefID='WAVE', PipelineID=pipeline.ID, Name='Method2')
    method1 = lds.Method(ID=1, MethodDefID='WAVE', PipelineID=pipeline.ID, Name='Method3')
    method3 = lds.Method(ID=3, MethodDefID='WAVE', PipelineID=pipeline.ID, Name='Method1')
    method_list = [method1, method2, method3]
    method_param_def1 = lds.MethodParamDef(ID='WAVE_SPEED', MethodDefID='WAVE', Name='Wave speed', DataType='FLOAT')
    method_param_def2 = lds.MethodParamDef(ID='ALARM_VALUE', MethodDefID='WAVE', Name='Alarm value', DataType='FLOAT')
    method_param_def_list = [method_param_def2, method_param_def1]
    method_param1 = lds.MethodParam(MethodID=1, MethodParamDefID='WAVE_SPEED', Value='100.5')
    method_param2 = lds.MethodParam(MethodID=1, MethodParamDefID='ALARM_VALUE', Value='0.1')
    method_param3 = lds.MethodParam(MethodID=2, MethodParamDefID='WAVE_SPEED', Value='99.1')
    method_param_list = [method_param1, method_param2, method_param3]
    method_data_list = []
    for pos in range(5, 20, 5):
        for time in range(100, 103):
            method_data_list.append(lds.MethodData(MethodID=method1.ID, Position=pos, Time=time, Value=random.random()))
            method_data_list.append(lds.MethodData(MethodID=method2.ID, Position=pos, Time=time))

    return [[method_def], [pipeline], method_list, method_param_def_list, method_param_list, method_data_list]


app.dependency_overrides[get_user_token] = lambda: {"sub": "test_user"}  # type: ignore[attr-defined]
test_client = TestClient(app)


@pytest.mark.parametrize('reset_lds_objects', [reset_method_data_objects], indirect=True)
def test_get_method_data_should_return_full_data_for_method(add_lds_objects):
    response = test_client.get(f"/method/{method2.ID}/data")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()['items']
    assert len(items) == 9
    returned_method_data_list = items
    expected_times = [100, 101, 102]*3
    expected_positions = [5, 5, 5, 10, 10, 10, 15, 15, 15]
    for expected_time, expected_position, returned_method_data in zip(expected_times, expected_positions, returned_method_data_list):
        assert returned_method_data['Position'] == expected_position
        assert returned_method_data['Time'] == expected_time
        assert returned_method_data['Value'] == 0

    response = test_client.get(f"/method/{method1.ID}/data")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()['items']
    assert len(items) == 9
    returned_method_data_list = items
    expected_times = [100, 101, 102]*3
    expected_positions = [5, 5, 5, 10, 10, 10, 15, 15, 15]
    for expected_time, expected_position, returned_method_data in zip(expected_times, expected_positions, returned_method_data_list):
        assert returned_method_data['Position'] == expected_position
        assert returned_method_data['Time'] == expected_time
        assert 0 < returned_method_data['Value'] < 1


@pytest.mark.parametrize('reset_lds_objects', [reset_method_data_objects], indirect=True)
def test_get_method_data_should_return_not_found_response_code_and_error_when_no_data_for_method(add_lds_objects):
    response = test_client.get(f"/method/{method3.ID}/data")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No method data for method with id = ' + str(method3.ID)


@pytest.mark.parametrize('reset_lds_objects', [reset_method_data_objects], indirect=True)
def test_get_method_data_should_return_not_found_response_code_and_error_when_no_method_with_given_id(add_lds_objects):
    response = test_client.get(f"/method/{method3.ID + 1}/data")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No method with id = ' + str(method3.ID + 1)


@pytest.mark.parametrize('reset_lds_objects', [reset_method_data_objects], indirect=True)
def test_get_method_data_should_return_ok_response_code_and_correct_page_data(add_lds_objects):
    size = 3
    page = 3
    response = test_client.get(f"/method/{method2.ID}/data?size={size}&page={page}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == size
    assert response.json()['total'] == 9
    assert response.json()['pages'] == 3
    assert response.json()['size'] == size
    assert response.json()['page'] == page


@pytest.mark.parametrize('reset_lds_objects', [reset_method_data_objects], indirect=True)
def test_get_method_data_should_return_ok_response_code_and_default_page_data(add_lds_objects):
    response = test_client.get(f"/method/{method1.ID}/data")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == len(method_data_list) // 2
    assert response.json()['total'] == len(method_data_list) // 2
    assert response.json()['pages'] == 1
    assert response.json()['size'] == 50
    assert response.json()['page'] == 1
