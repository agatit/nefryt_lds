import os
import sys
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from starlette import status
from starlette.testclient import TestClient
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))  # noqa: E402
from api.app import app
from db import get_engine
from api.routers.utils.security import get_user_token
from database import lds
import pytest

trend_group1 = lds.TrendGroup(ID=1, Name='Group 1', AnalysisOnly=False)
trend_group2 = lds.TrendGroup(ID=1, Name='Group 2', AnalysisOnly=True)
trend_groups_list = [trend_group1, trend_group2]


def reset_trend_group_objects():
    global trend_group1, trend_group2, trend_groups_list

    trend_group1 = lds.TrendGroup(ID=1, Name='Group 1', AnalysisOnly=False)
    trend_group2 = lds.TrendGroup(ID=2, Name='Group 2', AnalysisOnly=True)
    trend_def = lds.TrendDef(ID='ID_1', Name='TrendDef1')
    trend = lds.Trend(ID=1, TrendDefID=trend_def.ID, RawMin=1, RawMax=10, ScaledMin=0.5, ScaledMax=1.5, TrendGroupID=trend_group1.ID)
    trend_groups_list = [trend_group1, trend_group2]

    return [[trend_def], trend_groups_list, [trend]]


app.dependency_overrides[get_user_token] = lambda: {"sub": "test_user"}  # type: ignore[attr-defined]
test_client = TestClient(app)


def test_list_trend_groups_should_return_ok_response_code_and_empty_list_when_no_trend_groups():
    response = test_client.get("/trend_group")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['items']) == 0


@pytest.mark.parametrize('reset_lds_objects', [reset_trend_group_objects], indirect=True)
def test_list_trend_groups_should_return_ok_response_code_and_correct_trend_groups(add_lds_objects):
    response = test_client.get("/trend_group")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()['items']
    assert len(items) == len(trend_groups_list)
    for expected_trend_group, returned_trend_group in zip(trend_groups_list, items):
        assert returned_trend_group['ID'] == expected_trend_group.ID
        assert returned_trend_group['Name'] == expected_trend_group.Name
        assert returned_trend_group['AnalysisOnly'] == expected_trend_group.AnalysisOnly


