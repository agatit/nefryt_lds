import React from "react";
import "../../../../styles/features/lds/features/eventsPage.scss";
import { DetailPanel } from "onyks_shared_kendo";
import { Typography } from "@progress/kendo-react-common";
import { useTranslation } from "react-i18next";
import { LDSContext } from "../../contexts/ldsContext";
import Events from "./components/Events";
import { Event as ApiEvent } from "../../../../services/api";
import {
  Splitter,
  SplitterOnChangeEvent,
  SplitterPaneProps,
  TabStrip,
  TabStripSelectEventArguments,
  TabStripTab,
} from "@progress/kendo-react-layout";
import type { EventDef as EventDefType } from "../../../../services/api";
import EventsDef from "./components/EventsDef";
import EventsDefDetailsPanel from "./components/EventsDefDetailPanel";
import EventsDetailPanel from "./components/EventsDetailPanel";

export interface SelectionType {
  events: ApiEvent | null;
  eventDef: EventDefType | null;
}

const EventsPage = React.memo(function EventsPage() {
  const { t } = useTranslation(["events-page"]);
  const ldsContext = React.useContext(LDSContext);

  if (!ldsContext) return null;

  const { events, eventDefs } = ldsContext;
  const [tabSelected, setTabSelected] = React.useState<number>(0);
  const [selected, setSelected] = React.useState<ApiEvent | null>(null);
  const [showDialog, setShowDialog] = React.useState(false);
  const openDialog = () => setShowDialog(true);
  const closeDialog = () => setShowDialog(false);

  const [selection, setSelection] = React.useState<SelectionType>({
    events: null,
    eventDef: null,
  });

  const handleTabSelect = React.useCallback(
    (e: TabStripSelectEventArguments) => {
      setTabSelected(e.selected);
    },
    [],
  );

  const [verticalPanes, setVerticalPanes] = React.useState<SplitterPaneProps[]>(
    [{ size: "66%" }, {}],
  );

  const handleVerticalChange = (event: SplitterOnChangeEvent) => {
    setVerticalPanes(event.newState);
  };

  const [showAddNewEventDefDialog, setShowAddNewEventDefDialog] =
    React.useState(false);

  const openAddNewEventDefDialog = React.useCallback(() => {
    setShowAddNewEventDefDialog(true);
  }, []);

  const closeAddNewEventDefDialog = React.useCallback(() => {
    setShowAddNewEventDefDialog(false);
  }, []);

  const handleSelectedEventDefChange = React.useCallback(
    (value: EventDefType | null) => {
      setSelected(null);
      setSelection((prev) => ({
        ...prev,
        eventDef: value,
      }));
    },
    [],
  );

  const handleEventSelection = React.useCallback((event: ApiEvent) => {
    setSelection((prev) => ({ ...prev, eventDef: null }));
    setSelected(event);
  }, []);

  return (
    <main className="events-page">
      <Splitter
        className="config-grid-container"
        panes={verticalPanes}
        orientation="vertical"
        onChange={handleVerticalChange}
      >
        <div className="events-grid-container">
          <Events
            events={events}
            selected={selected}
            onSelectEvent={handleEventSelection}
            showDialog={showDialog}
            openDialog={openDialog}
            closeDialog={closeDialog}
            eventDefs={eventDefs}
          />
        </div>

        <TabStrip
          className="events-stuff-tab"
          selected={tabSelected}
          onSelect={handleTabSelect}
        >
          <TabStripTab title={t("event-page:events_types")}>
            <EventsDef
              showDialog={showAddNewEventDefDialog}
              openDialog={openAddNewEventDefDialog}
              closeDialog={closeAddNewEventDefDialog}
              eventDefs={ldsContext.eventDefs}
              addEventDef={ldsContext.addEventDef}
              deleteEventDef={ldsContext.deleteEventDef}
              selected={selection.eventDef}
              setSelected={handleSelectedEventDefChange}
            />
          </TabStripTab>
        </TabStrip>
      </Splitter>

      <DetailPanel
        className={
          "events-detail-panel" +
          (!selected && !selection.eventDef ? " no-selected" : "")
        }
        flexGrow={1}
        extandable={false}
      >
        {selected ? (
          <EventsDetailPanel selected={selected} />
        ) : selection.eventDef ? (
          <EventsDefDetailsPanel
            selected={selection.eventDef}
            editEventDef={ldsContext?.updateEventDef}
            deleteEventDef={ldsContext?.deleteEventDef}
            enterAddNewEventDef={openAddNewEventDefDialog}
          />
        ) : (
          <Typography.p>{t("events-page:select_element_to_edit")}</Typography.p>
        )}
      </DetailPanel>
    </main>
  );
});

export default EventsPage;
