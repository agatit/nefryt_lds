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
  setTrendDefs: (value: TrendDefBase[]) => void;
  selected: TrendDefBase | null;
  enterAddNewTrendDef: () => void;
}

const TrendDefConfigurationDetailPanel = React.memo(
  function TrendDefConfigurationDetailPanel({
    trendDefs,
    setTrendDefs,
    selected,
    enterAddNewTrendDef,
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

    const saveEdit = React.useCallback(() => {
      const newTrendDef: TrendDefBase = {
        ID: trendDefID!,
        Name: trendDefName!,
      };

      setTrendDefs(
        trendDefs.map((trendDef) => {
          if (trendDef.ID == newTrendDef.ID) return newTrendDef;
          return trendDef;
        })
      );
      setInEdit(false);
    }, [trendDefs, setTrendDefs, trendDefID, trendDefName]);

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
              />
            </div>
          </div>
        </div>
        <div className="separator" />
        <div className="item">
          {!inEdit ? (
            <div className="item-row">
              <Button svgIcon={pencilIcon} onClick={enterEdit}>
                {t("common:edit")}
              </Button>
              <Button svgIcon={plusIcon} onClick={enterAddNewTrendDef}>
                {t("config-page:add_new_trend_type")}
              </Button>
            </div>
          ) : (
            <div className="item-row">
              <Button svgIcon={cancelIcon} onClick={cancelEdit}>
                {t("common:cancel")}
              </Button>
              <Button
                svgIcon={saveIcon}
                onClick={saveEdit}
                themeColor={"primary"}
              >
                {t("common:save")}
              </Button>
            </div>
          )}
        </div>
      </div>
    );
  }
);

export default TrendDefConfigurationDetailPanel;
