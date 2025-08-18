import React from "react";
import { useTranslation } from "react-i18next";
import { TrendDefBase } from "../../../../services/api";
import { TextBox, TextBoxChangeEvent } from "@progress/kendo-react-inputs";
import { Label } from "@progress/kendo-react-labels";
import {
  cancelIcon,
  pencilIcon,
  plusIcon,
  saveIcon,
} from "@progress/kendo-svg-icons";
import { Button } from "@progress/kendo-react-buttons";

export interface TrendDefConfigurationDetailPanelProps {
  trendDefs: TrendDefBase[];
  selected: TrendDefBase | null;
}

const TrendDefConfigurationDetailPanel = React.memo(
  function TrendDefConfigurationDetailPanel({
    trendDefs,
    selected,
  }: TrendDefConfigurationDetailPanelProps) {
    const { t } = useTranslation(["common", "config-page"]);

    const setSelectedData = React.useCallback(
      (selectedTrendDef: TrendDefBase) => {
        setTrendDefID(selectedTrendDef.ID);
        setTrendDefName(selectedTrendDef.Name ?? "");
      },
      []
    );

    const [inEdit, setInEdit] = React.useState<boolean>(false);

    const enterEdit = React.useCallback(() => {
      setInEdit(true);
    }, []);
    const cancelEdit = React.useCallback(() => {
      setInEdit(false);
      if (selected !== null) setSelectedData(selected);
    }, [selected, setSelectedData]);

    const [trendDefID, setTrendDefID] = React.useState<string | undefined>(
      selected?.ID
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
