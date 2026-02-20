import React from "react";
import {
  Grid,
  GridColumn,
  GridToolbar,
  GridSearchBox,
  GridSelectionChangeEvent,
} from "@progress/kendo-react-grid";
import { Button, ButtonGroup } from "@progress/kendo-react-buttons";
import { plusIcon, trashIcon } from "@progress/kendo-svg-icons";
import { SelectDescriptor } from "@progress/kendo-react-data-tools";
import { useTranslation } from "react-i18next";
import {
  Trend,
  TrendDef,
  TrendGroup,
  Unit,
} from "../../../../../../services/api";
import ColorGridCell from "../../../../components/ColorGridCell";
import { ParsedTrendType } from "../../index";

export interface TrendConfigurationProps {
  trendDefs: TrendDef[];
  trendGroups: TrendGroup[];
  units: Unit[];
  trends: Trend[];
  selected: ParsedTrendType | null;
  setSelected: (value: ParsedTrendType) => void;
  enterAddNewTrend: () => void;
  requestDelete: (value: ParsedTrendType) => void;
}

const TrendConfiguration = React.memo(function TrendConfiguration({
  trendDefs,
  trendGroups,
  units,
  trends,
  selected,
  setSelected,
  enterAddNewTrend,
  requestDelete,
}: TrendConfigurationProps) {
  const { t } = useTranslation(["common", "config-page"]);
  const [select, setSelect] = React.useState<SelectDescriptor>();

  const data = React.useMemo((): ParsedTrendType[] => {
    return trends.map((trend) => {
      const unit = units.find((u) => u.ID === trend.UnitID);

      return {
        ...trend,
        trendType: trendDefs.find((d) => d.ID === trend.TrendDefID)?.Name ?? "",
        trendGroup:
          trendGroups.find((g) => g.ID === trend.TrendGroupID)?.Name ?? "",
        unit: unit ? `${unit.Name} [${unit.Symbol}]` : "",
      };
    });
  }, [trendDefs, trendGroups, trends, units]);

  const handleSelectionChange = (e: GridSelectionChangeEvent) => {
    setSelected(e.endDataItem);
    setSelect(e.select);
  };

  return (
    <Grid
      data={data}
      dataItemKey="ID"
      autoProcessData
      sortable
      filterable
      groupable
      selectable={{ mode: "single" }}
      select={select}
      onSelectionChange={handleSelectionChange}
    >
      <GridToolbar>
        <GridSearchBox />
        <ButtonGroup>
          <Button svgIcon={plusIcon} onClick={enterAddNewTrend}>
            {t("config-page:add_new_trend")}
          </Button>

          {selected && (
            <Button svgIcon={trashIcon} onClick={() => requestDelete(selected)}>
              {t("common:delete")}
            </Button>
          )}
        </ButtonGroup>
      </GridToolbar>

      <GridColumn field="Name" title={t("config-page:name")} />
      <GridColumn field="trendType" title={t("config-page:trend_type")} />
      <GridColumn field="trendGroup" title={t("config-page:trend_group")} />
      <GridColumn field="unit" title={t("config-page:unit")} />
      <GridColumn
        field="Color"
        title={t("config-page:color")}
        cells={{ data: ColorGridCell }}
      />
      <GridColumn field="RawMin" title="Raw Min" />
      <GridColumn field="RawMax" title="Raw Max" />
      <GridColumn field="ScaledMin" title="Scaled Min" />
      <GridColumn field="ScaledMax" title="Scaled Max" />
    </Grid>
  );
});

export default TrendConfiguration;
