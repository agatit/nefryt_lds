import React, { useContext, useEffect, useState, useCallback } from "react";
import "./pipelinesPage.scss";
import { useTranslation } from "react-i18next";
import { LDSContext } from "../../contexts/ldsContext";
import { Pipeline, PipelineParam } from "../../../../services/api";
import Pipelines from "./components/Pipelines/Pipelines";
import PipelinesDetailPanel from "./components/Pipelines/PipelinesDetailPanel";
import PipelineParams from "./components/PipelineParams/PipelineParams";
import PipelineParamDetailPanel from "./components/PipelineParams/PipelineParamsDetailPanel";
import { DetailPanel } from "onyks_shared_kendo";
import { Dialog, DialogActionsBar } from "@progress/kendo-react-dialogs";
import { Button } from "@progress/kendo-react-buttons";
import {
  Splitter,
  SplitterOnChangeEvent,
  SplitterPaneProps,
  TabStrip,
  TabStripSelectEventArguments,
  TabStripTab,
} from "@progress/kendo-react-layout";

const PipelinesPage = React.memo(function PipelinesPage() {
  const { t } = useTranslation(["common", "pipelines-page"]);
  const ldsContext = useContext(LDSContext);
  if (!ldsContext) return null;

  const {
    pipelines,
    addPipeline,
    updatePipeline,
    deletePipeline,
    pipelineParams,
    updatePipelineParam,
    addPipelineParams,
    deletePipelineParams,
    loadPipelineParamsByPipeline,
    loadPipelineParamDefs,
    pipelineParamDefs,
  } = ldsContext;

  const [selectedPipeline, setSelectedPipeline] = useState<Pipeline | null>(
    null,
  );
  const [selectedParam, setSelectedParam] = useState<PipelineParam | null>(
    null,
  );
  const [pipelineAddMode, setPipelineAddMode] = useState(false);
  const [paramAddMode, setParamAddMode] = useState(false);
  const [deletePipelineTarget, setDeletePipelineTarget] =
    useState<Pipeline | null>(null);
  const [deleteParamTarget, setDeleteParamTarget] =
    useState<PipelineParam | null>(null);
  const [panelOpen, setPanelOpen] = useState(false);
  const [tabSelected, setTabSelected] = useState<number>(0);
  const [verticalPanes, setVerticalPanes] = useState<SplitterPaneProps[]>([
    { size: "70%" },
    {},
  ]);

  const handleVerticalChange = (e: SplitterOnChangeEvent) =>
    setVerticalPanes(e.newState);

  const handleTabSelect = useCallback((e: TabStripSelectEventArguments) => {
    setTabSelected(e.selected);
  }, []);

  const handleSelectPipeline = (pipeline: Pipeline | null) => {
    setPipelineAddMode(false);
    setParamAddMode(false);
    setSelectedPipeline(pipeline);
    setSelectedParam(null);
    setPanelOpen(!!pipeline);
  };

  const confirmDeletePipeline = async () => {
    if (!deletePipelineTarget) return;

    await deletePipeline(deletePipelineTarget);
    setDeletePipelineTarget(null);
    setSelectedPipeline(null);
    setPanelOpen(false);
  };

  const confirmDeleteParam = async () => {
    if (!deleteParamTarget) return;

    await deletePipelineParams(deleteParamTarget);
    setDeleteParamTarget(null);
    setSelectedParam(null);
  };

  // const availableParamDefs = React.useMemo(() => {
  //   if (!pipelineParamDefs) return [];

  //   return pipelineParamDefs.filter((def) => {
  //     const alreadyUsed = pipelineParams.some(
  //       (p) => p.PipelineParamDefID === def.PipelineParamDefID,
  //     );

  //     if (selectedParam?.PipelineParamDefID === def.PipelineParamDefID) {
  //       return true;
  //     }

  //     return !alreadyUsed;
  //   });
  // }, [pipelineParamDefs, pipelineParams, selectedParam]);

  const availableParamDefs = React.useMemo(() => {
    if (!pipelineParamDefs) return [];

    return pipelineParamDefs.map((def) => {
      const alreadyUsed = pipelineParams.some(
        (p) => p.PipelineParamDefID === def.PipelineParamDefID,
      );

      return {
        ...def,
        disabled:
          alreadyUsed &&
          def.PipelineParamDefID !== selectedParam?.PipelineParamDefID,
      };
    });
  }, [pipelineParamDefs, pipelineParams, selectedParam]);

  useEffect(() => {
    if (!selectedPipeline?.ID) return;

    loadPipelineParamsByPipeline(selectedPipeline.ID);
    loadPipelineParamDefs(selectedPipeline.ID);
  }, [selectedPipeline?.ID]);

  return (
    <main className="pipelines-page">
      <Splitter
        panes={verticalPanes}
        orientation="vertical"
        onChange={handleVerticalChange}
        className="pipelines-grid-container"
      >
        <Pipelines
          pipelines={pipelines}
          selected={selectedPipeline}
          setSelected={handleSelectPipeline}
          enterAddNewPipeline={() => {
            setPipelineAddMode(true);
            setSelectedPipeline(null);
            setPanelOpen(true);
          }}
          requestDelete={setDeletePipelineTarget}
        />

        <div>
          {selectedPipeline ? (
            <TabStrip
              className="pipelines-stuff-tab"
              selected={tabSelected}
              onSelect={handleTabSelect}
            >
              <TabStripTab title={t("pipelines-page:pipelines_params")}>
                <PipelineParams
                  params={pipelineParams}
                  selected={selectedParam}
                  onSelect={setSelectedParam}
                  enterAddMode={() => {
                    if (!selectedPipeline) return;
                    setSelectedParam(null);
                    setParamAddMode(true);
                    setPanelOpen(true);
                  }}
                  requestDelete={setDeleteParamTarget}
                />
              </TabStripTab>
            </TabStrip>
          ) : (
            <div style={{ padding: 20 }}>
              {t("pipelines-page:choose_pipeline_first")}
            </div>
          )}
        </div>
      </Splitter>

      <DetailPanel
        className={
          "config-detail-panel" +
          (selectedPipeline || selectedParam || pipelineAddMode || paramAddMode
            ? ""
            : " no-selected")
        }
        flexGrow={1}
        extandable
        extended={panelOpen}
        onExtendedChange={setPanelOpen}
      >
        {(selectedParam || paramAddMode) && selectedPipeline && (
          <PipelineParamDetailPanel
            selected={selectedParam}
            pipelineID={selectedPipeline.ID}
            updateParam={updatePipelineParam}
            addParam={async (pipelineID, paramID, value) => {
              await addPipelineParams(
                { PipelineParamDefID: paramID, Value: value },
                pipelineID,
              );
            }}
            addMode={paramAddMode}
            setAddMode={setParamAddMode}
            requestDelete={setDeleteParamTarget}
            paramDefs={availableParamDefs}
            pipelineParams={pipelineParams}
          />
        )}

        {(selectedPipeline || pipelineAddMode) &&
          !(selectedParam || paramAddMode) && (
            <PipelinesDetailPanel
              selected={selectedPipeline}
              editPipeline={updatePipeline}
              addPipeline={addPipeline}
              addMode={pipelineAddMode}
              setAddMode={setPipelineAddMode}
              requestDelete={setDeletePipelineTarget}
            />
          )}
      </DetailPanel>

      {deletePipelineTarget && (
        <Dialog
          title={t("common:confirm_deletion")}
          onClose={() => setDeletePipelineTarget(null)}
        >
          {t("pipelines-page:delete_pipeline")}

          <DialogActionsBar>
            <Button onClick={() => setDeletePipelineTarget(null)}>
              {t("common:cancel")}
            </Button>
            <Button themeColor="primary" onClick={confirmDeletePipeline}>
              {t("common:delete")}
            </Button>
          </DialogActionsBar>
        </Dialog>
      )}

      {deleteParamTarget && (
        <Dialog
          title={t("common:confirm_deletion")}
          onClose={() => setDeleteParamTarget(null)}
        >
          {t("pipelines-page:delete_param")}

          <DialogActionsBar>
            <Button onClick={() => setDeleteParamTarget(null)}>
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
