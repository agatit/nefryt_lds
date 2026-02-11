import React from "react";
import "../../../../styles/features/lds/features/linkPage.scss";
import { DetailPanel } from "onyks_shared_kendo";
import { useTranslation } from "react-i18next";
import { Typography } from "@progress/kendo-react-common";
import { LDSContext } from "../../contexts/ldsContext";
import Links from "./components/Links";
import LinksDetailPanel from "./components/LinksDetailPanel";
import { Link, LinkUpdate } from "../../../../services/api";
import { Dialog, DialogActionsBar } from "@progress/kendo-react-dialogs";
import { cancelIcon, checkIcon } from "@progress/kendo-svg-icons";
import { Label } from "@progress/kendo-react-labels";
import { TextBox, TextBoxChangeEvent } from "@progress/kendo-react-inputs";
import { Button } from "@progress/kendo-react-buttons";
import { AppContext } from "../../../../contexts/appContext";

const LinksPage = React.memo(function LinksPage() {
  const { t } = useTranslation(["common", "link-page"]);
  const appContext = React.useContext(AppContext);
  if (!appContext) return null;

  const ldsContext = React.useContext(LDSContext);
  if (!ldsContext) return null;

  const { links, updateLink, deleteLink, addLink } = ldsContext;
  const [selected, setSelected] = React.useState<Link | null>(null);
  const [showAddDialog, setShowAddDialog] = React.useState(false);
  const [newBeginNodeID, setNewBeginNodeID] = React.useState("");
  const [newEndNodeID, setNewEndNodeID] = React.useState("");
  const [newLength, setNewLength] = React.useState("");

  const openAddDialog = () => setShowAddDialog(true);

  const handleEditLink = React.useCallback(
    async (link: LinkUpdate) => {
      if (!selected) return;
      updateLink(selected.ID, link);
    },
    [selected, updateLink],
  );

  const handleBeginNodeChange = React.useCallback((e: TextBoxChangeEvent) => {
    setNewBeginNodeID(String(e.value ?? ""));
  }, []);

  const handleEndNodeChange = React.useCallback((e: TextBoxChangeEvent) => {
    setNewEndNodeID(String(e.value ?? ""));
  }, []);

  const handleLengthChange = React.useCallback((e: TextBoxChangeEvent) => {
    setNewLength(String(e.value ?? ""));
  }, []);

  const confirmAdd = async () => {
    const showError = (message: string) =>
      appContext.showNotification({
        notificationType: { icon: true, style: "error" },
        message,
      });

    if (newBeginNodeID && !/^\d+$/.test(newBeginNodeID))
      return showError("Begin Node ID must be an integer");

    if (newEndNodeID && !/^\d+$/.test(newEndNodeID))
      return showError("End Node ID must be an integer");

    if (newLength && !/^\d+(\.\d+)?$/.test(newLength))
      return showError("Length must be a valid number");

    if (newBeginNodeID && newEndNodeID && newBeginNodeID === newEndNodeID)
      return showError("Begin and End Node cannot be the same");

    await addLink({
      BeginNodeID: newBeginNodeID === "" ? null : Number(newBeginNodeID),
      EndNodeID: newEndNodeID === "" ? null : Number(newEndNodeID),
      Length: newLength === "" ? null : Number(newLength),
    });

    setSelected(null);
    setShowAddDialog(false);
    setNewBeginNodeID("");
    setNewEndNodeID("");
    setNewLength("");
  };

  const handleDelete = async (link: Link) => {
    await deleteLink(link);
    setSelected(null);
  };

  const cancelAddLink = React.useCallback(() => {
    setShowAddDialog(false);
    setNewBeginNodeID("");
    setNewEndNodeID("");
    setNewLength("");
  }, []);

  return (
    <main className="links-page">
      <div className="links-grid-container">
        <Links
          links={links}
          selected={selected}
          onSelectLink={setSelected}
          openAddDialog={openAddDialog}
        />
      </div>

      <DetailPanel
        className={"links-detail-panel" + (selected ? "" : " no-selected")}
        flexGrow={1}
        extandable={false}
      >
        {selected ? (
          <LinksDetailPanel
            selected={selected}
            editLink={handleEditLink}
            deleteLink={handleDelete}
            openAddDialog={openAddDialog}
          />
        ) : (
          <Typography.p>{t("link-page:select_element_to_edit")}</Typography.p>
        )}
      </DetailPanel>

      {showAddDialog && (
        <Dialog
          title="Add new link"
          onClose={() => setShowAddDialog(false)}
          className="links-dialog"
        >
          <Label>Begin Node</Label>
          <TextBox value={newBeginNodeID} onChange={handleBeginNodeChange} />

          <Label>End Node</Label>
          <TextBox value={newEndNodeID} onChange={handleEndNodeChange} />

          <Label>Length</Label>
          <TextBox value={newLength} onChange={handleLengthChange} />

          <DialogActionsBar>
            <Button svgIcon={cancelIcon} onClick={cancelAddLink}>
              {t("common:cancel")}
            </Button>
            <Button
              svgIcon={checkIcon}
              themeColor="primary"
              onClick={confirmAdd}
            >
              {t("common:confirm")}
            </Button>
          </DialogActionsBar>
        </Dialog>
      )}
    </main>
  );
});

export default LinksPage;
