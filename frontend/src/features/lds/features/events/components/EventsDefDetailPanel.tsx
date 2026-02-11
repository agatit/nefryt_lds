import React from "react";
import { useTranslation } from "react-i18next";
import { EventDef, EventDefUpdate } from "../../../../../services/api";
import { TextBox, TextBoxChangeEvent } from "@progress/kendo-react-inputs";
import { Label } from "@progress/kendo-react-labels";
import {
  cancelIcon,
  pencilIcon,
  plusIcon,
  saveIcon,
  trashIcon,
} from "@progress/kendo-svg-icons";
import { Button } from "@progress/kendo-react-buttons";
import { Dialog, DialogActionsBar } from "@progress/kendo-react-dialogs";
import { DropDownList } from "@progress/kendo-react-dropdowns";
import { AppContext } from "../../../../../contexts/appContext";
import { DropDownListChangeEvent } from "@progress/kendo-react-dropdowns";

export interface EventDefDetailPanelProps {
  selected: EventDef | null;
  editEventDef?: (id: string, value: EventDefUpdate) => Promise<void>;
  deleteEventDef?: (value: EventDef) => Promise<void>;
  enterAddNewEventDef?: () => void;
}

const EventDefDetailPanel = React.memo(function EventDefDetailPanel({
  selected,
  editEventDef,
  deleteEventDef,
  enterAddNewEventDef,
}: EventDefDetailPanelProps) {
  const appContext = React.useContext(AppContext);
  if (!appContext) return null;

  const { t } = useTranslation(["common", "event-page", "config-page"]);
  const [inEdit, setInEdit] = React.useState(false);
  const [id, setId] = React.useState("");
  const [caption, setCaption] = React.useState("");
  const [verbosity, setVerbosity] = React.useState("");
  const [silent, setSilent] = React.useState(false);
  const [visible, setVisible] = React.useState(true);
  const [enabled, setEnabled] = React.useState(true);
  const [showDialog, setShowDialog] = React.useState(false);

  const setSelectedData = React.useCallback((def: EventDef) => {
    setId(def.ID ?? "");
    setCaption(def.Caption ?? "");
    setVerbosity(def.Verbosity ?? "");
    setSilent(!!def.Silent);
    setVisible(!!def.Visible);
    setEnabled(!!def.Enabled);
  }, []);

  const booleanOptions = [
    { text: "True", value: true },
    { text: "False", value: false },
  ];

  const handleCaptionChange = React.useCallback((e: TextBoxChangeEvent) => {
    setCaption(String(e.value ?? ""));
  }, []);

  const handleVerbosityChange = React.useCallback((e: TextBoxChangeEvent) => {
    setVerbosity(String(e.value ?? "").toUpperCase());
  }, []);

  const handleSilentChange = React.useCallback((e: DropDownListChangeEvent) => {
    setSilent(e.value?.value ?? false);
  }, []);

  const handleVisibleChange = React.useCallback(
    (e: DropDownListChangeEvent) => {
      setVisible(e.value?.value ?? false);
    },
    [],
  );

  const handleEnabledChange = React.useCallback(
    (e: DropDownListChangeEvent) => {
      setEnabled(e.value?.value ?? false);
    },
    [],
  );

  const getBooleanOption = (value: boolean) =>
    booleanOptions.find((o) => o.value === value);

  const cancelEdit = React.useCallback(() => {
    setInEdit(false);
    if (selected) setSelectedData(selected);
  }, [selected, setSelectedData]);

  const saveEdit = React.useCallback(async () => {
    if (!selected || !editEventDef) return;

    if (!caption.trim() || !verbosity.trim()) {
      appContext.showNotification({
        notificationType: {
          icon: true,
          style: "warning",
        },
        message: "Caption and Verbosity are required",
      });
      return;
    }

    await editEventDef(selected.ID, {
      Caption: caption,
      Verbosity: verbosity,
      Silent: silent,
      Visible: visible,
      Enabled: enabled,
    });

    setInEdit(false);
  }, [selected, editEventDef, caption, verbosity, silent, visible, enabled]);

  const confirmDeletion = React.useCallback(async () => {
    if (!selected || !deleteEventDef) return;
    await deleteEventDef(selected);
    setShowDialog(false);
    setInEdit(false);
  }, [selected, deleteEventDef]);

  React.useEffect(() => {
    if (selected) {
      setSelectedData(selected);
      setInEdit(false);
    }
  }, [selected, setSelectedData]);

  if (!selected) {
    return (
      <div className="detail-panel-content">
        <Label>{t("common:no_selection")}</Label>
      </div>
    );
  }

  return (
    <div className="detail-panel-content">
      <div className="item-column">
        <div>
          <Label>ID</Label>
          <TextBox value={id} disabled />
        </div>

        <div>
          <Label>Caption</Label>
          <TextBox
            value={caption}
            disabled={!inEdit}
            onChange={handleCaptionChange}
          />
        </div>

        <div>
          <Label>Verbosity</Label>
          <TextBox
            value={verbosity}
            disabled={!inEdit}
            onChange={handleVerbosityChange}
          />
        </div>

        <div>
          <Label>Silent</Label>
          <DropDownList
            data={booleanOptions}
            textField="text"
            dataItemKey="value"
            value={getBooleanOption(silent)}
            onChange={handleSilentChange}
            disabled={!inEdit}
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
            disabled={!inEdit}
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
            disabled={!inEdit}
          />
        </div>
      </div>

      <div className="item-row">
        {!inEdit ? (
          <>
            <Button svgIcon={pencilIcon} onClick={() => setInEdit(true)}>
              {t("common:edit")}
            </Button>

            <Button svgIcon={plusIcon} onClick={enterAddNewEventDef}>
              {t("config-page:add_new_event_def")}
            </Button>
          </>
        ) : (
          <>
            <Button svgIcon={cancelIcon} onClick={cancelEdit}>
              {t("common:cancel")}
            </Button>

            <Button svgIcon={trashIcon} onClick={() => setShowDialog(true)}>
              {t("common:delete")}
            </Button>

            <Button svgIcon={saveIcon} themeColor="primary" onClick={saveEdit}>
              {t("common:save")}
            </Button>
          </>
        )}
      </div>

      {showDialog && (
        <Dialog
          title={t("common:confirm_deletion")}
          onClose={() => setShowDialog(false)}
        >
          Delete event definition?
          <DialogActionsBar>
            <Button svgIcon={cancelIcon} onClick={() => setShowDialog(false)}>
              {t("common:cancel")}
            </Button>

            <Button
              svgIcon={trashIcon}
              themeColor="primary"
              onClick={confirmDeletion}
            >
              {t("common:delete")}
            </Button>
          </DialogActionsBar>
        </Dialog>
      )}
    </div>
  );
});

export default EventDefDetailPanel;
