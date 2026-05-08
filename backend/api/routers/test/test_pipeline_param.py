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

pipeline1 = lds.Pipeline(ID=1, Name='Pipeline1', BeginPos=100)
pipeline2 = lds.Pipeline(ID=2, Name='Pipeline2', BeginPos=200)
pipeline3 = lds.Pipeline(ID=3, Name='Pipeline3', BeginPos=300)
pipeline_list = [pipeline1, pipeline2, pipeline3]
pipeline_param_def1 = lds.PipelineParamDef(ID='BEGIN_POS', Name='Begin position', DataType='FLOAT')
pipeline_param_def2 = lds.PipelineParamDef(ID='METHODS', Name='Pipeline methods', DataType='LIST')
pipeline_param_def_list = [pipeline_param_def1, pipeline_param_def2]
pipeline_param1 = lds.PipelineParam(PipelineID=1, PipelineParamDefID='BEGIN_POS', Value='100.0')
pipeline_param2 = lds.PipelineParam(PipelineID=1, PipelineParamDefID='METHODS', Value='1,2,3')
pipeline_param3 = lds.PipelineParam(PipelineID=2, PipelineParamDefID='BEGIN_POS', Value='200.0')
pipeline_param_list = [pipeline_param1, pipeline_param2, pipeline_param3]


def reset_pipeline_objects():
    global pipeline1, pipeline2, pipeline3, pipeline_list
    pipeline1 = lds.Pipeline(ID=1, Name='Pipeline1', BeginPos=100)
    pipeline2 = lds.Pipeline(ID=2, Name='Pipeline2', BeginPos=200)
    pipeline3 = lds.Pipeline(ID=3, Name='Pipeline3', BeginPos=300)
    pipeline_list = [pipeline1, pipeline2, pipeline3]
    
    return [pipeline_list]


def reset_pipeline_param_objects():
    global pipeline1, pipeline2, pipeline3, pipeline_list, pipeline_param_def1, pipeline_param_def2, \
        pipeline_param_def_list, pipeline_param1, pipeline_param2, pipeline_param3, pipeline_param_list

    pipeline1 = lds.Pipeline(ID=1, Name='Pipeline1', BeginPos=100)
    pipeline2 = lds.Pipeline(ID=2, Name='Pipeline2', BeginPos=200)
    pipeline3 = lds.Pipeline(ID=3, Name='Pipeline3', BeginPos=300)
    pipeline_list = [pipeline1, pipeline2, pipeline3]
    pipeline_param_def1 = lds.PipelineParamDef(ID='BEGIN_POS', Name='Begin position', DataType='FLOAT')
    pipeline_param_def2 = lds.PipelineParamDef(ID='METHODS', Name='Pipeline methods', DataType='LIST')
    pipeline_param_def_list = [pipeline_param_def1, pipeline_param_def2]
    pipeline_param1 = lds.PipelineParam(PipelineID=1, PipelineParamDefID='BEGIN_POS', Value='100.0')
    pipeline_param2 = lds.PipelineParam(PipelineID=1, PipelineParamDefID='METHODS', Value='1,2,3')
    pipeline_param3 = lds.PipelineParam(PipelineID=2, PipelineParamDefID='BEGIN_POS', Value='200.0')
    pipeline_param_list = [pipeline_param1, pipeline_param2, pipeline_param3]
    
    return [pipeline_list, pipeline_param_def_list, pipeline_param_list]


