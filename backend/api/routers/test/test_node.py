import os
import sys
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from starlette import status
from starlette.testclient import TestClient
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))  # noqa: E402
from api import app
from api.db import get_engine, get_test_engine
from database import lds, editor
import pytest


def reset_node_objects():
    global lds_node1, lds_node2, editor_node1, editor_node2, nodes_list, lds_nodes_list, editor_nodes_list

    lds_node1 = lds.Node(ID=1, Type='type1', Name='name1')
    lds_node2 = lds.Node(ID=2, Type='type2', Name='name2')
    editor_node1 = editor.Node(ID=1, PosX=10, PosY=100)
    editor_node2 = editor.Node(ID=2, PosX=-10, PosY=-100)

    nodes_list = [lds_node1, lds_node2, editor_node1, editor_node2]
    lds_nodes_list = [lds_node1, lds_node2]
    editor_nodes_list = [editor_node1, editor_node2]

    return [lds_nodes_list, editor_nodes_list]


def reset_node_and_link_objects():
    global lds_node1, lds_node2, editor_node1, editor_node2, nodes_list, lds_nodes_list, editor_nodes_list

    lds_node1 = lds.Node(ID=1, Type='type1', Name='name1')
    lds_node2 = lds.Node(ID=2, Type='type2', Name='name2')
    editor_node1 = editor.Node(ID=1, PosX=10, PosY=100)
    editor_node2 = editor.Node(ID=2, PosX=-10, PosY=-100)
    link = lds.Link(ID=1, BeginNodeID=1, EndNodeID=2)

    nodes_list = [lds_node1, lds_node2, editor_node1, editor_node2]
    lds_nodes_list = [lds_node1, lds_node2]
    editor_nodes_list = [editor_node1, editor_node2]

    return [lds_nodes_list, editor_nodes_list, [link]]


app.dependency_overrides[get_engine] = get_test_engine
test_client = TestClient(app)


def test_list_nodes_should_return_ok_response_code_and_empty_list_when_no_nodes():
    response = test_client.get("/node")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 0


@pytest.mark.parametrize('reset_lds_objects', [reset_node_objects], indirect=True)
def test_list_nodes_should_return_ok_response_code_and_correct_nodes(add_lds_objects):
    response = test_client.get("/node")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2
    for expected_lds_node, expected_editor_node, returned_node \
            in zip(lds_nodes_list, editor_nodes_list, response.json()):
        assert returned_node['ID'] == expected_lds_node.ID
        assert returned_node['Type'] == expected_lds_node.Type.strip()
        assert returned_node['Name'] == expected_lds_node.Name
        assert returned_node['EditorParams']['PosX'] == expected_editor_node.PosX
        assert returned_node['EditorParams']['PosY'] == expected_editor_node.PosY


def test_create_node_should_return_created_response_code_and_created_node_data():
    node_dict = {'ID': 1, 'Type': 'type', 'Name': 'name', 'EditorParams':{'PosX': 22, 'PosY': 122}}
    response = test_client.post("/node", json=node_dict)
    assert response.status_code == status.HTTP_201_CREATED
    returned_node = response.json()
    assert returned_node['ID'] == node_dict['ID']
    assert returned_node['Type'] == node_dict['Type']
    assert returned_node['Name'] == node_dict['Name']
    assert returned_node['EditorParams']['PosX'] == node_dict['EditorParams']['PosX']
    assert returned_node['EditorParams']['PosY'] == node_dict['EditorParams']['PosY']
    with Session(get_test_engine()) as session:
        lds_nodes_count = session.execute(select(func.count()).select_from(lds.Node)).fetchall()[0][0]
        editor_nodes_count = session.execute(select(func.count()).select_from(editor.Node)).fetchall()[0][0]
    assert lds_nodes_count == 1
    assert editor_nodes_count == 1


