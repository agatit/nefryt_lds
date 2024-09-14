import os
import sys
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from starlette import status
from starlette.testclient import TestClient
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))  # noqa: E402
from api import app
from api.db import get_engine, get_test_engine
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

    return event_def_list


app.dependency_overrides[get_engine] = get_test_engine
test_client = TestClient(app)


def test_list_event_def_should_return_ok_response_code_and_empty_list_when_no_event_defs():
    response = test_client.get("/event_def")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 0


@pytest.mark.parametrize('reset_lds_objects', [reset_event_def_objects], indirect=True)
def test_list_event_def_should_return_ok_response_code_and_correct_event_defs(add_lds_objects):
    response = test_client.get("/event_def")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2
    for expected_event_def, returned_event_def in zip(event_def_list, response.json()):
        assert expected_event_def.ID.strip() == returned_event_def['ID']
        assert expected_event_def.Verbosity.strip() == returned_event_def['Verbosity']
        assert expected_event_def.Caption.strip() == returned_event_def['Caption']
        assert expected_event_def.Silent == returned_event_def['Silent']
        assert expected_event_def.Enabled == returned_event_def['Enabled']
        assert expected_event_def.Visible == returned_event_def['Visible']


def test_create_event_def_should_return_created_response_code_and_created_event_def_data():
    event_def_dict = {'ID': 'EVENT_DEF1', 'Verbosity': 'verbosity', 'Caption': 'caption',
                      'Silent': True, 'Visible': True, 'Enabled': True}
    response = test_client.post("/event_def", json=event_def_dict)
    assert response.status_code == status.HTTP_201_CREATED
    returned_event_def = response.json()
    assert event_def_dict['ID'] == returned_event_def['ID']
    assert event_def_dict['Verbosity'] == returned_event_def['Verbosity']
    assert event_def_dict['Caption'] == returned_event_def['Caption']
    assert event_def_dict['Silent'] == returned_event_def['Silent']
    assert event_def_dict['Enabled'] == returned_event_def['Enabled']
    assert event_def_dict['Visible'] == returned_event_def['Visible']
    with Session(get_test_engine()) as session:
        event_defs_count = session.execute(select(func.count()).select_from(lds.EventDef)).fetchall()[0][0]
    assert event_defs_count == 1


@pytest.mark.parametrize('reset_lds_objects', [reset_event_def_objects], indirect=True)
def test_create_event_def_should_return_conflict_response_code_and_error_when_id_not_unique(add_lds_objects):
    event_def_dict = {'ID': event_def1.ID, 'Verbosity': 'verbosity2', 'Caption': 'caption2',
                      'Silent': True, 'Visible': True, 'Enabled': True}
    response = test_client.post("/event_def", json=event_def_dict)
    assert response.status_code == status.HTTP_409_CONFLICT
    error = response.json()
    assert error['code'] == status.HTTP_409_CONFLICT
    assert error['message'] == 'Integrity error when creating event def'


@pytest.mark.parametrize('reset_lds_objects', [reset_event_def_objects], indirect=True)
def test_delete_event_def_by_id_should_return_no_content_response_code_and_remove_event_def(add_lds_objects):
    response = test_client.delete("/event_def/" + event_def1.ID)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    with Session(get_test_engine()) as session:
        event_defs_count = session.execute(select(func.count()).select_from(lds.EventDef)).fetchall()[0][0]
    assert event_defs_count == 1


def test_delete_event_def_by_id_should_return_not_found_response_code_and_error_when_no_event_def_with_given_id():
    response = test_client.delete("/event_def/" + event_def1.ID)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No event def with id = ' + event_def1.ID


@pytest.mark.parametrize('reset_lds_objects', [reset_event_def_objects], indirect=True)
def test_get_event_def_by_id_should_return_ok_response_code_and_event_def_of_given_id(add_lds_objects):
    response = test_client.get("/event_def/" + event_def1.ID)
    assert response.status_code == status.HTTP_200_OK
    returned_event_def = response.json()
    assert event_def1.ID.strip() == returned_event_def['ID']
    assert event_def1.Verbosity.strip() == returned_event_def['Verbosity']
    assert event_def1.Caption.strip() == returned_event_def['Caption']
    assert event_def1.Silent == returned_event_def['Silent']
    assert event_def1.Enabled == returned_event_def['Enabled']
    assert event_def1.Visible == returned_event_def['Visible']


def test_get_event_def_by_id_should_return_not_found_response_code_and_error_when_no_event_def_with_given_id():
    response = test_client.get("/event_def/" + event_def1.ID)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No event def with id = ' + event_def1.ID


@pytest.mark.parametrize('reset_lds_objects', [reset_event_def_objects], indirect=True)
def test_update_event_def_by_id_should_return_ok_response_code_and_event_def_of_given_id(add_lds_objects):
    update_event_def_dict = {'Verbosity': 'verbosity2', 'Caption': 'caption2',
                             'Silent': False, 'Visible': True, 'Enabled': False}
    response = test_client.put("/event_def/" + event_def1.ID, json=update_event_def_dict)
    assert response.status_code == status.HTTP_200_OK
    returned_event_def = response.json()
    assert event_def1.ID.strip() == returned_event_def['ID']
    assert update_event_def_dict['Verbosity'] == returned_event_def['Verbosity']
    assert update_event_def_dict['Caption'] == returned_event_def['Caption']
    assert update_event_def_dict['Silent'] == returned_event_def['Silent']
    assert update_event_def_dict['Enabled'] == returned_event_def['Enabled']
    assert update_event_def_dict['Visible'] == returned_event_def['Visible']


def test_update_event_def_by_id_should_return_not_found_response_code_and_error_when_no_event_def_with_given_id():
    update_event_def_dict = {'Verbosity': 'verbosity2', 'Caption': 'caption2',
                             'Silent': False, 'Visible': True, 'Enabled': False}
    response = test_client.put("/event_def/" + event_def1.ID, json=update_event_def_dict)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No event def with id = ' + event_def1.ID
