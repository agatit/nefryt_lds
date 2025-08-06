import React from "react";
import { useTranslation } from "react-i18next";
import { TrendDefBase, Unit } from "../../../../services/api";
import { TextBox, TextBoxChangeEvent } from "@progress/kendo-react-inputs";
import { Label } from "@progress/kendo-react-labels";
import {
  cancelIcon,
  pencilIcon,
  plusIcon,
  saveIcon,
} from "@progress/kendo-svg-icons";
import { Button } from "@progress/kendo-react-buttons";

export interface TrendUnitConfigurationDetailPanelProps {
  units: Unit[];
  setUnits: (value: Unit[]) => void;
  selected: Unit | null;
  enterAddNewUnit: () => void;
}

const TrendUnitConfigurationDetailPanel = React.memo(
  function TrendUnitConfigurationDetailPanel({
    units,
    setUnits,
    selected,
    enterAddNewUnit,
  }: TrendUnitConfigurationDetailPanelProps) {
    const { t } = useTranslation(["common", "config-page"]);

    const setSelectedData = React.useCallback((selectedUnit: Unit) => {
      setUnitID(selectedUnit.ID);
      setUnitName(selectedUnit.Name!);
      setUnitSymbol(selectedUnit.Symbol!);
      setUnitMultiplier(selectedUnit.Multiplier!);
    }, []);

    const [inEdit, setInEdit] = React.useState<boolean>(false);

    const enterEdit = React.useCallback(() => {
      setInEdit(true);
    }, []);
    const cancelEdit = React.useCallback(() => {
      setInEdit(false);
      if (selected !== null) setSelectedData(selected);
    }, [selected, setSelectedData]);

    const [unitID, setUnitID] = React.useState<string | undefined>();
    const [unitName, setUnitName] = React.useState<string | undefined>();
    const [unitSymbol, setUnitSymbol] = React.useState<string | undefined>();
    const [unitMultiplier, setUnitMultiplier] = React.useState<
      string | undefined
    >();

    const handleUnitNameChange = React.useCallback(
      (event: TextBoxChangeEvent) => {
        if (event.value) setUnitName(event.value.toString());
      },
      []
    );
    const handleUnitSymbolChange = React.useCallback(
      (event: TextBoxChangeEvent) => {
        if (event.value) setUnitSymbol(event.value.toString());
      },
      []
    );
    const handleUnitMultiplierChange = React.useCallback(
      (event: TextBoxChangeEvent) => {
        if (event.value) setUnitMultiplier(event.value.toString());
      },
      []
    );

    React.useEffect(() => {
      if (selected !== null) setSelectedData(selected);
    }, [selected]);

    const saveEdit = React.useCallback(() => {
      const newUnit: Unit = {
        ID: unitID!,
        Name: unitName,
        Symbol: unitSymbol,
        Multiplier: unitMultiplier,
      };

      setUnits(
        units.map((unit) => {
          if (unit.ID == newUnit.ID) return newUnit;
          return unit;
        })
      );
      setInEdit(false);
    }, [units, setUnits, unitID, unitName, unitSymbol, unitMultiplier]);

    return (
      <div className="detail-panel-content">
        <div className="item">
          <div className="item-column">
            <div>
              <Label editorId="unitName">{t("config-page:name")}</Label>
              <TextBox
                id="unitName"
                value={unitName}
                onChange={handleUnitNameChange}
              />
            </div>
            <div>
              <Label editorId="unitSymbol">{t("config-page:symbol")}</Label>
              <TextBox
                id="unitSymbol"
                value={unitSymbol}
                onChange={handleUnitSymbolChange}
              />
            </div>
            <div>
              <Label editorId="unitMultiplier">
                {t("config-page:multiplier")}
              </Label>
              <TextBox
                id="unitMultiplier"
                value={unitMultiplier}
                onChange={handleUnitMultiplierChange}
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
              <Button svgIcon={plusIcon} onClick={enterAddNewUnit}>
                {t("config-page:add_new_unit")}
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

export default TrendUnitConfigurationDetailPanel;
