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
  NumericTextBox,
  TextBox,
  TextBoxChangeEvent,
} from "@progress/kendo-react-inputs";
import { Label } from "@progress/kendo-react-labels";
import {
  cancelIcon,
  checkIcon,
  plusIcon,
  trashIcon,
} from "@progress/kendo-svg-icons";
import React from "react";
import { ParsedTrendType } from "../..";
import { useTranslation } from "react-i18next";
import {
  Trend,
  TrendDef,
  TrendGroup,
  TrendParamCreate,
  TrendParamDef,
  Unit,
} from "../../../../../../services/api";
import { rgbaToHex } from "../../../../../../lib/utilis";
import ColorGridCell from "../../../../components/ColorGridCell";
import { SelectDescriptor } from "@progress/kendo-react-data-tools";
import { useHandleApiResponse } from "../../../../../../hooks/useHandleApiResponse";
import { LDSContext } from "../../../../contexts/ldsContext";

export interface TrendConfigurationProps {
  showDialog: boolean;
  openDialog: () => void;
  closeDialog: () => void;
  trendDefs: TrendDef[];
  trendGroups: TrendGroup[];
  trendParamDefs: TrendParamDef[];
  units: Unit[];
  trends: Trend[];
  addTrend: (value: Trend) => Promise<Trend>;
  deleteTrend: (value: Trend) => Promise<void>;
  selected: ParsedTrendType | null;
  setSelected: (value: ParsedTrendType) => void;
}

const TrendConfiguration = React.memo(function TrendConfiguration({
  showDialog,
  openDialog,
  closeDialog,
  trendDefs,
  trendGroups,
  trendParamDefs,
  units,
  trends,
  addTrend,
  deleteTrend,
  selected,
  setSelected,
}: TrendConfigurationProps) {
  const { t } = useTranslation(["common", "config-page"]);

  const data = React.useMemo((): ParsedTrendType[] => {
    return trends.map((trend): ParsedTrendType => {
      const unit = units.find((unit) => unit.ID == trend.UnitID)!;
      return {
        ...trend,
        trendType: trendDefs.find((def) => def.ID == trend.TrendDefID)!.Name!,
        trendGroup: trendGroups.find((group) => group.ID == trend.TrendGroupID)!
          .Name!,
        unit: unit.Name! + " [" + unit.Symbol! + "]",
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
    [setSelected],
  );

  const [trendName, setTrendName] = React.useState<string | undefined>();
  const [trendType, setTrendType] = React.useState<TrendDef | undefined>();
  const [trendGroup, setTrendGroup] = React.useState<TrendGroup | undefined>();
  const [trendUnit, setTrendUnit] = React.useState<Unit | undefined>();
  const [trendColor, setTrendColor] = React.useState<string | undefined>();
  const [trendParams, setTrendParams] = React.useState<number[]>([]);

  React.useEffect(() => {
    setTrendParams([]);
  }, [trendType]);

  const handleTrendNameChange = React.useCallback(
    (event: TextBoxChangeEvent) => {
      if (event.value) setTrendName(event.value.toString());
    },
    [],
  );
  const handleTrendTypeChange = React.useCallback(
    (event: DropDownListChangeEvent) => {
      if (event.value) setTrendType(event.value);
    },
    [],
  );
  const handleTrendGroupChange = React.useCallback(
    (event: DropDownListChangeEvent) => {
      if (event.value) setTrendGroup(event.value);
    },
    [],
  );
  const handleTrendUnitChange = React.useCallback(
    (event: DropDownListChangeEvent) => {
      if (event.value) setTrendUnit(event.value);
    },
    [],
  );
  const handleTrendColorChange = React.useCallback(
    (event: FlatColorPickerChangeEvent) => {
      if (event.value) setTrendColor(rgbaToHex(event.value)!.slice(0, 7)); //slice to cut off opacity
    },
    [],
  );

  const requiredTrendParams = React.useMemo(() => {
    return trendParamDefs.filter((def) => def.TrendDefID == trendType?.ID);
  }, [trendParamDefs, trendType]);

  React.useEffect(() => {
    setTrendParams(Array(requiredTrendParams.length).fill(0));
  }, [requiredTrendParams]);

  const cancelAddNewTrend = React.useCallback(() => {
    setTrendName(undefined);
    setTrendType(undefined);
    setTrendGroup(undefined);
    setTrendUnit(undefined);
    setTrendColor(undefined);
    closeDialog();
  }, [closeDialog]);

  const handleApiResponse = useHandleApiResponse();
  const ldsContext = React.useContext(LDSContext);

  const addTrendParam = React.useCallback(
    async (value: TrendParamCreate, id: number) => {
      await handleApiResponse(
        ldsContext!.trendParamApi.createTrendParamTrendTrendIdParamPost.bind(
          ldsContext!.trendParamApi,
        ),
        id,
        value,
      );
    },
    [],
  );

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
    const trend = await addTrend(newTrend);

    for (let i = 0; i < trendParams.length; i++) {
      let newParam: TrendParamCreate = {
        TrendParamDefID: requiredTrendParams[i].ID,
        Value: trendParams[i].toString(),
      };
      try {
        const response = await handleApiResponse(
          ldsContext!.trendParamApi.createTrendParamTrendTrendIdParamPost.bind(
            ldsContext!.trendParamApi,
          ),
          trend.ID,
          newParam,
        );
      } catch (error) {
        console.log(error);
      }
    }

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
    trendParams,
  ]);

  // Deletion dialog
  const [showDeletionDialog, setShowDeletionDialog] =
    React.useState<boolean>(false);
  const openDeletionDialog = React.useCallback(() => {
    setShowDeletionDialog(true);
  }, []);
  const closeDeletionDialog = React.useCallback(() => {
    setShowDeletionDialog(false);
  }, []);

  const confirmDeletion = React.useCallback(async () => {
    await deleteTrend(selected!);
    closeDeletionDialog();
  }, [selected, deleteTrend]);

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
            {selected && (
              <Button svgIcon={trashIcon} onClick={openDeletionDialog}>
                {t("common:delete")}
              </Button>
            )}
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
          field="unit"
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
          {requiredTrendParams.map((trendParam, index) => {
            return (
              <div style={{ display: "flex", flexDirection: "column" }}>
                <Label editorId={"trendParam-" + trendParam.ID}>
                  {trendParam.Name}
                </Label>
                <NumericTextBox
                  key={"trendParam " + index}
                  id={"trendParam-" + trendParam.ID}
                  value={trendParams[index]}
                  onChange={(event) => {
                    let params = [...trendParams];
                    params.splice(index, 1, event.value ?? 0);
                    console.log(trendParams);
                    setTrendParams(params);
                  }}
                />
              </div>
            );
          })}
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
      {showDeletionDialog && (
        <Dialog
          title={t("common:confirm_deletion")}
          onClose={closeDeletionDialog}
        >
          {t("config-page:sure_you_want_delete_trend")}
          <DialogActionsBar>
            <Button svgIcon={cancelIcon} onClick={closeDeletionDialog}>
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
    </React.Fragment>
  );
});

export default TrendConfiguration;
