import React from "react";
import "./nodesPage.scss";
import { useTranslation } from "react-i18next";
import { LDSContext } from "../../contexts/ldsContext";
import Nodes from "./components/Nodes/Nodes";
import { Node } from "../../../../services/api";
import { Dialog, DialogActionsBar } from "@progress/kendo-react-dialogs";
import { Label } from "@progress/kendo-react-labels";
import { TextBox, TextBoxChangeEvent } from "@progress/kendo-react-inputs";
import { DetailPanel } from "onyks_shared_kendo";
import { Typography } from "@progress/kendo-react-common";
import { Button } from "@progress/kendo-react-buttons";
import NodesDetailPanel from "./components/Nodes/NodesDetailPanel";
import {
  NumericTextBox,
  NumericTextBoxChangeEvent,
} from "@progress/kendo-react-inputs";
import { AppContext } from "../../../../contexts/appContext";

interface EditorNode {
  PosX?: number;
  PosY?: number;
}

const NodesPage = React.memo(function NodesPage() {
  const { t } = useTranslation(["common", "nodes-page"]);
  const appContext = React.useContext(AppContext);
  if (!appContext) return null;

  const ldsContext = React.useContext(LDSContext);
  if (!ldsContext) return null;

  const { nodes, addNode, deleteNode, updateNode } = ldsContext;
  const [selected, setSelected] = React.useState<Node | null>(null);
  const [showAddDialog, setShowAddDialog] = React.useState(false);
  const [newType, setNewType] = React.useState("");
  const [newName, setNewName] = React.useState("");
  const [newEditorParams, setNewEditorParams] =
    React.useState<EditorNode | null>(null);
  const [newTrendID, setNewTrendID] = React.useState<number | null>(null);

  const openAddDialog = () => setShowAddDialog(true);

  const handleTypeChange = React.useCallback(
    (e: TextBoxChangeEvent) => setNewType(String(e.value ?? "").toUpperCase()),
    [],
  );

  const handleNameChange = React.useCallback(
    (e: TextBoxChangeEvent) => setNewName(String(e.value ?? "").toUpperCase()),
    [],
  );

  const handleTrendChange = React.useCallback(
    (e: NumericTextBoxChangeEvent) => {
      setNewTrendID(e.value ?? null);
    },
    [],
  );

  const handlePosXChange = React.useCallback((e: NumericTextBoxChangeEvent) => {
    setNewEditorParams((prev) => ({
      ...prev,
      PosX: e.value ?? 0,
    }));
  }, []);

  const handlePosYChange = React.useCallback((e: NumericTextBoxChangeEvent) => {
    setNewEditorParams((prev) => ({
      ...prev,
      PosY: e.value ?? 0,
    }));
  }, []);

  const confirmAdd = async () => {
    if (!newType.trim()) {
      appContext.showNotification({
        notificationType: { icon: true, style: "error" },
        message: "Type is required",
      });
      return;
    }

    if (newTrendID && isNaN(Number(newTrendID))) {
      appContext.showNotification({
        notificationType: { icon: true, style: "error" },
        message: "Trend ID must be a number",
      });
      return;
    }

    if (!/^[A-Z]+$/.test(newType.trim())) {
      appContext.showNotification({
        notificationType: { icon: true, style: "error" },
        message: "Type must contain uppercase letters only",
      });
      return;
    }

    if (newName && !/^[A-Z0-9-]+$/.test(newName.trim())) {
      appContext.showNotification({
        notificationType: { icon: true, style: "error" },
        message: "Name must contain uppercase letters and numbers only",
      });
      return;
    }

    await addNode({
      Type: newType,
      Name: newName || null,
      EditorParams: newEditorParams,
      TrendID: newTrendID,
    });

    cancelAddNode();
  };

  const cancelAddNode = React.useCallback(() => {
    setShowAddDialog(false);
    setNewType("");
    setNewName("");
    setNewEditorParams(null);
    setNewTrendID(null);
  }, []);

  const handleDelete = async (node: Node) => {
    await deleteNode(node);
    setSelected(null);
  };

  return (
    <main className="nodes-page">
      <div className="nodes-grid-container">
        <Nodes
          nodes={nodes}
          selected={selected}
          onSelectNode={setSelected}
          openAddDialog={openAddDialog}
        />
      </div>

      <DetailPanel
        className={"nodes-detail-panel" + (selected ? "" : " no-selected")}
        flexGrow={1}
        extandable={false}
      >
        {selected ? (
          <NodesDetailPanel
            selected={selected}
            editNode={updateNode}
            deleteNode={handleDelete}
            addNode={addNode}
            openAddDialog={openAddDialog}
          />
        ) : (
          <Typography.p>{t("nodes-page:select_element_to_edit")}</Typography.p>
        )}
      </DetailPanel>

      {showAddDialog && (
        <Dialog
          title="Add new node"
          onClose={() => setShowAddDialog(false)}
          className="links-dialog"
        >
          <Label>Type</Label>
          <TextBox value={newType} onChange={handleTypeChange} />

          <Label>Name</Label>
          <TextBox value={newName} onChange={handleNameChange} />

          <Label>Editor Params:</Label>
          <Label>Position X</Label>
          <NumericTextBox
            value={newEditorParams?.PosX ?? null}
            onChange={handlePosXChange}
          />

          <Label>Position Y</Label>
          <NumericTextBox
            value={newEditorParams?.PosY ?? null}
            onChange={handlePosYChange}
          />

          <Label>Trend ID</Label>
          <NumericTextBox value={newTrendID} onChange={handleTrendChange} />

          <DialogActionsBar>
            <Button onClick={cancelAddNode}>{t("common:cancel")}</Button>

            <Button themeColor="primary" onClick={confirmAdd}>
              {t("common:add")}
            </Button>
          </DialogActionsBar>
        </Dialog>
      )}
    </main>
  );
});

export default NodesPage;
