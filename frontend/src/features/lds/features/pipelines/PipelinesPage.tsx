import React from "react";
import "../../../../styles/features/lds/features/pipelinesPage.scss";
import { useTranslation } from "react-i18next";
import { LDSContext } from "../../contexts/ldsContext";
import { Pipeline } from "../../../../services/api";
import Pipelines from "./components/Pipelines";
import PipelinesDetailPanel from "./components/PipelinesDetailPanel";
import { DetailPanel } from "onyks_shared_kendo";
import { Typography } from "@progress/kendo-react-common";
import { Dialog, DialogActionsBar } from "@progress/kendo-react-dialogs";
import { Label } from "@progress/kendo-react-labels";
import { TextBox, TextBoxChangeEvent } from "@progress/kendo-react-inputs";
import { Button } from "@progress/kendo-react-buttons";
import { AppContext } from "../../../../contexts/appContext";

const PipelinesPage = React.memo(function PipelinesPage() {
  const { t } = useTranslation(["common", "pipeline-page"]);

  const appContext = React.useContext(AppContext);
  if (!appContext) return null;

  const ldsContext = React.useContext(LDSContext);
  if (!ldsContext) return null;

  const { pipelines, addPipeline, deletePipeline, updatePipeline } = ldsContext;

  const [selected, setSelected] = React.useState<Pipeline | null>(null);
  const [showAddDialog, setShowAddDialog] = React.useState(false);
  const [newName, setNewName] = React.useState("");

  const openAddDialog = () => setShowAddDialog(true);

  const handleNameChange = React.useCallback(
    (e: TextBoxChangeEvent) => setNewName(String(e.value ?? "")),
    [],
  );

  const cancelAddPipeline = React.useCallback(() => {
    setShowAddDialog(false);
    setNewName("");
  }, []);

  const confirmAdd = async () => {
    if (!newName.trim()) {
      appContext.showNotification({
        notificationType: { icon: true, style: "error" },
        message: "Pipeline name is required",
      });
      return;
    }

    await addPipeline({ Name: newName });
    cancelAddPipeline();
  };

  const handleDelete = async (pipeline: Pipeline) => {
    await deletePipeline(pipeline);
    setSelected(null);
  };

  return (
    <main className="pipelines-page">
      <div className="pipelines-grid-container">
        <Pipelines
          pipelines={pipelines}
          selected={selected}
          onSelectPipeline={setSelected}
          openAddDialog={openAddDialog}
        />
      </div>

      <DetailPanel
        className={"pipelines-detail-panel" + (selected ? "" : " no-selected")}
        flexGrow={1}
        extandable={false}
      >
        {selected ? (
          <PipelinesDetailPanel
            selected={selected}
            editPipeline={updatePipeline}
            deletePipeline={handleDelete}
            openAddDialog={openAddDialog}
          />
        ) : (
          <Typography.p>
            {t("pipeline-page:select_element_to_edit")}
          </Typography.p>
        )}
      </DetailPanel>

      {showAddDialog && (
        <Dialog
          title="Add new pipeline"
          onClose={cancelAddPipeline}
          className="pipelines-dialog"
        >
          <Label>Name</Label>
          <TextBox value={newName} onChange={handleNameChange} />

          <DialogActionsBar>
            <Button onClick={cancelAddPipeline}>{t("common:cancel")}</Button>

            <Button themeColor="primary" onClick={confirmAdd}>
              {t("common:add")}
            </Button>
          </DialogActionsBar>
        </Dialog>
      )}
    </main>
  );
});

export default PipelinesPage;
