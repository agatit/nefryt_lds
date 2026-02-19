import React from "react";
import {
  Form,
  Field,
  FormElement,
  FieldRenderProps,
} from "@progress/kendo-react-form";
import { DropDownList } from "@progress/kendo-react-dropdowns";
import {
  NumericTextBox,
  TextBox,
  FlatColorPicker,
} from "@progress/kendo-react-inputs";
import { Label, Error } from "@progress/kendo-react-labels";
import { Button } from "@progress/kendo-react-buttons";
import {
  cancelIcon,
  saveIcon,
  trashIcon,
  pencilIcon,
} from "@progress/kendo-svg-icons";

import {
  Trend,
  TrendDef,
  TrendGroup,
  Unit,
} from "../../../../../../services/api";
import { ParsedTrendType } from "../../index";

const ValidatedNumeric = (props: FieldRenderProps) => {
  const { validationMessage, touched, visited, ...inputProps } = props;

  return (
    <div>
      <NumericTextBox {...inputProps} />
      {(touched || visited) && validationMessage && (
        <Error>{validationMessage}</Error>
      )}
    </div>
  );
};

interface Props {
  selected: ParsedTrendType | null;
  trendDefs: TrendDef[];
  trendGroups: TrendGroup[];
  units: Unit[];
  editTrend: (value: Trend) => Promise<void>;
  deleteTrend: (value: Trend) => Promise<void>;
  addTrend: (value: Trend) => Promise<Trend>;
  addMode: boolean;
  setAddMode: (v: boolean) => void;
}

const TrendConfigurationDetailPanel = React.memo(function ({
  selected,
  trendDefs,
  trendGroups,
  units,
  editTrend,
  deleteTrend,
  addTrend,
  addMode,
  setAddMode,
}: Props) {
  const [inEdit, setInEdit] = React.useState(false);
  const [loading, setLoading] = React.useState(false);

  const initialValues =
    addMode || !selected
      ? {
          Name: "",
          TrendDefID: null,
          TrendGroupID: null,
          UnitID: null,
          Color: "#ffffff",
          RawMin: 0,
          RawMax: 100,
          ScaledMin: 0,
          ScaledMax: 100,
        }
      : selected;

  const handleSubmit = async (values: any) => {
    const payload: Trend = {
      ID: addMode ? 0 : selected!.ID,
      Name: values.Name,
      TrendDefID: values.TrendDefID?.ID ?? values.TrendDefID,
      TrendGroupID: values.TrendGroupID?.ID ?? values.TrendGroupID,
      UnitID: values.UnitID?.ID ?? values.UnitID,
      Color: values.Color,
      RawMin: values.RawMin,
      RawMax: values.RawMax,
      ScaledMin: values.ScaledMin,
      ScaledMax: values.ScaledMax,
    };

    try {
      setLoading(true);

      if (addMode) {
        await addTrend(payload);
        setAddMode(false);
        return;
      }

      await editTrend(payload);
      setInEdit(false);
    } finally {
      setLoading(false);
    }
  };

  React.useEffect(() => {
    setInEdit(addMode);
  }, [selected, addMode]);

  return (
    <Form
      key={addMode ? "add" : selected?.ID}
      initialValues={initialValues}
      onSubmit={handleSubmit}
      render={(formProps) => (
        <FormElement className="detail-panel-content">
          <Label>Name</Label>
          <Field name="Name" component={TextBox} disabled={!inEdit} />

          <Label>Trend Type</Label>
          <Field
            name="TrendDefID"
            component={(props: any) => (
              <DropDownList
                {...props}
                data={trendDefs}
                textField="Name"
                dataItemKey="ID"
                disabled={!inEdit}
                onChange={(e) => props.onChange({ value: e.value })}
              />
            )}
          />

          <Label>Trend Group</Label>
          <Field
            name="TrendGroupID"
            component={(props: any) => (
              <DropDownList
                {...props}
                data={trendGroups}
                textField="Name"
                dataItemKey="ID"
                disabled={!inEdit}
                onChange={(e) => props.onChange({ value: e.value })}
              />
            )}
          />

          <Label>Unit</Label>
          <Field
            name="UnitID"
            component={(props: any) => (
              <DropDownList
                {...props}
                data={units}
                textField="Symbol"
                dataItemKey="ID"
                disabled={!inEdit}
                onChange={(e) => props.onChange({ value: e.value })}
              />
            )}
          />

          <Label>Color</Label>
          <Field name="Color" component={FlatColorPicker} />

          <Label>Raw Min</Label>
          <Field
            name="RawMin"
            component={ValidatedNumeric}
            disabled={!inEdit}
          />

          <Label>Raw Max</Label>
          <Field
            name="RawMax"
            component={ValidatedNumeric}
            disabled={!inEdit}
          />

          <Label>Scaled Min</Label>
          <Field
            name="ScaledMin"
            component={ValidatedNumeric}
            disabled={!inEdit}
          />

          <Label>Scaled Max</Label>
          <Field
            name="ScaledMax"
            component={ValidatedNumeric}
            disabled={!inEdit}
          />

          <div className="item-row">
            {!inEdit && !addMode ? (
              <Button svgIcon={pencilIcon} onClick={() => setInEdit(true)}>
                Edit
              </Button>
            ) : (
              <>
                <Button
                  svgIcon={cancelIcon}
                  disabled={loading}
                  onClick={() => {
                    setAddMode(false);
                    setInEdit(false);
                    formProps.onFormReset();
                  }}
                >
                  Cancel
                </Button>

                {!addMode && selected && (
                  <Button
                    svgIcon={trashIcon}
                    disabled={loading}
                    onClick={() => deleteTrend(selected)}
                  >
                    Delete
                  </Button>
                )}

                <Button
                  svgIcon={saveIcon}
                  themeColor="primary"
                  disabled={!formProps.allowSubmit || loading}
                  onClick={formProps.onSubmit}
                >
                  {addMode ? "Add" : "Save"}
                </Button>
              </>
            )}
          </div>
        </FormElement>
      )}
    />
  );
});

export default TrendConfigurationDetailPanel;
