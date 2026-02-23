import { useState, useContext, useCallback, useEffect, memo } from "react";
import "./nodesPage.scss";
import { LDSContext } from "../../contexts/ldsContext";
import Nodes from "./components/Nodes/Nodes";
import { Node } from "../../../../services/api";
import { DetailPanel } from "onyks_shared_kendo";
import NodesDetailPanel from "./components/Nodes/NodesDetailPanel";
import { Dialog, DialogActionsBar } from "@progress/kendo-react-dialogs";
import { Button } from "@progress/kendo-react-buttons";
import { useTranslation } from "react-i18next";

const NodesPage = memo(function NodesPage() {
  const { t } = useTranslation(["common", "nodes-page"]);
  const [panelOpen, setPanelOpen] = useState(false);
  const [selected, setSelected] = useState<Node | null>(null);
  const [showDeleteDialog, setShowDeleteDialog] = useState(false);
  const [addMode, setAddMode] = useState(false);
  const ldsContext = useContext(LDSContext);
  if (!ldsContext) return null;

  const { nodes, addNode, deleteNode, updateNode } = ldsContext;

  const requestDelete = useCallback((node: Node) => {
    setSelected(node);
    setShowDeleteDialog(true);
  }, []);
  const confirmDelete = async () => {
    if (!selected) return;

    await deleteNode(selected);

    setShowDeleteDialog(false);
    setSelected(null);
  };

  useEffect(() => {
    if (selected) setPanelOpen(true);
  }, [selected]);

  return (
    <main className="nodes-page">
      <div className="nodes-grid-container">
        <Nodes
          nodes={nodes}
          selected={selected}
          onSelectNode={setSelected}
          onAdd={() => {
            setSelected(null);
            setAddMode(true);
            setPanelOpen(true);
          }}
          requestDelete={requestDelete}
        />
      </div>

      <DetailPanel
        className={"nodes-detail-panel" + (selected ? "" : " no-selected")}
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
          />
        )}
      </DetailPanel>

      {showDeleteDialog && (
        <Dialog
          title={t("common:confirm_deletion")}
          onClose={() => setShowDeleteDialog(false)}
        >
          {t("nodes-page:delete_node")}
          <DialogActionsBar>
            <Button onClick={() => setShowDeleteDialog(false)}>
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
