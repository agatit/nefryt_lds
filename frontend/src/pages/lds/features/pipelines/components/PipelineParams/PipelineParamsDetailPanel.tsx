import { memo, useEffect, useState, useMemo } from "react";
import {
  Form,
  Field,
  FormElement,
  FieldRenderProps,
} from "@progress/kendo-react-form";
import { useTranslation } from "react-i18next";
import { TFunction } from "i18next";
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
  pipelineParams: PipelineParam[];
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
        skipDisabledItems={true}
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

const pipelineParamValidator =
  (t: TFunction) => (values: PipelineParamFormValues) => {
    const errors: ValidationErrors = {};

    if (!values.PipelineParamDefID) {
      errors.PipelineParamDefID = t("pipelines-page:param_id");
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
  pipelineParams,
}: Props) {
  const { t } = useTranslation(["common", "pipelines-page"]);
  const [inEdit, setInEdit] = useState(false);
  const [loading, setLoading] = useState(false);

  const allParamsUsed =
    paramDefs.length > 0 && pipelineParams.length >= paramDefs.length;

  if (addMode && allParamsUsed) {
    return (
      <div className="detail-panel-content">
        <div className="item-column">
          <div className="k-messagebox k-messagebox-warning">
            {t("pipelines-page:no_more_params_for_pipeline")}
          </div>
        </div>
      </div>
    );
  }

  const initialValues = useMemo(() => {
    if (addMode || !selected) {
      return { PipelineParamDefID: null, Value: "" };
    }

    return {
      PipelineParamDefID:
        paramDefs.find(
          (d) => d.PipelineParamDefID === selected.PipelineParamDefID,
        ) ?? null,
      Value: selected.Value ?? "",
    };
  }, [selected?.PipelineParamDefID, addMode]);

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

      await updateParam(pipelineID, selected!.PipelineParamDefID, values.Value);
      setInEdit(false);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (addMode) setInEdit(true);
  }, [addMode]);

  return (
    <Form
      key={addMode ? "add" : selected?.PipelineParamDefID}
      initialValues={initialValues}
      validator={pipelineParamValidator(t)}
      onSubmit={(values) => handleSubmit(values as PipelineParamFormValues)}
      render={(formProps) => (
        <FormElement className="detail-panel-content">
          <div className="item-column">
            {selected && (
              <>
                <div>
                  <Label>{t("pipelines-page:data_type")}</Label>
                  <TextBox value={selected.DataType ?? ""} disabled />
                </div>
                <div>
                  <Label>{t("pipelines-page:param_id")}</Label>
                  <TextBox value={selected.PipelineParamDefID ?? ""} disabled />
                </div>
              </>
            )}

            <div>
              <Label>{t("pipelines-page:param_id")}</Label>

              {paramDefs.length === 0 ? (
                <div className="k-messagebox k-messagebox-warning">
                  {t("pipelines-page:no_param_defs_available")}
                </div>
              ) : (
                <Field
                  name="PipelineParamDefID"
                  component={ValidatedDropDown}
                  data={paramDefs}
                  textField="PipelineParamDefID"
                  dataItemKey="PipelineParamDefID"
                  disabled={!inEdit}
                />
              )}
            </div>
            <div>
              <Label>{t("pipelines-page:value")}</Label>
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
                  type="submit"
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
