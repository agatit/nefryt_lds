import { useContext, useState, useCallback } from "react";
import "./templatePage.scss";
import { useTranslation } from "react-i18next";
import Templates from "./components/Templates";
import TemplatesDetailPanel from "./components/TemplatesDetailPage";
import { LDSContext } from "../../contexts/ldsContext";
import { DetailPanel } from "onyks_shared_kendo";
import { Dialog, DialogActionsBar } from "@progress/kendo-react-dialogs";
import { Button } from "@progress/kendo-react-buttons";
import { Template } from "../../../../services/api";
import { AppContext } from "../../../../contexts/appContext";

const TemplatePage = () => {
  const { t } = useTranslation(["common", "template-page"]);
  const [selected, setSelected] = useState<Template | null>(null);
  const [panelOpen, setPanelOpen] = useState(false);
  const [addMode, setAddMode] = useState(false);
  const [deleteTarget, setDeleteTarget] = useState<Template | null>(null);
  const isSelected = addMode || !!selected;
  const appContext = useContext(AppContext);
  const lds = useContext(LDSContext);

  if (!appContext || !lds) return null;

  const { templates, addTemplate, updateTemplate, deleteTemplate } = lds;

  const openAddMode = () => {
    setSelected(null);
    setAddMode(true);
    setPanelOpen(true);
  };

  const handleSelectTemplate = useCallback((value: Template | null) => {
    setAddMode(false);

    if (value) {
      setSelected(value);
      setPanelOpen(true);
    }
  }, []);

  const confirmDelete = async () => {
    if (!deleteTarget) return;

    try {
      await deleteTemplate(deleteTarget.ID);
      setSelected(null);
      setPanelOpen(false);
    } finally {
      setDeleteTarget(null);
    }
  };

  return (
    <main className="templates-page">
      <div className="links-grid-container">
        <Templates
          templates={templates}
          selected={selected}
          onSelectTemplate={handleSelectTemplate}
          openAddPanel={openAddMode}
        />
      </div>

      <DetailPanel
        className={
          "templates-detail-panel" + (isSelected ? "" : " no-selected")
        }
        flexGrow={1}
        extandable
        extended={panelOpen}
        onExtendedChange={setPanelOpen}
      >
        {(selected || addMode) && (
          <TemplatesDetailPanel
            selected={selected}
            addMode={addMode}
            setAddMode={setAddMode}
            addTemplate={addTemplate}
            updateTemplate={updateTemplate}
            requestDelete={(t) => setDeleteTarget(t)}
            closePanel={() => setPanelOpen(false)}
          />
        )}
      </DetailPanel>

      {deleteTarget && (
        <Dialog
          title={t("common:confirm_deletion")}
          onClose={() => setDeleteTarget(null)}
        >
          {t("template-page:delete_template")}
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
};

export default TemplatePage;
