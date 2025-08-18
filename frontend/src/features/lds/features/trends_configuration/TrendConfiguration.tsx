import { Button, ButtonGroup } from "@progress/kendo-react-buttons";
import { Dialog, DialogActionsBar } from "@progress/kendo-react-dialogs";
import {
  DropDownList,
  DropDownListChangeEvent,
} from "@progress/kendo-react-dropdowns";
import {
  Grid,
  GridColumn,
  GridSearchBox,
  GridSelectionChangeEvent,
  GridToolbar,
} from "@progress/kendo-react-grid";
import {
  FlatColorPicker,
  FlatColorPickerChangeEvent,
  TextBox,
  TextBoxChangeEvent,
} from "@progress/kendo-react-inputs";
import { Label } from "@progress/kendo-react-labels";
import { cancelIcon, checkIcon, plusIcon } from "@progress/kendo-svg-icons";
import React from "react";
import { ParsedTrendType } from "./TrendConfigurationPage";
import { useTranslation } from "react-i18next";
import {
  Trend,
  TrendDefBase,
  TrendGroup,
  Unit,
} from "../../../../services/api";
import { rgbaToHex } from "../../../../lib/utilis";
import ColorGridCell from "../../components/ColorGridCell";
import { SelectDescriptor } from "@progress/kendo-react-data-tools";

export interface TrendConfigurationProps {
  showDialog: boolean;
  openDialog: () => void;
  closeDialog: () => void;
  trendDefs: TrendDefBase[];
  trendGroups: TrendGroup[];
  units: Unit[];
  trends: Trend[];
  addTrend: (value: Trend) => Promise<void>;
  selected: ParsedTrendType | null;
  setSelected: (value: ParsedTrendType) => void;
}

const TrendConfiguration = React.memo(function TrendConfiguration({
  showDialog,
  openDialog,
  closeDialog,
  trendDefs,
  trendGroups,
  units,
  trends,
  addTrend,
  selected,
  setSelected,
}: TrendConfigurationProps) {
  const { t } = useTranslation(["common", "config-page"]);

  const data = React.useMemo((): ParsedTrendType[] => {
    return trends.map((trend): ParsedTrendType => {
      // const unit = units.find((unit) => unit.ID == trend.UnitID)!; //waiting for unit api fix
      return {
        ...trend,
        trendType: trendDefs.find((def) => def.ID == trend.TrendDefID)!.Name!,
        trendGroup: trendGroups.find((group) => group.ID == trend.TrendGroupID)!
          .Name!,
        // unit: unit.Name! + " " + unit.Symbol!, //waiting for unit api fix
      };
    });
  }, [trendDefs, trendGroups, trends]);

  const [select, setSelect] = React.useState<SelectDescriptor>();
  React.useEffect(() => {
    if (selected == null) setSelect({});
  }, [selected]);

  const handleSelectionChange = React.useCallback(
    (event: GridSelectionChangeEvent) => {
      const item: ParsedTrendType = event.endDataItem;
      setSelected(item);
      setSelect(event.select);
    },
    [setSelected]
  );

  const [trendName, setTrendName] = React.useState<string | undefined>();
  const [trendType, setTrendType] = React.useState<TrendDefBase | undefined>();
  const [trendGroup, setTrendGroup] = React.useState<TrendGroup | undefined>();
  const [trendUnit, setTrendUnit] = React.useState<Unit | undefined>();
  const [trendColor, setTrendColor] = React.useState<string | undefined>();

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

  const cancelAddNewTrend = React.useCallback(() => {
    setTrendName(undefined);
    setTrendType(undefined);
    setTrendGroup(undefined);
    setTrendUnit(undefined);
    setTrendColor(undefined);
    closeDialog();
  }, [closeDialog]);

  const confirmAddNewTrend = React.useCallback(async () => {
    const newTrend: Trend = {
      ID: trends.length + 100,
      Name: trendName!,
      TrendDefID: trendType!.ID,
      TrendGroupID: trendGroup!.ID,
      UnitID: trendUnit!.ID,
      Color: trendColor!,
      RawMin: 0,
      RawMax: 0,
      ScaledMin: 0,
      ScaledMax: 0,
    };
    await addTrend(newTrend);
    closeDialog();
  }, [
    closeDialog,
    addTrend,
    trends,
    trendName,
    trendType,
    trendGroup,
    trendUnit,
    trendColor,
  ]);

  return (
    <React.Fragment>
      <Grid
        data={data}
        dataItemKey="ID"
        autoProcessData={true}
        sortable={true}
        groupable={true}
        selectable={{ enabled: true, mode: "single" }}
        select={select}
        filterable={true}
        onSelectionChange={handleSelectionChange}
      >
        <GridToolbar>
          <GridSearchBox />
          <ButtonGroup>
            <Button svgIcon={plusIcon} onClick={openDialog}>
              {t("config-page:add_new_trend")}
            </Button>
          </ButtonGroup>
        </GridToolbar>
        <GridColumn
          title={t("config-page:name")}
          sortable={true}
          filterable={true}
          field="Name"
        />
        <GridColumn
          title={t("config-page:trend_type")}
          sortable={true}
          groupable={true}
          filterable={true}
          field="trendType"
        />
        <GridColumn
          title={t("config-page:trend_group")}
          sortable={true}
          groupable={true}
          filterable={true}
          field="trendGroup"
        />
        <GridColumn
          title={t("config-page:unit")}
          sortable={true}
          groupable={true}
          field="Unit"
        />
        <GridColumn
          title={t("config-page:color")}
          sortable={true}
          groupable={true}
          field="Color"
          cells={{ data: ColorGridCell }}
        />
      </Grid>
      {showDialog && (
        <Dialog
          title={t("config-page:create_new_trend")}
          onClose={cancelAddNewTrend}
        >
          <div>
            <Label editorId="trendName">{t("config-page:name")}</Label>
            <TextBox
              id="trendName"
              value={trendName}
              onChange={handleTrendNameChange}
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
            />
          </div>
          <div>
            <Label editorId="trendGroup">{t("config-page:trend_group")}</Label>
            <DropDownList
              id="trendGroup"
              data={trendGroups}
              textField="Name"
              dataItemKey="ID"
              value={trendGroup}
              onChange={handleTrendGroupChange}
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
            />
          </div>
          <div style={{ display: "flex", flexDirection: "column" }}>
            <Label editorId="trendColor">{t("config-page:color")}</Label>
            <FlatColorPicker
              id="trendColor"
              format="hex"
              value={trendColor}
              onChange={handleTrendColorChange}
            />
          </div>
          <DialogActionsBar>
            <Button svgIcon={cancelIcon} onClick={cancelAddNewTrend}>
              {t("common:cancel")}
            </Button>
            <Button
              svgIcon={checkIcon}
              themeColor={"primary"}
              onClick={confirmAddNewTrend}
            >
              {t("common:confirm")}
            </Button>
          </DialogActionsBar>
        </Dialog>
      )}
    </React.Fragment>
  );
});

export default TrendConfiguration;
