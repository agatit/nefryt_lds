import React from "react";
import { Label, Error } from "@progress/kendo-react-labels";
import { useTranslation } from "react-i18next";
import { TextBox } from "@progress/kendo-react-inputs";
import { Button } from "@progress/kendo-react-buttons";
import { Dialog, DialogActionsBar } from "@progress/kendo-react-dialogs";
import {
  pencilIcon,
  cancelIcon,
  trashIcon,
  saveIcon,
  plusIcon,
} from "@progress/kendo-svg-icons";
import {
  Form,
  Field,
  FormElement,
  FieldRenderProps,
} from "@progress/kendo-react-form";
import { Link, LinkCreate, LinkUpdate } from "../../../../../../services/api";

interface Props {
  selected: Link | null;
  editLink: (id: number, value: LinkUpdate) => Promise<void>;
  deleteLink: (value: Link) => Promise<void>;
  addLink: (value: LinkCreate) => Promise<Link>;
  addMode: boolean;
  setAddMode: (v: boolean) => void;
}

const LinksDetailPanel = React.memo(function LinksDetailPanel({
  selected,
  editLink,
  deleteLink,
  addLink,
  addMode,
  setAddMode,
}: Props) {
  const { t } = useTranslation(["common", "link-page"]);
  const [inEdit, setInEdit] = React.useState(false);
  const [showDeleteDialog, setShowDeleteDialog] = React.useState(false);

  const initialValues = addMode
    ? {
        BeginNodeID: "",
        EndNodeID: "",
        Length: "",
      }
    : {
        BeginNodeID: selected?.BeginNodeID?.toString() ?? "",
        EndNodeID: selected?.EndNodeID?.toString() ?? "",
        Length: selected?.Length?.toString() ?? "",
      };

  const linkValidator = (values: any) => {
    const errors: any = {};

    if (values.BeginNodeID && !/^\d+$/.test(values.BeginNodeID)) {
      errors.BeginNodeID = "Begin Node ID must be an integer";
    }

    if (values.EndNodeID && !/^\d+$/.test(values.EndNodeID)) {
      errors.EndNodeID = "End Node ID must be an integer";
    }

    if (values.Length && !/^\d+(\.\d+)?$/.test(values.Length)) {
      errors.Length = "Length must be a valid number";
    }

    if (
      values.BeginNodeID &&
      values.EndNodeID &&
      values.BeginNodeID === values.EndNodeID
    ) {
      errors.EndNodeID = "Begin and End Node cannot be the same";
    }

    return Object.keys(errors).length ? errors : undefined;
  };

  const ValidatedInput = (props: FieldRenderProps) => {
    const { validationMessage, touched, visited, ...others } = props;

    return (
      <div className="field-wrapper">
        <TextBox {...others} />
        {(touched || visited) && validationMessage && (
          <Error>{validationMessage}</Error>
        )}
      </div>
    );
  };

  const handleSubmit = React.useCallback(
    async (values: any) => {
      const payload = {
        BeginNodeID:
          values.BeginNodeID === "" ? null : Number(values.BeginNodeID),
        EndNodeID: values.EndNodeID === "" ? null : Number(values.EndNodeID),
        Length: values.Length === "" ? null : Number(values.Length),
      };

      if (addMode) {
        await addLink(payload);
        setAddMode(false);
        return;
      }

      if (!selected) return;

      await editLink(selected.ID, payload);
      setInEdit(false);
    },
    [addMode, addLink, editLink, selected, setAddMode],
  );

  const confirmDelete = async () => {
    if (!selected) return;

    await deleteLink(selected);
    setShowDeleteDialog(false);
    setInEdit(false);
  };

  React.useEffect(() => {
    setInEdit(addMode);
  }, [selected, addMode]);

  return (
    <Form
      key={addMode ? "add" : (selected?.ID ?? "empty")}
      initialValues={initialValues}
      validator={linkValidator}
      onSubmit={handleSubmit}
      render={(formProps) => (
        <FormElement className="detail-panel-content">
          <div className="item">
            <div className="item-column">
              <div>
                <Label>Begin Node</Label>
                <Field
                  name="BeginNodeID"
                  component={ValidatedInput}
                  disabled={!inEdit}
                />
              </div>

              <div>
                <Label>End Node</Label>
                <Field
                  name="EndNodeID"
                  component={ValidatedInput}
                  disabled={!inEdit}
                />
              </div>

              <div>
                <Label>Length</Label>
                <Field
                  name="Length"
                  component={ValidatedInput}
                  disabled={!inEdit}
                />
              </div>
            </div>
          </div>

          <div className="item-row">
            {!inEdit && !addMode ? (
              <>
                <Button svgIcon={pencilIcon} onClick={() => setInEdit(true)}>
                  {t("common:edit")}
                </Button>

                <Button svgIcon={plusIcon} onClick={() => setAddMode(true)}>
                  {t("link-page:add_new_link")}
                </Button>
              </>
            ) : (
              <>
                <Button
                  svgIcon={cancelIcon}
                  onClick={() => {
                    setAddMode(false);
                    setInEdit(false);
                    formProps.onFormReset();
                  }}
                >
                  {t("common:cancel")}
                </Button>

                {!addMode && (
                  <Button
                    svgIcon={trashIcon}
                    onClick={() => setShowDeleteDialog(true)}
                  >
                    {t("common:delete")}
                  </Button>
                )}

                <Button
                  svgIcon={saveIcon}
                  themeColor="primary"
                  disabled={!formProps.allowSubmit}
                  onClick={formProps.onSubmit}
                >
                  {addMode ? t("common:add") : t("common:save")}
                </Button>
              </>
            )}
          </div>

          {showDeleteDialog && (
            <Dialog
              title={t("common:confirm_deletion")}
              onClose={() => setShowDeleteDialog(false)}
            >
              Delete this link?
              <DialogActionsBar>
                <Button onClick={() => setShowDeleteDialog(false)}>
                  {t("common:cancel")}
                </Button>
                <Button themeColor="primary" onClick={confirmDelete}>
                  {t("common:delete")}
                </Button>
              </DialogActionsBar>
            </Dialog>
          )}
        </FormElement>
      )}
    />
  );
});

export default LinksDetailPanel;