@pytest.mark.parametrize('add_test_context', [reset_pipeline_param_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_pipeline_params_by_pipeline_id_should_return_ok_response_code_and_empty_list_when_no_pipeline_params_for_given_pipeline_id(test_client):  # noqa
    response = test_client.get("/pipeline/" + str(pipeline3.ID) + "/param")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['items']) == 0


def test_list_pipeline_params_by_pipeline_id_should_return_not_found_response_code_and_error_when_no_pipeline_with_given_id(test_client):
    response = test_client.get("/pipeline/" + str(pipeline2.ID) + "/param")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No pipeline with id = ' + str(pipeline2.ID)


@pytest.mark.parametrize('add_test_context', [reset_pipeline_param_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_pipeline_params_by_pipeline_id_should_return_ok_response_code_and_correct_pipeline_params_for_given_pipeline_id(test_client):
    response = test_client.get("/pipeline/" + str(pipeline2.ID) + "/param")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()['items']
    assert len(items) == 1
    expected_pipeline_param_def_list = [pipeline_param_def1]
    expected_pipeline_param_list = [pipeline_param3]
    for expected_pipeline_param_def, expected_pipeline_param, returned_pipeline_param in (
            zip(expected_pipeline_param_def_list, expected_pipeline_param_list, items)):
        assert returned_pipeline_param['PipelineID'] == expected_pipeline_param.PipelineID
        assert returned_pipeline_param['PipelineParamDefID'] == expected_pipeline_param.PipelineParamDefID.strip()
        assert returned_pipeline_param['Value'] == expected_pipeline_param.Value
        assert returned_pipeline_param['DataType'] == expected_pipeline_param_def.DataType.strip()
        assert returned_pipeline_param['Name'] == expected_pipeline_param_def.Name


@pytest.mark.parametrize('add_test_context', [reset_pipeline_param_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_pipeline_params_by_pipeline_id_should_return_ok_response_code_and_correct_page_data(test_client):
    size = 2
    page = 1
    response = test_client.get("/pipeline/" + str(pipeline1.ID) + f"/param?size={size}&page={page}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == size
    assert response.json()['total'] == 2
    assert response.json()['pages'] == 1
    assert response.json()['size'] == size
    assert response.json()['page'] == page


@pytest.mark.parametrize('add_test_context', [reset_pipeline_param_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_pipeline_params_by_pipeline_id_should_return_ok_response_code_and_default_page_data(test_client):
    response = test_client.get("/pipeline/" + str(pipeline1.ID) + "/param")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == 2
    assert response.json()['total'] == 2
    assert response.json()['pages'] == 1
    assert response.json()['size'] == 50
    assert response.json()['page'] == 1


@pytest.mark.parametrize('add_test_context', [reset_pipeline_param_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_pipeline_params_by_pipeline_id_should_return_ok_response_code_and_data_filtered_by_odata_query(test_client):
    odata_filter = f'PipelineParamDefID eq \'{pipeline_param2.PipelineParamDefID.strip()}\''
    response = test_client.get("/pipeline/" + str(pipeline1.ID) + f"/param?filter={odata_filter}")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()['items']
    assert len(items) == 1
    returned_pipeline_param = items[0]
    assert returned_pipeline_param['PipelineID'] == pipeline_param2.PipelineID
    assert returned_pipeline_param['PipelineParamDefID'] == pipeline_param2.PipelineParamDefID.strip()
    assert returned_pipeline_param['Value'] == pipeline_param2.Value
    assert returned_pipeline_param['DataType'] == pipeline_param_def2.DataType.strip()
    assert returned_pipeline_param['Name'] == pipeline_param_def2.Name


@pytest.mark.parametrize('add_test_context', [reset_pipeline_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_required_pipeline_params_by_pipeline_id_should_return_ok_response_code_and_empty_list_when_no_pipeline_params_for_given_pipeline_id(test_client):  # noqa
    response = test_client.get("/pipeline/" + str(pipeline1.ID) + "/param/all")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['items']) == 0


def test_list_required_pipeline_params_by_pipeline_id_should_return_not_found_response_code_and_error_when_no_pipeline_with_given_id(test_client):
    response = test_client.get("/pipeline/" + str(pipeline2.ID) + "/param/all")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No pipeline with id = ' + str(pipeline2.ID)


@pytest.mark.parametrize('add_test_context', [reset_pipeline_param_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_required_pipeline_params_by_pipeline_id_should_return_ok_response_code_and_correct_pipeline_params_for_given_pipeline_id(test_client):
    response = test_client.get("/pipeline/" + str(pipeline3.ID) + "/param/all")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()['items']
    assert len(items) == 2
    expected_pipeline_param_def_list = [pipeline_param_def1, pipeline_param_def2]
    for expected_pipeline_param_def, expected_pipeline_param, returned_pipeline_param in (
            zip(expected_pipeline_param_def_list, pipeline_param_list, items)):
        assert returned_pipeline_param['PipelineID'] == pipeline3.ID
        assert returned_pipeline_param['PipelineParamDefID'] == expected_pipeline_param.PipelineParamDefID.strip()
        assert returned_pipeline_param['Value'] is None
        assert returned_pipeline_param['DataType'] == expected_pipeline_param_def.DataType.strip()
        assert returned_pipeline_param['Name'] == expected_pipeline_param_def.Name


@pytest.mark.parametrize('add_test_context', [reset_pipeline_param_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_required_pipeline_params_by_pipeline_id_should_return_ok_response_code_and_correct_page_data(test_client):
    size = 1
    page = 2
    response = test_client.get("/pipeline/" + str(pipeline2.ID) + f"/param/all?size={size}&page={page}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == size
    assert response.json()['total'] == 2
    assert response.json()['pages'] == 2 // size if 2 % size == 0 \
        else 2 // size + 1
    assert response.json()['size'] == size
    assert response.json()['page'] == page


@pytest.mark.parametrize('add_test_context', [reset_pipeline_param_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_required_pipeline_params_by_pipeline_id_should_return_ok_response_code_and_default_page_data(test_client):
    response = test_client.get("/pipeline/" + str(pipeline1.ID) + "/param/all")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == 2
    assert response.json()['total'] == 2
    assert response.json()['pages'] == 1
    assert response.json()['size'] == 50
    assert response.json()['page'] == 1


@pytest.mark.parametrize('add_test_context', [reset_pipeline_param_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_required_pipeline_params_by_pipeline_id_should_return_ok_response_code_and_data_filtered_by_odata_query(test_client):
    odata_filter = f'ID eq \'{pipeline_param_def1.ID.strip()}\''
    response = test_client.get("/pipeline/" + str(pipeline3.ID) + f"/param/all?filter={odata_filter}")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()['items']
    assert len(items) == 1
    returned_pipeline_param = items[0]
    assert returned_pipeline_param['PipelineID'] == pipeline3.ID
    assert returned_pipeline_param['PipelineParamDefID'] == pipeline_param1.PipelineParamDefID.strip()
    assert returned_pipeline_param['Value'] is None
    assert returned_pipeline_param['DataType'] == pipeline_param_def1.DataType.strip()
    assert returned_pipeline_param['Name'] == pipeline_param_def1.Name


@pytest.mark.parametrize('add_test_context', [reset_pipeline_param_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_get_pipeline_param_by_pipeline_param_def_id_should_return_ok_response_code_and_trend_param_of_given_trend_and_trend_param_id(test_client):  # noqa
    response = test_client.get("/pipeline/" + str(pipeline1.ID) + "/param/" + pipeline_param2.PipelineParamDefID.strip())
    assert response.status_code == status.HTTP_200_OK
    returned_pipeline_param = response.json()
    assert returned_pipeline_param['PipelineID'] == pipeline_param2.PipelineID
    assert returned_pipeline_param['PipelineParamDefID'] == pipeline_param2.PipelineParamDefID.strip()
    assert returned_pipeline_param['Value'] == pipeline_param2.Value
    assert returned_pipeline_param['DataType'] == pipeline_param_def2.DataType.strip()
    assert returned_pipeline_param['Name'] == pipeline_param_def2.Name


@pytest.mark.parametrize('add_test_context', [reset_pipeline_param_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_get_pipeline_param_by_pipeline_param_def_id_should_return_not_found_response_code_and_error_when_no_trend_param_with_given_id(test_client):
    response = test_client.get("/pipeline/" + str(pipeline2.ID) + "/param/" + pipeline_param2.PipelineParamDefID.strip())
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == (f"No pipeline param for pipeline with id = {pipeline2.ID} "
                                f"and pipeline param def with id = {pipeline_param2.PipelineParamDefID.strip()}")


def test_get_pipeline_param_by_pipeline_param_def_id_should_return_not_found_response_code_and_error_when_no_pipeline_with_given_id(test_client):
    response = test_client.get("/pipeline/" + str(pipeline1.ID) + "/param/" + pipeline_param1.PipelineParamDefID.strip())
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No pipeline with id = ' + str(pipeline1.ID)


@pytest.mark.parametrize('add_test_context', [reset_pipeline_param_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_update_pipeline_param_should_return_ok_response_code_and_pipeline_param_of_given_id(test_client):
    update_pipeline_param_value = '2,3,4'
    response = test_client.put("/pipeline/" + str(pipeline1.ID) + "/param/" + pipeline_param2.PipelineParamDefID.strip(),
                               json=update_pipeline_param_value)
    assert response.status_code == status.HTTP_200_OK
    returned_pipeline_param = response.json()
    assert returned_pipeline_param['PipelineID'] == pipeline_param2.PipelineID
    assert returned_pipeline_param['PipelineParamDefID'] == pipeline_param2.PipelineParamDefID.strip()
    assert returned_pipeline_param['Value'] == update_pipeline_param_value
    assert returned_pipeline_param['DataType'] == pipeline_param_def2.DataType.strip()
    assert returned_pipeline_param['Name'] == pipeline_param_def2.Name


@pytest.mark.parametrize('add_test_context', [reset_pipeline_param_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_update_pipeline_param_should_return_not_found_response_code_and_error_when_no_pipeline_param_with_given_id(test_client):
    update_pipeline_param_value = '2,3,4'
    response = test_client.put("/pipeline/" + str(pipeline3.ID) + "/param/" + pipeline_param2.PipelineParamDefID.strip(),
                               json=update_pipeline_param_value)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == (f"No pipeline param for pipeline with id = {pipeline3.ID} "
                                    f"and pipeline param def with id = {pipeline_param2.PipelineParamDefID.strip()}")


def test_update_pipeline_param_should_return_not_found_response_code_and_error_when_no_pipeline_with_given_id(test_client):
    update_pipeline_param_value = '987.65'
    response = test_client.put("/pipeline/" + str(pipeline1.ID) + "/param/" + pipeline_param1.PipelineParamDefID.strip(),
                               json=update_pipeline_param_value)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No pipeline with id = ' + str(pipeline1.ID)


@pytest.mark.parametrize('add_test_context', [reset_pipeline_param_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_create_pipeline_param_should_return_created_response_code_and_created_pipeline_param(test_client):
    pipeline_param_dict = {'PipelineParamDefID': pipeline_param_def2.ID.strip(), 'Value': '1,2'}
    response = test_client.post("/pipeline/" + str(pipeline2.ID) + "/param", json=pipeline_param_dict)
    assert response.status_code == status.HTTP_201_CREATED
    returned_pipeline_param = response.json()
    assert returned_pipeline_param['PipelineID'] == pipeline2.ID
    assert returned_pipeline_param['PipelineParamDefID'] == pipeline_param_dict['PipelineParamDefID'].strip()
    assert returned_pipeline_param['Value'] == pipeline_param_dict['Value']
    assert returned_pipeline_param['DataType'] == pipeline_param_def2.DataType.strip()
    assert returned_pipeline_param['Name'] == pipeline_param_def2.Name
    with Session(get_engine()) as session:
        pipeline_params_count = session.execute(select(func.count()).select_from(lds.PipelineParam)).fetchall()[0][0]
    assert pipeline_params_count == len(pipeline_param_list)+1


@pytest.mark.parametrize('add_test_context', [reset_pipeline_param_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_create_pipeline_should_return_conflict_response_code_and_error_when_param_with_given_key_exists(test_client):
    pipeline_param_dict = {'PipelineParamDefID': pipeline_param_def1.ID.strip(), 'Value': '234.56'}
    response = test_client.post("/pipeline/" + str(pipeline1.ID) + "/param", json=pipeline_param_dict)
    assert response.status_code == status.HTTP_409_CONFLICT
    error = response.json()
    assert error['code'] == status.HTTP_409_CONFLICT
    assert error['message'] == 'Integrity error when creating pipeline param'


def test_create_pipeline_should_return_not_found_response_code_and_error_when_no_pipeline_with_given_id(test_client):
    pipeline_param_dict = {'PipelineParamDefID': pipeline_param_def1.ID.strip(), 'Value': '1111.11'}
    response = test_client.post("/pipeline/" + str(pipeline3.ID) + "/param", json=pipeline_param_dict)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No pipeline with id = ' + str(pipeline3.ID)


@pytest.mark.parametrize('add_test_context', [reset_pipeline_param_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_delete_pipeline_param_by_id_should_return_no_content_response_code_and_remove_pipeline_param(test_client):
    response = test_client.delete("/pipeline/" + str(pipeline1.ID) + "/param/" + pipeline_param_def1.ID.strip())
    assert response.status_code == status.HTTP_204_NO_CONTENT
    with Session(get_engine()) as session:
        pipelines_count = session.execute(select(func.count()).select_from(lds.PipelineParam)).fetchall()[0][0]
    assert pipelines_count == len(pipeline_list) - 1


@pytest.mark.parametrize('add_test_context', [reset_pipeline_param_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_delete_pipeline_param_by_id_should_return_not_found_response_code_and_error_when_no_pipeline_param_for_given_ids(test_client):
    response = test_client.delete("/pipeline/" + str(pipeline3.ID) + "/param/" + pipeline_param_def1.ID.strip())
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == ('No pipeline param for pipeline with id = ' + str(pipeline3.ID)
                                + ' and pipeline param def with id = ' + pipeline_param_def1.ID.strip())


def test_delete_pipeline_param_by_id_should_return_not_found_response_code_and_error_when_no_pipeline_with_given_id(test_client):
    response = test_client.delete("/pipeline/" + str(pipeline2.ID) + "/param/" + pipeline_param_def1.ID.strip())
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No pipeline with id = ' + str(pipeline2.ID)
