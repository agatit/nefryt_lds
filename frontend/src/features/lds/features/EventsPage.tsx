import React from "react";
import "../../../styles/features/lds/features/eventsPage.scss";
import {
  Grid,
  GridColumn,
  GridSearchBox,
  GridToolbar,
} from "@progress/kendo-react-grid";
import { DetailPanel } from "onyks_shared_kendo";
import { EventOut } from "../../../services/api";
import { AuthContext } from "../../../contexts/authContext";
import { useRefreshableRequest } from "../../../hooks/useRefreshableRequest";
import { useTranslation } from "react-i18next";
import { Typography } from "@progress/kendo-react-common";

export interface ParsedEventType extends EventOut {}

const EventsPage = React.memo(function EventsPage() {
  const auth = React.useContext(AuthContext);
  const refreshableRequest = useRefreshableRequest();
  const { t } = useTranslation(["common", "events-page"]);

  const [selected, setSelected] = React.useState<ParsedEventType | null>(null);

  return (
    <React.Fragment>
      <main className="events-page">
        <div className="events-grid-container">
          <Grid>
            <GridToolbar>
              <GridSearchBox />
            </GridToolbar>
            <GridColumn title={t("events-page:method")} />
            <GridColumn title={t("events-page:details")} />
            <GridColumn title={t("events-page:position")} />
            <GridColumn title={t("events-page:event_type")} />
            <GridColumn title={t("events-page:verbosity")} />
            <GridColumn title={t("events-page:caption")} />
            <GridColumn title={t("events-page:silient")} />
            <GridColumn title={t("events-page:begin_date")} />
            <GridColumn title={t("events-page:ack_date")} />
            <GridColumn title={t("events-page:end_date")} />
          </Grid>
        </div>
        <DetailPanel
          className={
            "events-detail-panel" + (selected !== null ? "" : " no-selected")
          }
          flexGrow={1}
          extandable={false}
        >
          {selected !== null ? (
            <></>
          ) : (
            <Typography.p style={{ marginBottom: 0 }}>
              {t("events-page:select_element_to_edit")}
            </Typography.p>
          )}
        </DetailPanel>
      </main>
    </React.Fragment>
  );
});

export default EventsPage;
