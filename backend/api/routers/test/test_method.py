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
method1 = lds.Method(ID=1, MethodDefID='COMBINED', PipelineID=pipeline.ID, Name='Method1')
method2 = lds.Method(ID=2, MethodDefID='WAVE', PipelineID=pipeline.ID, Name='Method2')
method3 = lds.Method(ID=3, MethodDefID='WAVE', PipelineID=pipeline.ID, Name='Method3')
method_list = [method1, method2, method3]


def reset_method_objects():
    global method_def1, method_def2, method_def_list,  method1, method2, method3, method_list, pipeline

    method_def1 = lds.MethodDef(ID='COMBINED', Name='CombineOtherResults')
    method_def2 = lds.MethodDef(ID='WAVE', Name='WaveHeatmap')
    method_def_list = [method_def1, method_def2]
    pipeline = lds.Pipeline(ID=1, Name='Pipeline1')
    method1 = lds.Method(ID=1, MethodDefID='COMBINED', PipelineID=pipeline.ID, Name='Method1')
    method2 = lds.Method(ID=2, MethodDefID='WAVE', PipelineID=pipeline.ID, Name='Method2')
    method3 = lds.Method(ID=3, MethodDefID='WAVE', PipelineID=pipeline.ID, Name='Method3')
    method_list = [method1, method2, method3]

    return [method_def_list, [pipeline], method_list]


def test_list_methods_should_return_ok_response_code_and_empty_list_when_no_methods(test_client):
    response = test_client.get("/method")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['items']) == 0


