import { useEffect, useState, useContext, useCallback, useMemo } from "react";
import { useTranslation } from "react-i18next";
import {
  Splitter,
  SplitterOnChangeEvent,
  SplitterPaneProps,
  TabStrip,
  TabStripSelectEventArguments,
  TabStripTab,
} from "@progress/kendo-react-layout";
import { Button } from "@progress/kendo-react-buttons";
import { DetailPanel } from "onyks_shared_kendo";
import { Typography } from "@progress/kendo-react-common";
import { Dialog, DialogActionsBar } from "@progress/kendo-react-dialogs";
import { LDSContext } from "../../contexts/ldsContext";
import Methods from "./components/Methods/Methods";
import MethodsDetailPanel from "./components/Methods/MethodsDetailPanel";
import MethodParams from "./components/MethodParams/MethodParams";
import MethodParamDetailPanel from "./components/MethodParams/MethodParamDetailPanel";
import MethodDefs from "./components/MethodDefs/MethodDefs";
import { AppContext } from "../../../../contexts/appContext";
import { Method, MethodDef, MethodParam } from "../../../../services/api";
import "./methodsPage.scss";

const MethodsPage = () => {
  const { t } = useTranslation(["common", "method-page"]);
  const appContext = useContext(AppContext);
  const ldsContext = useContext(LDSContext);
  if (!appContext || !ldsContext) return null;

  const {
    methodDefs,
    pipelines,
    methods,
    addMethod,
    updateMethod,
    deleteMethod,
    deleteMethodParam,
    loadMethodParamsByMethod,
    methodParamDefs,
    methodParams,
  } = ldsContext;
  const [selectedMethod, setSelectedMethod] = useState<Method | null>(null);
  const [verticalPanes, setVerticalPanes] = useState<SplitterPaneProps[]>([
    { size: "65%" },
    {},
  ]);
  const [methodAddMode, setMethodAddMode] = useState(false);
  const [paramAddMode, setParamAddMode] = useState(false);
  const [showDeleteDialog, setShowDeleteDialog] = useState(false);
  const [selectedMethodDef, setSelectedMethodDef] = useState<MethodDef | null>(
    null,
  );
  const [selectedMethodParam, setSelectedMethodParam] =
    useState<MethodParam | null>(null);
  const [tabSelected, setTabSelected] = useState<number>(0);
  const [showDeleteParamDialog, setShowDeleteParamDialog] = useState(false);
  const [panelOpen, setPanelOpen] = useState(false);

  const handleVerticalChange = (e: SplitterOnChangeEvent) =>
    setVerticalPanes(e.newState);

  const handleTabSelect = useCallback((e: TabStripSelectEventArguments) => {
    setTabSelected(e.selected);
  }, []);

  const confirmDeleteMethod = async () => {
    if (!selectedMethod) return;
    await deleteMethod(selectedMethod);
    setSelectedMethod(null);
    setShowDeleteDialog(false);
  };

  const availableParamDefs = useMemo(() => {
    if (!selectedMethod) return [];

    const methodDefID = selectedMethod.MethodDefID;

    const usedDefs = methodParams
      .filter((p) => p.MethodID === selectedMethod.ID)
      .map((p) => p.MethodParamDefID);

    return methodParamDefs
      .filter((def) => String(def.MethodDefID) === String(methodDefID))
      .map((def) => ({
        ...def,
        disabled: usedDefs.some((id) => String(id) === String(def.ID)),
      }));
  }, [methodParamDefs, methodParams, selectedMethod]);

  const availableMethodDefs = useMemo(() => {
    if (!selectedMethod) return methodDefs;

    const usedDefs = methods
      .filter((m) => m.PipelineID === selectedMethod.PipelineID)
      .map((m) => m.MethodDefID);

    return methodDefs.map((def) => ({
      ...def,
      disabled: usedDefs.includes(def.ID),
    }));
  }, [methodDefs, methods, selectedMethod]);

  const confirmDeleteParam = async () => {
    if (!selectedMethod || !selectedMethodParam) return;

    await deleteMethodParam(
      selectedMethod.ID,
      selectedMethodParam.MethodParamDefID,
    );

    setSelectedMethodParam(null);
    setShowDeleteParamDialog(false);

    await loadMethodParamsByMethod(selectedMethod.ID);
  };

  useEffect(() => {
    if (!selectedMethod) return;

    loadMethodParamsByMethod(selectedMethod.ID);
  }, [selectedMethod?.ID]);

  return (
    <main className="methods-page">
      <Splitter
        className="methods-grid-container"
        panes={verticalPanes}
        orientation="vertical"
        onChange={handleVerticalChange}
      >
        <div className="methods-grid-container">
          <Methods
            methods={methods}
            selected={selectedMethod}
            onSelect={(m) => {
              setSelectedMethod(m);
              setSelectedMethodParam(null);
              setSelectedMethodDef(null);
              setMethodAddMode(false);
              setPanelOpen(!!m);
            }}
            onAdd={() => {
              setSelectedMethod(null);
              setSelectedMethodParam(null);
              setMethodAddMode(true);
              setPanelOpen(true);
            }}
            requestDelete={(m) => {
              setSelectedMethod(m);
              setShowDeleteDialog(true);
            }}
          />
        </div>

        <TabStrip
          className="method-stuff-tab"
          selected={tabSelected}
          onSelect={handleTabSelect}
        >
          <TabStripTab title={t("method-page:method_defs")}>
            <MethodDefs
              methodDefs={methodDefs}
              selected={selectedMethodDef}
              setSelected={(d) => {
                setSelectedMethodDef(d);
                setSelectedMethod(null);
                setSelectedMethodParam(null);
              }}
            />
          </TabStripTab>
          <TabStripTab title={t("method-page:method_params")}>
            {selectedMethod ? (
              <MethodParams
                selectedMethod={selectedMethod}
                selectedParam={selectedMethodParam}
                setSelectedParam={setSelectedMethodParam}
                methodParams={methodParams}
                openDialog={() => {
                  if (!selectedMethod) return;

                  if (availableParamDefs.length === 0) {
                    appContext.showNotification({
                      notificationType: { icon: true, style: "warning" },
                      message: "No available parameters to add.",
                    });
                    return;
                  }

                  setParamAddMode(true);
                  setSelectedMethodParam(null);
                }}
              />
            ) : (
              <Typography.p style={{ padding: 20 }}>
                {t("method-page:select_method")}
              </Typography.p>
            )}
          </TabStripTab>
        </TabStrip>
      </Splitter>

      <DetailPanel
        flexGrow={1}
        extandable
        extended={panelOpen}
        onExtendedChange={setPanelOpen}
        className={
          "methods-detail-panel" +
          (selectedMethod ||
          selectedMethodDef ||
          selectedMethodParam ||
          methodAddMode ||
          paramAddMode
            ? ""
            : " no-selected")
        }
      >
        {(selectedMethodParam || paramAddMode) && selectedMethod && (
          <MethodParamDetailPanel
            selected={selectedMethodParam}
            selectedMethod={selectedMethod}
            updateParam={ldsContext.updateMethodParam}
            deleteParam={ldsContext.deleteMethodParam}
            addMode={paramAddMode}
            setAddMode={setParamAddMode}
            requestDelete={() => setShowDeleteParamDialog(true)}
            paramDefs={availableParamDefs}
            methodParams={methodParams}
            addMethodParam={ldsContext.addMethodParam}
          />
        )}

        {(selectedMethod || methodAddMode) &&
          !(selectedMethodParam || paramAddMode) && (
            <MethodsDetailPanel
              selected={selectedMethod}
              updateMethod={updateMethod}
              addMethod={addMethod}
              addMode={methodAddMode}
              setAddMode={setMethodAddMode}
              requestDelete={() => setShowDeleteDialog(true)}
              pipelines={pipelines}
              methodDefs={availableMethodDefs}
            />
          )}

        {!selectedMethod &&
          !selectedMethodDef &&
          !selectedMethodParam &&
          !methodAddMode &&
          !paramAddMode && (
            <Typography.p style={{ padding: 20 }}>
              {t("method-page:select_method")}
            </Typography.p>
          )}
      </DetailPanel>

      {showDeleteDialog && (
        <Dialog
          title={t("common:confirm_deletion")}
          onClose={() => setShowDeleteDialog(false)}
        >
          {t("method-page:delete_method")}

          <DialogActionsBar>
            <Button onClick={() => setShowDeleteDialog(false)}>
              {t("common:cancel")}
            </Button>

            <Button themeColor="primary" onClick={confirmDeleteMethod}>
              {t("common:delete")}
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
};

export default MethodsPage;
