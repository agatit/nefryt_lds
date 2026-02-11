import React from "react";
import "../../../../styles/features/lds/features/linkPage.scss";
import { useTranslation } from "react-i18next";
import { LDSContext } from "../../contexts/ldsContext";
import Nodes from "./components/Nodes";
import { Node } from "../../../../services/api";
import { Dialog, DialogActionsBar } from "@progress/kendo-react-dialogs";
import { Label } from "@progress/kendo-react-labels";
import { TextBox, TextBoxChangeEvent } from "@progress/kendo-react-inputs";
import { DetailPanel } from "onyks_shared_kendo";
import { Typography } from "@progress/kendo-react-common";
import { Button } from "@progress/kendo-react-buttons";
import NodesDetailPanel from "./components/NodesDetailPanel";
import { AppContext } from "../../../../contexts/appContext";

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
  const [newEditorParams, setNewEditorParams] = React.useState("");
  const [newTrendID, setNewTrendID] = React.useState("");

  const openAddDialog = () => setShowAddDialog(true);

  const handleTypeChange = React.useCallback(
    (e: TextBoxChangeEvent) => setNewType(String(e.value ?? "").toUpperCase()),
    [],
  );

  const handleNameChange = React.useCallback(
    (e: TextBoxChangeEvent) => setNewName(String(e.value ?? "").toUpperCase()),
    [],
  );

  const handleParamsChange = React.useCallback(
    (e: TextBoxChangeEvent) => setNewEditorParams(String(e.value ?? "")),
    [],
  );

  const handleTrendChange = React.useCallback(
    (e: TextBoxChangeEvent) => setNewTrendID(String(e.value ?? "")),
    [],
  );

  const confirmAdd = async () => {
    if (!newType.trim()) {
      appContext.showNotification({
        notificationType: { icon: true, style: "error" },
        message: "Type is required",
      });
      return;
    }

    let parsedParams = null;

    if (newEditorParams.trim()) {
      try {
        parsedParams = JSON.parse(newEditorParams);
      } catch {
        appContext.showNotification({
          notificationType: { icon: true, style: "error" },
          message: "Editor Params must be valid JSON",
        });
        return;
      }
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

    const trendIdNum = newTrendID === "" ? null : Number(newTrendID);

    await addNode({
      Type: newType,
      Name: newName || null,
      EditorParams: parsedParams,
      TrendID: trendIdNum,
    });

    cancelAddNode();
  };

  const cancelAddNode = React.useCallback(() => {
    setShowAddDialog(false);
    setNewType("");
    setNewName("");
    setNewEditorParams("");
    setNewTrendID("");
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

          <Label>Editor Params (JSON)</Label>
          <TextBox
            value={newEditorParams}
            placeholder='e.g. {"PosX":100,"PosY":200}'
            onChange={handleParamsChange}
          />

          <Label>Trend ID</Label>
          <TextBox value={newTrendID} onChange={handleTrendChange} />

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
