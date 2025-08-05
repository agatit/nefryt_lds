import { Button, ButtonGroup } from "@progress/kendo-react-buttons";
import {
  Grid,
  GridColumn,
  GridSearchBox,
  GridToolbar,
} from "@progress/kendo-react-grid";
import { plusIcon } from "@progress/kendo-svg-icons";
import React from "react";
import { useTranslation } from "react-i18next";
import { TrendDefBase, Unit } from "../../../../services/api";
import { TextBoxChangeEvent } from "@progress/kendo-react-inputs";

export interface TrendUnitConfigurationProps {
  showDialog: boolean;
  openDialog: () => void;
  closeDialog: () => void;
  units: Unit[];
  setUnits: (value: Unit[]) => void;
}

const TrendUnitConfiguration = React.memo(function TrendUnitConfiguration({
  showDialog,
  openDialog,
  closeDialog,
  units,
  setUnits,
}: TrendUnitConfigurationProps) {
  const { t } = useTranslation(["common", "config-page"]);

  const [unitName, setUnitName] = React.useState<string | undefined>();
  const [unitSymbol, setUnitSymbol] = React.useState<string | undefined>();
  const [unitMultiplier, setUnitMultiplier] = React.useState<
    string | undefined
  >();

  const handleUnitNameChange = React.useCallback(
    (event: TextBoxChangeEvent) => {
      if (event.value) setUnitName(event.value.toString());
    },
    []
  );
  const handleUnitSymbolChange = React.useCallback(
    (event: TextBoxChangeEvent) => {
      if (event.value) setUnitSymbol(event.value.toString());
    },
    []
  );
  const handleUnitMultiplierChange = React.useCallback(
    (event: TextBoxChangeEvent) => {
      if (event.value) setUnitMultiplier(event.value.toString());
    },
    []
  );

  const cancelAddNewUnit = React.useCallback(() => {
    setUnitName(undefined);
    setUnitSymbol(undefined);
    setUnitMultiplier(undefined);
    closeDialog();
  }, [closeDialog]);

  const confirmAddNewUnit = React.useCallback(() => {
    const newUnit: Unit = {
      ID: (units.length + 100).toString(),
      Name: unitName!,
      Symbol: unitSymbol!,
      Multiplier: unitMultiplier!,
    };
    setUnits([...units, newUnit]);
    closeDialog();
  }, [closeDialog, setUnits, units, unitName, unitSymbol, unitMultiplier]);

  return (
    <React.Fragment>
      <Grid
        data={units}
        sortable={true}
        selectable={{ enabled: true, mode: "single" }}
      >
        <GridToolbar>
          <GridSearchBox />
          <ButtonGroup>
            <Button svgIcon={plusIcon}>{t("config-page:add_new_unit")}</Button>
          </ButtonGroup>
        </GridToolbar>
        <GridColumn
          title={t("config-page:name")}
          sortable={true}
          field="Name"
        />
        <GridColumn
          title={t("config-page:symbol")}
          sortable={true}
          field="Symbol"
        />
        <GridColumn
          title={t("config-page:multiplier")}
          sortable={true}
          field="Multiplier"
        />
      </Grid>
    </React.Fragment>
  );
});

export default TrendUnitConfiguration;
