import { memo, useContext } from "react";
import { useTranslation } from "react-i18next";
import { MethodDef } from "../../../../../../services/api";
import { TextBox } from "@progress/kendo-react-inputs";
import { Label } from "@progress/kendo-react-labels";
import { AppContext } from "../../../../../../contexts/appContext";

export interface Props {
  selected: MethodDef | null;
}

const MethodDefDetailPanel = memo(function MethodDefDetailPanel({
  selected,
}: Props) {
  const appContext = useContext(AppContext);
  const { t } = useTranslation(["methods-page"]);

  if (!appContext || !selected) return null;

  return (
    <div className="detail-panel-content">
      <div className="item-column">
        <div>
          <Label>{t("methods-page:id")}</Label>
          <TextBox value={selected.ID} disabled />
        </div>

        <div>
          <Label>{t("methods-page:name")}</Label>
          <TextBox value={selected.Name ?? ""} disabled />
        </div>
      </div>
    </div>
  );
});

export default MethodDefDetailPanel;