@pytest.mark.parametrize('add_test_context', [reset_method_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_methods_should_return_ok_response_code_and_correct_methods(test_client):
    response = test_client.get("/method")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()['items']
    assert len(items) == len(method_list)
    for expected_method, returned_method in zip(method_list, items):
        assert returned_method['ID'] == expected_method.ID
        assert returned_method['MethodDefID'] == expected_method.MethodDefID.strip()
        assert returned_method['PipelineID'] == expected_method.PipelineID
        assert returned_method['Name'] == expected_method.Name


@pytest.mark.parametrize('add_test_context', [reset_method_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_methods_should_return_ok_response_code_and_correct_page_data(test_client):
    size = 2
    page = 2
    response = test_client.get(f"/method?size={size}&page={page}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == 1
    assert response.json()['total'] == len(method_list)
    assert response.json()['pages'] == len(method_list) // size if len(method_list) % size == 0 \
        else len(method_list) // size + 1
    assert response.json()['size'] == size
    assert response.json()['page'] == page


@pytest.mark.parametrize('add_test_context', [reset_method_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_methods_should_return_ok_response_code_and_default_page_data(test_client):
    response = test_client.get("/method")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == len(method_list)
    assert response.json()['total'] == len(method_list)
    assert response.json()['pages'] == 1
    assert response.json()['size'] == 50
    assert response.json()['page'] == 1


@pytest.mark.parametrize('add_test_context', [reset_method_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_methods_should_return_ok_response_code_and_data_filtered_by_odata_query(test_client):
    odata_filter = f'PipelineID eq {pipeline.ID}'
    response = test_client.get(f"/method?filter={odata_filter}")
    assert response.status_code == status.HTTP_200_OK
    returned_methods = response.json()['items']
    assert len(returned_methods) == len(method_list)
    for returned_method, expected_method in zip(returned_methods, method_list):
        assert returned_method['ID'] == expected_method.ID
        assert returned_method['MethodDefID'] == expected_method.MethodDefID.strip()
        assert returned_method['PipelineID'] == expected_method.PipelineID
        assert returned_method['Name'] == expected_method.Name


@pytest.mark.parametrize('add_test_context', [reset_method_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_create_method_should_return_created_response_code_and_created_method_data(test_client):
    method_dict = {'MethodDefID': method_def2.ID, 'PipelineID': pipeline.ID}
    response = test_client.post("/method", json=method_dict)
    assert response.status_code == status.HTTP_201_CREATED
    returned_method = response.json()
    assert returned_method['ID'] == method3.ID+1
    assert returned_method['MethodDefID'] == method_dict['MethodDefID'].strip()
    assert returned_method['PipelineID'] == method_dict['PipelineID']
    assert returned_method['Name'] is None
    with Session(get_engine()) as session:
        methods_count = session.execute(select(func.count()).select_from(lds.Method)).fetchall()[0][0]
    assert methods_count == len(method_list)+1


@pytest.mark.parametrize('add_test_context', [reset_method_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_create_method_should_return_conflict_response_code_and_error_when_no_method_def_with_given_id(test_client):
    method_dict = {'MethodDefID': 'DUMMY', 'PipelineID': pipeline.ID, 'Name': 'Method'}
    response = test_client.post("/method", json=method_dict)
    assert response.status_code == status.HTTP_409_CONFLICT
    error = response.json()
    assert error['code'] == status.HTTP_409_CONFLICT
    assert error['message'] == 'Integrity error when creating method'


@pytest.mark.parametrize('add_test_context', [reset_method_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_create_method_should_return_conflict_response_code_and_error_when_no_pipeline_with_given_id(test_client):
    method_dict = {'MethodDefID': 'DUMMY', 'PipelineID': pipeline.ID+10, 'Name': 'Method'}
    response = test_client.post("/method", json=method_dict)
    assert response.status_code == status.HTTP_409_CONFLICT
    error = response.json()
    assert error['code'] == status.HTTP_409_CONFLICT
    assert error['message'] == 'Integrity error when creating method'


@pytest.mark.parametrize('add_test_context', [reset_method_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_delete_method_by_id_should_return_no_content_response_code_and_remove_method(test_client):
    response = test_client.delete("/method/" + str(method2.ID))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    with Session(get_engine()) as session:
        methods_count = session.execute(select(func.count()).select_from(lds.Method)).fetchall()[0][0]
    assert methods_count == len(method_list) - 1


def test_delete_method_by_id_should_return_not_found_response_code_and_error_when_no_method_with_given_id(test_client):
    response = test_client.delete("/method/" + str(method3.ID))
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No method with id = ' + str(method3.ID)


@pytest.mark.parametrize('add_test_context', [reset_method_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_get_method_by_id_should_return_ok_response_code_and_method_of_given_id(test_client):
    response = test_client.get("/method/" + str(method3.ID))
    assert response.status_code == status.HTTP_200_OK
    returned_method = response.json()
    assert returned_method['ID'] == method3.ID
    assert returned_method['MethodDefID'] == method3.MethodDefID.strip()
    assert returned_method['PipelineID'] == method3.PipelineID
    assert returned_method['Name'] == method3.Name


def test_get_method_by_id_should_return_not_found_response_code_and_error_when_no_method_with_given_id(test_client):
    response = test_client.get("/method/" + str(method1.ID))
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No method with id = ' + str(method1.ID)


@pytest.mark.parametrize('add_test_context', [reset_method_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_update_method_by_id_should_return_ok_response_code_and_method_of_given_id(test_client):
    update_method_dict = {'MethodDefID': 'COMBINED', 'Name': 'MethodUpdated'}
    response = test_client.put("/method/" + str(method3.ID), json=update_method_dict)
    assert response.status_code == status.HTTP_200_OK
    returned_method = response.json()
    assert returned_method['ID'] == method3.ID
    assert returned_method['MethodDefID'] == update_method_dict['MethodDefID']
    assert returned_method['PipelineID'] == method3.PipelineID
    assert returned_method['Name'] == update_method_dict['Name']


@pytest.mark.parametrize('add_test_context', [reset_method_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_update_method_by_id_should_return_conflict_response_code_and_error_when_no_method_def_with_given_id(test_client):
    update_method_dict = {'MethodDefID': 'DUMMY', 'Name': 'MethodUpdated'}
    response = test_client.put("/method/" + str(method3.ID), json=update_method_dict)
    assert response.status_code == status.HTTP_409_CONFLICT
    error = response.json()
    assert error['code'] == status.HTTP_409_CONFLICT
    assert error['message'] == 'Integrity error when updating method with id = ' + str(method3.ID)


@pytest.mark.parametrize('add_test_context', [reset_method_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_update_method_by_id_should_return_conflict_response_code_and_error_when_no_pipeline_with_given_id(test_client):
    update_method_dict = {'Name': 'MethodUpdated', 'PipelineID': pipeline.ID+5}
    response = test_client.put("/method/" + str(method3.ID), json=update_method_dict)
    assert response.status_code == status.HTTP_409_CONFLICT
    error = response.json()
    assert error['code'] == status.HTTP_409_CONFLICT
    assert error['message'] == 'Integrity error when updating method with id = ' + str(method3.ID)


def test_update_method_by_id_should_return_not_found_response_code_and_error_when_no_method_with_given_id(test_client):
    update_method_dict = {'MethodDefID': 'COMBINED', 'Name': 'MethodUpdated'}
    response = test_client.put("/method/" + str(method1.ID), json=update_method_dict)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No method with id = ' + str(method1.ID)
