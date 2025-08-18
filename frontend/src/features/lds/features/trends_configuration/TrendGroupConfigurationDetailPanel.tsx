import React from "react";
import { useTranslation } from "react-i18next";
import { TrendDefBase, TrendGroup } from "../../../../services/api";
import { TextBox, TextBoxChangeEvent } from "@progress/kendo-react-inputs";
import { Label } from "@progress/kendo-react-labels";
import {
  cancelIcon,
  pencilIcon,
  plusIcon,
  saveIcon,
} from "@progress/kendo-svg-icons";
import { Button } from "@progress/kendo-react-buttons";

export interface TrendGroupConfigurationDetailPanelProps {
  editTrendGroup: (value: TrendGroup) => Promise<void>;
  selected: TrendGroup | null;
  enterAddNewTrendGroup: () => void;
}

const TrendGroupConfigurationDetailPanel = React.memo(
  function TrendGroupConfigurationDetailPanel({
    editTrendGroup,
    selected,
    enterAddNewTrendGroup,
  }: TrendGroupConfigurationDetailPanelProps) {
    const { t } = useTranslation(["common", "config-page"]);

    const setSelectedData = React.useCallback(
      (selectedTrendGroup: TrendGroup) => {
        setTrendGroupID(selectedTrendGroup.ID);
        setTrendGroupName(selectedTrendGroup.Name ?? "");
      },
      []
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
      selected?.ID
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
      []
    );

    const saveEdit = React.useCallback(async () => {
      const newTrendGroup: TrendGroup = {
        ID: trendGroupID!,
        Name: trendGroupName!,
      };

      await editTrendGroup(newTrendGroup);
      setInEdit(false);
    }, [editTrendGroup, trendGroupID, trendGroupName]);

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
      </div>
    );
  }
);

export default TrendGroupConfigurationDetailPanel;
