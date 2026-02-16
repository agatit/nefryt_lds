import React from "react";
import "./methodsPage.scss";
import { useTranslation } from "react-i18next";
import { LDSContext } from "../../contexts/ldsContext";
import {
  Method,
  MethodCreate,
  MethodDef,
  MethodParam,
  MethodParamCreate,
  MethodParamDef,
} from "../../../../services/api";
import Methods from "./components/Methods/Methods";
import MethodDefDetailPanel from "./components/MethodDefs/MethodDefsDetailPanel";
import MethodsDetailPanel from "./components/Methods/MethodsDetailPanel";
import MethodParams from "./components/MethodParams/MethodParams";
import MethodParamDetailPanel from "./components/MethodParams/MethodParamDetailPanel";
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
import {
  Splitter,
  SplitterOnChangeEvent,
  SplitterPaneProps,
  TabStrip,
  TabStripSelectEventArguments,
  TabStripTab,
} from "@progress/kendo-react-layout";
import { AppContext } from "../../../../contexts/appContext";
import MethodDefs from "./components/MethodDefs/MethodDefs";

const MethodsPage = () => {
  const { t } = useTranslation(["common", "method-page"]);
  const appContext = React.useContext(AppContext);
  const ldsContext = React.useContext(LDSContext);
  if (!appContext || !ldsContext) return null;

  const {
    methodDefs,
    pipelines,
    methods,
    addMethod,
    updateMethod,
    deleteMethod,
    addMethodParam,
    updateMethodParam,
    deleteMethodParam,
    loadMethodParamsByMethod,
    methodParamDefs,
    methodParams,
  } = ldsContext;
  const [selectedMethod, setSelectedMethod] = React.useState<Method | null>(
    null,
  );
  const [verticalPanes, setVerticalPanes] = React.useState<SplitterPaneProps[]>(
    [{ size: "65%" }, {}],
  );
  const [showAddDialog, setShowAddDialog] = React.useState(false);
  const [showDeleteDialog, setShowDeleteDialog] = React.useState(false);
  const [name, setName] = React.useState("");
  const [dialogSelectedPipeline, setDialogSelectedPipeline] = React.useState<
    any | null
  >(null);
  const [dialogSelectedMethod, setDialogSelectedMethod] =
    React.useState<Method | null>(null);
  const [selectedMethodDef, setSelectedMethodDef] =
    React.useState<MethodDef | null>(null);
  const [selectedMethodParam, setSelectedMethodParam] =
    React.useState<MethodParam | null>(null);
  const [tabSelected, setTabSelected] = React.useState<number>(0);
  const [showAddParamDialog, setShowAddParamDialog] = React.useState(false);
  const [showDeleteParamDialog, setShowDeleteParamDialog] =
    React.useState(false);
  const [paramValue, setParamValue] = React.useState("");
  const [selectedParamDef, setSelectedParamDef] =
    React.useState<MethodParamDef | null>(null);

  const handleParamValueChange = React.useCallback((e: TextBoxChangeEvent) => {
    setParamValue(String(e.value ?? ""));
  }, []);

  const handleParamDefChange = React.useCallback(
    (e: DropDownListChangeEvent) => {
      setSelectedParamDef(e.value);
    },
    [],
  );

  const handleVerticalChange = (e: SplitterOnChangeEvent) =>
    setVerticalPanes(e.newState);

  const handlePipelineChange = React.useCallback(
    (e: DropDownListChangeEvent) => {
      setDialogSelectedPipeline(e.value?.ID ?? null);
    },
    [],
  );

  const handleMethodChange = React.useCallback((e: DropDownListChangeEvent) => {
    setDialogSelectedMethod(e.value);
  }, []);

  const handleNameChange = React.useCallback((e: TextBoxChangeEvent) => {
    setName(String(e.value ?? ""));
  }, []);

  const handleTabSelect = React.useCallback(
    (e: TabStripSelectEventArguments) => {
      setTabSelected(e.selected);
    },
    [],
  );

  const selectedPipelineObject = React.useMemo(() => {
    return pipelines.find((p) => p.ID === dialogSelectedPipeline) ?? null;
  }, [pipelines, dialogSelectedPipeline]);

  const confirmDeleteMethod = async () => {
    if (!selectedMethod) return;
    await deleteMethod(selectedMethod);
    setSelectedMethod(null);
    setShowDeleteDialog(false);
  };

  const confirmAddMethod = async () => {
    if (!dialogSelectedPipeline || !dialogSelectedMethod) {
      appContext.showNotification({
        notificationType: { icon: true, style: "error" },
        message: "Method definition required",
      });
      return;
    }

    const method: MethodCreate = {
      PipelineID: dialogSelectedPipeline,
      MethodDefID: dialogSelectedMethod.MethodDefID,
      Name: name || null,
    };

    await addMethod(method);

    setName("");
    setDialogSelectedPipeline(null);
    setDialogSelectedMethod(null);
    setShowAddDialog(false);
  };

  const availableParamDefs = React.useMemo(() => {
    if (!selectedMethod) return [];

    const usedDefs = methodParams
      .filter((p) => p.MethodID === selectedMethod.ID)
      .map((p) => p.MethodParamDefID);

    return methodParamDefs.filter(
      (def) =>
        def.MethodDefID === selectedMethod.MethodDefID &&
        !usedDefs.includes(def.ID),
    );
  }, [methodParamDefs, methodParams, selectedMethod]);

  const handleOpenAddParamDialog = React.useCallback(() => {
    if (availableParamDefs.length === 0) {
      appContext.showNotification({
        notificationType: { icon: true, style: "warning" },
        message: "No available parameters to add.",
      });
      return;
    }

    setShowAddParamDialog(true);
  }, [availableParamDefs, appContext]);

  const confirmAddParam = async () => {
    if (!selectedMethod || !selectedParamDef?.ID || !paramValue.trim()) {
      appContext.showNotification({
        notificationType: { icon: true, style: "error" },
        message: "Select parameter definition and enter value",
      });
      return;
    }

    const param: MethodParamCreate = {
      MethodParamDefID: selectedParamDef.ID,
      Value: paramValue,
    };

    await addMethodParam(selectedMethod.ID, param);
    setShowAddParamDialog(false);
    setParamValue("");
    setSelectedParamDef(null);
    await loadMethodParamsByMethod(selectedMethod.ID);
  };

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

  React.useEffect(() => {
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
            }}
            openAddDialog={() => setShowAddDialog(true)}
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
                openDialog={handleOpenAddParamDialog}
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
        extandable={false}
        className={
          "methods-detail-panel" +
          (selectedMethod || selectedMethodDef || selectedMethodParam
            ? ""
            : " no-selected")
        }
      >
        {selectedMethodParam && selectedMethod ? (
          <MethodParamDetailPanel
            selected={selectedMethodParam}
            selectedMethod={selectedMethod}
            updateParam={ldsContext.updateMethodParam}
            deleteParam={ldsContext.deleteMethodParam}
            openAddDialog={() => setShowAddParamDialog(true)}
            openDeleteDialog={() => setShowDeleteParamDialog(true)}
          />
        ) : selectedMethodDef ? (
          <MethodDefDetailPanel selected={selectedMethodDef} />
        ) : selectedMethod ? (
          <MethodsDetailPanel
            selected={selectedMethod}
            updateMethod={updateMethod}
            deleteMethod={async () => setShowDeleteDialog(true)}
            openAddDialog={() => setShowAddDialog(true)}
          />
        ) : (
          <Typography.p style={{ padding: 20 }}>
            {t("method-page:select_method")}
          </Typography.p>
        )}
      </DetailPanel>

      {showAddParamDialog && (
        <Dialog
          title="Add method parameter"
          onClose={() => setShowAddParamDialog(false)}
          className="methods-dialog"
        >
          <Label>Parameter definition</Label>
          <DropDownList
            data={availableParamDefs}
            textField="Name"
            dataItemKey="MethodParamDefID"
            value={selectedParamDef}
            onChange={handleParamDefChange}
          />

          <Label>Value</Label>
          <TextBox value={paramValue} onChange={handleParamValueChange} />

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

      {showAddDialog && (
        <Dialog
          title="Add new method"
          onClose={() => setShowAddDialog(false)}
          className="methods-dialog"
        >
          <Label>Pipeline</Label>
          <DropDownList
            data={pipelines}
            textField="Name"
            dataItemKey="ID"
            value={selectedPipelineObject}
            onChange={handlePipelineChange}
          />

          <Label>Method definition</Label>
          <DropDownList
            data={methods}
            textField="Name"
            dataItemKey="ID"
            value={dialogSelectedMethod}
            onChange={handleMethodChange}
          />

          <Label>Name</Label>
          <TextBox value={name} onChange={handleNameChange} />

          <DialogActionsBar>
            <Button onClick={() => setShowAddDialog(false)}>
              {t("common:cancel")}
            </Button>
            <Button themeColor="primary" onClick={confirmAddMethod}>
              {t("common:add")}
            </Button>
          </DialogActionsBar>
        </Dialog>
      )}

      {showDeleteDialog && (
        <Dialog
          title="Confirm deletion"
          onClose={() => setShowDeleteDialog(false)}
          className="methods-dialog"
        >
          Delete selected method?
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
