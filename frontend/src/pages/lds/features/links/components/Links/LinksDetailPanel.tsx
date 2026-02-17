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
} from "@progress/kendo-svg-icons";
import { Link, LinkUpdate } from "../../../../../../services/api";
import { plusIcon } from "@progress/kendo-svg-icons";

interface Props {
  selected: Link;
  editLink: (id: number, value: LinkUpdate) => Promise<void>;
  deleteLink: (value: Link) => Promise<void>;
  openAddDialog: () => void;
}

const LinksDetailPanel = React.memo(function LinksDetailPanel({
  selected,
  editLink,
  deleteLink,
  openAddDialog,
}: Props) {
  const { t } = useTranslation(["common", "link-page"]);
  const [inEdit, setInEdit] = React.useState(false);
  const [showDeleteDialog, setShowDeleteDialog] = React.useState(false);
  const [beginNodeID, setBeginNodeID] = React.useState("");
  const [endNodeID, setEndNodeID] = React.useState("");
  const [length, setLength] = React.useState("");

  const handleBeginNodeChange = React.useCallback((e: TextBoxChangeEvent) => {
    setBeginNodeID(String(e.value ?? ""));
  }, []);

  const handleEndNodeChange = React.useCallback((e: TextBoxChangeEvent) => {
    setEndNodeID(String(e.value ?? ""));
  }, []);

  const handleLengthChange = React.useCallback((e: TextBoxChangeEvent) => {
    setLength(String(e.value ?? ""));
  }, []);

  const saveEdit = async () => {
    await editLink(selected.ID, {
      BeginNodeID: beginNodeID === "" ? null : Number(beginNodeID),
      EndNodeID: endNodeID === "" ? null : Number(endNodeID),
      Length: length === "" ? null : Number(length),
    });

    setInEdit(false);
  };

  const confirmDelete = React.useCallback(async () => {
    if (!selected) return;

    await deleteLink(selected);
    setShowDeleteDialog(false);
    setInEdit(false);
  }, [selected, deleteLink]);

  const setSelectedData = React.useCallback((link: Link) => {
    setBeginNodeID(link.BeginNodeID?.toString() ?? "");
    setEndNodeID(link.EndNodeID?.toString() ?? "");
    setLength(link.Length?.toString() ?? "");
  }, []);

  const cancelEdit = () => {
    setSelectedData(selected);
    setInEdit(false);
  };

  React.useEffect(() => {
    if (!selected) return;

    setSelectedData(selected);
    setInEdit(false);
  }, [selected, setSelectedData]);

  return (
    <div className="detail-panel-content">
      <div className="item-column">
        <Label>ID</Label>
        <TextBox value={selected.ID.toString()} disabled />

        <Label>Begin Node</Label>
        <TextBox
          value={beginNodeID}
          disabled={!inEdit}
          onChange={handleBeginNodeChange}
        />

        <Label>End Node</Label>
        <TextBox
          value={endNodeID}
          disabled={!inEdit}
          onChange={handleEndNodeChange}
        />

        <Label>Length</Label>
        <TextBox
          value={length}
          disabled={!inEdit}
          onChange={handleLengthChange}
        />
      </div>

      <div className="item-row">
        {!inEdit ? (
          <>
            <Button svgIcon={pencilIcon} onClick={() => setInEdit(true)}>
              {t("common:edit")}
            </Button>

            <Button svgIcon={plusIcon} onClick={openAddDialog}>
              {t("link-page:add_new_link")}
            </Button>
          </>
        ) : (
          <>
            <Button svgIcon={cancelIcon} onClick={cancelEdit}>
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
          Delete this link?
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

export default LinksDetailPanel;
