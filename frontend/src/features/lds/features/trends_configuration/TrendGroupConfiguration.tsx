import { Button, ButtonGroup } from "@progress/kendo-react-buttons";
import {
  Grid,
  GridColumn,
  GridSearchBox,
  GridSelectionChangeEvent,
  GridToolbar,
} from "@progress/kendo-react-grid";
import {
  cancelIcon,
  checkIcon,
  plusIcon,
  trashIcon,
} from "@progress/kendo-svg-icons";
import React from "react";
import { useTranslation } from "react-i18next";
import { TrendGroup } from "../../../../services/api";
import { TextBox, TextBoxChangeEvent } from "@progress/kendo-react-inputs";
import { Dialog, DialogActionsBar } from "@progress/kendo-react-dialogs";
import { Label } from "@progress/kendo-react-labels";
import { SelectDescriptor } from "@progress/kendo-react-data-tools";

export interface TrendGroupConfigurationProps {
  showDialog: boolean;
  openDialog: () => void;
  closeDialog: () => void;
  trendGroups: TrendGroup[];
  addTrendGroup: (value: TrendGroup) => Promise<void>;
  deleteTrendGroup: (value: TrendGroup) => Promise<void>;
  selected: TrendGroup | null;
  setSelected: (valeu: TrendGroup) => void;
}

const TrendGroupConfiguration = React.memo(function TrendGroupConfiguration({
  showDialog,
  openDialog,
  closeDialog,
  trendGroups,
  addTrendGroup,
  deleteTrendGroup,
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

  const confirmAddNewTrendGroup = React.useCallback(async () => {
    const newTrendGroup: TrendGroup = {
      ID: trendGroups.length + 100,
      Name: trendGroupName!,
    };
    await addTrendGroup(newTrendGroup);
    closeDialog();
  }, [closeDialog, addTrendGroup, trendGroups, trendGroupName]);

  // Deletion dialog
  const [showDeletionDialog, setShowDeletionDialog] =
    React.useState<boolean>(false);
  const openDeletionDialog = React.useCallback(() => {
    setShowDeletionDialog(true);
  }, []);
  const closeDeletionDialog = React.useCallback(() => {
    setShowDeletionDialog(false);
  }, []);

  const confirmDeletion = React.useCallback(async () => {
    await deleteTrendGroup(selected!);
  }, [selected, deleteTrendGroup]);

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
            {selected && (
              <Button svgIcon={trashIcon} onClick={openDeletionDialog}>
                {t("common:delete")}
              </Button>
            )}
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
      {showDeletionDialog && (
        <Dialog
          title={t("common:confirm_deletion")}
          onClose={closeDeletionDialog}
        >
          {t("config-page:sure_you_want_delete_trend_group")}
          <DialogActionsBar>
            <Button svgIcon={cancelIcon} onClick={closeDeletionDialog}>
              {t("common:cancel")}
            </Button>
            <Button
              svgIcon={trashIcon}
              onClick={confirmDeletion}
              themeColor={"primary"}
            >
              {t("common:delete")}
            </Button>
          </DialogActionsBar>
        </Dialog>
      )}
    </React.Fragment>
  );
});

export default TrendGroupConfiguration;
