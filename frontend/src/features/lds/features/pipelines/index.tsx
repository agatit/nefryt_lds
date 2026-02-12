import React from "react";
import "./pipelinesPage.scss";
import { useTranslation } from "react-i18next";
import { LDSContext } from "../../contexts/ldsContext";
import {
  Pipeline,
  PipelineParam,
  PipelineParamCreate,
} from "../../../../services/api";
import Pipelines from "./components/Pipelines/Pipelines";
import PipelinesDetailPanel from "./components/Pipelines/PipelinesDetailPanel";
import PipelineParams from "./components/PipelineParams/PipelineParams";
import PipelinesParamDetailPanel from "./components/PipelineParams/PipelineParamsDetailPanel";
import { DetailPanel } from "onyks_shared_kendo";
import { Typography } from "@progress/kendo-react-common";
import { Dialog, DialogActionsBar } from "@progress/kendo-react-dialogs";
import { Label } from "@progress/kendo-react-labels";
import { TextBox, TextBoxChangeEvent } from "@progress/kendo-react-inputs";
import { Button } from "@progress/kendo-react-buttons";
import { AppContext } from "../../../../contexts/appContext";
import {
  Splitter,
  SplitterPaneProps,
  SplitterOnChangeEvent,
} from "@progress/kendo-react-layout";

