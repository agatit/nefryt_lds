import React from "react";
import { useTranslation } from "react-i18next";
import { TrendDefBase } from "../../../../services/api";
import { TextBox, TextBoxChangeEvent } from "@progress/kendo-react-inputs";
import { Label } from "@progress/kendo-react-labels";

export interface TrendDefConfigurationDetailPanelProps {
  selected: TrendDefBase | null;
}

const TrendDefConfigurationDetailPanel = React.memo(
  function TrendDefConfigurationDetailPanel({
    selected,
  }: TrendDefConfigurationDetailPanelProps) {
    const { t } = useTranslation(["common", "config-page"]);

    const setSelectedData = React.useCallback(
      (selectedTrendDef: TrendDefBase) => {
        setTrendDefName(selectedTrendDef.Name ?? "");
      },
      []
    );
    const [trendDefName, setTrendDefName] = React.useState<string | undefined>(
      selected?.Name ?? ""
    );

    React.useEffect(() => {
      if (selected !== null) setSelectedData(selected);
    }, [selected]);

    const handleTrendDefNameChange = React.useCallback(
      (event: TextBoxChangeEvent) => {
        if (event.value) setTrendDefName(event.value.toString());
      },
      []
    );

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
  }
);

export default TrendDefConfigurationDetailPanel;
