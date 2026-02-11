import React from "react";
import { Label } from "@progress/kendo-react-labels";
import { TextBox, TextBoxChangeEvent } from "@progress/kendo-react-inputs";
import { Button } from "@progress/kendo-react-buttons";
import { Dialog, DialogActionsBar } from "@progress/kendo-react-dialogs";
import {
  pencilIcon,
  cancelIcon,
  trashIcon,
  saveIcon,
  plusIcon,
} from "@progress/kendo-svg-icons";
import { Node, NodeCreate, NodeUpdate } from "../../../../../services/api";

interface Props {
  selected: Node;
  deleteNode: (value: Node) => Promise<void>;
  addNode: (value: NodeCreate) => Promise<Node>;
  editNode: (id: number, value: NodeUpdate) => Promise<void>;
  openAddDialog: () => void;
}

const NodesDetailPanel = React.memo(function NodesDetailPanel({
  selected,
  editNode,
  deleteNode,
  openAddDialog,
}: Props) {
  const [inEdit, setInEdit] = React.useState(false);
  const [showDeleteDialog, setShowDeleteDialog] = React.useState(false);
  const [type, setType] = React.useState("");
  const [name, setName] = React.useState("");
  const [editorParams, setEditorParams] = React.useState("");
  const [trendID, setTrendID] = React.useState("");

  React.useEffect(() => {
    setType(selected.Type ?? "");
    setName(selected.Name ?? "");
    setEditorParams(
      selected.EditorParams ? JSON.stringify(selected.EditorParams) : "",
    );
    setTrendID(selected.TrendID?.toString() ?? "");
    setInEdit(false);
  }, [selected]);

  const saveEdit = async () => {
    let parsedParams = null;

    try {
      parsedParams = editorParams ? JSON.parse(editorParams) : null;
    } catch {
      parsedParams = null;
    }

    await editNode(selected.ID!, {
      Type: type,
      Name: name,
      EditorParams: parsedParams,
    });

    setInEdit(false);
  };

  const confirmDelete = async () => {
    await deleteNode(selected);
    setShowDeleteDialog(false);
  };

  return (
    <div className="detail-panel-content">
      <div className="item-column">
        <Label>ID</Label>
        <TextBox value={selected.ID!.toString() ?? ""} disabled />

        <Label>Type</Label>
        <TextBox
          value={type}
          disabled={!inEdit}
          onChange={(e: TextBoxChangeEvent) =>
            setType(e.value?.toString() ?? "")
          }
        />

        <Label>Name</Label>
        <TextBox
          value={name}
          disabled={!inEdit}
          onChange={(e: TextBoxChangeEvent) =>
            setName(e.value?.toString() ?? "")
          }
        />

        <Label>Editor Params</Label>
        <TextBox
          value={editorParams}
          disabled={!inEdit}
          onChange={(e: TextBoxChangeEvent) =>
            setEditorParams(e.value?.toString() ?? "")
          }
        />

        <Label>Trend ID</Label>
        <TextBox
          value={trendID}
          disabled={!inEdit}
          onChange={(e: TextBoxChangeEvent) =>
            setTrendID(e.value?.toString() ?? "")
          }
        />
      </div>

      <div className="item-row">
        {!inEdit ? (
          <>
            <Button svgIcon={pencilIcon} onClick={() => setInEdit(true)}>
              Edit
            </Button>

            <Button svgIcon={plusIcon} onClick={openAddDialog}>
              Add new node
            </Button>
          </>
        ) : (
          <>
            <Button svgIcon={cancelIcon} onClick={() => setInEdit(false)}>
              Cancel
            </Button>

            <Button svgIcon={saveIcon} themeColor="primary" onClick={saveEdit}>
              Save
            </Button>

            <Button
              svgIcon={trashIcon}
              onClick={() => setShowDeleteDialog(true)}
            >
              Delete
            </Button>
          </>
        )}
      </div>

      {showDeleteDialog && (
        <Dialog
          title="Confirm deletion"
          onClose={() => setShowDeleteDialog(false)}
        >
          Delete this node?
          <DialogActionsBar>
            <Button onClick={() => setShowDeleteDialog(false)}>Cancel</Button>
            <Button themeColor="primary" onClick={confirmDelete}>
              Delete
            </Button>
          </DialogActionsBar>
        </Dialog>
      )}
    </div>
  );
});

export default NodesDetailPanel;
