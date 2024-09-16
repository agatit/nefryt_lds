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


def reset_link_objects():
    global node1, node2, link1, link2, links_list, lds_objects

    node1 = lds.Node(ID=1, Type='type', Name='name')
    node2 = lds.Node(ID=2, Type='type', Name='name')
    link1 = lds.Link(ID=1, BeginNodeID=1, EndNodeID=2)
    link2 = lds.Link(ID=2, BeginNodeID=2, EndNodeID=1)
    links_list = [link1, link2]
    lds_objects = [node1, node2, link1, link2]

    return [lds_objects]


def reset_node_objects():
    global node1, node2, lds_objects

    node1 = lds.Node(ID=1, Type='type', Name='name')
    node2 = lds.Node(ID=2, Type='type', Name='name')
    lds_objects = [node1, node2]

    return [lds_objects]


app.dependency_overrides[get_engine] = get_test_engine
test_client = TestClient(app)


def test_list_links_should_return_ok_response_code_and_empty_list_when_no_links():
    response = test_client.get("/link")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 0


@pytest.mark.parametrize('reset_lds_objects', [reset_link_objects], indirect=True)
def test_list_links_should_return_ok_response_code_and_correct_links(add_lds_objects):
    response = test_client.get("/link")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2
    for expected_link, returned_link in zip(links_list, response.json()):
        assert returned_link['ID'] == expected_link.ID
        assert returned_link['BeginNodeID'] == expected_link.BeginNodeID
        assert returned_link['EndNodeID'] == expected_link.EndNodeID
        assert returned_link['Length'] == expected_link.Length


@pytest.mark.parametrize('reset_lds_objects', [reset_node_objects], indirect=True)
def test_create_link_should_return_created_response_code_and_created_link_data(add_lds_objects):
    link_dict = {'ID': 1, 'BeginNodeID': 1, 'EndNodeID': 2, 'Length': 100.11}
    response = test_client.post("/link", json=link_dict)
    assert response.status_code == status.HTTP_201_CREATED
    returned_link = response.json()
    assert returned_link['ID'] == link_dict['ID']
    assert returned_link['BeginNodeID'] == link_dict['BeginNodeID']
    assert returned_link['EndNodeID'] == link_dict['EndNodeID']
    assert returned_link['Length'] == link_dict['Length']
    with Session(get_test_engine()) as session:
        links_count = session.execute(select(func.count()).select_from(lds.Link)).fetchall()[0][0]
    assert links_count == 1


@pytest.mark.parametrize('reset_lds_objects', [reset_link_objects], indirect=True)
def test_create_link_should_return_conflict_response_code_and_error_when_id_not_unique(add_lds_objects):
    link_dict = {'ID': link1.ID, 'BeginNodeID': 1, 'EndNodeID': 2, 'Length': 100.11}
    response = test_client.post("/link", json=link_dict)
    assert response.status_code == status.HTTP_409_CONFLICT
    error = response.json()
    assert error['code'] == status.HTTP_409_CONFLICT
    assert error['message'] == 'Integrity error when creating link'


@pytest.mark.parametrize('reset_lds_objects', [reset_link_objects], indirect=True)
def test_delete_link_by_id_should_return_no_content_response_code_and_remove_link(add_lds_objects):
    response = test_client.delete("/link/" + str(link1.ID))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    with Session(get_test_engine()) as session:
        links_count = session.execute(select(func.count()).select_from(lds.Link)).fetchall()[0][0]
    assert links_count == 1


def test_delete_link_by_id_should_return_not_found_response_code_and_error_when_no_link_with_given_id():
    response = test_client.delete("/link/" + str(link1.ID))
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No link with id = ' + str(link1.ID)


@pytest.mark.parametrize('reset_lds_objects', [reset_link_objects], indirect=True)
def test_get_link_by_id_should_return_ok_response_code_and_link_of_given_id(add_lds_objects):
    response = test_client.get("/link/" + str(link1.ID))
    assert response.status_code == status.HTTP_200_OK
    returned_link = response.json()
    assert returned_link['ID'] == link1.ID
    assert returned_link['BeginNodeID'] == link1.BeginNodeID
    assert returned_link['EndNodeID'] == link1.EndNodeID
    assert returned_link['Length'] == link1.Length


def test_get_link_by_id_should_return_not_found_response_code_and_error_when_no_link_with_given_id():
    response = test_client.get("/link/" + str(link1.ID))
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No link with id = ' + str(link1.ID)


@pytest.mark.parametrize('reset_lds_objects', [reset_link_objects], indirect=True)
def test_update_link_by_id_should_return_ok_response_code_and_link_of_given_id(add_lds_objects):
    updated_link_dict = {'BeginNodeID': 1, 'EndNodeID': 2, 'Length': 99.99}
    response = test_client.put("/link/" + str(link2.ID), json=updated_link_dict)
    assert response.status_code == status.HTTP_200_OK
    returned_link = response.json()
    assert returned_link['ID'] == link2.ID
    assert returned_link['BeginNodeID'] == updated_link_dict['BeginNodeID']
    assert returned_link['EndNodeID'] == updated_link_dict['EndNodeID']
    assert returned_link['Length'] == updated_link_dict['Length']


def test_update_link_by_id_should_return_not_found_response_code_and_error_when_no_link_with_given_id():
    updated_link_dict = {'BeginNodeID': 1, 'EndNodeID': 2, 'Length': 99.99}
    response = test_client.put("/link/" + str(link2.ID), json=updated_link_dict)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No link with id = ' + str(link2.ID)


@pytest.mark.parametrize('reset_lds_objects', [reset_link_objects], indirect=True)
def test_update_link_by_id_should_return_conflict_response_code_and_error_when_no_node_with_given_id(add_lds_objects):
    updated_link_dict = {'BeginNodeID': 1, 'EndNodeID': 5, 'Length': 99.999}
    response = test_client.put("/link/" + str(link2.ID), json=updated_link_dict)
    assert response.status_code == status.HTTP_409_CONFLICT
    error = response.json()
    assert error['code'] == status.HTTP_409_CONFLICT
    assert error['message'] == 'Integrity error when updating link with id = ' + str(link2.ID)