@pytest.mark.parametrize('reset_lds_objects', [reset_node_objects], indirect=True)
def test_create_node_should_return_conflict_response_code_and_error_when_id_not_unique(add_lds_objects):
    node_dict = {'ID': 1, 'Type': 'type', 'Name': 'name', 'PosX': 22, 'PosY': 122}
    response = test_client.post("/node", json=node_dict)
    assert response.status_code == status.HTTP_409_CONFLICT
    error = response.json()
    assert error['code'] == status.HTTP_409_CONFLICT
    assert error['message'] == 'Integrity error when creating node'


@pytest.mark.parametrize('reset_lds_objects', [reset_node_objects], indirect=True)
def test_delete_node_by_id_should_return_no_content_response_code_and_remove_node(add_lds_objects):
    response = test_client.delete("/node/" + str(lds_node1.ID))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    with Session(get_test_engine()) as session:
        lds_nodes_count = session.execute(select(func.count()).select_from(lds.Node)).fetchall()[0][0]
        editor_nodes_count = session.execute(select(func.count()).select_from(editor.Node)).fetchall()[0][0]
    assert lds_nodes_count == 1
    assert editor_nodes_count == 1


@pytest.mark.parametrize('reset_lds_objects', [reset_node_and_link_objects], indirect=True)
def test_delete_node_by_id_should_return_conflict_response_code_and_error_when_node_used_in_link_record(add_lds_objects): # noqa
    response = test_client.delete("/node/" + str(lds_node1.ID))
    assert response.status_code == status.HTTP_409_CONFLICT
    error = response.json()
    assert error['code'] == status.HTTP_409_CONFLICT
    assert error['message'] == 'Integrity error when deleting node with id = ' + str(lds_node1.ID)


def test_delete_link_by_id_should_return_not_found_response_code_and_error_when_no_node_with_given_id():
    response = test_client.delete("/node/" + str(lds_node1.ID))
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No node with id = ' + str(lds_node1.ID)


@pytest.mark.parametrize('reset_lds_objects', [reset_node_objects], indirect=True)
def test_get_node_by_id_should_return_ok_response_code_and_node_of_given_id(add_lds_objects):
    response = test_client.get("/node/" + str(lds_node1.ID))
    assert response.status_code == status.HTTP_200_OK
    returned_node = response.json()
    assert returned_node['ID'] == lds_node1.ID
    assert returned_node['Type'] == lds_node1.Type.strip()
    assert returned_node['Name'] == lds_node1.Name
    assert returned_node['EditorParams']['PosX'] == editor_node1.PosX
    assert returned_node['EditorParams']['PosY'] == editor_node1.PosY


def test_get_node_by_id_should_return_not_found_response_code_and_error_when_no_node_with_given_id():
    response = test_client.get("/node/" + str(lds_node1.ID))
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No node with id = ' + str(lds_node1.ID)


@pytest.mark.parametrize('reset_lds_objects', [reset_node_objects], indirect=True)
def test_update_node_by_id_should_return_ok_response_code_and_node_of_given_id(add_lds_objects):
    updated_node_dict = {'Type': 'type2', 'Name': 'name2', 'EditorParams': {'PosX': 150, 'PosY': -150}}
    response = test_client.put("/node/" + str(lds_node1.ID), json=updated_node_dict)
    assert response.status_code == status.HTTP_200_OK
    returned_node = response.json()
    assert returned_node['ID'] == lds_node1.ID
    assert returned_node['Type'] == updated_node_dict['Type']
    assert returned_node['Name'] == updated_node_dict['Name']
    assert returned_node['EditorParams']['PosX'] == updated_node_dict['EditorParams']['PosX']
    assert returned_node['EditorParams']['PosY'] == updated_node_dict['EditorParams']['PosY']


def test_update_node_by_id_should_return_not_found_response_code_and_error_when_no_node_with_given_id():
    updated_node_dict = {'Type': 'type2', 'Name': 'name2', 'EditorParams': {'PosX': 150, 'PosY': -150}}
    response = test_client.put("/node/" + str(lds_node1.ID), json=updated_node_dict)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No node with id = ' + str(lds_node1.ID)