@pytest.mark.parametrize('reset_lds_objects', [reset_trend_group_objects], indirect=True)
def test_list_trend_groups_should_return_ok_response_code_and_correct_page_data(add_lds_objects):
    size = 1
    page = 1
    response = test_client.get(f"/trend_group?size={size}&page={page}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == size if size < len(trend_groups_list) else len(trend_groups_list)
    assert response.json()['total'] == len(trend_groups_list)
    assert response.json()['pages'] == len(trend_groups_list) // size if len(trend_groups_list) % size == 0 \
        else len(trend_groups_list) // size + 1
    assert response.json()['size'] == size
    assert response.json()['page'] == page


@pytest.mark.parametrize('reset_lds_objects', [reset_trend_group_objects], indirect=True)
def test_list_trend_groups_should_return_ok_response_code_and_default_page_data(add_lds_objects):
    response = test_client.get("/trend_group")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == len(trend_groups_list)
    assert response.json()['total'] == len(trend_groups_list)
    assert response.json()['pages'] == 1
    assert response.json()['size'] == 50
    assert response.json()['page'] == 1


@pytest.mark.parametrize('reset_lds_objects', [reset_trend_group_objects], indirect=True)
def test_list_trend_groups_should_return_ok_response_code_and_data_filtered_by_odata_query(add_lds_objects):
    odata_filter = f'ID eq {trend_group1.ID}'
    response = test_client.get(f"/trend_group?filter={odata_filter}")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()['items']
    assert len(items) == 1
    returned_trend_group = items[0]
    assert returned_trend_group['ID'] == trend_group1.ID
    assert returned_trend_group['Name'] == trend_group1.Name
    assert returned_trend_group['AnalysisOnly'] == trend_group1.AnalysisOnly


@pytest.mark.parametrize('reset_lds_objects', [reset_trend_group_objects], indirect=True)
def test_create_trend_group_should_return_created_response_code_and_created_trend_group_data(add_lds_objects):
    trend_group_dict = {'Name': 'Group 3', 'AnalysisOnly': True}
    response = test_client.post("/trend_group", json=trend_group_dict)
    assert response.status_code == status.HTTP_201_CREATED
    returned_trend_group = response.json()
    assert returned_trend_group['ID'] == trend_group2.ID + 1
    assert returned_trend_group['Name'] == trend_group_dict['Name']
    assert returned_trend_group['AnalysisOnly'] == trend_group_dict['AnalysisOnly']
    with Session(get_engine()) as session:
        trend_groups_count = session.execute(select(func.count()).select_from(lds.TrendGroup)).fetchall()[0][0]
    assert trend_groups_count == len(trend_groups_list) + 1


@pytest.mark.parametrize('reset_lds_objects', [reset_trend_group_objects], indirect=True)
def test_delete_trend_group_by_id_should_return_no_content_response_code_and_remove_trend_group(add_lds_objects):
    response = test_client.delete("/trend_group/" + str(trend_group2.ID))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    with Session(get_engine()) as session:
        trend_groups_count = session.execute(select(func.count()).select_from(lds.TrendGroup)).fetchall()[0][0]
    assert trend_groups_count == len(trend_groups_list) - 1


def test_delete_trend_group_by_id_should_return_not_found_response_code_and_error_when_no_trend_group_with_given_id():
    response = test_client.delete("/trend_group/" + str(trend_group1.ID))
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No trend group with id = ' + str(trend_group1.ID)


@pytest.mark.parametrize('reset_lds_objects', [reset_trend_group_objects], indirect=True)
def test_delete_trend_group_by_id_should_return_conflict_response_code_and_error_when_exist_trends_with_given_trend_group_id(add_lds_objects):
    response = test_client.delete("/trend_group/" + str(trend_group1.ID))
    assert response.status_code == status.HTTP_409_CONFLICT
    error = response.json()
    assert error['code'] == status.HTTP_409_CONFLICT
    assert error['message'] == 'Integrity error when deleting trend group with id = ' + str(trend_group1.ID)


@pytest.mark.parametrize('reset_lds_objects', [reset_trend_group_objects], indirect=True)
def test_get_trend_group_by_id_should_return_ok_response_code_and_trend_group_of_given_id(add_lds_objects):
    response = test_client.get("/trend_group/" + str(trend_group2.ID))
    assert response.status_code == status.HTTP_200_OK
    returned_trend_group = response.json()
    assert returned_trend_group['ID'] == trend_group2.ID
    assert returned_trend_group['Name'] == trend_group2.Name
    assert returned_trend_group['AnalysisOnly'] == trend_group2.AnalysisOnly


def test_get_trend_group_by_id_should_return_not_found_response_code_and_error_when_no_trend_group_with_given_id():
    response = test_client.get("/trend_group/" + str(trend_group2.ID))
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No trend group with id = ' + str(trend_group2.ID)


@pytest.mark.parametrize('reset_lds_objects', [reset_trend_group_objects], indirect=True)
def test_update_trend_group_should_return_ok_response_code_and_trend_group_of_given_id(add_lds_objects):
    updated_trend_group_dict = {'Name': 'UpdatedGroup2', 'AnalysisOnly': False}
    response = test_client.put("/trend_group/" + str(trend_group2.ID), json=updated_trend_group_dict)
    assert response.status_code == status.HTTP_200_OK
    returned_trend_group = response.json()
    assert returned_trend_group['ID'] == trend_group2.ID
    assert returned_trend_group['Name'] == updated_trend_group_dict['Name']
    assert returned_trend_group['AnalysisOnly'] == updated_trend_group_dict['AnalysisOnly']


def test_update_trend_group_should_return_not_found_response_code_and_error_when_no_trend_group_with_given_id():
    updated_trend_group_dict = {'Name': 'UpdatedGroup2', 'AnalysisOnly': False}
    response = test_client.put("/trend_group/" + str(trend_group2.ID), json=updated_trend_group_dict)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No trend group with id = ' + str(trend_group2.ID)
