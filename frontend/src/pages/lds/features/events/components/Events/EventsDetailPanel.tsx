import React from "react";
import { useTranslation } from "react-i18next";
import { Label } from "@progress/kendo-react-labels";
import { TextBox } from "@progress/kendo-react-inputs";
import { Event as ApiEvent } from "../../../../../../services/api";

export interface EventsDetailPanelProps {
  selected: ApiEvent;
}

const EventsDetailPanel = React.memo(function EventsDetailPanel({
  selected,
}: EventsDetailPanelProps) {
  const { t } = useTranslation(["events-page"]);

  return (
    <div className="detail-panel-content">
      <div className="item">
        <div className="item-column">
          <div>
            <Label>{t("events-page:event_def_id")}</Label>
            <TextBox value={String(selected.EventDefID)} disabled />
          </div>
          <div>
            <Label>{t("events-page:method")}</Label>
            <TextBox value={String(selected.MethodID ?? "")} disabled />
          </div>
          <div>
            <Label>{t("events-page:begin_date")}</Label>
            <TextBox
              value={
                selected.BeginDate
                  ? new Date(selected.BeginDate).toLocaleString()
                  : ""
              }
              disabled
            />
          </div>
          <div>
            <Label>{t("events-page:ack_date")}</Label>
            <TextBox
              value={
                selected.AckDate
                  ? new Date(selected.AckDate).toLocaleString()
                  : t("events-page:not_acknowledged")
              }
              disabled
            />
          </div>
          <div>
            <Label>{t("events-page:end_date")}</Label>
            <TextBox
              value={
                selected.EndDate
                  ? new Date(selected.EndDate).toLocaleString()
                  : ""
              }
              disabled
            />
          </div>
          <div>
            <Label>{t("events-page:details")}</Label>
            <TextBox value={selected.Details ?? ""} disabled />
          </div>
          <div>
            <Label>{t("events-page:position")}</Label>
            <TextBox value={String(selected.Position ?? "")} disabled />
          </div>
          <div>
            <Label>{t("events-page:verbosity")}</Label>
            <TextBox value={selected.Verbosity ?? ""} disabled />
          </div>
          <div>
            <Label>{t("events-page:caption")}</Label>
            <TextBox value={selected.Caption ?? ""} disabled />
          </div>
          <div>
            <Label>{t("events-page:silent")}</Label>
            <TextBox
              value={
                selected.Silent ? t("events-page:yes") : t("events-page:no")
              }
              disabled
            />
          </div>
        </div>
      </div>
    </div>
  );
});

export default EventsDetailPanel;
