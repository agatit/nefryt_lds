import { memo, useEffect, useState, useMemo } from "react";
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
import { useTranslation } from "react-i18next";
import {
  Pipeline,
  PipelineCreate,
  PipelineUpdate,
} from "../../../../../../services/api";

interface Props {
  selected: Pipeline | null;
  editPipeline: (id: number, value: PipelineUpdate) => Promise<void>;
  addPipeline: (value: PipelineCreate) => Promise<Pipeline>;
  addMode: boolean;
  setAddMode: (v: boolean) => void;
  requestDelete: (value: Pipeline) => void;
  closePanel: () => void;
}

interface PipelineFormValues {
  Name: string;
}

interface ValidationErrors {
  [key: string]: string;
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

const pipelineValidator = (values: PipelineFormValues) => {
  const errors: ValidationErrors = {};
  if (!values.Name?.trim()) errors.Name = "Name required";
  return Object.keys(errors).length ? errors : undefined;
};

const PipelinesDetailPanel = memo(function PipelinesDetailPanel({
  selected,
  editPipeline,
  addPipeline,
  addMode,
  setAddMode,
  requestDelete,
  closePanel,
}: Props) {
  const { t } = useTranslation(["common", "pipelines-page"]);
  const [inEdit, setInEdit] = useState(false);
  const [loading, setLoading] = useState(false);

  const initialValues = useMemo(() => {
    if (addMode || !selected) {
      return { Name: "" };
    }

    return { Name: selected.Name ?? "" };
  }, [selected?.ID, addMode]);

  const handleSubmit = async (values: PipelineFormValues) => {
    try {
      setLoading(true);

      if (addMode) {
        await addPipeline({ Name: values.Name });
        setAddMode(false);
        closePanel();
        return;
      }

      if (!selected) return;

      await editPipeline(selected.ID, { Name: values.Name });
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
      key={addMode ? "add" : selected?.ID}
      initialValues={initialValues}
      validator={pipelineValidator}
      onSubmit={(values) => handleSubmit(values as PipelineFormValues)}
      render={(formProps) => (
        <FormElement className="detail-panel-content">
          <div className="item-column">
            <div>
              <Label>{t("pipelines-page:name")}</Label>
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
      )}
    />
  );
});

export default PipelinesDetailPanel;
