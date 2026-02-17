import React from "react";
import { useTranslation } from "react-i18next";
import { MethodDef } from "../../../../../../services/api";
import { TextBox } from "@progress/kendo-react-inputs";
import { Label } from "@progress/kendo-react-labels";
import { AppContext } from "../../../../../../contexts/appContext";

export interface Props {
  selected: MethodDef | null;
}

const MethodDefDetailPanel = React.memo(function MethodDefDetailPanel({
  selected,
}: Props) {
  const appContext = React.useContext(AppContext);
  const { t } = useTranslation(["common", "method-page"]);

  if (!appContext || !selected) return null;

  return (
    <div className="detail-panel-content">
      <div className="item-column">
        <div>
          <Label>{t("common:id")}</Label>
          <TextBox value={selected.ID} disabled />
        </div>

        <div>
          <Label>{t("common:name")}</Label>
          <TextBox value={selected.Name ?? ""} disabled />
        </div>
      </div>
    </div>
  );
});

export default MethodDefDetailPanel;
