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


pipeline1 = lds.Pipeline(ID=1, Name='Pipeline1')
pipeline2 = lds.Pipeline(ID=2, Name='Pipeline2')
pipeline_list = [pipeline1, pipeline2]


def reset_pipeline_objects():
    global pipeline1, pipeline2, pipeline_list

    pipeline1 = lds.Pipeline(ID=1, Name='Pipeline1')
    pipeline2 = lds.Pipeline(ID=2, Name='Pipeline2')
    pipeline_list = [pipeline1, pipeline2]

    return [pipeline_list]


def test_list_pipelines_should_return_ok_response_code_and_empty_list_when_no_pipelines(test_client):
    response = test_client.get("/pipeline")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['items']) == 0


@pytest.mark.parametrize('add_test_context', [reset_pipeline_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_pipelines_should_return_ok_response_code_and_correct_pipelines(test_client):
    response = test_client.get("/pipeline")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()['items']
    assert len(items) == len(pipeline_list)
    for expected_pipeline, returned_pipeline in zip(pipeline_list, items):
        assert returned_pipeline['ID'] == expected_pipeline.ID
        assert returned_pipeline['Name'] == expected_pipeline.Name


@pytest.mark.parametrize('add_test_context', [reset_pipeline_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_pipelines_should_return_ok_response_code_and_correct_page_data(test_client):
    size = 1
    page = 2
    response = test_client.get(f"/pipeline?size={size}&page={page}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == size
    assert response.json()['total'] == len(pipeline_list)
    assert response.json()['pages'] == len(pipeline_list) // size if len(pipeline_list) % size == 0 \
        else len(pipeline_list) // size + 1
    assert response.json()['size'] == size
    assert response.json()['page'] == page


@pytest.mark.parametrize('add_test_context', [reset_pipeline_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_pipelines_should_return_ok_response_code_and_default_page_data(test_client):
    response = test_client.get("/pipeline")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == len(pipeline_list)
    assert response.json()['total'] == len(pipeline_list)
    assert response.json()['pages'] == 1
    assert response.json()['size'] == 50
    assert response.json()['page'] == 1


@pytest.mark.parametrize('add_test_context', [reset_pipeline_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_pipelines_should_return_ok_response_code_and_data_filtered_by_odata_query(test_client):
    odata_filter = f'Name eq \'{pipeline1.Name}\''
    response = test_client.get(f"/pipeline?filter={odata_filter}")
    assert response.status_code == status.HTTP_200_OK
    returned_pipelines = response.json()['items']
    assert len(returned_pipelines) == 1
    expected_pipelines = [pipeline1]
    for returned_pipeline, expected_pipeline in zip(returned_pipelines, expected_pipelines):
        assert returned_pipeline['ID'] == expected_pipeline.ID
        assert returned_pipeline['Name'] == expected_pipeline.Name


@pytest.mark.parametrize('add_test_context', [reset_pipeline_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_create_pipeline_should_return_created_response_code_and_created_pipeline_data(test_client):
    pipeline_dict = {'Name': 'Pipeline3'}
    response = test_client.post("/pipeline", json=pipeline_dict)
    assert response.status_code == status.HTTP_201_CREATED
    returned_pipeline = response.json()
    assert returned_pipeline['ID'] >= pipeline2.ID+1
    assert returned_pipeline['Name'] == pipeline_dict['Name']
    with Session(get_engine()) as session:
        pipelines_count = session.execute(select(func.count()).select_from(lds.Pipeline)).fetchall()[0][0]
    assert pipelines_count == len(pipeline_list)+1


@pytest.mark.parametrize('add_test_context', [reset_pipeline_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_delete_pipeline_by_id_should_return_no_content_response_code_and_remove_pipeline(test_client):
    response = test_client.delete("/pipeline/" + str(pipeline2.ID))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    with Session(get_engine()) as session:
        pipelines_count = session.execute(select(func.count()).select_from(lds.Pipeline)).fetchall()[0][0]
    assert pipelines_count == len(pipeline_list) - 1


def test_delete_pipeline_by_id_should_return_not_found_response_code_and_error_when_no_pipeline_with_given_id(test_client):
    response = test_client.delete("/pipeline/" + str(pipeline2.ID))
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No pipeline with id = ' + str(pipeline2.ID)


@pytest.mark.parametrize('add_test_context', [reset_pipeline_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_get_pipeline_by_id_should_return_ok_response_code_and_pipeline_of_given_id(test_client):
    response = test_client.get("/pipeline/" + str(pipeline1.ID))
    assert response.status_code == status.HTTP_200_OK
    returned_pipeline = response.json()
    assert returned_pipeline['ID'] == pipeline1.ID
    assert returned_pipeline['Name'] == pipeline1.Name


def test_get_pipeline_by_id_should_return_not_found_response_code_and_error_when_no_pipeline_with_given_id(test_client):
    response = test_client.get("/pipeline/" + str(pipeline2.ID))
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No pipeline with id = ' + str(pipeline2.ID)


@pytest.mark.parametrize('add_test_context', [reset_pipeline_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_update_pipeline_by_id_should_return_ok_response_code_and_pipeline_of_given_id(test_client):
    update_pipeline_dict = {'Name': 'New name'}
    response = test_client.put("/pipeline/" + str(pipeline1.ID), json=update_pipeline_dict)
    assert response.status_code == status.HTTP_200_OK
    returned_pipeline = response.json()
    assert returned_pipeline['ID'] == pipeline1.ID
    assert returned_pipeline['Name'] == update_pipeline_dict['Name']


def test_update_pipeline_by_id_should_return_not_found_response_code_and_error_when_no_pipeline_with_given_id(test_client):
    update_pipeline_dict = {'Name': 'New name'}
    response = test_client.put("/pipeline/" + str(pipeline2.ID), json=update_pipeline_dict)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No pipeline with id = ' + str(pipeline2.ID)
