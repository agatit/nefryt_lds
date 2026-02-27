import {
  Grid,
  GridColumn,
  GridSearchBox,
  GridSelectionChangeEvent,
  GridToolbar,
} from "@progress/kendo-react-grid";
import React from "react";
import { useTranslation } from "react-i18next";
import { TrendDef } from "../../../../../../services/api";
import { SelectDescriptor } from "@progress/kendo-react-data-tools";

export interface TrendDefConfigurationProps {
  trendDefs: TrendDef[];
  selected: TrendDef | null;
  setSelected: (value: TrendDef) => void;
}

const TrendDefConfiguration = React.memo(function TrendDefConfiguration({
  trendDefs,
  selected,
  setSelected,
}: TrendDefConfigurationProps) {
  const { t } = useTranslation(["common", "config-page"]);

  const [select, setSelect] = React.useState<SelectDescriptor>();
  
  React.useEffect(() => {
    if (selected == null) setSelect({});
  }, [selected]);

  const handleSelectionChange = React.useCallback(
    (event: GridSelectionChangeEvent) => {
      const item: TrendDef = event.endDataItem;
      setSelected(item);
      setSelect(event.select);
    },
    [setSelected]
  );

  return (
    <React.Fragment>
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
        <GridColumn
          title={t("config-page:name")}
          sortable={true}
          field="Name"
        />
      </Grid>
    </React.Fragment>
  );
});

export default TrendDefConfiguration;
