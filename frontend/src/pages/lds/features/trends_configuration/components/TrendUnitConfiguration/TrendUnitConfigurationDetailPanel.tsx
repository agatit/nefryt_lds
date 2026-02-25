import { memo, useEffect, useMemo, useState } from "react";
import { useTranslation } from "react-i18next";
import { TFunction } from "i18next";
import {
  Form,
  Field,
  FormElement,
  FieldRenderProps,
} from "@progress/kendo-react-form";
import { TextBox } from "@progress/kendo-react-inputs";
import { DropDownList } from "@progress/kendo-react-dropdowns";
import { Label, Error } from "@progress/kendo-react-labels";
import { Button } from "@progress/kendo-react-buttons";
import {
  cancelIcon,
  pencilIcon,
  saveIcon,
  trashIcon,
} from "@progress/kendo-svg-icons";
import { Unit } from "../../../../../../services/api";

export interface TrendUnitConfigurationDetailPanelProps {
  editUnit: (value: Unit) => Promise<void>;
  addUnit: (value: Unit) => Promise<void>;
  requestDelete: (value: Unit) => void;
  selected: Unit | null;
  addMode: boolean;
  setAddMode: (v: boolean) => void;
  symbols: string[];
  closePanel: () => void;
}

interface UnitFormValues {
  Name: string;
  Symbol: string | null;
  Multiplier: string | number;
}

interface ValidationErrors {
  [key: string]: string;
}

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

const ValidatedDropDown = (props: FieldRenderProps & { data: string[] }) => {
  const { validationMessage, touched, modified, value, onChange, data } = props;

  return (
    <div className="field-wrapper">
      <DropDownList
        data={data}
        value={value ?? ""}
        onChange={(e) => onChange({ value: e.value ?? "" })}
      />

      {(touched || modified) && validationMessage && (
        <Error>{validationMessage}</Error>
      )}
    </div>
  );
};
const validator = (t: TFunction) => (values: UnitFormValues) => {
  const errors: ValidationErrors = {};

  if (!values.Name?.trim()) {
    errors.Name = t("config-page:name_required");
  }

  if (!values.Symbol?.trim()) {
    errors.Symbol = t("config-page:symbol_required");
  }

  return Object.keys(errors).length ? errors : undefined;
};
const TrendUnitConfigurationDetailPanel = memo(
  function TrendUnitConfigurationDetailPanel({
    editUnit,
    addUnit,
    requestDelete,
    selected,
    addMode,
    setAddMode,
    symbols,
    closePanel,
  }: TrendUnitConfigurationDetailPanelProps) {
    const { t } = useTranslation(["common", "config-page"]);
    const [inEdit, setInEdit] = useState(false);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
      setInEdit(addMode);
    }, [selected, addMode]);

    const initialValues = useMemo(() => {
      if (addMode || !selected) {
        return {
          Name: "",
          Symbol: "",
          Multiplier: "",
        };
      }

      return {
        Name: selected.Name ?? "",
        Symbol: selected.Symbol ?? "",
        Multiplier: selected.Multiplier ?? "",
      };
    }, [addMode, selected]);

    const handleSubmit = async (values: UnitFormValues) => {
      const payload: Unit = {
        ID: addMode ? "0" : selected!.ID,
        Name: values.Name,
        Symbol: values.Symbol ?? "",
        Multiplier: String(values.Multiplier ?? ""),
      };

      try {
        setLoading(true);

        if (addMode) {
          await addUnit(payload);
          setAddMode(false);
          closePanel();
          return;
        }

        await editUnit(payload);
        setInEdit(false);
      } finally {
        setLoading(false);
      }
    };

    return (
      <Form
        key={addMode ? "add" : selected?.ID}
        initialValues={initialValues}
        validator={validator(t)}
        onSubmit={(values) => handleSubmit(values as UnitFormValues)}
        render={(formProps) => (
          <FormElement className="detail-panel-content">
            <div className="item-column">
              <div>
                <Label>{t("config-page:name")}</Label>
                <Field
                  name="Name"
                  component={ValidatedTextBox}
                  disabled={!inEdit && !addMode}
                />
              </div>

              <div>
                <Label>{t("config-page:symbol")}</Label>
                <Field
                  name="Symbol"
                  component={ValidatedDropDown}
                  data={symbols}
                  disabled={!inEdit && !addMode}
                />
              </div>

              <div>
                <Label>{t("config-page:multiplier")}</Label>
                <Field
                  name="Multiplier"
                  component={ValidatedTextBox}
                  disabled={!inEdit && !addMode}
                />
              </div>
            </div>

            <div className="separator" />

            <div className="item-row">
              {!inEdit && !addMode ? (
                <Button
                  svgIcon={pencilIcon}
                  disabled={loading}
                  onClick={() => setInEdit(true)}
                >
                  {t("common:edit")}
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
                    {t("common:cancel")}
                  </Button>

                  {!addMode && selected && (
                    <Button
                      svgIcon={trashIcon}
                      disabled={loading}
                      onClick={() => requestDelete(selected)}
                    >
                      {t("common:delete")}
                    </Button>
                  )}

                  <Button
                    svgIcon={saveIcon}
                    themeColor="primary"
                    disabled={!formProps.allowSubmit || loading}
                    onClick={formProps.onSubmit}
                  >
                    {addMode ? t("common:add") : t("common:save")}
                  </Button>
                </>
              )}
            </div>
          </FormElement>
        )}
      />
    );
  },
);

export default TrendUnitConfigurationDetailPanel;
