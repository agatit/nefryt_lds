import { useState, useEffect, memo, useMemo, useCallback } from "react";
import { Label, Error } from "@progress/kendo-react-labels";
import { useTranslation } from "react-i18next";
import { TFunction } from "i18next";
import { NumericTextBox } from "@progress/kendo-react-inputs";
import { Button } from "@progress/kendo-react-buttons";
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
  addLink: (value: LinkCreate) => Promise<Link>;
  addMode: boolean;
  setAddMode: (v: boolean) => void;
  requestDelete: (value: Link) => void;
  closePanel: () => void;
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

const LinksDetailPanel = memo(function LinksDetailPanel({
  selected,
  editLink,
  addLink,
  addMode,
  setAddMode,
  requestDelete,
  closePanel,
}: Props) {
  const { t } = useTranslation(["common", "links-page"]);
  const [inEdit, setInEdit] = useState(false);
  const [loading, setLoading] = useState(false);

  const initialValues = useMemo(() => {
    if (addMode || !selected) {
      return {
        BeginNodeID: null,
        EndNodeID: null,
        Length: null,
      };
    }

    return {
      BeginNodeID: selected.BeginNodeID ?? null,
      EndNodeID: selected.EndNodeID ?? null,
      Length: selected.Length != null ? Number(selected.Length) : null,
    };
  }, [selected, addMode]);

  const handleSubmit = useCallback(
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
          closePanel();
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

  useEffect(() => {
    setInEdit(addMode);
  }, [selected, addMode]);

  return (
    <Form
      key={addMode ? "add" : selected?.ID}
      initialValues={initialValues}
      validator={linkValidator(t)}
      onSubmit={(values) => handleSubmit(values as LinkFormValues)}
      render={(formProps) => (
        <FormElement className="detail-panel-content">
          <div className="item-column">
            <div>
              <Label>{t("links-page:begin_node")}</Label>
              <Field
                name="BeginNodeID"
                component={ValidatedInput}
                disabled={!inEdit}
              />
            </div>
            <div>
              <Label>{t("links-page:end_node")}</Label>
              <Field
                name="EndNodeID"
                component={ValidatedInput}
                disabled={!inEdit}
              />
            </div>
            <div>
              <Label>{t("links-page:length")}</Label>
              <Field
                name="Length"
                component={ValidatedInput}
                disabled={!inEdit}
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

export default LinksDetailPanel;
