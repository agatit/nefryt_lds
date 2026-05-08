import os
import sys
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from starlette import status
from starlette.testclient import TestClient
from api.schemas.base import Axis
from conftest import test_client
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))  # noqa: E402
from db import get_engine
from api.routers.utils.security import get_user_token
from database import lds
import pytest
import warnings


trend_def1 = lds.TrendDef(ID='ID_1', Name='TrendDef1')
trend_def2 = lds.TrendDef(ID='ID_2', Name='TrendDef2')
trend_def_list = [trend_def1, trend_def2]
trend_group = lds.TrendGroup(ID=1, Name='Group1')
unit = lds.Unit(ID='Unit1', Name='Unit1', Symbol='U')
trend1 = lds.Trend(ID=1, TrendDefID=trend_def1.ID, RawMin=1, RawMax=10, ScaledMin=0.5, ScaledMax=1.5,
                   Name='Trend1', TrendGroupID=trend_group.ID, UnitID=unit.ID, Color='Black')
trend2 = lds.Trend(ID=2, TrendDefID=trend_def2.ID, RawMin=2, RawMax=20, ScaledMin=0.2, ScaledMax=1.2,
                   Name='Trend2', TrendGroupID=trend_group.ID, UnitID=unit.ID, Color='Red')
trend_list = [trend1, trend2]
axis1 = Axis(TrendsID=[1], Title='Axis1', UnitID=unit.ID, ScaledMin=0.5, ScaledMax=1.5)
axis2 = Axis(TrendsID=[1, 2], Title='Axis2', UnitID=unit.ID, ScaledMin=1.5, ScaledMax=2.5)
axis3 = Axis(TrendsID=[1, 2, 3], Title='Axis3', UnitID=unit.ID, ScaledMax=2.5, ScaledMin=3.5)
axis4 = Axis(TrendsID=[2], Title='Axis4', UnitID=unit.ID+'2', ScaledMax=3.5, ScaledMin=4.5)
axes_list = [axis1, axis2, axis3, axis4]
template1 = lds.Template(ID=1, Name='Template1', Axes=[])
template2 = lds.Template(ID=2, Name='Template2', Axes=[axis1.model_dump(), axis2.model_dump()])
template3 = lds.Template(ID=3, Name='Template3', Axes=[axis3.model_dump()])
templates_list = [template1, template2, template3]


def reset_templates_objects():
    global trend_def1, trend_def2, trend_def_list, trend1, trend2, trend_list, template1, template2, template3, \
        templates_list, unit, trend_group

    trend_def1 = lds.TrendDef(ID='ID_1', Name='TrendDef1')
    trend_def2 = lds.TrendDef(ID='ID_2', Name='TrendDef2')
    trend_def_list = [trend_def1, trend_def2]
    trend_group = lds.TrendGroup(ID=1, Name='Group1')
    unit = lds.Unit(ID='Unit1', Name='Unit1', Symbol='U')
    trend1 = lds.Trend(ID=1, TrendDefID=trend_def1.ID, RawMin=1, RawMax=10, ScaledMin=0.5, ScaledMax=1.5,
                       Name='Trend1', TrendGroupID=trend_group.ID, UnitID=unit.ID, Color='Black')
    trend2 = lds.Trend(ID=2, TrendDefID=trend_def2.ID, RawMin=2, RawMax=20, ScaledMin=0.2, ScaledMax=1.2,
                       Name='Trend2', TrendGroupID=trend_group.ID, UnitID=unit.ID, Color='Red')
    trend_list = [trend1, trend2]
    template1 = lds.Template(ID=1, Name='Template1', Axes=[])
    template2 = lds.Template(ID=2, Name='Template2', Axes=[axis1.model_dump(), axis2.model_dump()])
    template3 = lds.Template(ID=3, Name='Template3', Axes=[axis3.model_dump()])
    templates_list = [template1, template2, template3]
    lds_objects = [trend_def_list, [trend_group], [unit], trend_list, templates_list]

    return lds_objects


def test_list_templates_should_return_ok_response_code_and_empty_list_when_no_templates(test_client):
    response = test_client.get("/template")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['items']) == 0


