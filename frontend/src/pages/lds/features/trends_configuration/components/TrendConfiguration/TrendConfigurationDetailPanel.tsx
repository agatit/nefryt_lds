import { memo, useState, useEffect, useMemo } from "react";
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
import { useTranslation } from "react-i18next";
import { TFunction } from "i18next";
import {
  Trend,
  TrendDef,
  TrendGroup,
  Unit,
  TrendUpdate,
  TrendCreate,
} from "../../../../../../services/api";
import { ParsedTrendType } from "../../index";

interface Props {
  selected: ParsedTrendType | null;
  trendDefs: TrendDef[];
  trendGroups: TrendGroup[];
  units: Unit[];
  editTrend: (id: number, value: TrendUpdate) => Promise<void>;
  deleteTrend: (value: Trend) => Promise<void>;
  addTrend: (value: TrendCreate) => Promise<Trend>;
  addMode: boolean;
  setAddMode: (v: boolean) => void;
  requestDelete: (value: ParsedTrendType) => void;
  closePanel: () => void;
}

interface TrendFormValues {
  Name: string;
  TrendDefID: TrendDef | null;
  TrendGroupID: TrendGroup | null;
  UnitID: Unit | null;
  Color: string;
  RawMin: number;
  RawMax: number;
  ScaledMin: number;
  ScaledMax: number;
}

interface ValidationErrors {
  [key: string]: string;
}

const ValidatedInput = (props: FieldRenderProps) => {
  const { validationMessage, touched, modified, ...inputProps } = props;

  return (
    <div className="field-wrapper">
      <NumericTextBox {...inputProps} />
      {(touched || modified) && validationMessage && (
        <Error>{validationMessage}</Error>
      )}
    </div>
  );
};

const ValidatedTextBox = (props: FieldRenderProps) => {
  const { validationMessage, touched, modified, ...inputProps } = props;

  return (
    <div className="field-wrapper">
      <TextBox {...inputProps} />
      {(touched || modified) && validationMessage && (
        <Error>{validationMessage}</Error>
      )}
    </div>
  );
};

const ValidatedDropDown = (
  props: FieldRenderProps & {
    data: any[];
    textField: string;
    dataItemKey: string;
    disabled?: boolean;
  },
) => {
  const { validationMessage, touched, modified, ...rest } = props;

  return (
    <div className="field-wrapper">
      <DropDownList
        {...rest}
        validationMessage={validationMessage ?? undefined}
        onChange={(e) => props.onChange({ value: e.value })}
      />

      {(touched || modified) && validationMessage && (
        <Error>{validationMessage}</Error>
      )}
    </div>
  );
};

const ValidatedColor = (props: FieldRenderProps) => {
  const { validationMessage, touched, modified, ...rest } = props;

  return (
    <div className="field-wrapper">
      <FlatColorPicker
        {...rest}
        showButtons={false}
        showClearButton={false}
        showPreview={false}
        onChange={(e) => props.onChange({ value: e.value })}
      />

      {(touched || modified) && validationMessage && (
        <Error>{validationMessage}</Error>
      )}
    </div>
  );
};

const trendValidator = (t: TFunction) => (values: TrendFormValues) => {
  const errors: ValidationErrors = {};

  if (!values.Name?.trim()) {
    errors.Name = t("config-page:name_required");
  }

  if (!values.TrendDefID) {
    errors.TrendDefID = t("config-page:type_required");
  }

  if (!values.TrendGroupID) {
    errors.TrendGroupID = t("config-page:group_required");
  }

  if (!values.UnitID) {
    errors.UnitID = t("config-page:unit_required");
  }

  if (
    values.RawMin != null &&
    values.RawMax != null &&
    values.RawMin === values.RawMax
  ) {
    errors.RawMin = " ";
    errors.RawMax = t("config-page:raw_same");
  }

  if (
    values.RawMin != null &&
    values.RawMax != null &&
    values.RawMin > values.RawMax
  ) {
    errors.RawMin = " ";
    errors.RawMax = t("config-page:raw_range");
  }

  if (
    values.ScaledMin != null &&
    values.ScaledMax != null &&
    values.ScaledMin > values.ScaledMax
  ) {
    errors.ScaledMin = " ";
    errors.ScaledMax = t("config-page:scaled_same");
  }

  if (
    values.ScaledMin != null &&
    values.ScaledMax != null &&
    values.ScaledMin === values.ScaledMax
  ) {
    errors.ScaledMin = " ";
    errors.ScaledMax = t("config-page:scaled_range");
  }

  return Object.keys(errors).length ? errors : undefined;
};

