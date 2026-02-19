import React from "react";
import { Label, Error } from "@progress/kendo-react-labels";
import { useTranslation } from "react-i18next";
import { TFunction } from "i18next";
import { NumericTextBox } from "@progress/kendo-react-inputs";
import { Button } from "@progress/kendo-react-buttons";
import { Dialog, DialogActionsBar } from "@progress/kendo-react-dialogs";
import {
  pencilIcon,
  cancelIcon,
  trashIcon,
  saveIcon,
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

interface LinkFormValues {
  BeginNodeID: number | null;
  EndNodeID: number | null;
  Length: number | null;
}

interface ValidationErrors {
  [key: string]: string;
}
const linkValidator = (t: TFunction) => (values: LinkFormValues) => {
  const errors: ValidationErrors = {};

  if (values.BeginNodeID != null && values.BeginNodeID < 0) {
    errors.BeginNodeID = t("links-page:begin_node_positive");
  }

  if (values.EndNodeID != null && values.EndNodeID < 0) {
    errors.EndNodeID = t("links-page:end_node_positive");
  }

  if (
    values.BeginNodeID != null &&
    values.EndNodeID != null &&
    values.BeginNodeID === values.EndNodeID
  ) {
    errors.EndNodeID = t("links-page:nodes_same_error");
  }

  if (values.Length != null && values.Length < 0) {
    errors.Length = t("links-page:length_positive");
  }

  return Object.keys(errors).length ? errors : undefined;
};

const ValidatedInput = (props: FieldRenderProps) => {
  const {
    validationMessage,
    touched,
    visited,
    valid,
    modified,
    ...inputProps
  } = props;

  return (
    <div className="field-wrapper">
      <NumericTextBox
        {...inputProps}
        validationMessage={validationMessage ?? undefined}
      />

      {(touched || visited) && validationMessage && (
        <Error className="error-container">{validationMessage}</Error>
      )}
    </div>
  );
};

const LinksDetailPanel = React.memo(function LinksDetailPanel({
  selected,
  editLink,
  deleteLink,
  addLink,
  addMode,
  setAddMode,
}: Props) {
  const { t } = useTranslation(["common", "links-page"]);
  const [inEdit, setInEdit] = React.useState(false);
  const [showDeleteDialog, setShowDeleteDialog] = React.useState(false);
  const [loading, setLoading] = React.useState(false);

  const initialValues: LinkFormValues = addMode
    ? {
        BeginNodeID: null,
        EndNodeID: null,
        Length: null,
      }
    : {
        BeginNodeID: selected?.BeginNodeID ?? null,
        EndNodeID: selected?.EndNodeID ?? null,
        Length: selected?.Length != null ? Number(selected.Length) : null,
      };

  const handleSubmit = React.useCallback(
    async (values: LinkFormValues) => {
      const payload = {
        BeginNodeID: values.BeginNodeID,
        EndNodeID: values.EndNodeID,
        Length: values.Length,
      };

      try {
        setLoading(true);

        if (addMode) {
          await addLink(payload as LinkCreate);
          setAddMode(false);
          return;
        }

        if (!selected) return;

        await editLink(selected.ID, payload as LinkUpdate);
        setInEdit(false);
      } finally {
        setLoading(false);
      }
    },
    [addMode, addLink, editLink, selected, setAddMode],
  );

  const confirmDelete = async () => {
    if (!selected) return;

    try {
      setLoading(true);
      await deleteLink(selected);
      setShowDeleteDialog(false);
      setInEdit(false);
    } finally {
      setLoading(false);
    }
  };

  React.useEffect(() => {
    setInEdit(addMode);
  }, [selected, addMode]);

  return (
    <Form
      key={addMode ? "add" : (selected?.ID ?? "empty")}
      initialValues={initialValues}
      validator={linkValidator(t)}
      onSubmit={(values) => handleSubmit(values as LinkFormValues)}
      render={(formProps) => (
        <FormElement className="detail-panel-content">
          <div className="item-column">
            <Label>{t("links-page:begin_node")}</Label>
            <Field
              name="BeginNodeID"
              component={ValidatedInput}
              disabled={!inEdit}
            />

            <Label>{t("links-page:end_node")}</Label>
            <Field
              name="EndNodeID"
              component={ValidatedInput}
              disabled={!inEdit}
            />

            <Label>{t("links-page:length")}</Label>
            <Field
              name="Length"
              component={ValidatedInput}
              disabled={!inEdit}
            />
          </div>

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
                    disabled={loading}
                    onClick={async () => {
                      if (!selected) return;
                      setLoading(true);
                      await deleteLink(selected);
                      setInEdit(false);
                      setLoading(false);
                    }}
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

          {showDeleteDialog && selected && (
            <Dialog
              title={t("common:confirm_deletion")}
              onClose={() => setShowDeleteDialog(false)}
            >
              Delete link?
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
