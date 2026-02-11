import React from "react";
import { Label } from "@progress/kendo-react-labels";
import { useTranslation } from "react-i18next";
import { TextBox, TextBoxChangeEvent } from "@progress/kendo-react-inputs";
import { Button } from "@progress/kendo-react-buttons";
import { Dialog, DialogActionsBar } from "@progress/kendo-react-dialogs";
import {
  pencilIcon,
  cancelIcon,
  trashIcon,
  saveIcon,
  plusIcon,
} from "@progress/kendo-svg-icons";
import { Pipeline, PipelineUpdate } from "../../../../../services/api";

interface Props {
  selected: Pipeline;
  editPipeline: (id: number, value: PipelineUpdate) => Promise<void>;
  deletePipeline: (value: Pipeline) => Promise<void>;
  openAddDialog: () => void;
}

const PipelinesDetailPanel = React.memo(function PipelinesDetailPanel({
  selected,
  editPipeline,
  deletePipeline,
  openAddDialog,
}: Props) {
  const { t } = useTranslation(["common", "pipeline-page"]);
  const [inEdit, setInEdit] = React.useState(false);
  const [showDeleteDialog, setShowDeleteDialog] = React.useState(false);
  const [name, setName] = React.useState("");

  const handleNameChange = React.useCallback((e: TextBoxChangeEvent) => {
    setName(String(e.value ?? ""));
  }, []);

  const saveEdit = async () => {
    await editPipeline(selected.ID, {
      Name: name || null,
    });
    setInEdit(false);
  };

  const confirmDelete = async () => {
    if (!selected) return;

    await deletePipeline(selected);
    setShowDeleteDialog(false);
    setInEdit(false);
  };

  const cancelEdit = () => {
    setName(selected.Name ?? "");
    setInEdit(false);
  };

  React.useEffect(() => {
    setName(selected.Name ?? "");
    setInEdit(false);
  }, [selected]);

  return (
    <div className="detail-panel-content">
      <div className="item-column">
        <Label>ID</Label>
        <TextBox value={selected.ID.toString()} disabled />

        <Label>Name</Label>
        <TextBox value={name} disabled={!inEdit} onChange={handleNameChange} />
      </div>

      <div className="item-row">
        {!inEdit ? (
          <>
            <Button svgIcon={pencilIcon} onClick={() => setInEdit(true)}>
              {t("common:edit")}
            </Button>

            <Button svgIcon={plusIcon} onClick={openAddDialog}>
              {t("pipeline-page:add_new_pipeline")}
            </Button>
          </>
        ) : (
          <>
            <Button svgIcon={cancelIcon} onClick={cancelEdit}>
              {t("common:cancel")}
            </Button>

            <Button svgIcon={saveIcon} themeColor="primary" onClick={saveEdit}>
              {t("common:save")}
            </Button>

            <Button
              svgIcon={trashIcon}
              onClick={() => setShowDeleteDialog(true)}
            >
              {t("common:delete")}
            </Button>
          </>
        )}
      </div>

      {showDeleteDialog && (
        <Dialog
          title="Confirm deletion"
          onClose={() => setShowDeleteDialog(false)}
        >
          Delete this pipeline?
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
    </div>
  );
});

export default PipelinesDetailPanel;
