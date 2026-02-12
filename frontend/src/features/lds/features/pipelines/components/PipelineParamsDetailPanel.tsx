import React from "react";
import { useTranslation } from "react-i18next";
import { PipelineParam } from "../../../../../services/api";
import { TextBox } from "@progress/kendo-react-inputs";
import { Label } from "@progress/kendo-react-labels";

export interface PipelineParamDetailPanelProps {
  selected: PipelineParam | null;
  deleteParam?: (value: PipelineParam) => Promise<void>;
}

const PipelineParamDetailPanel = React.memo(function PipelineParamDetailPanel({
  selected,
}: PipelineParamDetailPanelProps) {
  const { t } = useTranslation(["common", "pipeline-page"]);

  React.useEffect(() => {
    if (!selected) return;
  }, [selected]);

  if (!selected) {
    return (
      <div className="detail-panel-content">{t("common:no_selection")}</div>
    );
  }

  return (
    <div className="detail-panel-content">
      <div className="item-column">
        <Label>Param ID</Label>
        <TextBox value={selected.PipelineParamDefID} disabled />

        <Label>Name</Label>
        <TextBox value={selected.Name ?? ""} disabled />

        <Label>Value</Label>
        <TextBox value={selected.Value ?? ""} disabled />

        <Label>DataType</Label>
        <TextBox value={selected.DataType ?? ""} disabled />
      </div>
    </div>
  );
});

export default PipelineParamDetailPanel;
