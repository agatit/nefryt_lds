import { useState, useEffect, memo, useMemo, useCallback } from "react";
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
  closePanel: () => void;
}

interface NodesFormValues {
  Type: string;
  Name?: string | null;
  PosX?: number | null;
  PosY?: number | null;
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

const ValidatedNumeric = (props: FieldRenderProps) => {
  const { validationMessage, touched, modified, ...rest } = props;
  return (
    <div className="field-wrapper">
      <NumericTextBox {...rest} />
      {(touched || modified) && validationMessage && (
        <Error>{validationMessage}</Error>
      )}
    </div>
  );
};

const NodesDetailPanel = memo(function NodesDetailPanel({
  selected,
  editNode,
  requestDelete,
  addNode,
  addMode,
  setAddMode,
  closePanel,
}: Props) {
  const { t } = useTranslation(["common", "nodes-page"]);
  const [inEdit, setInEdit] = useState(false);
  const [loading, setLoading] = useState(false);

  const initialValues = useMemo(() => {
    if (addMode || !selected) {
      return {
        Type: "",
        Name: "",
        PosX: null,
        PosY: null,
      };
    }

    return {
      Type: selected.Type ?? "",
      Name: selected.Name ?? "",
      PosX: selected.EditorParams?.PosX ?? null,
      PosY: selected.EditorParams?.PosY ?? null,
    };
  }, [selected?.ID, addMode]);

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
          });

          setAddMode(false);
          closePanel();
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
    [addMode, addNode, editNode, selected, setAddMode, closePanel],
  );

  useEffect(() => setInEdit(addMode), [selected, addMode]);

  return (
    <Form
      key={addMode ? "add" : selected?.ID}
      initialValues={initialValues}
      onSubmit={(values) => handleSubmit(values as NodesFormValues)}
      render={(formProps) => (
        <FormElement className="detail-panel-content">
          <div className="item-column">
            <div>
              <Label>{t("nodes-page:type")}</Label>
              <Field
                name="Type"
                component={ValidatedTextBox}
                disabled={!inEdit}
              />
            </div>
            <div>
              <Label>{t("nodes-page:name")}</Label>
              <Field
                name="Name"
                component={ValidatedTextBox}
                disabled={!inEdit}
              />{" "}
            </div>
            <div>
              <Label>{t("nodes-page:pos_x")}</Label>
              <Field
                name="PosX"
                component={ValidatedNumeric}
                disabled={!inEdit}
              />{" "}
            </div>
            <div>
              <Label>{t("nodes-page:pos_y")}</Label>
              <Field
                name="PosY"
                component={ValidatedNumeric}
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
      )}
    />
  );
});

export default NodesDetailPanel;