@pytest.mark.parametrize('add_test_context', [reset_templates_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_templates_should_return_ok_response_code_and_correct_templates(test_client):
    response = test_client.get("/template")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()['items']
    assert len(items) == len(templates_list)
    for expected_template, returned_template in zip(templates_list, items):
        assert returned_template['ID'] == expected_template.ID
        assert returned_template['Name'] == expected_template.Name
        assert returned_template['Axes'] == expected_template.Axes


@pytest.mark.parametrize('add_test_context', [reset_templates_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_templates_should_return_ok_response_code_and_correct_page_data(test_client):
    size = 2
    page = 1
    response = test_client.get(f"/template?size={size}&page={page}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == size
    assert response.json()['total'] == len(templates_list)
    assert response.json()['pages'] == len(templates_list) // size if len(templates_list) % size == 0 \
        else len(templates_list) // size + 1
    assert response.json()['size'] == size
    assert response.json()['page'] == page


@pytest.mark.parametrize('add_test_context', [reset_templates_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_templates_should_return_ok_response_code_and_default_page_data(test_client):
    response = test_client.get("/template")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    assert len(response.json()['items']) == len(templates_list)
    assert response.json()['total'] == len(templates_list)
    assert response.json()['pages'] == 1
    assert response.json()['size'] == 50
    assert response.json()['page'] == 1


@pytest.mark.parametrize('add_test_context', [reset_templates_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_list_templates_should_return_ok_response_code_and_data_filtered_by_odata_query(test_client):
    odata_filter = f'ID gt {template1.ID} and ID lt {template3.ID}'
    response = test_client.get(f"/template?filter={odata_filter}")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()['items']
    assert len(items) == 1
    returned_template = items[0]
    assert returned_template['ID'] == template2.ID
    assert returned_template['Name'] == template2.Name
    assert returned_template['Axes'] == template2.Axes


@pytest.mark.parametrize('add_test_context', [reset_templates_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_create_template_should_return_created_response_code_and_created_template_data(test_client):
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")

        template_dict = {'Name': 'Template3', 'Axes': [
            axis1.model_dump(),
            axis2.model_dump()
        ]}
        response = test_client.post("/template", json=template_dict)
        assert response.status_code == status.HTTP_201_CREATED
        returned_link = response.json()
        assert returned_link['ID'] == template3.ID + 1
        assert returned_link['Name'] == template_dict['Name']
        assert returned_link['Axes'] == template_dict['Axes']
        with Session(get_engine()) as session:
            templates_count = session.execute(select(func.count()).select_from(lds.Template)).fetchall()[0][0]
        assert templates_count == len(templates_list) + 1


@pytest.mark.parametrize('add_test_context', [reset_templates_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_create_template_should_return_not_acceptable_response_code_and_error_when_no_trends_with_given_ids(test_client):
    template_dict = {'Name': 'Template3', 'Axes': [
        axis1.model_dump(),
        axis2.model_dump(),
        axis3.model_dump()
    ]}
    response = test_client.post("/template", json=template_dict)
    assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE
    error = response.json()
    assert error['code'] == status.HTTP_406_NOT_ACCEPTABLE
    assert error['message'] == 'No trends with ids = [3]'


@pytest.mark.parametrize('add_test_context', [reset_templates_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_create_template_should_return_not_acceptable_response_code_and_error_when_no_units_with_given_ids(test_client):
    template_dict = {'Name': 'Template3', 'Axes': [
        axis1.model_dump(),
        axis4.model_dump()
    ]}
    response = test_client.post("/template", json=template_dict)
    assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE
    error = response.json()
    assert error['code'] == status.HTTP_406_NOT_ACCEPTABLE
    assert error['message'] == f'No units with ids = [{axis4.UnitID}]'


@pytest.mark.parametrize('add_test_context', [reset_templates_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_delete_template_by_id_should_return_no_content_response_code_and_remove_template(test_client):
    response = test_client.delete("/template/" + str(template1.ID))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    with Session(get_engine()) as session:
        templates_count = session.execute(select(func.count()).select_from(lds.Template)).fetchall()[0][0]
    assert templates_count == len(templates_list) - 1


def test_delete_template_by_id_should_return_not_found_response_code_and_error_when_no_template_with_given_id(test_client):
    response = test_client.delete("/template/" + str(template1.ID))
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No template with id = ' + str(template1.ID)


@pytest.mark.parametrize('add_test_context', [reset_templates_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_get_template_by_id_should_return_ok_response_code_and_template_of_given_id(test_client):
    response = test_client.get("/template/" + str(template1.ID))
    assert response.status_code == status.HTTP_200_OK
    returned_link = response.json()
    assert returned_link['ID'] == template1.ID
    assert returned_link['Name'] == template1.Name
    assert returned_link['Axes'] == template1.Axes


def test_get_template_by_id_should_return_not_found_response_code_and_error_when_no_template_with_given_id(test_client):
    response = test_client.get("/template/" + str(template1.ID))
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No template with id = ' + str(template1.ID)


@pytest.mark.parametrize('add_test_context', [reset_templates_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_update_template_should_return_ok_response_code_and_template_of_given_id(test_client):
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")

        updated_template_dict = {'Axes': [axis1.model_dump(), axis2.model_dump()]}
        response = test_client.put("/template/" + str(template1.ID), json=updated_template_dict)
        assert response.status_code == status.HTTP_200_OK
        returned_link = response.json()
        assert returned_link['ID'] == template1.ID
        assert returned_link['Name'] == template1.Name
        assert returned_link['Axes'] == updated_template_dict['Axes']


@pytest.mark.parametrize('add_test_context', [reset_templates_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_update_template_should_return_not_acceptable_response_code_and_error_when_no_trends_with_given_ids(test_client):
    updated_template_dict = {'Axes': [axis1.model_dump(), axis2.model_dump(), axis3.model_dump()]}
    response = test_client.put("/template/" + str(template1.ID), json=updated_template_dict)
    assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE
    error = response.json()
    assert error['code'] == status.HTTP_406_NOT_ACCEPTABLE
    assert error['message'] == 'No trends with ids = [3]'


@pytest.mark.parametrize('add_test_context', [reset_templates_objects], indirect=True)
@pytest.mark.usefixtures("add_test_context")
def test_update_template_should_return_not_acceptable_response_code_and_error_when_no_unit_with_given_ids(test_client):
    updated_template_dict = {'Axes': [axis1.model_dump(), axis2.model_dump(), axis4.model_dump()]}
    response = test_client.put("/template/" + str(template1.ID), json=updated_template_dict)
    assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE
    error = response.json()
    assert error['code'] == status.HTTP_406_NOT_ACCEPTABLE
    assert error['message'] == f'No units with ids = [{axis4.UnitID}]'


def test_update_template_should_return_not_found_response_code_and_error_when_no_template_with_given_id(test_client):
    updated_template_dict = {'Name': 'NewTemplateName', 'Axes': [axis1.model_dump(), axis2.model_dump()]}
    response = test_client.put("/template/" + str(template2.ID), json=updated_template_dict)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error['code'] == status.HTTP_404_NOT_FOUND
    assert error['message'] == 'No template with id = ' + str(template2.ID)
