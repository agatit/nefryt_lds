import { Button, ButtonGroup } from "@progress/kendo-react-buttons";
import { Dialog, DialogActionsBar } from "@progress/kendo-react-dialogs";
import {
  Grid,
  GridColumn,
  GridSearchBox,
  GridSelectionChangeEvent,
  GridToolbar,
} from "@progress/kendo-react-grid";
import { cancelIcon, plusIcon, trashIcon } from "@progress/kendo-svg-icons";
import React from "react";
import { ParsedTrendType } from "../../index";
import { useTranslation } from "react-i18next";
import {
  Trend,
  TrendDef,
  TrendGroup,
  TrendParamDef,
  Unit,
} from "../../../../../../services/api";
import ColorGridCell from "../../../../components/ColorGridCell";
import { SelectDescriptor } from "@progress/kendo-react-data-tools";

export interface TrendConfigurationProps {
  trendDefs: TrendDef[];
  trendGroups: TrendGroup[];
  trendParamDefs: TrendParamDef[];
  units: Unit[];
  trends: Trend[];
  deleteTrend: (value: Trend) => Promise<void>;
  selected: ParsedTrendType | null;
  setSelected: (value: ParsedTrendType) => void;
  enterAddNewTrend: () => void;
}

const TrendConfiguration = React.memo(function TrendConfiguration({
  trendDefs,
  trendGroups,
  units,
  trends,
  deleteTrend,
  selected,
  setSelected,
  enterAddNewTrend,
}: TrendConfigurationProps) {
  const { t } = useTranslation(["common", "config-page"]);
  const [select, setSelect] = React.useState<SelectDescriptor>();

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
            <Button svgIcon={plusIcon} onClick={enterAddNewTrend}>
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
