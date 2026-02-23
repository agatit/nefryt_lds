import { memo, useState, useCallback, useEffect } from "react";
import { useTranslation } from "react-i18next";
import { TrendDef } from "../../../../../../services/api";
import { TextBox, TextBoxChangeEvent } from "@progress/kendo-react-inputs";
import { Label } from "@progress/kendo-react-labels";

export interface TrendDefConfigurationDetailPanelProps {
  selected: TrendDef | null;
}

const TrendDefConfigurationDetailPanel = memo(
  function TrendDefConfigurationDetailPanel({
    selected,
  }: TrendDefConfigurationDetailPanelProps) {
    const { t } = useTranslation(["common", "config-page"]);
    const [trendDefName, setTrendDefName] = useState<string | undefined>(
      selected?.Name ?? "",
    );

    const setSelectedData = useCallback((selectedTrendDef: TrendDef) => {
      setTrendDefName(selectedTrendDef.Name ?? "");
    }, []);

    const handleTrendDefNameChange = useCallback(
      (event: TextBoxChangeEvent) => {
        if (event.value) setTrendDefName(event.value.toString());
      },
      [],
    );

    useEffect(() => {
      if (selected !== null) setSelectedData(selected);
    }, [selected]);

    return (
      <div className="detail-panel-content">
        <div className="item">
          <div className="item-column">
            <div>
              <Label editorId="trendDefName">{t("config-page:name")}</Label>
              <TextBox
                id="trendDefName"
                value={trendDefName}
                onChange={handleTrendDefNameChange}
                disabled={true}
              />
            </div>
          </div>
        </div>
        <div className="separator" />
      </div>
    );
  },
);

export default TrendDefConfigurationDetailPanel;
