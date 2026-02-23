import { memo, useEffect, useState } from "react";
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
import { useTranslation } from "react-i18next";
import { Unit } from "../../../../../../services/api";

export interface TrendUnitConfigurationDetailPanelProps {
  editUnit: (value: Unit) => Promise<void>;
  addUnit: (value: Unit) => Promise<void>;
  requestDelete: (value: Unit) => void;
  selected: Unit | null;
  addMode: boolean;
  setAddMode: (v: boolean) => void;
  symbols: string[];
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
const validator = (values: any) => {
  const errors: any = {};

  if (!values.Name?.trim()) {
    errors.Name = "Required";
  }

  if (!values.Symbol?.trim()) {
    errors.Symbol = "Required";
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
  }: TrendUnitConfigurationDetailPanelProps) {
    const { t } = useTranslation(["common", "config-page"]);
    const [inEdit, setInEdit] = useState(false);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
      setInEdit(addMode);
    }, [selected, addMode]);

    const initialValues =
      addMode || !selected
        ? {
            Name: "",
            Symbol: "",
            Multiplier: "",
          }
        : {
            Name: selected.Name ?? "",
            Symbol: selected.Symbol ?? "",
            Multiplier: selected.Multiplier ?? "",
          };

    const handleSubmit = async (values: any) => {
      const payload: Unit = {
        ID: addMode ? "0" : selected!.ID,
        Name: values.Name,
        Symbol: values.Symbol?.Symbol ?? "",
        Multiplier: values.Multiplier,
      };

      try {
        setLoading(true);

        if (addMode) {
          await addUnit(payload);
          setAddMode(false);
          return;
        }

        await editUnit(payload);
        setInEdit(false);
      } finally {
        setLoading(false);
      }
    };

    console.log("Units:", symbols);

    return (
      <Form
        key={addMode ? "add" : selected?.ID}
        initialValues={initialValues}
        validator={validator}
        onSubmit={handleSubmit}
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
