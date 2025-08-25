import { Button } from "@progress/kendo-react-buttons";
import {
  DropDownList,
  DropDownListChangeEvent,
} from "@progress/kendo-react-dropdowns";
import {
  FlatColorPicker,
  FlatColorPickerChangeEvent,
  TextBox,
  TextBoxChangeEvent,
} from "@progress/kendo-react-inputs";
import { Label } from "@progress/kendo-react-labels";
import {
  cancelIcon,
  pencilIcon,
  plusIcon,
  saveIcon,
  trashIcon,
} from "@progress/kendo-svg-icons";
import React from "react";
import { useTranslation } from "react-i18next";
import { Trend, TrendDef, TrendGroup, Unit } from "../../../../services/api";
import { ParsedTrendType } from "./TrendConfigurationPage";
import { rgbaToHex } from "../../../../lib/utilis";
import { Dialog, DialogActionsBar } from "@progress/kendo-react-dialogs";

export interface TrendConfigurationDetailPanelProps {
  trendDefs: TrendDef[];
  trendGroups: TrendGroup[];
  units: Unit[];
  editTrend: (value: Trend) => Promise<void>;
  deleteTrend: (value: Trend) => Promise<void>;
  selected: ParsedTrendType | null;
  enterAddNewTrend: () => void;
}

