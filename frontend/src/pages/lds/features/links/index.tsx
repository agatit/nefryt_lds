import React, { useCallback, useContext, useState } from "react";
import { DetailPanel } from "onyks_shared_kendo";
import { LDSContext } from "../../contexts/ldsContext";
import { AppContext } from "../../../../contexts/appContext";
import { Link, LinkUpdate } from "../../../../services/api";
import Links from "./components/Links/Links";
import LinksDetailPanel from "./components/Links/LinksDetailPanel";
import "./linkPage.scss";

const LinksPage: React.FC = () => {
  const appContext = useContext(AppContext);
  const ldsContext = useContext(LDSContext);

  if (!appContext || !ldsContext) {
    throw new Error("Context missing");
  }

  const { links, updateLink, deleteLink, addLink } = ldsContext;

  const [selected, setSelected] = useState<Link | null>(null);
  const [panelOpen, setPanelOpen] = useState(false);
  const [addMode, setAddMode] = useState(false);

  const handleEditLink = useCallback(
    async (id: number, value: LinkUpdate) => {
      await updateLink(id, value);
    },
    [updateLink],
  );

  const handleDelete = useCallback(
    async (link: Link) => {
      await deleteLink(link);
      setSelected(null);
    },
    [deleteLink],
  );

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
          openAddDialog={openAddPanel}
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
            deleteLink={handleDelete}
            addLink={addLink}
            addMode={addMode}
            setAddMode={setAddMode}
          />
        )}
      </DetailPanel>
    </main>
  );
};

export default LinksPage;
