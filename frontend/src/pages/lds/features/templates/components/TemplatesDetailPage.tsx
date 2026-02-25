import { memo, useEffect, useMemo, useState, useContext } from "react";
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
  plusIcon,
} from "@progress/kendo-svg-icons";
import {
  Template,
  TemplateCreate,
  TemplateUpdate,
  Axis,
  Unit,
} from "../../../../../services/api";
import { LDSContext } from "../../../contexts/ldsContext";

interface Props {
  selected: Template | null;
  updateTemplate: (id: number, value: TemplateUpdate) => Promise<void>;
  addTemplate: (value: TemplateCreate) => Promise<void>;
  requestDelete: (value: Template) => void;
  addMode: boolean;
  setAddMode: (v: boolean) => void;
  closePanel: () => void;
}

interface AxisForm {
  Title: string;
  UnitID: Unit | null;
  ScaledMin: number | string;
  ScaledMax: number | string;
}

interface TemplateFormValues {
  Name: string;
  Axes: AxisForm[];
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

const ValidatedDropDown = (props: FieldRenderProps) => {
  const { validationMessage, touched, modified, data, ...inputProps } = props;

  return (
    <div className="field-wrapper">
      <DropDownList
        {...inputProps}
        data={data}
        onChange={(e) => props.onChange({ value: e.value })}
      />
      {(touched || modified) && validationMessage && (
        <Error>{validationMessage}</Error>
      )}
    </div>
  );
};

const templateValidator =
  (t: TFunction) =>
  (values: TemplateFormValues): ValidationErrors | undefined => {
    const errors: ValidationErrors = {};

    if (!values.Name?.trim()) {
      errors.Name = t("templates-page:name_required");
    }

    if (!values.Axes?.length) {
      errors.Axes = t("templates-page:axis_required");
    }

    if (values.Axes?.some((a) => !a.Title || !a.UnitID)) {
      errors.Axes = t("templates-page:axis_invalid");
    }

    return Object.keys(errors).length ? errors : undefined;
  };

const TemplatesDetailPanel = memo(function TemplatesDetailPanel({
  selected,
  updateTemplate,
  addTemplate,
  requestDelete,
  addMode,
  setAddMode,
  closePanel,
}: Props) {
  const { t } = useTranslation(["common", "templates-page"]);
  const [inEdit, setInEdit] = useState(false);
  const [loading, setLoading] = useState(false);
  const ldsContext = useContext(LDSContext);

  if (!ldsContext) return null;

  const { units } = ldsContext;

  const initialValues = useMemo(() => {
    if (addMode || !selected) {
      return { Name: "", Axes: [] };
    }

    return {
      Name: selected.Name ?? "",
      Axes:
        selected.Axes?.map((a) => ({
          Title: a.Title ?? "",
          UnitID: units.find((u) => u.ID === a.UnitID) ?? null,
          ScaledMin: a.ScaledMin ?? 0,
          ScaledMax: a.ScaledMax ?? 0,
        })) ?? [],
    };
  }, [selected, addMode, units]);

  const handleSubmit = async (values: TemplateFormValues) => {
    try {
      setLoading(true);

      const payload = {
        Name: values.Name,
        Axes: values.Axes.map((a) => ({
          Title: a.Title,
          UnitID: a.UnitID?.ID ?? "",
          ScaledMin: Number(a.ScaledMin),
          ScaledMax: Number(a.ScaledMax),
        })),
      };

      if (addMode) {
        await addTemplate(payload);
        setAddMode(false);
        closePanel();
        return;
      }

      if (!selected) return;

      await updateTemplate(selected.ID, payload);
      setInEdit(false);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (addMode) {
      setInEdit(true);
    }
  }, [addMode]);

  return (
    <Form
      key={addMode ? "add-template" : selected?.ID}
      initialValues={initialValues}
      validator={templateValidator(t)}
      onSubmit={(v) => handleSubmit(v as TemplateFormValues)}
      render={(formProps) => {
        const axes: Axis[] = formProps.valueGetter("Axes") || [];

        const addAxis = () => {
          formProps.onChange("Axes", {
            value: [
              ...axes,
              {
                TrendsID: [],
                Title: "",
                UnitID: "",
                ScaledMin: 0,
                ScaledMax: 0,
              },
            ],
          });
        };

        return (
          <FormElement className="detail-panel-content">
            <div className="item-column">
              <div>
                <Label>{t("templates-page:name")}</Label>
                <Field
                  name="Name"
                  component={ValidatedTextBox}
                  disabled={!inEdit}
                />
              </div>
              <div>
                <Label>{t("templates-page:axes")}</Label>
                {axes.map((_, i) => (
                  <div key={i} className="axis-card">
                    <div>
                      <Label>{t("templates-page:title")}</Label>
                      <Field
                        name={`Axes[${i}].Title`}
                        component={ValidatedTextBox}
                        disabled={!inEdit}
                      />
                    </div>
                    <div>
                      <Label>{t("templates-page:unit")}</Label>
                      <Field
                        name={`Axes[${i}].UnitID`}
                        component={ValidatedDropDown}
                        data={units}
                        textField="Symbol"
                        dataItemKey="ID"
                      />
                    </div>
                    <div>
                      <Label>{t("templates-page:min")}</Label>
                      <Field
                        name={`Axes[${i}].ScaledMin`}
                        component={ValidatedTextBox}
                        disabled={!inEdit}
                      />
                    </div>
                    <div>
                      <Label>{t("templates-page:max")}</Label>
                      <Field
                        name={`Axes[${i}].ScaledMax`}
                        component={ValidatedTextBox}
                        disabled={!inEdit}
                      />
                    </div>
                  </div>
                ))}

                {(inEdit || addMode) && (
                  <Button
                    type="button"
                    svgIcon={plusIcon}
                    onClick={addAxis}
                    style={{ marginTop: 12 }}
                  >
                    {t("templates-page:add_axes")}
                  </Button>
                )}
              </div>
            </div>
            <div className="separator" />
            <div className="item-row">
              {!inEdit && !addMode ? (
                <Button
                  type="button"
                  svgIcon={pencilIcon}
                  onClick={() => setInEdit(true)}
                >
                  {t("common:edit")}
                </Button>
              ) : (
                <>
                  <Button
                    type="button"
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
                      type="button"
                      svgIcon={trashIcon}
                      disabled={loading}
                      onClick={() => requestDelete(selected)}
                    >
                      {t("common:delete")}
                    </Button>
                  )}

                  <Button
                    type="submit"
                    svgIcon={saveIcon}
                    themeColor="primary"
                    disabled={!formProps.allowSubmit || loading}
                  >
                    {addMode ? t("common:add") : t("common:save")}
                  </Button>
                </>
              )}
            </div>
          </FormElement>
        );
      }}
    />
  );
});

export default TemplatesDetailPanel;
