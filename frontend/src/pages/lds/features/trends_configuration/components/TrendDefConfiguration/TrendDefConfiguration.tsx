import { memo, useState, useEffect, useCallback } from "react";
import {
  Grid,
  GridColumn,
  GridSearchBox,
  GridSelectionChangeEvent,
  GridToolbar,
} from "@progress/kendo-react-grid";
import { SelectDescriptor } from "@progress/kendo-react-data-tools";
import { useTranslation } from "react-i18next";
import { TrendDef } from "../../../../../../services/api";

export interface TrendDefConfigurationProps {
  trendDefs: TrendDef[];
  selected: TrendDef | null;
  setSelected: (value: TrendDef) => void;
}

const TrendDefConfiguration = memo(function TrendDefConfiguration({
  trendDefs,
  selected,
  setSelected,
}: TrendDefConfigurationProps) {
  const { t } = useTranslation(["common", "config-page"]);
  const [select, setSelect] = useState<SelectDescriptor>();

  const handleSelectionChange = useCallback(
    (event: GridSelectionChangeEvent) => {
      const item: TrendDef = event.endDataItem;
      setSelected(item);
      setSelect(event.select);
    },
    [setSelected],
  );

  useEffect(() => {
    if (selected == null) setSelect({});
  }, [selected]);

  return (
    <Grid
      data={trendDefs}
      dataItemKey="ID"
      sortable={true}
      selectable={{ enabled: true, mode: "single" }}
      select={select}
      onSelectionChange={handleSelectionChange}
    >
      <GridToolbar>
        <GridSearchBox />
      </GridToolbar>
      <GridColumn title={t("config-page:id")} sortable={true} field="ID" />
      <GridColumn title={t("config-page:name")} sortable={true} field="Name" />
    </Grid>
  );
});

export default TrendDefConfiguration;
