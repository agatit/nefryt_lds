import React from "react";
import { useTranslation } from "react-i18next";
import { PipelineParam } from "../../../../../../services/api";
import { TextBox, TextBoxChangeEvent } from "@progress/kendo-react-inputs";
import { Label } from "@progress/kendo-react-labels";
import { Button } from "@progress/kendo-react-buttons";
import {
  pencilIcon,
  cancelIcon,
  trashIcon,
  saveIcon,
  plusIcon,
} from "@progress/kendo-svg-icons";

interface Props {
  selected: PipelineParam | null;
  pipelineID: number;
  updateParam: (
    pipelineID: number,
    paramID: string,
    value: string,
  ) => Promise<void>;
  deleteParam: (value: PipelineParam) => Promise<void>;
  openAddDialog: () => void;
  openDeleteDialog: () => void;
}

const PipelineParamDetailPanel = React.memo(function PipelineParamDetailPanel({
  selected,
  pipelineID,
  updateParam,
  openDeleteDialog,
  openAddDialog,
}: Props) {
  const { t } = useTranslation(["common", "pipeline-page"]);
  const [inEdit, setInEdit] = React.useState(false);
  const [value, setValue] = React.useState("");

  const handleValueChange = React.useCallback((e: TextBoxChangeEvent) => {
    setValue(String(e.value ?? ""));
  }, []);

  const saveEdit = async () => {
    if (!selected) return;

    await updateParam(pipelineID, selected.PipelineParamDefID, value);

    setInEdit(false);
  };

  React.useEffect(() => {
    if (selected) setValue(selected.Value ?? "");
    setInEdit(false);
  }, [selected]);

  if (!selected) {
    return (
      <div className="detail-panel-content">{t("common:no_selection")}</div>
    );
  }

  return (
    <div className="detail-panel-content">
      <div className="item-column">
        <Label>Param ID</Label>
        <TextBox value={selected.PipelineParamDefID} disabled />

        <Label>Name</Label>
        <TextBox value={selected.Name ?? ""} disabled />

        <Label>Value</Label>
        <TextBox
          value={value}
          disabled={!inEdit}
          onChange={handleValueChange}
        />

        <Label>DataType</Label>
        <TextBox value={selected.DataType ?? ""} disabled />
      </div>

      <div className="item-row">
        {!inEdit ? (
          <>
            <Button svgIcon={pencilIcon} onClick={() => setInEdit(true)}>
              {t("common:edit")}
            </Button>

            <Button svgIcon={plusIcon} onClick={openAddDialog}>
              {t("pipeline-page:add_pipeline_param")}
            </Button>
          </>
        ) : (
          <>
            <Button svgIcon={cancelIcon} onClick={() => setInEdit(false)}>
              {t("common:cancel")}
            </Button>

            <Button svgIcon={saveIcon} themeColor="primary" onClick={saveEdit}>
              {t("common:save")}
            </Button>

            <Button svgIcon={trashIcon} onClick={openDeleteDialog}>
              {t("common:delete")}
            </Button>
          </>
        )}
      </div>
    </div>
  );
});

export default PipelineParamDetailPanel;
