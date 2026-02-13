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
import PipelineParamsDetailPanel from "./components/PipelineParams/PipelineParamsDetailPanel";
import { DetailPanel } from "onyks_shared_kendo";
import { Typography } from "@progress/kendo-react-common";
import { Dialog, DialogActionsBar } from "@progress/kendo-react-dialogs";
import { Label } from "@progress/kendo-react-labels";
import { TextBox, TextBoxChangeEvent } from "@progress/kendo-react-inputs";
import { Button } from "@progress/kendo-react-buttons";
import {
  DropDownList,
  DropDownListChangeEvent,
} from "@progress/kendo-react-dropdowns";
import { AppContext } from "../../../../contexts/appContext";
import {
  Splitter,
  SplitterOnChangeEvent,
  SplitterPaneProps,
  TabStrip,
  TabStripSelectEventArguments,
  TabStripTab,
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
    pipelineParamDefs,
    addPipelineParams,
    deletePipelineParams,
    updatePipelineParam,
    loadPipelineParamsByPipeline,
    loadPipelineParamDefs,
  } = ldsContext;

  const [selectedPipeline, setSelectedPipeline] =
    React.useState<Pipeline | null>(null);
  const [selectedParam, setSelectedParam] =
    React.useState<PipelineParam | null>(null);
  const [showAddPipelineDialog, setShowAddPipelineDialog] =
    React.useState(false);
  const [showDeleteParamDialog, setShowDeleteParamDialog] =
    React.useState(false);
  const [showAddParamDialog, setShowAddParamDialog] = React.useState(false);
  const [newName, setNewName] = React.useState("");
  const [value, setValue] = React.useState("");
  const [selectedDef, setSelectedDef] = React.useState<PipelineParam | null>(
    null,
  );
  const [verticalPanes, setVerticalPanes] = React.useState<SplitterPaneProps[]>(
    [{ size: "65%" }, {}],
  );

  const [tabSelected, setTabSelected] = React.useState<number>(0);

  const handleParamChange = React.useCallback((e: DropDownListChangeEvent) => {
    setSelectedDef(e.value);
  }, []);

  const handleValueChange = React.useCallback((e: TextBoxChangeEvent) => {
    setValue(String(e.value ?? ""));
  }, []);

  const handleNameChange = React.useCallback((e: TextBoxChangeEvent) => {
    setNewName(String(e.value ?? ""));
  }, []);

  const availableDefs = React.useMemo(() => {
    return pipelineParamDefs?.filter(
      (def) =>
        !pipelineParams.some(
          (p) => p.PipelineParamDefID === def.PipelineParamDefID,
        ),
    );
  }, [pipelineParamDefs, pipelineParams]);

  const confirmAddPipeline = async () => {
    if (!newName.trim()) {
      appContext.showNotification({
        notificationType: { icon: true, style: "error" },
        message: "Pipeline name required",
      });
      return;
    }

    await addPipeline({ Name: newName });
    setNewName("");
    setShowAddPipelineDialog(false);
  };

  const confirmAddParam = async () => {
    if (!selectedPipeline) return;

    if (!selectedDef || !value.trim()) {
      appContext.showNotification({
        notificationType: { icon: true, style: "error" },
        message: "Select parameter and enter value",
      });
      return;
    }

    if (!value || !value.trim()) {
      appContext.showNotification({
        notificationType: { icon: true, style: "error" },
        message: "Parameter value cannot be empty",
      });
      return;
    }

    const param: PipelineParamCreate = {
      PipelineParamDefID: selectedDef?.PipelineParamDefID,
      Value: value,
    };

    await addPipelineParams(param, selectedPipeline.ID);

    setSelectedDef(null);
    setValue("");
    setShowAddParamDialog(false);
  };

  const confirmDeleteParam = async () => {
    if (!selectedParam) return;

    await deletePipelineParams(selectedParam);
    setSelectedParam(null);
    setShowDeleteParamDialog(false);
  };

  const handleDeletePipeline = async (pipeline: Pipeline) => {
    await deletePipeline(pipeline);
    setSelectedPipeline(null);
  };

  const handleVerticalChange = (e: SplitterOnChangeEvent) =>
    setVerticalPanes(e.newState);

  React.useEffect(() => {
    if (selectedPipeline?.ID) {
      loadPipelineParamsByPipeline(selectedPipeline.ID);
    }
  }, [selectedPipeline?.ID]);

  React.useEffect(() => {
    if (!selectedPipeline?.ID) return;

    loadPipelineParamsByPipeline(selectedPipeline.ID);
    loadPipelineParamDefs(selectedPipeline.ID);
  }, [selectedPipeline?.ID]);

  const handleTabSelect = React.useCallback(
    (e: TabStripSelectEventArguments) => {
      setTabSelected(e.selected);
    },
    [],
  );

  return (
    <main className="pipelines-page">
      <Splitter
        className="pipelines-grid-container"
        panes={verticalPanes}
        orientation="vertical"
        onChange={handleVerticalChange}
      >
        <div className="pipelines-grid-container">
          <Pipelines
            pipelines={pipelines}
            selected={selectedPipeline}
            onSelectPipeline={setSelectedPipeline}
            openAddDialog={() => setShowAddPipelineDialog(true)}
          />
        </div>

        <div>
          {selectedPipeline ? (
            <TabStrip
              className="events-stuff-tab"
              selected={tabSelected}
              onSelect={handleTabSelect}
            >
              <TabStripTab title={t("event-page:events_types")}>
                <PipelineParams
                  params={pipelineParams}
                  selected={selectedParam}
                  onSelect={setSelectedParam}
                  pipelineID={selectedPipeline.ID}
                  openDialog={() => setShowAddParamDialog(true)}
                />
              </TabStripTab>
            </TabStrip>
          ) : (
            <Typography.p style={{ padding: "20px" }} fontSize="large">
              {t("pipeline-page:choose_pipeline_first") ||
                "Choose pipeline above to see parameters"}
            </Typography.p>
          )}
        </div>
      </Splitter>

      <DetailPanel flexGrow={1} extandable={false}>
        {selectedParam ? (
          <PipelineParamsDetailPanel
            selected={selectedParam}
            pipelineID={selectedPipeline!.ID}
            updateParam={updatePipelineParam}
            deleteParam={async () => setShowDeleteParamDialog(true)}
            openAddDialog={() => setShowAddParamDialog(true)}
            openDeleteDialog={() => setShowDeleteParamDialog(true)}
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

      {showAddParamDialog && (
        <Dialog
          title="Add pipeline parameter"
          onClose={() => setShowAddParamDialog(false)}
          className="pipeline-dialog"
        >
          <Label>Parameter</Label>
          <DropDownList
            data={availableDefs}
            textField="Name"
            dataItemKey="PipelineParamDefID"
            value={selectedDef}
            onChange={handleParamChange}
          />

          <Label>Value</Label>
          <TextBox value={value} onChange={handleValueChange} />

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

      {showAddPipelineDialog && (
        <Dialog
          title="Add pipeline"
          onClose={() => setShowAddPipelineDialog(false)}
          className="pipeline-dialog"
        >
          <Label>Name</Label>
          <TextBox value={newName} onChange={handleNameChange} />

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
