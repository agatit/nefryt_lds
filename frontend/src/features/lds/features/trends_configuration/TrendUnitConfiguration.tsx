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
import { TrendDefBase, Unit } from "../../../../services/api";
import { TextBox, TextBoxChangeEvent } from "@progress/kendo-react-inputs";
import { Dialog, DialogActionsBar } from "@progress/kendo-react-dialogs";
import { Label } from "@progress/kendo-react-labels";
import { SelectDescriptor } from "@progress/kendo-react-data-tools";

export interface TrendUnitConfigurationProps {
  showDialog: boolean;
  openDialog: () => void;
  closeDialog: () => void;
  units: Unit[];
  addUnit: (value: Unit) => Promise<void>;
  selected: Unit | null;
  setSelected: (value: Unit) => void;
}

const TrendUnitConfiguration = React.memo(function TrendUnitConfiguration({
  showDialog,
  openDialog,
  closeDialog,
  units,
  addUnit,
  selected,
  setSelected,
}: TrendUnitConfigurationProps) {
  const { t } = useTranslation(["common", "config-page"]);

  const [select, setSelect] = React.useState<SelectDescriptor>();
  React.useEffect(() => {
    if (selected == null) setSelect({});
  }, [selected]);

  const handleSelectionChange = React.useCallback(
    (event: GridSelectionChangeEvent) => {
      const item: Unit = event.endDataItem;
      setSelected(item);
      setSelect(event.select);
    },
    [setSelected]
  );

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

  const confirmAddNewUnit = React.useCallback(async () => {
    const newUnit: Unit = {
      ID: (units.length + 100).toString(),
      Name: unitName!,
      Symbol: unitSymbol!,
      Multiplier: unitMultiplier!,
    };
    await addUnit(newUnit);
    closeDialog();
  }, [closeDialog, addUnit, units, unitName, unitSymbol, unitMultiplier]);

  return (
    <React.Fragment>
      <Grid
        data={units}
        sortable={true}
        dataItemKey="ID"
        selectable={{ enabled: true, mode: "single" }}
        select={select}
        onSelectionChange={handleSelectionChange}
      >
        <GridToolbar>
          <GridSearchBox />
          <ButtonGroup>
            <Button svgIcon={plusIcon} onClick={openDialog}>
              {t("config-page:add_new_unit")}
            </Button>
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
      {showDialog && (
        <Dialog
          title={t("config-page:create_new_trend_group")}
          onClose={cancelAddNewUnit}
        >
          <div>
            <Label editorId="unitName">{t("config-page:name")}</Label>
            <TextBox
              id="unitName"
              value={unitName}
              onChange={handleUnitNameChange}
            />
          </div>
          <div>
            <Label editorId="unitSymbol">{t("config-page:symbol")}</Label>
            <TextBox
              id="unitSymbol"
              value={unitSymbol}
              onChange={handleUnitSymbolChange}
            />
          </div>
          <div>
            <Label editorId="unitMultiplier">
              {t("config-page:multiplier")}
            </Label>
            <TextBox
              id="unitMultiplier"
              value={unitMultiplier}
              onChange={handleUnitMultiplierChange}
            />
          </div>
          <DialogActionsBar>
            <Button svgIcon={cancelIcon} onClick={cancelAddNewUnit}>
              {t("common:cancel")}
            </Button>
            <Button
              svgIcon={checkIcon}
              themeColor={"primary"}
              onClick={confirmAddNewUnit}
            >
              {t("common:confirm")}
            </Button>
          </DialogActionsBar>
        </Dialog>
      )}
    </React.Fragment>
  );
});

export default TrendUnitConfiguration;
