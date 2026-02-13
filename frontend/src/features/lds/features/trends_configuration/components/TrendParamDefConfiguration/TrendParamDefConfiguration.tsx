import {
  Grid,
  GridColumn,
  GridSearchBox,
  GridSelectionChangeEvent,
  GridToolbar,
} from "@progress/kendo-react-grid";
import React from "react";
import { useTranslation } from "react-i18next";
import { SelectDescriptor } from "@progress/kendo-react-data-tools";
import { TrendParamDef } from "../../../../../../services/api";

export interface TrendParamDefConfigurationProps {
  trendParamDefs: TrendParamDef[];
  selected: TrendParamDef | null;
  setSelected: (value: TrendParamDef) => void;
}

const TrendParamDefConfiguration = React.memo(
  function TrendParamDefConfiguration({
    trendParamDefs,
    selected,
    setSelected,
  }: TrendParamDefConfigurationProps) {
    const { t } = useTranslation(["common", "config-page"]);

    const [select, setSelect] = React.useState<SelectDescriptor>();
    React.useEffect(() => {
      if (selected == null) setSelect({});
    }, [selected]);

    const handleSelectionChange = React.useCallback(
      (event: GridSelectionChangeEvent) => {
        const item: TrendParamDef = event.endDataItem;
        setSelected(item);
        setSelect(event.select);
      },
      [setSelected],
    );

    return (
      <React.Fragment>
        <Grid
          data={trendParamDefs}
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
            title={t("config-page:trend_type")}
            sortable={true}
            field="TrendDefID"
          />
          <GridColumn
            title={t("config-page:name")}
            sortable={true}
            field="Name"
          />
          <GridColumn
            title={t("config-page:data_type")}
            sortable={true}
            field="DataType"
          />
        </Grid>
      </React.Fragment>
    );
  },
);

export default TrendParamDefConfiguration;
