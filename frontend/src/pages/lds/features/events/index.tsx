import React from "react";
import { DetailPanel } from "onyks_shared_kendo";
import { LDSContext } from "../../contexts/ldsContext";
import { Event as ApiEvent } from "../../../../services/api";
import Events from "./components/Events/Events";
import EventsDetailPanel from "./components/Events/EventsDetailPanel";
import "./eventsPage.scss";

export interface SelectionType {
  events: ApiEvent | null;
}

const EventsPage = React.memo(function EventsPage() {
  const ldsContext = React.useContext(LDSContext);
  if (!ldsContext) return null;

  const { events } = ldsContext;
  const [selected, setSelected] = React.useState<ApiEvent | null>(null);
  const [showDialog, setShowDialog] = React.useState(false);
  const openDialog = () => setShowDialog(true);
  const closeDialog = () => setShowDialog(false);

  const [panelOpen, setPanelOpen] = React.useState(false);

  const handleEventSelection = React.useCallback((event: ApiEvent) => {
    setSelected(event);
    setPanelOpen(true);
  }, []);

  return (
    <main className="events-page">
      <div className="events-grid-container">
        <Events
          events={events}
          selected={selected}
          onSelectEvent={handleEventSelection}
          showDialog={showDialog}
          openDialog={openDialog}
          closeDialog={closeDialog}
        />
      </div>

      <DetailPanel
        className={"events-detail-panel" + (!selected ? "" : " no-selected")}
        flexGrow={1}
        extandable
        extended={panelOpen}
        onExtendedChange={setPanelOpen}
      >
        {selected ? <EventsDetailPanel selected={selected} /> : ""}
      </DetailPanel>
    </main>
  );
});

export default EventsPage;
