import {
  Grid,
  GridColumn,
  GridSearchBox,
  GridSelectionChangeEvent,
  GridToolbar,
} from "@progress/kendo-react-grid";
import { Button, ButtonGroup } from "@progress/kendo-react-buttons";
import { cancelIcon, checkIcon, plusIcon } from "@progress/kendo-svg-icons";
import React from "react";
import { useTranslation } from "react-i18next";
import { EventDef, EventDefCreate } from "../../../../../services/api";
import { SelectDescriptor } from "@progress/kendo-react-data-tools";
import { Dialog, DialogActionsBar } from "@progress/kendo-react-dialogs";
import { TextBox, TextBoxChangeEvent } from "@progress/kendo-react-inputs";
import { DropDownListChangeEvent } from "@progress/kendo-react-dropdowns";
import { Label } from "@progress/kendo-react-labels";
import { DropDownList } from "@progress/kendo-react-dropdowns";
import { AppContext } from "../../../../../contexts/appContext";

export interface EventsDefProps {
  showDialog: boolean;
  openDialog: () => void;
  closeDialog: () => void;
  eventDefs: EventDef[];
  addEventDef: (value: EventDefCreate) => Promise<void>;
  deleteEventDef: (value: EventDef) => Promise<void>;
  selected: EventDef | null;
  setSelected: (value: EventDef | null) => void;
}

const EventsDef = React.memo(function EventsDef({
  showDialog,
  openDialog,
  closeDialog,
  eventDefs,
  addEventDef,
  selected,
  setSelected,
}: EventsDefProps) {
  const appContext = React.useContext(AppContext);
  if (!appContext) return null;

  const { t } = useTranslation(["common", "event-page"]);
  const [select, setSelect] = React.useState<SelectDescriptor>();
  const [caption, setCaption] = React.useState<string>("");
  const [verbosity, setVerbosity] = React.useState<string>("");
  const [silent, setSilent] = React.useState<boolean>(false);
  const [visible, setVisible] = React.useState<boolean>(true);
  const [enabled, setEnabled] = React.useState<boolean>(true);
  const [id, setId] = React.useState("");

  const handleIdChange = React.useCallback((e: TextBoxChangeEvent) => {
    setId(String(e.value ?? "").toUpperCase());
  }, []);

  const handleCaptionChange = React.useCallback((e: TextBoxChangeEvent) => {
    setCaption(String(e.value ?? ""));
  }, []);

  const handleVerbosityChange = React.useCallback((e: TextBoxChangeEvent) => {
    setVerbosity(String(e.value ?? "").toUpperCase());
  }, []);

  const handleSilentChange = React.useCallback((e: DropDownListChangeEvent) => {
    setSilent(e.value.value ?? false);
  }, []);

  const handleVisibleChange = React.useCallback(
    (e: DropDownListChangeEvent) => {
      setVisible(e.value.value ?? false);
    },
    [],
  );

  const handleEnabledChange = React.useCallback(
    (e: DropDownListChangeEvent) => {
      setEnabled(e.value.value ?? false);
    },
    [],
  );

  const getBooleanOption = (value: boolean) =>
    booleanOptions.find((o) => o.value === value);

  const booleanOptions = [
    { text: "True", value: true },
    { text: "False", value: false },
  ];

  const cancelAddNewEventDef = React.useCallback(() => {
    setId("");
    setCaption("");
    setVerbosity("");
    setSilent(false);
    setVisible(true);
    setEnabled(true);
    closeDialog();
  }, [closeDialog]);

  const confirmAddNewEventDef = React.useCallback(async () => {
    if (!id.trim() || !caption.trim() || !verbosity.trim()) {
      appContext.showNotification({
        notificationType: {
          icon: true,
          style: "warning",
        },
        message: "ID, Caption and Verbosity are required",
      });
      return;
    }

    if (!/^[A-Z_]+$/.test(id)) {
      appContext.showNotification({
        notificationType: {
          icon: true,
          style: "error",
        },
        message: "ID: use uppercase letters and underscores only",
      });
      return;
    }

    if (!/^[a-z]+$/.test(caption)) {
      appContext.showNotification({
        notificationType: {
          icon: true,
          style: "error",
        },
        message: "Caption: use letters only",
      });
      return;
    }

    if (!/^[A-Z]+$/.test(verbosity)) {
      appContext.showNotification({
        notificationType: {
          icon: true,
          style: "error",
        },
        message: "Verbosity: use uppercase letters only",
      });
      return;
    }

    const newEventDef: EventDefCreate = {
      ID: id,
      Caption: caption,
      Verbosity: verbosity,
      Silent: silent,
      Visible: visible,
      Enabled: enabled,
    };

    await addEventDef(newEventDef);
    closeDialog();
  }, [
    id,
    caption,
    verbosity,
    addEventDef,
    closeDialog,
    silent,
    visible,
    enabled,
  ]);

  const handleSelectionChange = React.useCallback(
    (event: GridSelectionChangeEvent) => {
      const item: EventDef = event.endDataItem;
      setSelected(item);
      setSelect(event.select);
    },
    [setSelected],
  );

  React.useEffect(() => {
    if (selected == null) setSelect({});
  }, [selected]);

  return (
    <>
      <Grid
        data={eventDefs}
        dataItemKey="ID"
        selectable={{ enabled: true, mode: "single" }}
        select={select}
        onSelectionChange={handleSelectionChange}
      >
        <GridToolbar>
          <GridSearchBox />
          <ButtonGroup>
            <Button svgIcon={plusIcon} onClick={openDialog}>
              {t("event-page:add_new_event_def")}
            </Button>
          </ButtonGroup>
        </GridToolbar>

        <GridColumn field="ID" title="ID" width="150px" />
        <GridColumn field="Caption" title="Caption" />
        <GridColumn field="Verbosity" title="Verbosity" />
        <GridColumn field="Enabled" title="Enabled" />
        <GridColumn field="Visible" title="Visible" />
        <GridColumn field="Silent" title="Silent" />
      </Grid>

      {showDialog && (
        <Dialog title="Create Event Definition" onClose={cancelAddNewEventDef}>
          <div>
            <Label>ID</Label>
            <TextBox value={id} onChange={handleIdChange} />
          </div>

          <div>
            <Label>Caption</Label>
            <TextBox value={caption} onChange={handleCaptionChange} />
          </div>

          <div>
            <Label>Verbosity</Label>
            <TextBox value={verbosity} onChange={handleVerbosityChange} />
          </div>

          <div>
            <Label>Silent</Label>
            <DropDownList
              data={booleanOptions}
              textField="text"
              dataItemKey="value"
              value={getBooleanOption(silent)}
              onChange={handleSilentChange}
            />
          </div>
          <div>
            <Label>Visible</Label>
            <DropDownList
              data={booleanOptions}
              textField="text"
              dataItemKey="value"
              value={getBooleanOption(visible)}
              onChange={handleVisibleChange}
            />
          </div>
          <div>
            <Label>Enabled</Label>
            <DropDownList
              data={booleanOptions}
              textField="text"
              dataItemKey="value"
              value={getBooleanOption(enabled)}
              onChange={handleEnabledChange}
            />
          </div>

          <DialogActionsBar>
            <Button svgIcon={cancelIcon} onClick={cancelAddNewEventDef}>
              {t("common:cancel")}
            </Button>
            <Button
              svgIcon={checkIcon}
              themeColor="primary"
              onClick={confirmAddNewEventDef}
            >
              {t("common:confirm")}
            </Button>
          </DialogActionsBar>
        </Dialog>
      )}
    </>
  );
});

export default EventsDef;
