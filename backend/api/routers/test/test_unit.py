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

unit1 = lds.Unit(ID='C', Name='celsius', Symbol='C', BaseID='C')
unit2 = lds.Unit(ID='F', Name='fahrenheit', Symbol='F', BaseID='C', Multiplier=5/9)
unit3 = lds.Unit(ID='K', Name='kelvin', Symbol='K', BaseID='K')
units_list = [unit1, unit2, unit3]


def reset_unit_objects():
    global unit1, unit2, unit3, units_list

    unit1 = lds.Unit(ID='C', Name='celsius', Symbol='C', BaseID='C')
    unit2 = lds.Unit(ID='F', Name='fahrenheit', Symbol='F', BaseID='C', Multiplier=5/9)
    unit3 = lds.Unit(ID='K', Name='kelvin', Symbol='K', BaseID='K')
    units_list = [unit1, unit2, unit3]

    return [units_list]


app.dependency_overrides[get_user_token] = lambda: {"sub": "test_user"}  # type: ignore[attr-defined]
test_client = TestClient(app)


def test_list_units_should_return_ok_response_code_and_empty_list_when_no_units():
    response = test_client.get("/unit")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['items']) == 0


@pytest.mark.parametrize('reset_lds_objects', [reset_unit_objects], indirect=True)
def test_list_units_should_return_ok_response_code_and_correct_units(add_lds_objects):
    response = test_client.get("/unit")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()['items']
    assert len(items) == len(units_list)
    for expected_unit, returned_unit in zip(units_list, items):
        assert returned_unit['ID'] == expected_unit.ID.strip()
        assert returned_unit['Name'] == expected_unit.Name
        assert returned_unit['Symbol'] == expected_unit.Symbol
        assert returned_unit['BaseID'] == expected_unit.BaseID.strip()
        assert returned_unit['Multiplier'] == str(expected_unit.Multiplier)


@pytest.mark.parametrize('reset_lds_objects', [reset_unit_objects], indirect=True)
def test_list_units_should_return_ok_response_code_and_correct_page_data(add_lds_objects):
    size = 2
    page = 1
    response = test_client.get(f"/unit?size={size}&page={page}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == size if size < len(units_list) else len(units_list)
    assert response.json()['total'] == len(units_list)
    assert response.json()['pages'] == len(units_list) // size if len(units_list) % size == 0 \
        else len(units_list) // size + 1
    assert response.json()['size'] == size
    assert response.json()['page'] == page


@pytest.mark.parametrize('reset_lds_objects', [reset_unit_objects], indirect=True)
def test_list_units_should_return_ok_response_code_and_default_page_data(add_lds_objects):
    response = test_client.get("/unit")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == len(units_list)
    assert response.json()['total'] == len(units_list)
    assert response.json()['pages'] == 1
    assert response.json()['size'] == 50
    assert response.json()['page'] == 1


@pytest.mark.parametrize('reset_lds_objects', [reset_unit_objects], indirect=True)
def test_list_units_should_return_ok_response_code_and_data_filtered_by_odata_query(add_lds_objects):
    odata_filter = f'BaseID eq \'{unit1.BaseID.strip()}\''
    response = test_client.get(f"/unit?filter={odata_filter}")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()['items']
    assert len(items) == 2
    for expected_unit, returned_unit in zip(units_list[:-1], items):
        assert returned_unit['ID'] == expected_unit.ID.strip()
        assert returned_unit['Name'] == expected_unit.Name
        assert returned_unit['Symbol'] == expected_unit.Symbol
        assert returned_unit['BaseID'] == expected_unit.BaseID.strip()
        assert returned_unit['Multiplier'] == str(expected_unit.Multiplier)


@pytest.mark.parametrize('reset_lds_objects', [reset_unit_objects], indirect=True)
def test_create_unit_should_return_created_response_code_and_created_unit_data(add_lds_objects):
    unit_dict = {'ID': 'Pa', 'Symbol': 'Pa', 'Name': 'Pascal', 'BaseID': 'Pa', 'Multiplier': 1}
    response = test_client.post("/unit", json=unit_dict)
    assert response.status_code == status.HTTP_201_CREATED
    returned_unit = response.json()
    assert returned_unit['ID'] == unit_dict['ID']
    assert returned_unit['Name'] == unit_dict['Name']
    assert returned_unit['Symbol'] == unit_dict['Symbol']
    assert returned_unit['BaseID'] == unit_dict['BaseID']
    assert returned_unit['Multiplier'] == unit_dict['Multiplier']
    with Session(get_engine()) as session:
        units_count = session.execute(select(func.count()).select_from(lds.Unit)).fetchall()[0][0]
    assert units_count == len(units_list) + 1


@pytest.mark.parametrize('reset_lds_objects', [reset_unit_objects], indirect=True)
def test_delete_unit_by_id_should_return_no_content_response_code_and_remove_unit(add_lds_objects):
    response = test_client.delete("/unit/" + unit1.ID)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    with Session(get_engine()) as session:
        units_count = session.execute(select(func.count()).select_from(lds.Unit)).fetchall()[0][0]
    assert units_count == len(units_list) - 1


def test_delete_unit_by_id_should_return_not_found_response_code_and_error_when_no_unit_with_given_id():
    response = test_client.delete("/unit/" + unit1.ID)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No unit with id = ' + str(unit1.ID)


@pytest.mark.parametrize('reset_lds_objects', [reset_unit_objects], indirect=True)
def test_get_unit_by_id_should_return_ok_response_code_and_unit_of_given_id(add_lds_objects):
    response = test_client.get("/unit/" + unit3.ID)
    assert response.status_code == status.HTTP_200_OK
    returned_unit = response.json()
    assert returned_unit['ID'] == unit3.ID.strip()
    assert returned_unit['Name'] == unit3.Name
    assert returned_unit['Symbol'] == unit3.Symbol
    assert returned_unit['BaseID'] == unit3.BaseID.strip()
    assert returned_unit['Multiplier'] == str(unit3.Multiplier)


def test_get_unit_by_id_should_return_not_found_response_code_and_error_when_no_unit_with_given_id():
    response = test_client.get("/unit/" + unit2.ID)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No unit with id = ' + str(unit2.ID)


@pytest.mark.parametrize('reset_lds_objects', [reset_unit_objects], indirect=True)
def test_update_unit_should_return_ok_response_code_and_unit_of_given_id(add_lds_objects):
    updated_unit_dict = {'Symbol': 'Fa'}
    response = test_client.put("/unit/" + unit2.ID, json=updated_unit_dict)
    assert response.status_code == status.HTTP_200_OK
    returned_unit = response.json()
    assert returned_unit['ID'] == unit2.ID.strip()
    assert returned_unit['Name'] == unit2.Name
    assert returned_unit['Symbol'] == updated_unit_dict['Symbol']
    assert returned_unit['BaseID'] == unit2.BaseID.strip()
    assert returned_unit['Multiplier'] == str(unit2.Multiplier)


def test_update_unit_should_return_not_found_response_code_and_error_when_no_unit_with_given_id():
    updated_unit_dict = {'Symbol': 'Fa'}
    response = test_client.put("/unit/" + unit3.ID, json=updated_unit_dict)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No unit with id = ' + str(unit3.ID)
