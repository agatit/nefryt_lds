import { memo, useEffect, useState } from "react";
import {
  Form,
  Field,
  FormElement,
  FieldRenderProps,
} from "@progress/kendo-react-form";
import { TextBox } from "@progress/kendo-react-inputs";
import { Label, Error } from "@progress/kendo-react-labels";
import { Button } from "@progress/kendo-react-buttons";
import {
  cancelIcon,
  saveIcon,
  trashIcon,
  pencilIcon,
} from "@progress/kendo-svg-icons";
import { DropDownList } from "@progress/kendo-react-dropdowns";
import { useTranslation } from "react-i18next";
import {
  MethodParam,
  Method,
  MethodParamDef,
  MethodParamCreate,
} from "../../../../../../services/api";

interface Props {
  selected: MethodParam | null;
  selectedMethod: Method | null;
  updateParam: (
    methodID: number,
    paramDefID: string,
    value: string,
  ) => Promise<void>;
  deleteParam: (methodID: number, paramDefID: string) => Promise<void>;
  addMode: boolean;
  setAddMode: (v: boolean) => void;
  requestDelete: () => void;
  paramDefs: MethodParamDef[];
  methodParams: MethodParam[];
  closePanel: () => void;
  addMethodParam: (methodID: number, value: MethodParamCreate) => Promise<void>;
}

interface ValidationErrors {
  [key: string]: string;
}

interface MethodParamFormValues {
  MethodParamDefID: MethodParamDef | null;
  Value: string;
}

const ValidatedTextBox = (props: FieldRenderProps) => {
  const { validationMessage, touched, modified, ...rest } = props;

  return (
    <div className="field-wrapper">
      <TextBox {...rest} />
      {(touched || modified) && validationMessage && (
        <Error>{validationMessage}</Error>
      )}
    </div>
  );
};

const ValidatedDropDown = (props: FieldRenderProps) => {
  const { validationMessage, touched, modified, data, ...rest } = props;

  return (
    <div className="field-wrapper">
      <DropDownList
        {...rest}
        data={data}
        textField={props.textField}
        dataItemKey={props.dataItemKey}
        value={props.value}
        onChange={(e) => props.onChange({ value: e.value })}
      />

      {(touched || modified) && validationMessage && (
        <Error>{validationMessage}</Error>
      )}
    </div>
  );
};

const methodParamValidator = (values: MethodParamFormValues) => {
  const errors: ValidationErrors = {};

  if (!values.MethodParamDefID) errors.MethodParamDefID = "Required";

  if (!values.Value?.trim()) errors.Value = "Value required";

  return Object.keys(errors).length ? errors : undefined;
};

const MethodParamDetailPanel = memo(function MethodParamDetailPanel({
  selected,
  selectedMethod,
  updateParam,
  addMode,
  setAddMode,
  requestDelete,
  paramDefs,
  addMethodParam,
  methodParams,
  closePanel,
}: Props) {
  const { t } = useTranslation(["common", "methods-page"]);
  const [inEdit, setInEdit] = useState(false);
  const [loading, setLoading] = useState(false);

  if (!selectedMethod && !addMode) {
    return (
      <div className="detail-panel-content">{t("common:no_selection")}</div>
    );
  }

  const initialValues =
    addMode || !selected
      ? { MethodParamDefID: null, Value: "" }
      : {
          MethodParamDefID:
            paramDefs.find((d) => d.ID === selected.MethodParamDefID) ?? null,
          Value: selected.Value ?? "",
        };

  const handleSubmit = async (values: MethodParamFormValues) => {
    try {
      setLoading(true);

      if (!selectedMethod) return;

      if (addMode) {
        await addMethodParam(selectedMethod.ID, {
          MethodParamDefID: values.MethodParamDefID!.ID,
          Value: values.Value,
        });

        setAddMode(false);
        closePanel();
        return;
      }

      await updateParam(
        selectedMethod.ID,
        selected!.MethodParamDefID,
        values.Value,
      );

      setInEdit(false);
    } finally {
      setLoading(false);
    }
  };

  const allParamsUsed =
    paramDefs.length > 0 &&
    paramDefs.every((def: MethodParamDef) =>
      methodParams.some((p: MethodParam) => p.MethodParamDefID === def.ID),
    );

  useEffect(() => {
    if (addMode) {
      setInEdit(true);
    }
  }, [addMode]);

  if (addMode && allParamsUsed) {
    return (
      <div className="detail-panel-content">
        <div className="item-column">
          <div className="k-messagebox k-messagebox-warning">
            {t("pipelines-page:no_more_params_for_method")}
          </div>
        </div>
      </div>
    );
  }

  return (
    <Form
      key={addMode ? "add" : selected?.MethodParamDefID}
      initialValues={initialValues}
      validator={methodParamValidator}
      onSubmit={(values) => handleSubmit(values as MethodParamFormValues)}
      render={(formProps) => (
        <FormElement className="detail-panel-content">
          <div className="item-column">
            {!addMode && selected && (
              <>
                <div>
                  <Label>{t("methods-page:name")}</Label>
                  <TextBox value={selected.Name ?? ""} disabled />
                </div>
                <div>
                  <Label>{t("methods-page:data_type")}</Label>
                  <TextBox value={selected.DataType ?? ""} disabled />
                </div>
              </>
            )}
            <div>
              <Label>{t("methods-page:param_id")}</Label>
              <Field
                name="MethodParamDefID"
                component={ValidatedDropDown}
                data={paramDefs}
                textField="Name"
                dataItemKey="ID"
                disabled={!inEdit || !addMode}
              />
            </div>
            <div>
              <Label>{t("methods-page:value")}</Label>
              <Field
                name="Value"
                component={ValidatedTextBox}
                disabled={!inEdit}
              />
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
                    onClick={() => requestDelete}
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
      )}
    />
  );
});

export default MethodParamDetailPanel;
