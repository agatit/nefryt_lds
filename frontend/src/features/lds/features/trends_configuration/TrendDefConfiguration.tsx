import { Button, ButtonGroup } from "@progress/kendo-react-buttons";
import {
  Grid,
  GridColumn,
  GridSearchBox,
  GridSelectionChangeEvent,
  GridToolbar,
} from "@progress/kendo-react-grid";
import { cancelIcon, checkIcon, plusIcon } from "@progress/kendo-svg-icons";
import React from "react";
import { useTranslation } from "react-i18next";
import { TrendDefBase } from "../../../../services/api";
import { Dialog, DialogActionsBar } from "@progress/kendo-react-dialogs";
import { Label } from "@progress/kendo-react-labels";
import { TextBox, TextBoxChangeEvent } from "@progress/kendo-react-inputs";
import { SelectDescriptor } from "@progress/kendo-react-data-tools";

export interface TrendDefConfigurationProps {
  trendDefs: TrendDefBase[];
  selected: TrendDefBase | null;
  setSelected: (value: TrendDefBase) => void;
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
      const item: TrendDefBase = event.endDataItem;
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
