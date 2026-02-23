import { useState, useEffect, memo, useCallback } from "react";
import { useTranslation } from "react-i18next";
import {
  Form,
  Field,
  FormElement,
  FieldRenderProps,
} from "@progress/kendo-react-form";
import { Label, Error } from "@progress/kendo-react-labels";
import { TextBox, NumericTextBox } from "@progress/kendo-react-inputs";
import { Button } from "@progress/kendo-react-buttons";
import {
  pencilIcon,
  cancelIcon,
  trashIcon,
  saveIcon,
} from "@progress/kendo-svg-icons";
import { Node, NodeCreate, NodeUpdate } from "../../../../../../services/api";

interface Props {
  selected: Node | null;
  requestDelete: (value: Node) => void;
  addNode: (value: NodeCreate) => Promise<Node>;
  editNode: (id: number, value: NodeUpdate) => Promise<void>;
  addMode: boolean;
  setAddMode: (v: boolean) => void;
}

interface NodesFormValues {
  Type: string;
  Name?: string | null;
  PosX?: number | null;
  PosY?: number | null;
  TrendID?: number | null;
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

const ValidatedNumeric = (props: FieldRenderProps) => {
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

const nodeValidator = (values: NodesFormValues) => {
  const errors: ValidationErrors = {};

  if (!values.Type?.trim()) {
    errors.Type = "Type required";
  } else if (!/^[A-Z]+$/.test(values.Type)) {
    errors.Type = "Uppercase letters only";
  }

  if (values.Name && !/^[A-Z0-9-]+$/.test(values.Name)) {
    errors.Name = "Invalid name";
  }

  return Object.keys(errors).length ? errors : undefined;
};

const NodesDetailPanel = memo(function NodesDetailPanel({
  selected,
  editNode,
  requestDelete,
  addNode,
  addMode,
  setAddMode,
}: Props) {
  const { t } = useTranslation(["common", "nodes-page"]);
  const [inEdit, setInEdit] = useState(false);
  const [loading, setLoading] = useState(false);

  const initialValues: NodesFormValues =
    addMode || !selected
      ? {
          Type: "",
          Name: "",
          PosX: null,
          PosY: null,
          TrendID: null,
        }
      : {
          Type: selected.Type ?? "",
          Name: selected.Name ?? "",
          PosX: selected.EditorParams?.PosX ?? null,
          PosY: selected.EditorParams?.PosY ?? null,
          TrendID: selected.TrendID ?? null,
        };

  const handleSubmit = useCallback(
    async (values: NodesFormValues) => {
      try {
        setLoading(true);

        if (addMode) {
          await addNode({
            Type: values.Type,
            Name: values.Name || null,
            EditorParams: {
              PosX: values.PosX ?? 0,
              PosY: values.PosY ?? 0,
            },
            TrendID: values.TrendID ?? null,
          });

          setAddMode(false);
          return;
        }

        if (!selected) return;

        await editNode(selected.ID!, {
          Type: values.Type,
          Name: values.Name ?? null,
          EditorParams: {
            PosX: values.PosX ?? 0,
            PosY: values.PosY ?? 0,
          },
        });

        setInEdit(false);
      } finally {
        setLoading(false);
      }
    },
    [addMode, addNode, editNode, selected, setAddMode],
  );

  useEffect(() => {
    setInEdit(addMode);
  }, [selected, addMode]);

  return (
    <>
      <Form
        key={addMode ? "add" : selected?.ID}
        initialValues={initialValues}
        validator={nodeValidator}
        onSubmit={(values) => handleSubmit(values as NodesFormValues)}
        render={(formProps) => (
          <FormElement className="detail-panel-content">
            <div className="item-column">
              <div>
                <Label>{t("nodes-page:type")}</Label>
                <Field
                  name="Type"
                  component={ValidatedTextBox}
                  disabled={!inEdit && !addMode}
                />
              </div>
              <div>
                <Label>{t("nodes-page:name")}</Label>
                <Field
                  name="Name"
                  component={ValidatedTextBox}
                  disabled={!inEdit && !addMode}
                />
              </div>
              <div>
                <Label>{t("nodes-page:pos_x")}</Label>
                <Field
                  name="PosX"
                  component={ValidatedNumeric}
                  disabled={!inEdit && !addMode}
                />
              </div>
              <div>
                <Label>{t("nodes-page:pos_y")}</Label>
                <Field
                  name="PosY"
                  component={ValidatedNumeric}
                  disabled={!inEdit && !addMode}
                />
              </div>
            </div>
            <div className="separator" />

            <div className="item-row">
              {!inEdit && !addMode ? (
                <>
                  <Button svgIcon={pencilIcon} onClick={() => setInEdit(true)}>
                    {t("common:edit")}
                  </Button>
                </>
              ) : (
                <>
                  <Button
                    svgIcon={cancelIcon}
                    disabled={loading}
                    onClick={() => {
                      setInEdit(false);
                      setAddMode(false);
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
    </>
  );
});

export default NodesDetailPanel;
