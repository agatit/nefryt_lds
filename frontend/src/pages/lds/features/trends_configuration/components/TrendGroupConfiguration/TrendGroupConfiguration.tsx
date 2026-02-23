import { memo, useState, useEffect, useCallback } from "react";
import { Button, ButtonGroup } from "@progress/kendo-react-buttons";
import {
  Grid,
  GridColumn,
  GridSearchBox,
  GridSelectionChangeEvent,
  GridToolbar,
} from "@progress/kendo-react-grid";
import { plusIcon, trashIcon } from "@progress/kendo-svg-icons";
import { useTranslation } from "react-i18next";
import { TrendGroup } from "../../../../../../services/api";
import { SelectDescriptor } from "@progress/kendo-react-data-tools";

export interface TrendGroupConfigurationProps {
  trendGroups: TrendGroup[];
  selected: TrendGroup | null;
  setSelected: (value: TrendGroup | null) => void;
  requestDelete: (value: TrendGroup) => void;
  enterAddNewTrendGroup: () => void;
}

const TrendGroupConfiguration = memo(function TrendGroupConfiguration({
  trendGroups,
  selected,
  setSelected,
  requestDelete,
  enterAddNewTrendGroup,
}: TrendGroupConfigurationProps) {
  const { t } = useTranslation(["common", "config-page"]);
  const [select, setSelect] = useState<SelectDescriptor>();

  useEffect(() => {
    if (!selected) setSelect({});
  }, [selected]);

  const handleSelectionChange = useCallback(
    (event: GridSelectionChangeEvent) => {
      const item = event.endDataItem as TrendGroup;
      setSelected(item);
      setSelect(event.select);
    },
    [setSelected],
  );

  return (
    <>
      <Grid
        data={trendGroups}
        sortable
        filterable
        dataItemKey="ID"
        selectable={{ enabled: true, mode: "single" }}
        select={select}
        onSelectionChange={handleSelectionChange}
      >
        <GridToolbar>
          <GridSearchBox />
          <ButtonGroup>
            <Button svgIcon={plusIcon} onClick={enterAddNewTrendGroup}>
              {t("config-page:add_new_trend_group")}
            </Button>

            {selected && (
              <Button
                svgIcon={trashIcon}
                onClick={() => requestDelete(selected)}
              >
                {t("common:delete")}
              </Button>
            )}
          </ButtonGroup>
        </GridToolbar>

        <GridColumn field="ID" title={t("config-page:id")} />
        <GridColumn field="Name" title={t("config-page:name")} />
      </Grid>
    </>
  );
});

export default TrendGroupConfiguration;
