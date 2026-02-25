import { useCallback, useContext, useState, memo } from "react";
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

type AddModeType = "link" | null;

interface SelectionType {
  link: Link | null;
}

const LinksPage = memo(function LinksPage() {
  const { t } = useTranslation(["common", "links-page"]);
  const appContext = useContext(AppContext);
  const ldsContext = useContext(LDSContext);

  if (!appContext || !ldsContext) return null;

  const { links, updateLink, deleteLink, addLink } = ldsContext;

  const [panelOpen, setPanelOpen] = useState(false);
  const [addMode, setAddMode] = useState<AddModeType>(null);
  const [deleteTarget, setDeleteTarget] = useState<Link | null>(null);

  const [selection, setSelection] = useState<SelectionType>({
    link: null,
  });

  const clearSelection = () => setSelection({ link: null });

  const openAddMode = () => {
    clearSelection();
    setAddMode("link");
    setPanelOpen(true);
  };

  const handleSelectLink = useCallback((value: Link | null) => {
    setAddMode(null);
    clearSelection();

    if (value) {
      setSelection({ link: value });
      setPanelOpen(true);
    }
  }, []);

  const requestDelete = useCallback((link: Link) => {
    setDeleteTarget(link);
  }, []);

  const confirmDelete = useCallback(async () => {
    if (!deleteTarget) return;

    try {
      await deleteLink(deleteTarget);
      clearSelection();
      setPanelOpen(false);
    } finally {
      setDeleteTarget(null);
    }
  }, [deleteTarget, deleteLink]);

  const handleEditLink = useCallback(
    async (id: number, value: LinkUpdate) => {
      await updateLink(id, value);
    },
    [updateLink],
  );

  const isSelected = addMode !== null || selection.link;

  const SelectedDetailPanel = () => {
    if (selection.link || addMode === "link") {
      return (
        <LinksDetailPanel
          selected={selection.link}
          editLink={handleEditLink}
          requestDelete={requestDelete}
          addLink={addLink}
          addMode={addMode === "link"}
          setAddMode={(v) => setAddMode(v ? "link" : null)}
          closePanel={() => setPanelOpen(false)}
        />
      );
    }

    return null;
  };

  return (
    <main className="links-page">
      <div className="links-grid-container">
        <Links
          links={links}
          selected={selection.link}
          onSelectLink={handleSelectLink}
          openAddPanel={openAddMode}
          requestDelete={requestDelete}
        />
      </div>

      <DetailPanel
        className={"links-detail-panel" + (isSelected ? "" : " no-selected")}
        flexGrow={1}
        extandable
        extended={panelOpen}
        onExtendedChange={setPanelOpen}
      >
        {isSelected && <SelectedDetailPanel />}
      </DetailPanel>

      {deleteTarget && (
        <Dialog
          title={t("common:confirm_deletion")}
          onClose={() => setDeleteTarget(null)}
        >
          {t("links-page:delete_link")}
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

export default LinksPage;