const PipelinesPage = React.memo(function PipelinesPage() {
  const { t } = useTranslation(["common", "pipeline-page"]);

  const appContext = React.useContext(AppContext);
  const ldsContext = React.useContext(LDSContext);
  if (!appContext || !ldsContext) return null;

  const {
    pipelines,
    addPipeline,
    updatePipeline,
    deletePipeline,
    pipelineParams,
    addPipelineParams,
    deletePipelineParams,
    loadPipelineParamsByPipeline,
  } = ldsContext;

  const [selectedPipeline, setSelectedPipeline] =
    React.useState<Pipeline | null>(null);

  const [selectedParam, setSelectedParam] =
    React.useState<PipelineParam | null>(null);

  const [showAddPipelineDialog, setShowAddPipelineDialog] =
    React.useState(false);

  const [showAddParamDialog, setShowAddParamDialog] = React.useState(false);

  const [showDeleteParamDialog, setShowDeleteParamDialog] =
    React.useState(false);

  const [newName, setNewName] = React.useState("");
  const [pipelineParamDefID, setPipelineParamDefID] = React.useState("");
  const [value, setValue] = React.useState("");

  const [verticalPanes, setVerticalPanes] = React.useState<SplitterPaneProps[]>(
    [{ size: "65%" }, {}],
  );

  const handleVerticalChange = React.useCallback((e: SplitterOnChangeEvent) => {
    setVerticalPanes(e.newState);
  }, []);

  const confirmAddPipeline = async () => {
    if (!newName.trim()) {
      appContext.showNotification({
        notificationType: { icon: true, style: "error" },
        message: "Pipeline name is required",
      });
      return;
    }

    await addPipeline({ Name: newName });
    setNewName("");
    setShowAddPipelineDialog(false);
  };

  const handleDeletePipeline = async (pipeline: Pipeline) => {
    await deletePipeline(pipeline);
    setSelectedPipeline(null);
  };

  const confirmAddParam = async () => {
    if (!selectedPipeline) return;

    if (!pipelineParamDefID.trim() || !value.trim()) {
      appContext.showNotification({
        notificationType: { icon: true, style: "error" },
        message: "Param ID and value required",
      });
      return;
    }

    const param: PipelineParamCreate = {
      PipelineParamDefID: pipelineParamDefID,
      Value: value,
    };

    await addPipelineParams(param, selectedPipeline.ID);

    setPipelineParamDefID("");
    setValue("");
    setShowAddParamDialog(false);
  };

  const confirmDeleteParam = async () => {
    if (!selectedParam) return;

    await deletePipelineParams(selectedParam);
    setSelectedParam(null);
    setShowDeleteParamDialog(false);
  };

  React.useEffect(() => {
    if (!selectedPipeline?.ID) return;
    loadPipelineParamsByPipeline(selectedPipeline.ID);
  }, [selectedPipeline?.ID]);

  return (
    <main className="pipelines-page">
      <Splitter
        className="pipelines-grid-container"
        panes={verticalPanes}
        orientation="vertical"
        onChange={handleVerticalChange}
      >
        <div>
          <Pipelines
            pipelines={pipelines}
            selected={selectedPipeline}
            onSelectPipeline={setSelectedPipeline}
            openAddDialog={() => setShowAddPipelineDialog(true)}
          />
        </div>

        <div>
          {selectedPipeline && (
            <PipelineParams
              params={pipelineParams}
              selected={selectedParam}
              onSelect={setSelectedParam}
              openDialog={() => setShowAddParamDialog(true)}
              closeDialog={() => setShowAddParamDialog(false)}
              showDialog={showAddParamDialog}
              addPipelineParam={confirmAddParam}
              pipelineID={selectedPipeline.ID}
            />
          )}
        </div>
      </Splitter>

      <DetailPanel
        className={
          "pipelines-detail-panel" +
          (!selectedPipeline && !selectedParam ? " no-selected" : "")
        }
        flexGrow={1}
        extandable={false}
      >
        {selectedParam ? (
          <PipelinesParamDetailPanel
            selected={selectedParam}
            deleteParam={async () => setShowDeleteParamDialog(true)}
          />
        ) : selectedPipeline ? (
          <PipelinesDetailPanel
            selected={selectedPipeline}
            editPipeline={updatePipeline}
            deletePipeline={handleDeletePipeline}
            openAddDialog={() => setShowAddPipelineDialog(true)}
          />
        ) : (
          <Typography.p>
            {t("pipeline-page:select_element_to_edit")}
          </Typography.p>
        )}
      </DetailPanel>

      {showAddPipelineDialog && (
        <Dialog
          title="Add pipeline"
          onClose={() => setShowAddPipelineDialog(false)}
        >
          <Label>Name</Label>
          <TextBox
            value={newName}
            onChange={(e: TextBoxChangeEvent) =>
              setNewName(String(e.value ?? ""))
            }
          />

          <DialogActionsBar>
            <Button onClick={() => setShowAddPipelineDialog(false)}>
              {t("common:cancel")}
            </Button>
            <Button themeColor="primary" onClick={confirmAddPipeline}>
              {t("common:add")}
            </Button>
          </DialogActionsBar>
        </Dialog>
      )}

      {showAddParamDialog && (
        <Dialog
          title="Add pipeline parameter"
          onClose={() => setShowAddParamDialog(false)}
        >
          <Label>Param ID</Label>
          <TextBox
            value={pipelineParamDefID}
            onChange={(e: TextBoxChangeEvent) =>
              setPipelineParamDefID(String(e.value ?? "").toUpperCase())
            }
          />

          <Label>Value</Label>
          <TextBox
            value={value}
            onChange={(e: TextBoxChangeEvent) =>
              setValue(String(e.value ?? ""))
            }
          />

          <DialogActionsBar>
            <Button onClick={() => setShowAddParamDialog(false)}>
              {t("common:cancel")}
            </Button>
            <Button themeColor="primary" onClick={confirmAddParam}>
              {t("common:add")}
            </Button>
          </DialogActionsBar>
        </Dialog>
      )}

      {showDeleteParamDialog && (
        <Dialog
          title={t("common:confirm_deletion")}
          onClose={() => setShowDeleteParamDialog(false)}
        >
          Delete pipeline parameter?
          <DialogActionsBar>
            <Button onClick={() => setShowDeleteParamDialog(false)}>
              {t("common:cancel")}
            </Button>
            <Button themeColor="primary" onClick={confirmDeleteParam}>
              {t("common:delete")}
            </Button>
          </DialogActionsBar>
        </Dialog>
      )}
    </main>
  );
});

export default PipelinesPage;