const TrendConfigurationDetailPanel = React.memo(
  function TrendConfigurationDetailPanel({
    trendDefs,
    trendGroups,
    units,
    editTrend,
    deleteTrend,
    selected,
    enterAddNewTrend,
  }: TrendConfigurationDetailPanelProps) {
    const { t } = useTranslation(["common", "config-page"]);

    const setSelectedData = React.useCallback(
      (selectedTrend: ParsedTrendType) => {
        setTrendID(selectedTrend.ID);
        setTrendName(selectedTrend.Name!);
        setTrendType(
          trendDefs.find((def) => def.ID == selectedTrend.TrendDefID)!
        );
        setTrendGroup(
          trendGroups.find((group) => group.ID == selectedTrend.TrendGroupID)!
        );
        setTrendUnit(units.find((unit) => unit.ID == selectedTrend.UnitID));
        setTrendColor(selectedTrend.Color!);
      },
      [trendDefs, trendGroups]
    );

    const [inEdit, setInEdit] = React.useState<boolean>(false);

    const enterEdit = React.useCallback(() => {
      setInEdit(true);
    }, []);
    const cancelEdit = React.useCallback(() => {
      setInEdit(false);
      if (selected !== null) setSelectedData(selected);
    }, [selected, setSelectedData]);

    const [trendID, setTrendID] = React.useState<number | undefined>(
      selected?.ID
    );
    const [trendName, setTrendName] = React.useState<string | undefined>(
      selected?.Name!
    );
    const [trendType, setTrendType] = React.useState<TrendDef | undefined>(
      trendDefs.find((def) => def.ID == selected?.TrendDefID)
    );
    const [trendGroup, setTrendGroup] = React.useState<TrendGroup | undefined>(
      trendGroups.find((group) => group.ID == selected?.TrendGroupID)
    );
    const [trendUnit, setTrendUnit] = React.useState<Unit | undefined>(
      units.find((unit) => unit.ID == selected?.UnitID)
    );
    const [trendColor, setTrendColor] = React.useState<string | undefined>(
      selected?.Color!
    );

    React.useEffect(() => {
      if (selected !== null) setSelectedData(selected);
    }, [selected]);

    const handleTrendNameChange = React.useCallback(
      (event: TextBoxChangeEvent) => {
        if (event.value) setTrendName(event.value.toString());
      },
      []
    );
    const handleTrendTypeChange = React.useCallback(
      (event: DropDownListChangeEvent) => {
        if (event.value) setTrendType(event.value);
      },
      []
    );
    const handleTrendGroupChange = React.useCallback(
      (event: DropDownListChangeEvent) => {
        if (event.value) setTrendGroup(event.value);
      },
      []
    );
    const handleTrendUnitChange = React.useCallback(
      (event: DropDownListChangeEvent) => {
        if (event.value) setTrendUnit(event.value);
      },
      []
    );
    const handleTrendColorChange = React.useCallback(
      (event: FlatColorPickerChangeEvent) => {
        if (event.value) setTrendColor(rgbaToHex(event.value)!.slice(0, 7)); //slice to cut off opacity
      },
      []
    );

    const saveEdit = React.useCallback(async () => {
      const newTrend: Trend = {
        ID: trendID!,
        Name: trendName!,
        TrendDefID: trendType!.ID,
        TrendGroupID: trendGroup!.ID,
        UnitID: trendUnit!.ID!,
        Color: trendColor!,
        RawMin: 0,
        RawMax: 0,
        ScaledMin: 0,
        ScaledMax: 0,
      };
      await editTrend(newTrend);
      setInEdit(false);
    }, [
      editTrend,
      trendID,
      trendName,
      trendType,
      trendGroup,
      trendUnit,
      trendColor,
    ]);

    // Deletion dialog
    const [showDialog, setShowDialog] = React.useState<boolean>(false);
    const openDialog = React.useCallback(() => {
      setShowDialog(true);
    }, []);
    const closeDialog = React.useCallback(() => {
      setShowDialog(false);
    }, []);

    const confirmDeletion = React.useCallback(async () => {
      const { trendType, trendGroup, ...selectedTrend } = selected!;
      await deleteTrend(selectedTrend);
      setInEdit(false);
    }, [selected, deleteTrend]);

    return (
      <div className="detail-panel-content">
        <div className="item">
          <div className="item-column">
            <div>
              <Label editorId="trendName">{t("config-page:name")}</Label>
              <TextBox
                value={trendName}
                onChange={handleTrendNameChange}
                disabled={!inEdit}
              />
            </div>
            <div>
              <Label editorId="trendType">{t("config-page:trend_type")}</Label>
              <DropDownList
                id="trendType"
                data={trendDefs}
                textField="Name"
                dataItemKey="ID"
                value={trendType}
                onChange={handleTrendTypeChange}
                disabled={!inEdit}
              />
            </div>
            <div>
              <Label editorId="trendGroup">
                {t("config-page:trend_group")}
              </Label>
              <DropDownList
                id="trendGroup"
                data={trendGroups}
                textField="Name"
                dataItemKey="ID"
                value={trendGroup}
                onChange={handleTrendGroupChange}
                disabled={!inEdit}
              />
            </div>
            <div>
              <Label editorId="trendUnit">{t("config-page:unit")}</Label>
              <DropDownList
                id="trendUnit"
                data={units}
                textField="Symbol"
                dataItemKey="ID"
                value={trendUnit}
                onChange={handleTrendUnitChange}
                disabled={!inEdit}
              />
            </div>
            <div style={{ display: "flex", flexDirection: "column" }}>
              <Label editorId="trendColor">{t("config-page:color")}</Label>
              <FlatColorPicker
                id="trendColor"
                format="hex"
                value={trendColor}
                onChange={handleTrendColorChange}
                disabled={!inEdit}
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
              <Button svgIcon={plusIcon} onClick={enterAddNewTrend}>
                {t("config-page:add_new_trend")}
              </Button>
            </div>
          ) : (
            <div className="item-row">
              <Button svgIcon={cancelIcon} onClick={cancelEdit}>
                {t("common:cancel")}
              </Button>
              <Button svgIcon={trashIcon} onClick={openDialog}>
                {t("common:delete")}
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
        {showDialog && (
          <Dialog title={t("common:confirm_deletion")} onClose={closeDialog}>
            {t("config-page:sure_you_want_delete_trend")}
            <DialogActionsBar>
              <Button svgIcon={cancelIcon} onClick={closeDialog}>
                {t("common:cancel")}
              </Button>
              <Button
                svgIcon={trashIcon}
                onClick={confirmDeletion}
                themeColor={"primary"}
              >
                {t("common:delete")}
              </Button>
            </DialogActionsBar>
          </Dialog>
        )}
      </div>
    );
  }
);

export default TrendConfigurationDetailPanel;
