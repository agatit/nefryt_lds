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
import { TrendDefBase, TrendGroup } from "../../../../services/api";
import { TextBox, TextBoxChangeEvent } from "@progress/kendo-react-inputs";
import { Dialog, DialogActionsBar } from "@progress/kendo-react-dialogs";
import { Label } from "@progress/kendo-react-labels";
import { SelectDescriptor } from "@progress/kendo-react-data-tools";

export interface TrendGroupConfigurationProps {
  showDialog: boolean;
  openDialog: () => void;
  closeDialog: () => void;
  trendGroups: TrendGroup[];
  setTrendGroups: (value: TrendGroup[]) => void;
  selected: TrendGroup | null;
  setSelected: (valeu: TrendGroup) => void;
}

const TrendGroupConfiguration = React.memo(function TrendGroupConfiguration({
  showDialog,
  openDialog,
  closeDialog,
  trendGroups,
  setTrendGroups,
  selected,
  setSelected,
}: TrendGroupConfigurationProps) {
  const { t } = useTranslation(["common", "config-page"]);

  const [select, setSelect] = React.useState<SelectDescriptor>();
  React.useEffect(() => {
    if (selected == null) setSelect({});
  }, [selected]);

  const handleSelectionChange = React.useCallback(
    (event: GridSelectionChangeEvent) => {
      const item: TrendGroup = event.endDataItem;
      setSelected(item);
      setSelect(event.select);
    },
    [setSelected]
  );

  const [trendGroupName, setTrendGroupName] = React.useState<
    string | undefined
  >();

  const handleTrendGroupNameChange = React.useCallback(
    (event: TextBoxChangeEvent) => {
      if (event.value) setTrendGroupName(event.value.toString());
    },
    []
  );

  const cancelAddNewTrendGroup = React.useCallback(() => {
    setTrendGroupName(undefined);
    closeDialog();
  }, [closeDialog]);

  const confirmAddNewTrendGroup = React.useCallback(() => {
    const newTrendGroup: TrendGroup = {
      ID: trendGroups.length + 100,
      Name: trendGroupName!,
    };
    setTrendGroups([...trendGroups, newTrendGroup]);
    closeDialog();
  }, [closeDialog, setTrendGroups, trendGroups, trendGroupName]);

  return (
    <React.Fragment>
      <Grid
        data={trendGroups}
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
              {t("config-page:add_new_trend_group")}
            </Button>
          </ButtonGroup>
        </GridToolbar>
        <GridColumn title={t("config-page:id")} sortable={true} field="ID" />
        <GridColumn
          title={t("config-page:name")}
          sortable={true}
          field="Name"
        />
      </Grid>
      {showDialog && (
        <Dialog
          title={t("config-page:create_new_trend_group")}
          onClose={cancelAddNewTrendGroup}
        >
          <div>
            <Label editorId="trendDefName">{t("config-page:name")}</Label>
            <TextBox
              id="trendDefName"
              value={trendGroupName}
              onChange={handleTrendGroupNameChange}
            />
          </div>
          <DialogActionsBar>
            <Button svgIcon={cancelIcon} onClick={cancelAddNewTrendGroup}>
              {t("common:cancel")}
            </Button>
            <Button
              svgIcon={checkIcon}
              themeColor={"primary"}
              onClick={confirmAddNewTrendGroup}
            >
              {t("common:confirm")}
            </Button>
          </DialogActionsBar>
        </Dialog>
      )}
    </React.Fragment>
  );
});

export default TrendGroupConfiguration;
