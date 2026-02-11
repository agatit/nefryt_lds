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

const NodesPage = React.memo(function NodesPage() {
  const { t } = useTranslation(["common", "nodes-page"]);
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

  const confirmAdd = async () => {
    if (!newType.trim()) {
      // add
      return;
    }

    let parsedParams = null;

    try {
      parsedParams = newEditorParams ? JSON.parse(newEditorParams) : null;
    } catch {
      parsedParams = null;
    }

    await addNode({
      Type: newType,
      Name: newName || null,
      EditorParams: parsedParams,
      TrendID: newTrendID === "" ? null : Number(newTrendID),
    });

    setShowAddDialog(false);
    setNewType("");
    setNewName("");
    setNewEditorParams("");
    setNewTrendID("");
  };

  const handleDelete = async (node: Node) => {
    await deleteNode(node);
    setSelected(null);
  };

  return (
    <main className="links-page">
      <div className="links-grid-container">
        <Nodes
          nodes={nodes}
          selected={selected}
          onSelectNode={setSelected}
          openAddDialog={openAddDialog}
        />
      </div>

      <DetailPanel
        className={"links-detail-panel" + (selected ? "" : " no-selected")}
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
          <TextBox
            value={newType}
            onChange={(e: TextBoxChangeEvent) =>
              setNewType(e.value?.toString() ?? "")
            }
          />

          <Label>Name</Label>
          <TextBox
            value={newName}
            onChange={(e: TextBoxChangeEvent) =>
              setNewName(e.value?.toString() ?? "")
            }
          />

          <Label>Editor Params (JSON)</Label>
          <TextBox
            value={newEditorParams}
            onChange={(e: TextBoxChangeEvent) =>
              setNewEditorParams(e.value?.toString() ?? "")
            }
          />

          <Label>Trend ID</Label>
          <TextBox
            value={newTrendID}
            onChange={(e: TextBoxChangeEvent) =>
              setNewTrendID(e.value?.toString() ?? "")
            }
          />

          <DialogActionsBar>
            <Button onClick={() => setShowAddDialog(false)}>
              {t("common:cancel")}
            </Button>

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
