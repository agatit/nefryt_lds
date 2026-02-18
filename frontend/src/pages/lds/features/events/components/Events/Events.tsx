import React from "react";
import { useTranslation } from "react-i18next";
import {
  Grid,
  GridColumn,
  GridSearchBox,
  GridToolbar,
  GridSelectionChangeEvent,
  GridCellProps,
} from "@progress/kendo-react-grid";
import { SelectDescriptor } from "@progress/kendo-react-data-tools";
import { Event as ApiEvent } from "../../../../../../services/api";

interface EventsProps {
  events: ApiEvent[];
  selected: ApiEvent | null;
  onSelectEvent: (value: ApiEvent) => void;
  showDialog: boolean;
  openDialog: () => void;
  closeDialog: () => void;
}

const Events = React.memo(function EventsGrid({
  events,
  selected,
  onSelectEvent,
}: EventsProps) {
  const { t } = useTranslation(["events-page"]);
  const [select, setSelect] = React.useState<SelectDescriptor>();

  const handleSelectionChange = React.useCallback(
    (event: GridSelectionChangeEvent) => {
      const item: ApiEvent = event.endDataItem;
      onSelectEvent(item);
      setSelect(event.select);
    },
    [onSelectEvent],
  );

  React.useEffect(() => {
    if (selected == null) setSelect({});
  }, [selected]);

  return (
    <Grid
      data={events}
      dataItemKey="ID"
      autoProcessData
      sortable
      filterable
      selectable={{ enabled: true, mode: "single" }}
      select={select}
      onSelectionChange={handleSelectionChange}
    >
      <GridToolbar>
        <GridSearchBox />
      </GridToolbar>
      <GridColumn field="EventDefID" title={t("events-page:event_def_id")} />
      <GridColumn field="MethodID" title={t("events-page:method")} />
      <GridColumn
        field="BeginDate"
        title={t("events-page:begin_date")}
        cells={{
          data: (props: GridCellProps) => (
            <td>
              {props.dataItem.BeginDate
                ? new Date(props.dataItem.BeginDate).toLocaleString()
                : ""}
            </td>
          ),
        }}
      />
      <GridColumn field="AckDate" title={t("events-page:ack_date")} />
      <GridColumn field="EndDate" title={t("events-page:end_date")} />
      <GridColumn field="Details" title={t("events-page:details")} />
      <GridColumn field="Position" title={t("events-page:position")} />
      <GridColumn field="Verbosity" title={t("events-page:verbosity")} />
      <GridColumn field="Caption" title={t("events-page:caption")} />
      <GridColumn
        field="Silent"
        title={t("events-page:silent")}
        cells={{
          data: (props: GridCellProps) => (
            <td>
              {props.dataItem.Silent
                ? t("events-page:yes")
                : t("events-page:no")}
            </td>
          ),
        }}
      />
    </Grid>
  );
});

export default Events;
