import React, { useCallback, useContext, useState } from "react";
import { DetailPanel } from "onyks_shared_kendo";
import { Dialog, DialogActionsBar } from "@progress/kendo-react-dialogs";
import { Button } from "@progress/kendo-react-buttons";
import { useTranslation } from "react-i18next";
import { LDSContext } from "../../contexts/ldsContext";
import { AppContext } from "../../../../contexts/appContext";
import { Link, LinkUpdate } from "../../../../services/api";
import Links from "./components/Links/Links";
import LinksDetailPanel from "./components/Links/LinksDetailPanel";
import "./linkPage.scss";

const LinksPage = React.memo(function LinksPage() {
  const { t } = useTranslation(["common, links-page"]);
  const appContext = useContext(AppContext);
  const ldsContext = useContext(LDSContext);

  if (!appContext || !ldsContext) return null;

  const { links, updateLink, deleteLink, addLink } = ldsContext;
  const [selected, setSelected] = useState<Link | null>(null);
  const [panelOpen, setPanelOpen] = useState(false);
  const [addMode, setAddMode] = useState(false);
  const [showDeleteDialog, setShowDeleteDialog] = useState(false);

  const handleEditLink = useCallback(
    async (id: number, value: LinkUpdate) => {
      await updateLink(id, value);
    },
    [updateLink],
  );

  const requestDelete = useCallback((link: Link) => {
    setSelected(link);
    setShowDeleteDialog(true);
  }, []);

  const confirmDelete = useCallback(async () => {
    if (!selected) return;

    try {
      await deleteLink(selected);
      setSelected(null);
      setPanelOpen(false);
    } finally {
      setShowDeleteDialog(false);
    }
  }, [selected, deleteLink]);

  const openAddPanel = useCallback(() => {
    setSelected(null);
    setAddMode(true);
    setPanelOpen(true);
  }, []);

  const handleSelectLink = useCallback((link: Link) => {
    setAddMode(false);
    setSelected(link);
    setPanelOpen(true);
  }, []);

  return (
    <main className="links-page">
      <div className="links-grid-container">
        <Links
          links={links}
          selected={selected}
          onSelectLink={handleSelectLink}
          openAddPanel={openAddPanel}
          requestDelete={requestDelete}
        />
      </div>

      <DetailPanel
        className={"links-detail-panel" + (selected ? "" : " no-selected")}
        flexGrow={1}
        extandable
        extended={panelOpen}
        onExtendedChange={setPanelOpen}
      >
        {(selected || addMode) && (
          <LinksDetailPanel
            selected={selected}
            editLink={handleEditLink}
            requestDelete={requestDelete}
            addLink={addLink}
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
          {t("links-page:delete_link")}
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

export default LinksPage;
