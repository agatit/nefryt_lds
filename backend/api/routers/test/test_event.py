import os
import sys
from datetime import datetime
import jwt
from sqlalchemy.orm import Session
from starlette import status
from starlette.testclient import TestClient
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))  # noqa: E402
from api import app
from api.db import get_engine, get_test_engine
from database import lds
import pytest
from api.routers.security import SECRET_KEY, ALGORITHM


def reset_event_objects():
    global event_def_visible, event_def_invisible, event_def_disabled
    global method_def, pipeline, method
    global event_visible, event_invisible, event_disabled, lds_objects, events

    event_def_visible = lds.EventDef(ID='VISIBLE', Verbosity='verbosity', Caption='caption',
                                     Silent=False, Visible=True, Enabled=True)
    event_def_invisible = lds.EventDef(ID='INVISIBLE', Verbosity='verbosity', Caption='caption',
                                       Silent=False, Visible=False, Enabled=True)
    event_def_disabled = lds.EventDef(ID='DISABLED', Verbosity='verbosity', Caption='caption',
                                      Silent=False, Visible=True, Enabled=False)
    method_def = lds.MethodDef(ID='METHODDEF')
    pipeline = lds.Pipeline(ID=10)
    method = lds.Method(ID=1, MethodDefID='METHODDEF', PipelineID=10)
    event_visible = lds.Event(ID=1, EventDefID='VISIBLE', MethodID=1, BeginDate=datetime.now())
    event_invisible = lds.Event(ID=2, EventDefID='INVISIBLE', MethodID=1, BeginDate=datetime.now())
    event_disabled = lds.Event(ID=3, EventDefID='DISABLED', MethodID=1, BeginDate=datetime.now())
    lds_objects = [event_def_visible, event_def_invisible, event_def_disabled, method_def, pipeline, method,
                   event_visible, event_invisible, event_disabled]
    events = [event_visible, event_invisible, event_disabled]

    return lds_objects


app.dependency_overrides[get_engine] = get_test_engine
test_client = TestClient(app)


def test_list_event_def_should_return_ok_response_code_and_empty_list_when_no_events():
    response = test_client.get("/event")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 0


@pytest.mark.parametrize('reset_lds_objects', [reset_event_objects], indirect=True)
def test_list_trend_def_should_return_ok_response_code_and_correct_visible_and_enabled_events(add_lds_objects):
    response = test_client.get("/event")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    returned_event = response.json()[0]
    assert returned_event['ID'] == event_visible.ID
    assert returned_event['EventDefID'] == event_visible.EventDefID.strip()
    assert returned_event['Verbosity'] == event_def_visible.Verbosity.strip()
    assert returned_event['Caption'] == event_def_visible.Caption
    assert returned_event['MethodID'] == event_visible.MethodID
    assert returned_event['BeginDate']
    assert not returned_event['AckDate']
    assert not returned_event['EndDate']


@pytest.mark.parametrize('reset_lds_objects', [reset_event_objects], indirect=True)
def test_get_event_by_id_should_return_ok_response_code_and_correct_event(add_lds_objects):
    response = test_client.get("/event/"+str(event_invisible.ID))
    assert response.status_code == status.HTTP_200_OK
    returned_event = response.json()
    assert returned_event['ID'] == event_invisible.ID
    assert returned_event['EventDefID'] == event_invisible.EventDefID.strip()
    assert returned_event['Verbosity'] == event_def_invisible.Verbosity.strip()
    assert returned_event['Caption'] == event_def_invisible.Caption
    assert returned_event['MethodID'] == event_invisible.MethodID
    assert returned_event['BeginDate']
    assert not returned_event['AckDate']
    assert not returned_event['EndDate']


def test_get_event_by_id_should_return_not_found_response_code_and_error_when_no_event_with_given_id():
    event_id = -1
    response = test_client.get("/event/" + str(event_id))
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No event with id = ' + str(event_id)


@pytest.mark.parametrize('reset_lds_objects', [reset_event_objects], indirect=True)
def test_ack_event_should_return_ok_response_code_and_information_and_set_ack_date(add_lds_objects):
    token_data = {
        'perms': ['admin']
    }
    encoded_token = jwt.encode(token_data, SECRET_KEY, ALGORITHM)
    header = {"Authorization": f"Bearer {encoded_token}"}
    response = test_client.post("/event/" + str(event_invisible.ID) + "/ack", headers=header)
    assert response.status_code == status.HTTP_200_OK
    information = response.json()
    assert information['message'] == "Event acknowledged"
    assert information['affected'] == 1
    assert information['status'] == status.HTTP_200_OK
    with Session(get_test_engine()) as session:
        changed_event = session.get(lds.Event, event_invisible.ID)
    assert changed_event.AckDate


# tested because its only method with authorization other than auth
@pytest.mark.parametrize('reset_lds_objects', [reset_event_objects], indirect=True)
def test_ack_event_should_return_unauthorized_response_code_when_header_is_invalid(add_lds_objects):
    token_data = {
        'perms': ['admin']
    }
    encoded_token = jwt.encode(token_data, SECRET_KEY, ALGORITHM)
    header = {"Authorizations": f"Bearer {encoded_token}"}
    response = test_client.post("/event/" + str(event_invisible.ID) + "/ack", headers=header)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize('reset_lds_objects', [reset_event_objects], indirect=True)
def test_ack_event_should_return_forbidden_response_code_and_error_when_permissions_are_incorrect(add_lds_objects):
    token_data = {
        'perms': ['user']
    }
    encoded_token = jwt.encode(token_data, SECRET_KEY, ALGORITHM)
    header = {"Authorization": f"Bearer {encoded_token}"}
    response = test_client.post("/event/" + str(event_invisible.ID) + "/ack", headers=header)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    error = response.json()
    assert error['code'] == status.HTTP_403_FORBIDDEN
    assert error['message'] == 'Forbidden'


def test_ack_event_should_return_not_found_response_code_and_error_when_no_event_with_given_id():
    event_id = -1
    token_data = {
        'perms': ['admin']
    }
    encoded_token = jwt.encode(token_data, SECRET_KEY, ALGORITHM)
    header = {"Authorization": f"Bearer {encoded_token}"}
    response = test_client.post("/event/" + str(event_id) + "/ack", headers=header)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No event with id = ' + str(event_id)
