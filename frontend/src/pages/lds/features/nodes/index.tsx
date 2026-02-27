import React, { useCallback, useContext, useState } from "react";
import { DetailPanel } from "onyks_shared_kendo";
import { Dialog, DialogActionsBar } from "@progress/kendo-react-dialogs";
import { Button } from "@progress/kendo-react-buttons";
import { useTranslation } from "react-i18next";
import { LDSContext } from "../../contexts/ldsContext";
import { Node } from "../../../../services/api";
import Nodes from "./components/Nodes/Nodes";
import NodesDetailPanel from "./components/Nodes/NodesDetailPanel";
import "./nodesPage.scss";

const NodesPage = React.memo(function NodesPage() {
  const { t } = useTranslation(["common", "nodes-page"]);
  const ldsContext = useContext(LDSContext);

  if (!ldsContext) return null;

  const { nodes, updateNode, deleteNode, addNode } = ldsContext;

  const [selected, setSelected] = useState<Node | null>(null);
  const [panelOpen, setPanelOpen] = useState(false);
  const [addMode, setAddMode] = useState(false);
  const [deleteTarget, setDeleteTarget] = useState<Node | null>(null);

  const handleSelectNode = useCallback((node: Node | null) => {
    setAddMode(false);
    setSelected(node);
    setPanelOpen(!!node);
  }, []);

  const openAddPanel = useCallback(() => {
    setSelected(null);
    setAddMode(true);
    setPanelOpen(true);
  }, []);

  const requestDelete = useCallback((node: Node) => {
    setDeleteTarget(node);
  }, []);

  const confirmDelete = useCallback(async () => {
    if (!deleteTarget) return;

    await deleteNode(deleteTarget);
    setDeleteTarget(null);
    setSelected(null);
    setPanelOpen(false);
  }, [deleteTarget, deleteNode]);

  return (
    <main className="nodes-page">
      <div className="nodes-grid-container">
        <Nodes
          nodes={nodes}
          selected={selected}
          onSelectNode={handleSelectNode}
          onAdd={openAddPanel}
          requestDelete={requestDelete}
        />
      </div>

      <DetailPanel
        className={
          "nodes-detail-panel" + (selected || addMode ? "" : " no-selected")
        }
        flexGrow={1}
        extandable
        extended={panelOpen}
        onExtendedChange={setPanelOpen}
      >
        {(selected || addMode) && (
          <NodesDetailPanel
            selected={selected}
            editNode={updateNode}
            requestDelete={requestDelete}
            addNode={addNode}
            addMode={addMode}
            setAddMode={setAddMode}
            closePanel={() => setPanelOpen(false)}
          />
        )}
      </DetailPanel>

      {deleteTarget && (
        <Dialog
          title={t("common:confirm_deletion")}
          onClose={() => setDeleteTarget(null)}
        >
          {t("nodes-page:delete_node")}
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
});

export default NodesPage;
