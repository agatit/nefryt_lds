import { memo, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
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
import {
  Method,
  MethodCreate,
  MethodUpdate,
  MethodDef,
} from "../../../../../../services/api";

interface Props {
  selected: Method | null;
  updateMethod: (id: number, value: MethodUpdate) => Promise<void>;
  requestDelete: () => void;
  addMethod: (value: MethodCreate) => Promise<Method>;
  addMode: boolean;
  setAddMode: (v: boolean) => void;
  pipelines: any[];
  methodDefs: MethodDef[];
}

interface ValidationErrors {
  [key: string]: string;
}

export interface MethodFormValues {
  MethodDefID: MethodDef | null;
  PipelineID: { ID: number; Name: string } | null;
  Name?: string;
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
        skipDisabledItems={true}
        onChange={(e) => props.onChange({ value: e.value })}
      />

      {(touched || modified) && validationMessage && (
        <Error>{validationMessage}</Error>
      )}
    </div>
  );
};

const methodValidator = (values: MethodFormValues) => {
  const errors: ValidationErrors = {};

  if (!values.PipelineID) errors.PipelineID = "Required";
  if (!values.MethodDefID) errors.MethodDefID = "Required";

  return Object.keys(errors).length ? errors : undefined;
};

const MethodsDetailPanel = memo(function MethodsDetailPanel({
  selected,
  updateMethod,
  requestDelete,
  addMethod,
  addMode,
  setAddMode,
  pipelines,
  methodDefs,
}: Props) {
  const { t } = useTranslation(["common"]);
  const [inEdit, setInEdit] = useState(false);
  const [loading, setLoading] = useState(false);

  const initialValues =
    addMode || !selected
      ? { Name: "", PipelineID: null, MethodDefID: null }
      : {
          Name: selected.Name ?? "",
          PipelineID:
            pipelines.find((p) => p.ID === selected.PipelineID) ?? null,
          MethodDefID:
            methodDefs.find((d) => d.ID === selected.MethodDefID) ?? null,
        };

  const handleSubmit = async (values: MethodFormValues) => {
    try {
      setLoading(true);

      const payload: MethodCreate = {
        Name: values.Name,
        PipelineID: values.PipelineID!.ID,
        MethodDefID: values.MethodDefID!.ID,
      };

      if (addMode) {
        await addMethod(payload);
        setAddMode(false);
        return;
      }

      await updateMethod(selected!.ID, payload);
      setInEdit(false);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => setInEdit(addMode), [selected, addMode]);

  return (
    <Form
      initialValues={initialValues}
      validator={methodValidator}
      onSubmit={(values) => handleSubmit(values as MethodFormValues)}
      render={(formProps) => (
        <FormElement className="detail-panel-content">
          <div className="item-column">
            <div>
              <Label>Pipeline</Label>
              <Field
                name="PipelineID"
                component={ValidatedDropDown}
                data={pipelines}
                textField="Name"
                dataItemKey="ID"
                disabled={!inEdit}
              />
            </div>
            <div>
              <Label>Method definition</Label>
              <Field
                name="MethodDefID"
                component={ValidatedDropDown}
                data={methodDefs}
                textField="ID"
                dataItemKey="ID"
                disabled={!inEdit}
              />
            </div>
            <div>
              <Label>Name</Label>
              <Field
                name="Name"
                component={ValidatedTextBox}
                disabled={!inEdit}
              />
            </div>
          </div>
          <div className="separator" />
          <div className="item-row">
            {!inEdit && !addMode ? (
              <Button svgIcon={pencilIcon} onClick={() => setInEdit(true)}>
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
                    onClick={requestDelete}
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
});

export default MethodsDetailPanel;
