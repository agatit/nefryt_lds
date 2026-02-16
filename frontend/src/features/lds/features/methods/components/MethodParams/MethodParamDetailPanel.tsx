import React from "react";
import { useTranslation } from "react-i18next";
import { MethodParam, Method } from "../../../../../../services/api";
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
  selected: MethodParam | null;
  selectedMethod: Method | null;
  updateParam: (
    methodID: number,
    paramDefID: string,
    value: string,
  ) => Promise<void>;
  deleteParam: (methodID: number, paramDefID: string) => Promise<void>;
  openAddDialog: () => void;
  openDeleteDialog: () => void;
}

const MethodParamDetailPanel = React.memo(function MethodParamDetailPanel({
  selected,
  selectedMethod,
  updateParam,
  openAddDialog,
  openDeleteDialog,
}: Props) {
  const { t } = useTranslation(["common", "method-page"]);
  const [inEdit, setInEdit] = React.useState(false);
  const [value, setValue] = React.useState("");

  const handleValueChange = React.useCallback((e: TextBoxChangeEvent) => {
    setValue(String(e.value ?? ""));
  }, []);

  const saveEdit = async () => {
    if (!selected || !selectedMethod) return;

    await updateParam(selectedMethod.ID, selected.MethodParamDefID, value);

    setInEdit(false);
  };

  if (!selected || !selectedMethod) {
    return (
      <div className="detail-panel-content">{t("common:no_selection")}</div>
    );
  }

  React.useEffect(() => {
    if (selected) setValue(selected.Value ?? "");
    setInEdit(false);
  }, [selected]);

  return (
    <div className="detail-panel-content">
      <div className="item-column">
        <Label>Param ID</Label>
        <TextBox value={selected.MethodParamDefID} disabled />

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
              {t("method-page:add_method_param")}
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

export default MethodParamDetailPanel;