const TrendConfigurationDetailPanel = memo(function ({
  selected,
  trendDefs,
  trendGroups,
  units,
  editTrend,
  requestDelete,
  addTrend,
  addMode,
  setAddMode,
  closePanel,
}: Props) {
  const [inEdit, setInEdit] = useState(false);
  const [loading, setLoading] = useState(false);
  const { t } = useTranslation(["common", "config-page"]);

  const initialValues = useMemo(() => {
    if (addMode || !selected) {
      return {
        Name: "",
        TrendDefID: null,
        TrendGroupID: null,
        UnitID: null,
        Color: "#ffffff",
        RawMin: 0,
        RawMax: 0,
        ScaledMin: 0,
        ScaledMax: 0,
      };
    }

    return {
      ...selected,
      TrendDefID: trendDefs.find((t) => t.ID === selected.TrendDefID),
      TrendGroupID: trendGroups.find((t) => t.ID === selected.TrendGroupID),
      UnitID: units.find((t) => t.ID === selected.UnitID),
    };
  }, [selected?.ID, addMode]);

  const handleSubmit = async (values: TrendFormValues) => {
    const payload: Trend = {
      ID: addMode ? 0 : selected!.ID,
      Name: values.Name,
      TrendDefID: String(values.TrendDefID?.ID ?? ""),
      TrendGroupID: values.TrendGroupID?.ID ?? 0,
      UnitID: String(values.UnitID?.ID ?? ""),
      Color: values.Color,
      RawMin: values.RawMin ?? 0,
      RawMax: values.RawMax ?? 0,
      ScaledMin: values.ScaledMin ?? 0,
      ScaledMax: values.ScaledMax ?? 0,
    };

    try {
      setLoading(true);

      if (addMode) {
        await addTrend(payload);
        setAddMode(false);
        closePanel();
        return;
      }

      await editTrend(selected!.ID, payload);
      setInEdit(false);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    setInEdit(addMode);
  }, [selected, addMode]);

  return (
    <Form
      key={addMode ? "add" : selected?.ID}
      initialValues={initialValues}
      validator={trendValidator(t)}
      onSubmit={(values) => handleSubmit(values as TrendFormValues)}
      render={(formProps) => (
        <FormElement className="detail-panel-content">
          <div className="item-column">
            <div>
              <Label>{t("config-page:name")}</Label>
              <Field
                name="Name"
                component={ValidatedTextBox}
                disabled={!inEdit}
              />
            </div>
            <div>
              <Label>{t("config-page:trend_type")}</Label>
              <Field
                name="TrendDefID"
                component={ValidatedDropDown}
                data={trendDefs}
                textField="Name"
                dataItemKey="ID"
                disabled={!inEdit}
              />
            </div>
            <div>
              <Label>{t("config-page:trend_group")}</Label>
              <Field
                name="TrendGroupID"
                component={ValidatedDropDown}
                data={trendGroups}
                textField="Name"
                dataItemKey="ID"
                disabled={!inEdit}
              />
            </div>
            <div>
              <Label>{t("config-page:unit")}</Label>
              <Field
                name="UnitID"
                component={ValidatedDropDown}
                data={units}
                textField="Name"
                dataItemKey="ID"
                disabled={!inEdit}
              />
            </div>
            <div>
              <Label>{t("config-page:color")}</Label>
              <Field
                name="Color"
                component={ValidatedColor}
                disabled={!inEdit}
              />{" "}
            </div>
            <div>
              <Label>{t("config-page:raw_min")}</Label>
              <Field
                name="RawMin"
                component={ValidatedInput}
                disabled={!inEdit}
              />
            </div>

            <div>
              <Label>{t("config-page:raw_max")}</Label>
              <Field
                name="RawMax"
                component={ValidatedInput}
                disabled={!inEdit}
              />
            </div>
            <div>
              <Label>{t("config-page:scaled_min")}</Label>
              <Field
                name="ScaledMin"
                component={ValidatedInput}
                disabled={!inEdit}
              />
            </div>
            <div>
              <Label>{t("config-page:scaled_max")}</Label>
              <Field
                name="ScaledMax"
                component={ValidatedInput}
                disabled={!inEdit}
              />
            </div>
          </div>
          <div className="separator" />
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
                    onClick={() => requestDelete(selected)}
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
