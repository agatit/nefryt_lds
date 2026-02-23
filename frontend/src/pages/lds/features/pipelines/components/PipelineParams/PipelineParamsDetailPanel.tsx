import { memo, useEffect, useState } from "react";
import {
  Form,
  Field,
  FormElement,
  FieldRenderProps,
} from "@progress/kendo-react-form";
import { DropDownList } from "@progress/kendo-react-dropdowns";
import { TextBox } from "@progress/kendo-react-inputs";
import { Label, Error } from "@progress/kendo-react-labels";
import { Button } from "@progress/kendo-react-buttons";
import {
  cancelIcon,
  saveIcon,
  trashIcon,
  pencilIcon,
} from "@progress/kendo-svg-icons";
import { useTranslation } from "react-i18next";
import { PipelineParam } from "../../../../../../services/api";

interface Props {
  selected: PipelineParam | null;
  pipelineID: number;
  updateParam: (
    pipelineID: number,
    paramID: string,
    value: string,
  ) => Promise<void>;
  addParam: (
    pipelineID: number,
    paramID: string,
    value: string,
  ) => Promise<void>;
  addMode: boolean;
  setAddMode: (v: boolean) => void;
  requestDelete: (value: PipelineParam) => void;
  paramDefs: PipelineParam[];
}

interface ValidationErrors {
  [key: string]: string;
}

interface PipelineParamFormValues {
  PipelineParamDefID: PipelineParam | null;
  Value: string;
}

const ValidatedDropDown = (props: FieldRenderProps) => {
  const { validationMessage, touched, modified, ...rest } = props;

  return (
    <div className="field-wrapper">
      <DropDownList
        {...rest}
        data={props.data}
        textField={props.textField}
        dataItemKey={props.dataItemKey}
        onChange={(e) => props.onChange({ value: e.value })}
      />

      {(touched || modified) && validationMessage && (
        <Error>{validationMessage}</Error>
      )}
    </div>
  );
};

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

const pipelineParamValidator = (values: PipelineParamFormValues) => {
  const errors: ValidationErrors = {};

  if (!values.PipelineParamDefID) {
    errors.PipelineParamDefID = "Parameter definition required";
  }

  if (!values.Value?.trim()) {
    errors.Value = "Value required";
  }

  return Object.keys(errors).length ? errors : undefined;
};

const PipelineParamDetailPanel = memo(function PipelineParamDetailPanel({
  selected,
  pipelineID,
  updateParam,
  addParam,
  addMode,
  setAddMode,
  requestDelete,
  paramDefs,
}: Props) {
  const { t } = useTranslation(["common", "pipelines-page"]);
  const [inEdit, setInEdit] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => setInEdit(addMode), [selected, addMode]);

  const initialValues =
    addMode || !selected
      ? { PipelineParamDefID: "", Value: "" }
      : {
          PipelineParamDefID: selected.PipelineParamDefID,
          Value: selected.Value ?? "",
        };

  const handleSubmit = async (values: PipelineParamFormValues) => {
    try {
      setLoading(true);

      if (addMode) {
        await addParam(
          pipelineID,
          values.PipelineParamDefID?.PipelineParamDefID ?? "",
          values.Value,
        );

        setAddMode(false);
        return;
      }

      await updateParam(
        pipelineID,
        values.PipelineParamDefID?.PipelineParamDefID ?? "",
        values.Value,
      );
      setInEdit(false);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Form
      key={addMode ? "add" : selected?.PipelineParamDefID}
      initialValues={initialValues}
      validator={pipelineParamValidator}
      onSubmit={(values) => handleSubmit(values as PipelineParamFormValues)}
      render={(formProps) => (
        <FormElement className="detail-panel-content">
          {selected && (
            <>
              <Label>{t("pipelines-page:name")}</Label>
              <TextBox value={selected.Name ?? ""} disabled />

              <Label>{t("pipelines-page:data_type")}</Label>
              <TextBox value={selected.DataType ?? ""} disabled />

              <Label>{t("pipelines-page:param_id")}</Label>
              <TextBox value={selected.PipelineParamDefID ?? ""} disabled />
            </>
          )}

          <Label>{t("pipelines-page:name")}</Label>
          <Field
            name="PipelineParamDefID"
            component={ValidatedDropDown}
            data={paramDefs}
            textField="Name"
            dataItemKey="PipelineParamDefID"
          />

          <Label>{t("pipelines-page:value")}</Label>
          <Field name="Value" component={ValidatedTextBox} disabled={!inEdit} />

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
});

export default PipelineParamDetailPanel;
