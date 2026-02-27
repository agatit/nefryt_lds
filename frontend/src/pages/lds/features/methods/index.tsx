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
import MethodDefDetailPanel from "./components/MethodDefs/MethodDefsDetailPanel";
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
  const [selectedMethodDef, setSelectedMethodDef] = useState<MethodDef | null>(
    null,
  );
  const [selectedMethodParam, setSelectedMethodParam] =
    useState<MethodParam | null>(null);
  const [tabSelected, setTabSelected] = useState<number>(0);
  const [panelOpen, setPanelOpen] = useState(false);

  type DeleteTarget =
    | { type: "method"; item: Method }
    | { type: "param"; item: MethodParam }
    | { type: "methodDef"; item: MethodDef }
    | null;

  const [deleteTarget, setDeleteTarget] = useState<DeleteTarget>(null);

  const requestDeleteMethod = (m: Method) =>
    setDeleteTarget({ type: "method", item: m });

  const requestDeleteParam = (p: MethodParam) =>
    setDeleteTarget({ type: "param", item: p });

  const handleVerticalChange = (e: SplitterOnChangeEvent) =>
    setVerticalPanes(e.newState);

  const handleTabSelect = useCallback((e: TabStripSelectEventArguments) => {
    setTabSelected(e.selected);
  }, []);

  const confirmDelete = async () => {
    if (!deleteTarget) return;

    try {
      switch (deleteTarget.type) {
        case "method":
          await deleteMethod(deleteTarget.item);
          setSelectedMethod(null);
          break;

        case "param":
          if (!selectedMethod) return;
          await deleteMethodParam(
            selectedMethod.ID,
            deleteTarget.item.MethodParamDefID,
          );
          setSelectedMethodParam(null);
          break;
      }
    } finally {
      setDeleteTarget(null);
    }
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

  useEffect(() => {
    if (!selectedMethod) return;

    loadMethodParamsByMethod(selectedMethod.ID);
  }, [selectedMethod?.ID]);

  return (
    <main className="methods-page">
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
          requestDelete={(m) => requestDeleteMethod(m)}
        />
      </div>

      {/* <TabStrip
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
                setPanelOpen(!!d);
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
                requestDelete={(param) => requestDeleteParam(param)}
              />
            ) : (
              <Typography.p style={{ padding: 20 }}>
                {t("method-page:select_method")}
              </Typography.p>
            )}
          </TabStripTab>
        </TabStrip> */}

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
          paramAddMode ||
          selectedMethodDef
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
            requestDelete={() =>
              selectedMethodParam && requestDeleteParam(selectedMethodParam)
            }
            paramDefs={availableParamDefs}
            methodParams={methodParams}
            addMethodParam={ldsContext.addMethodParam}
            closePanel={() => setPanelOpen(false)}
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
              requestDelete={() =>
                selectedMethod && requestDeleteMethod(selectedMethod)
              }
              pipelines={pipelines}
              methodDefs={availableMethodDefs}
              closePanel={() => setPanelOpen(false)}
            />
          )}

        {selectedMethodDef && !selectedMethod && !selectedMethodParam && (
          <MethodDefDetailPanel selected={selectedMethodDef} />
        )}
      </DetailPanel>

      {deleteTarget && (
        <Dialog
          title={t("common:confirm_deletion")}
          onClose={() => setDeleteTarget(null)}
        >
          {deleteTarget.type === "method" && t("method-page:delete_method")}

          {deleteTarget.type === "param" && t("method-page:delete_param")}

          {deleteTarget.type === "methodDef" &&
            t("method-page:delete_method_def")}

          <DialogActionsBar>
            <Button onClick={() => setDeleteTarget(null)}>
              {t("common:cancel")}
            </Button>

            <Button themeColor="primary" onClick={confirmDelete}>
              {t("common:delete")}
            </Button>
          </DialogActionsBar>
        </Dialog>
      )}
    </main>
  );
};

export default MethodsPage;
