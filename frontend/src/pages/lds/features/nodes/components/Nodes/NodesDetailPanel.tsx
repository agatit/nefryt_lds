import React from "react";
import { Label } from "@progress/kendo-react-labels";
import { useTranslation } from "react-i18next";
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
import { Node, NodeCreate, NodeUpdate } from "../../../../../../services/api";
import { AppContext } from "../../../../../../contexts/appContext";

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
  const { t } = useTranslation(["common", "node-page"]);
  const appContext = React.useContext(AppContext);
  if (!appContext) return null;

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

  const handleTypeChange = React.useCallback(
    (e: TextBoxChangeEvent) => setType(String(e.value ?? "").toUpperCase()),
    [],
  );

  const handleNameChange = React.useCallback(
    (e: TextBoxChangeEvent) => setName(String(e.value ?? "").toUpperCase()),
    [],
  );

  const handleParamsChange = React.useCallback(
    (e: TextBoxChangeEvent) => setEditorParams(String(e.value ?? "")),
    [],
  );

  const saveEdit = async () => {
    let parsedParams = null;

    if (editorParams.trim()) {
      try {
        parsedParams = JSON.parse(editorParams);
      } catch {
        appContext.showNotification({
          notificationType: { icon: true, style: "error" },
          message: "Editor Params must be valid JSON",
        });
        return;
      }
    }

    if (trendID && isNaN(Number(trendID))) {
      appContext.showNotification({
        notificationType: { icon: true, style: "error" },
        message: "Trend ID must be a number",
      });
      return;
    }

    if (!/^[A-Z]+$/.test(type.trim())) {
      appContext.showNotification({
        notificationType: { icon: true, style: "error" },
        message: "Type must contain uppercase letters only",
      });
      return;
    }

    if (name && !/^[A-Z0-9-]+$/.test(name.trim())) {
      appContext.showNotification({
        notificationType: { icon: true, style: "error" },
        message: "Name must contain uppercase letters and numbers only",
      });
      return;
    }

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
        <TextBox value={selected.ID!} disabled />

        <Label>Type</Label>
        <TextBox value={type} disabled={!inEdit} onChange={handleTypeChange} />

        <Label>Name</Label>
        <TextBox value={name} disabled={!inEdit} onChange={handleNameChange} />

        <Label>Editor Params</Label>
        <TextBox
          value={editorParams}
          disabled={!inEdit}
          onChange={handleParamsChange}
        />

        <Label>Trend ID</Label>
        <TextBox value={trendID} disabled />
      </div>

      <div className="item-row">
        {!inEdit ? (
          <>
            <Button svgIcon={pencilIcon} onClick={() => setInEdit(true)}>
              {t("common:edit")}
            </Button>

            <Button svgIcon={plusIcon} onClick={openAddDialog}>
              {t("node-page:add_new_node")}
            </Button>
          </>
        ) : (
          <>
            <Button svgIcon={cancelIcon} onClick={() => setInEdit(false)}>
              {t("common:cancel")}
            </Button>

            <Button svgIcon={saveIcon} themeColor="primary" onClick={saveEdit}>
              {t("common:save")}
            </Button>

            <Button
              svgIcon={trashIcon}
              onClick={() => setShowDeleteDialog(true)}
            >
              {t("common:delete")}
            </Button>
          </>
        )}
      </div>

      {showDeleteDialog && (
        <Dialog
          title={t("common:confirm_deletion")}
          onClose={() => setShowDeleteDialog(false)}
        >
          Delete this node?
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
    </div>
  );
});

export default NodesDetailPanel;
