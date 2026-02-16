import React from "react";
import "./methodsPage.scss";
import { useTranslation } from "react-i18next";
import { LDSContext } from "../../contexts/ldsContext";
import { Method, MethodCreate, MethodDef } from "../../../../services/api";
import Methods from "./components/Methods/Methods";
import MethodDefDetailPanel from "./components/MethodDefs/MethodDefsDetailPanel";
import MethodsDetailPanel from "./components/Methods/MethodsDetailPanel";
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
  const [tabSelected, setTabSelected] = React.useState<number>(0);

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

  React.useEffect(() => {
    if (selectedMethod && selectedMethodDef) {
      setSelectedMethodDef(null);
    }
  }, [selectedMethod, selectedMethodDef]);

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
            onSelect={setSelectedMethod}
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
              setSelected={setSelectedMethodDef}
            />
          </TabStripTab>
        </TabStrip>
      </Splitter>

      <DetailPanel
        flexGrow={1}
        extandable={false}
        className={
          "methods-detail-panel" +
          (selectedMethod || selectedMethodDef ? "" : " no-selected")
        }
      >
        {selectedMethod && (
          <MethodsDetailPanel
            selected={selectedMethod}
            updateMethod={updateMethod}
            deleteMethod={async () => setShowDeleteDialog(true)}
            openAddDialog={() => setShowAddDialog(true)}
          />
        )}

        {selectedMethodDef && (
          <MethodDefDetailPanel selected={selectedMethodDef} />
        )}

        {!selectedMethod && !selectedMethodDef && (
          <Typography.p style={{ padding: 20 }}>
            {t("method-page:select_method")}
          </Typography.p>
        )}
      </DetailPanel>

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
    </main>
  );
};

export default MethodsPage;
