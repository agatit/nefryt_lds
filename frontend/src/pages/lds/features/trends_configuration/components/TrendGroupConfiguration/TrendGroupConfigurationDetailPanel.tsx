import React from "react";
import { useTranslation } from "react-i18next";
import { TrendGroup } from "../../../../../../services/api";
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

export interface TrendGroupConfigurationDetailPanelProps {
  editTrendGroup: (value: TrendGroup) => Promise<void>;
  deleteTrendGroup: (value: TrendGroup) => Promise<void>;
  selected: TrendGroup | null;
  enterAddNewTrendGroup: () => void;
}

const TrendGroupConfigurationDetailPanel = React.memo(
  function TrendGroupConfigurationDetailPanel({
    editTrendGroup,
    deleteTrendGroup,
    selected,
    enterAddNewTrendGroup,
  }: TrendGroupConfigurationDetailPanelProps) {
    const { t } = useTranslation(["common", "config-page"]);

    const setSelectedData = React.useCallback(
      (selectedTrendGroup: TrendGroup) => {
        setTrendGroupID(selectedTrendGroup.ID);
        setTrendGroupName(selectedTrendGroup.Name ?? "");
      },
      [],
    );

    const [inEdit, setInEdit] = React.useState<boolean>(false);

    const enterEdit = React.useCallback(() => {
      setInEdit(true);
    }, []);
    const cancelEdit = React.useCallback(() => {
      setInEdit(false);
      if (selected !== null) setSelectedData(selected);
    }, [selected, setSelectedData]);

    const [trendGroupID, setTrendGroupID] = React.useState<number | undefined>(
      selected?.ID,
    );
    const [trendGroupName, setTrendGroupName] = React.useState<
      string | undefined
    >(selected?.Name ?? "");

    React.useEffect(() => {
      if (selected !== null) setSelectedData(selected);
    }, [selected]);

    const handleTrendGroupNameChange = React.useCallback(
      (event: TextBoxChangeEvent) => {
        if (event.value) setTrendGroupName(event.value.toString());
      },
      [],
    );

    const saveEdit = React.useCallback(async () => {
      const newTrendGroup: TrendGroup = {
        ID: trendGroupID!,
        Name: trendGroupName!,
      };

      await editTrendGroup(newTrendGroup);
      setInEdit(false);
    }, [editTrendGroup, trendGroupID, trendGroupName]);

    // Deletion dialog
    const [showDialog, setShowDialog] = React.useState<boolean>(false);
    const openDialog = React.useCallback(() => {
      setShowDialog(true);
    }, []);
    const closeDialog = React.useCallback(() => {
      setShowDialog(false);
    }, []);

    const confirmDeletion = React.useCallback(async () => {
      await deleteTrendGroup(selected!);
      setInEdit(false);
      closeDialog();
    }, [selected, deleteTrendGroup]);

    return (
      <div className="detail-panel-content">
        <div className="item">
          <div className="item-column">
            <div>
              <Label editorId="trendGroupName">{t("config-page:name")}</Label>
              <TextBox
                id="trendGroupName"
                value={trendGroupName}
                onChange={handleTrendGroupNameChange}
                disabled={!inEdit}
              />
            </div>
          </div>
        </div>
        <div className="separator" />
        <div className="item">
          {!inEdit ? (
            <div className="item-row">
              <Button svgIcon={pencilIcon} onClick={enterEdit}>
                {t("common:edit")}
              </Button>
              <Button svgIcon={plusIcon} onClick={enterAddNewTrendGroup}>
                {t("config-page:add_new_trend_group")}
              </Button>
            </div>
          ) : (
            <div className="item-row">
              <Button svgIcon={cancelIcon} onClick={cancelEdit}>
                {t("common:cancel")}
              </Button>
              <Button svgIcon={trashIcon} onClick={openDialog}>
                {t("common:delete")}
              </Button>
              <Button
                svgIcon={saveIcon}
                onClick={saveEdit}
                themeColor={"primary"}
              >
                {t("common:save")}
              </Button>
            </div>
          )}
        </div>
        {showDialog && (
          <Dialog title={t("common:confirm_deletion")} onClose={closeDialog}>
            {t("config-page:sure_you_want_delete_trend_group")}
            <DialogActionsBar>
              <Button svgIcon={cancelIcon} onClick={closeDialog}>
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
      </div>
    );
  },
);

export default TrendGroupConfigurationDetailPanel;
