import os
import sys
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from starlette import status
from starlette.testclient import TestClient
from conftest import test_client
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))  # noqa: E402
from db import get_engine
from api.routers.utils.security import get_user_token
from database import lds
import pytest

event_def1 = lds.EventDef(ID='EVENT_DEF1', Verbosity='verbosity', Caption='caption',
                          Silent=True, Visible=True, Enabled=True)
event_def2 = lds.EventDef(ID='EVENT_DEF2', Verbosity='verbosity', Caption='caption',
                          Silent=False, Visible=False, Enabled=False)
event_def_list = [event_def1, event_def2]


def reset_event_def_objects():
    global event_def1, event_def2, event_def_list

    event_def1 = lds.EventDef(ID='EVENT_DEF1', Verbosity='verbosity', Caption='caption',
                              Silent=True, Visible=True, Enabled=True)
    event_def2 = lds.EventDef(ID='EVENT_DEF2', Verbosity='verbosity', Caption='caption',
                              Silent=False, Visible=False, Enabled=False)
    event_def_list = [event_def1, event_def2]

    return [event_def_list]


def test_list_event_defs_should_return_ok_response_code_and_empty_list_when_no_event_defs(test_client):
    response = test_client.get("/event_def")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['items']) == 0


@pytest.mark.parametrize('add_test_context', [reset_event_def_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_event_defs_should_return_ok_response_code_and_correct_event_defs(test_client):
    response = test_client.get("/event_def")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()['items']
    assert len(items) == len(event_def_list)
    for expected_event_def, returned_event_def in zip(event_def_list, items):
        assert returned_event_def['ID'] == expected_event_def.ID.strip()
        assert returned_event_def['Verbosity'] == expected_event_def.Verbosity.strip()
        assert returned_event_def['Caption'] == expected_event_def.Caption.strip()
        assert returned_event_def['Silent'] == expected_event_def.Silent
        assert returned_event_def['Enabled'] == expected_event_def.Enabled
        assert returned_event_def['Visible'] == expected_event_def.Visible


@pytest.mark.parametrize('add_test_context', [reset_event_def_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_event_defs_should_return_ok_response_code_and_correct_page_data(test_client):
    size = 1
    page = 2
    response = test_client.get(f"/event_def?size={size}&page={page}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == size
    assert response.json()['total'] == len(event_def_list)
    assert response.json()['pages'] == len(event_def_list) // size if len(event_def_list) % size == 0 \
        else len(event_def_list) // size + 1
    assert response.json()['size'] == size
    assert response.json()['page'] == page


@pytest.mark.parametrize('add_test_context', [reset_event_def_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_event_defs_should_return_ok_response_code_and_default_page_data(test_client):
    response = test_client.get("/event_def")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == len(event_def_list)
    assert response.json()['total'] == len(event_def_list)
    assert response.json()['pages'] == 1
    assert response.json()['size'] == 50
    assert response.json()['page'] == 1


def test_create_event_def_should_return_created_response_code_and_created_event_def_data(test_client):
    event_def_dict = {'ID': 'EVENT_DEF1', 'Verbosity': 'verbosity', 'Caption': 'caption',
                      'Silent': True, 'Visible': True, 'Enabled': True}
    response = test_client.post("/event_def", json=event_def_dict)
    assert response.status_code == status.HTTP_201_CREATED
    returned_event_def = response.json()
    assert returned_event_def['ID'] == event_def_dict['ID']
    assert returned_event_def['Verbosity'] == event_def_dict['Verbosity']
    assert returned_event_def['Caption'] == event_def_dict['Caption']
    assert returned_event_def['Silent'] == event_def_dict['Silent']
    assert returned_event_def['Enabled'] == event_def_dict['Enabled']
    assert returned_event_def['Visible'] == event_def_dict['Visible']
    with Session(get_engine()) as session:
        event_defs_count = session.execute(select(func.count()).select_from(lds.EventDef)).fetchall()[0][0]
    assert event_defs_count == 1


@pytest.mark.parametrize('add_test_context', [reset_event_def_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_create_event_def_should_return_conflict_response_code_and_error_when_id_not_unique(test_client):
    event_def_dict = {'ID': event_def1.ID, 'Verbosity': 'verbosity2', 'Caption': 'caption2',
                      'Silent': True, 'Visible': True, 'Enabled': True}
    response = test_client.post("/event_def", json=event_def_dict)
    assert response.status_code == status.HTTP_409_CONFLICT
    error = response.json()
    assert error['code'] == status.HTTP_409_CONFLICT
    assert error['message'] == 'Integrity error when creating event def'


@pytest.mark.parametrize('add_test_context', [reset_event_def_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_delete_event_def_by_id_should_return_no_content_response_code_and_remove_event_def(test_client):
    response = test_client.delete("/event_def/" + event_def1.ID)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    with Session(get_engine()) as session:
        event_defs_count = session.execute(select(func.count()).select_from(lds.EventDef)).fetchall()[0][0]
    assert event_defs_count == 1


def test_delete_event_def_by_id_should_return_not_found_response_code_and_error_when_no_event_def_with_given_id(test_client):
    response = test_client.delete("/event_def/" + event_def1.ID)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No event def with id = ' + event_def1.ID


@pytest.mark.parametrize('add_test_context', [reset_event_def_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_get_event_def_by_id_should_return_ok_response_code_and_event_def_of_given_id(test_client):
    response = test_client.get("/event_def/" + event_def1.ID)
    assert response.status_code == status.HTTP_200_OK
    returned_event_def = response.json()
    assert returned_event_def['ID'] == event_def1.ID.strip()
    assert returned_event_def['Verbosity'] == event_def1.Verbosity.strip()
    assert returned_event_def['Caption'] == event_def1.Caption.strip()
    assert returned_event_def['Silent'] == event_def1.Silent
    assert returned_event_def['Enabled'] == event_def1.Enabled
    assert returned_event_def['Visible'] == event_def1.Visible


def test_get_event_def_by_id_should_return_not_found_response_code_and_error_when_no_event_def_with_given_id(test_client):
    response = test_client.get("/event_def/" + event_def1.ID)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No event def with id = ' + event_def1.ID


@pytest.mark.parametrize('add_test_context', [reset_event_def_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_update_event_def_should_return_ok_response_code_and_event_def_of_given_id(test_client):
    update_event_def_dict = {'Verbosity': 'verbosity2', 'Caption': 'caption2',
                             'Silent': False, 'Visible': True, 'Enabled': False}
    response = test_client.put("/event_def/" + event_def1.ID, json=update_event_def_dict)
    assert response.status_code == status.HTTP_200_OK
    returned_event_def = response.json()
    assert returned_event_def['ID'] == event_def1.ID.strip()
    assert returned_event_def['Verbosity'] == update_event_def_dict['Verbosity']
    assert returned_event_def['Caption'] == update_event_def_dict['Caption']
    assert returned_event_def['Silent'] == update_event_def_dict['Silent']
    assert returned_event_def['Enabled'] == update_event_def_dict['Enabled']
    assert returned_event_def['Visible'] == update_event_def_dict['Visible']


def test_update_event_def_should_return_not_found_response_code_and_error_when_no_event_def_with_given_id(test_client):
    update_event_def_dict = {'Verbosity': 'verbosity2', 'Caption': 'caption2',
                             'Silent': False, 'Visible': True, 'Enabled': False}
    response = test_client.put("/event_def/" + event_def1.ID, json=update_event_def_dict)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No event def with id = ' + event_def1.ID
