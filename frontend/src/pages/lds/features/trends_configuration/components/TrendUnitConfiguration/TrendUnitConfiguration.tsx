import { Button, ButtonGroup } from "@progress/kendo-react-buttons";
import {
  Grid,
  GridColumn,
  GridSearchBox,
  GridSelectionChangeEvent,
  GridToolbar,
} from "@progress/kendo-react-grid";
import { plusIcon, trashIcon } from "@progress/kendo-svg-icons";
import React from "react";
import { useTranslation } from "react-i18next";
import { Unit } from "../../../../../../services/api";
import { SelectDescriptor } from "@progress/kendo-react-data-tools";

export interface TrendUnitConfigurationProps {
  units: Unit[];
  deleteUnit: (value: Unit) => void;
  selected: Unit | null;
  setSelected: (value: Unit | null) => void;
  enterAddNewUnit: () => void;
}

const TrendUnitConfiguration = React.memo(function TrendUnitConfiguration({
  units,
  deleteUnit,
  selected,
  setSelected,
  enterAddNewUnit,
}: TrendUnitConfigurationProps) {
  const { t } = useTranslation(["common", "config-page"]);
  const [select, setSelect] = React.useState<SelectDescriptor>();

  const handleSelectionChange = React.useCallback(
    (event: GridSelectionChangeEvent) => {
      const item = event.endDataItem as Unit;
      setSelected(item);
      setSelect(event.select);
    },
    [setSelected],
  );

  React.useEffect(() => {
    if (!selected) setSelect({});
  }, [selected]);

  return (
    <Grid
      data={units}
      sortable
      dataItemKey="ID"
      selectable={{ enabled: true, mode: "single" }}
      select={select}
      onSelectionChange={handleSelectionChange}
    >
      <GridToolbar>
        <GridSearchBox />
        <ButtonGroup>
          <Button svgIcon={plusIcon} onClick={enterAddNewUnit}>
            {t("config-page:add_new_unit")}
          </Button>

          {selected && (
            <Button svgIcon={trashIcon} onClick={() => deleteUnit(selected)}>
              {t("common:delete")}
            </Button>
          )}
        </ButtonGroup>
      </GridToolbar>

      <GridColumn field="Name" title={t("config-page:name")} />
      <GridColumn field="Symbol" title={t("config-page:symbol")} />
      <GridColumn field="Multiplier" title={t("config-page:multiplier")} />
    </Grid>
  );
});

export default TrendUnitConfiguration;
