import React from "react";
import { useTranslation } from "react-i18next";
import {
  Form,
  Field,
  FormElement,
  FieldRenderProps,
} from "@progress/kendo-react-form";
import { TextBox } from "@progress/kendo-react-inputs";
import { Label, Error } from "@progress/kendo-react-labels";
import {
  cancelIcon,
  pencilIcon,
  saveIcon,
  trashIcon,
} from "@progress/kendo-svg-icons";
import { Button } from "@progress/kendo-react-buttons";
import { Dialog, DialogActionsBar } from "@progress/kendo-react-dialogs";
import { TrendGroup } from "../../../../../../services/api";

export interface TrendGroupConfigurationDetailPanelProps {
  editTrendGroup: (value: TrendGroup) => Promise<void>;
  deleteTrendGroup: (value: TrendGroup) => Promise<void>;
  addTrendGroup: (value: TrendGroup) => Promise<void>;
  selected: TrendGroup | null;
  addMode: boolean;
  setAddMode: (v: boolean) => void;
  closePanel: () => void;
}

interface TrendGroupFormValues {
  Name: string;
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

const validator = (values: TrendGroupFormValues) => {
  const errors: any = {};

  if (!values.Name?.trim()) {
    errors.Name = "Name required";
  }

  return Object.keys(errors).length ? errors : undefined;
};

const TrendGroupConfigurationDetailPanel = React.memo(
  function TrendGroupConfigurationDetailPanel({
    editTrendGroup,
    deleteTrendGroup,
    addTrendGroup,
    selected,
    addMode,
    closePanel,
    setAddMode,
  }: TrendGroupConfigurationDetailPanelProps) {
    const { t } = useTranslation(["common", "config-page"]);

    const [inEdit, setInEdit] = React.useState(false);
    const [loading, setLoading] = React.useState(false);
    const [showDeleteDialog, setShowDeleteDialog] = React.useState(false);

    React.useEffect(() => {
      setInEdit(addMode);
    }, [selected, addMode]);

    const initialValues: TrendGroupFormValues =
      addMode || !selected ? { Name: "" } : { Name: selected.Name ?? "" };

    const handleSubmit = async (values: TrendGroupFormValues) => {
      try {
        setLoading(true);

        if (addMode) {
          await addTrendGroup({
            ID: 0,
            Name: values.Name,
          });

          setAddMode(false);
          closePanel();
          return;
        }

        if (!selected) return;

        await editTrendGroup({
          ID: selected.ID,
          Name: values.Name,
        });

        setInEdit(false);
      } finally {
        setLoading(false);
      }
    };

    const confirmDelete = async () => {
      if (!selected) return;

      try {
        setLoading(true);
        await deleteTrendGroup(selected);
        setShowDeleteDialog(false);
      } finally {
        setLoading(false);
      }
    };

    return (
      <>
        <Form
          key={addMode ? "add" : selected?.ID}
          initialValues={initialValues}
          validator={validator}
          onSubmit={(values) => handleSubmit(values as TrendGroupFormValues)}
          render={(formProps) => (
            <FormElement className="detail-panel-content">
              <div className="item-column">
                <div>
                  <Label>{t("config-page:name")}</Label>
                  <Field
                    name="Name"
                    component={ValidatedTextBox}
                    disabled={!inEdit && !addMode}
                  />
                </div>
              </div>

              <div className="separator" />

              <div className="item-row">
                {!inEdit && !addMode ? (
                  <>
                    <Button
                      svgIcon={pencilIcon}
                      onClick={() => setInEdit(true)}
                    >
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
                        onClick={() => setShowDeleteDialog(true)}
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

        {showDeleteDialog && (
          <Dialog
            title={t("common:confirm_deletion")}
            onClose={() => setShowDeleteDialog(false)}
          >
            {t("config-page:sure_you_want_delete_trend_group")}

            <DialogActionsBar>
              <Button
                disabled={loading}
                onClick={() => setShowDeleteDialog(false)}
              >
                {t("common:cancel")}
              </Button>

              <Button
                themeColor="primary"
                disabled={loading}
                onClick={confirmDelete}
              >
                {t("common:delete")}
              </Button>
            </DialogActionsBar>
          </Dialog>
        )}
      </>
    );
  },
);

export default TrendGroupConfigurationDetailPanel;
