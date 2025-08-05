import { Button, ButtonGroup } from "@progress/kendo-react-buttons";
import {
  Grid,
  GridColumn,
  GridSearchBox,
  GridToolbar,
} from "@progress/kendo-react-grid";
import { cancelIcon, checkIcon, plusIcon } from "@progress/kendo-svg-icons";
import React from "react";
import { useTranslation } from "react-i18next";
import { TrendDefBase } from "../../../../services/api";
import { Dialog, DialogActionsBar } from "@progress/kendo-react-dialogs";
import { Label } from "@progress/kendo-react-labels";
import { TextBox, TextBoxChangeEvent } from "@progress/kendo-react-inputs";

export interface TrendDefConfigurationProps {
  showDialog: boolean;
  openDialog: () => void;
  closeDialog: () => void;
  trendDefs: TrendDefBase[];
  setTrendDefs: (value: TrendDefBase[]) => void;
}

const TrendDefConfiguration = React.memo(function TrendDefConfiguration({
  showDialog,
  openDialog,
  closeDialog,
  trendDefs,
  setTrendDefs,
}: TrendDefConfigurationProps) {
  const { t } = useTranslation(["common", "config-page"]);

  const [trendDefID, setTrendDefID] = React.useState<string | undefined>();
  const [trendDefName, setTrendDefName] = React.useState<string | undefined>();

  const handleTrendDefIDChange = React.useCallback(
    (event: TextBoxChangeEvent) => {
      if (event.value) setTrendDefID(event.value.toString());
    },
    []
  );
  const handleTrendDefNameChange = React.useCallback(
    (event: TextBoxChangeEvent) => {
      if (event.value) setTrendDefName(event.value.toString());
    },
    []
  );

  const cancelAddNewTrendDef = React.useCallback(() => {
    setTrendDefID(undefined);
    setTrendDefName(undefined);
    closeDialog();
  }, [closeDialog]);

  const confirmAddNewTrendDef = React.useCallback(() => {
    const newTrendDef: TrendDefBase = {
      ID: trendDefID!,
      Name: trendDefName!,
    };
    setTrendDefs([...trendDefs, newTrendDef]);
    closeDialog();
  }, [closeDialog, setTrendDefs, trendDefs, trendDefID, trendDefName]);

  return (
    <React.Fragment>
      <Grid
        data={trendDefs}
        sortable={true}
        selectable={{ enabled: true, mode: "single" }}
      >
        <GridToolbar>
          <GridSearchBox />
          <ButtonGroup>
            <Button svgIcon={plusIcon} onClick={openDialog}>
              {t("config-page:add_new_trend_type")}
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
          title={t("config-page:create_new_trend_type")}
          onClose={cancelAddNewTrendDef}
        >
          <div>
            <Label editorId="trendDefID">{t("config-page:id")}</Label>
            <TextBox
              id="trendDefID"
              value={trendDefID}
              onChange={handleTrendDefIDChange}
            />
          </div>
          <div>
            <Label editorId="trendDefName">{t("config-page:name")}</Label>
            <TextBox
              id="trendDefName"
              value={trendDefName}
              onChange={handleTrendDefNameChange}
            />
          </div>
          <DialogActionsBar>
            <Button svgIcon={cancelIcon} onClick={cancelAddNewTrendDef}>
              {t("common:cancel")}
            </Button>
            <Button
              svgIcon={checkIcon}
              themeColor={"primary"}
              onClick={confirmAddNewTrendDef}
            >
              {t("common:confirm")}
            </Button>
          </DialogActionsBar>
        </Dialog>
      )}
    </React.Fragment>
  );
});

export default TrendDefConfiguration;
