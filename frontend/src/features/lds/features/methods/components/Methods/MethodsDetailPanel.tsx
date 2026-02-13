import React from "react";
import { Method, MethodUpdate } from "../../../../../../services/api";
import { Label } from "@progress/kendo-react-labels";
import { useTranslation } from "react-i18next";
import { TextBox, TextBoxChangeEvent } from "@progress/kendo-react-inputs";
import { Button } from "@progress/kendo-react-buttons";
import {
  pencilIcon,
  cancelIcon,
  trashIcon,
  saveIcon,
  plusIcon,
} from "@progress/kendo-svg-icons";

interface Props {
  selected: Method;
  updateMethod: (id: number, value: MethodUpdate) => Promise<void>;
  deleteMethod: (m: Method) => Promise<void>;
  openAddDialog: () => void;
}

const MethodsDetailPanel: React.FC<Props> = ({
  selected,
  updateMethod,
  openAddDialog,
  deleteMethod,
}) => {
  const { t } = useTranslation(["common"]);
  const [inEdit, setInEdit] = React.useState(false);
  const [name, setName] = React.useState(selected.Name ?? "");
  const definition = selected.MethodDefID ?? "";
  const pipeline = selected.PipelineID ?? "";
  const id = selected.ID ?? "";

  const handleNameChange = React.useCallback((e: TextBoxChangeEvent) => {
    setName(String(e.value ?? ""));
  }, []);

  const cancelEdit = () => {
    setName(selected.Name ?? "");
    setInEdit(false);
  };

  const saveEdit = async () => {
    await updateMethod(selected.ID, {
      Name: name,
      MethodDefID: selected.MethodDefID,
      PipelineID: selected.PipelineID,
    });

    setInEdit(false);
  };

  React.useEffect(() => {
    setName(selected.Name ?? "");
    setInEdit(false);
  }, [selected]);

  return (
    <div className="detail-panel-content">
      <div className="item-column">
        <Label>ID</Label>
        <TextBox value={id} disabled />

        <Label>Pipeline ID</Label>
        <TextBox value={pipeline} disabled />

        <Label>Method definition ID</Label>
        <TextBox value={definition} disabled />

        <Label>Name</Label>
        <TextBox value={name} disabled={!inEdit} onChange={handleNameChange} />

        <div className="item-row">
          {!inEdit ? (
            <>
              <Button svgIcon={pencilIcon} onClick={() => setInEdit(true)}>
                {t("common:edit")}
              </Button>

              <Button svgIcon={plusIcon} onClick={openAddDialog}>
                {t("link-page:add_new_method")}
              </Button>
            </>
          ) : (
            <>
              <Button svgIcon={cancelIcon} onClick={cancelEdit}>
                {t("common:cancel")}
              </Button>

              <Button
                svgIcon={saveIcon}
                themeColor="primary"
                onClick={saveEdit}
              >
                {t("common:save")}
              </Button>

              <Button
                svgIcon={trashIcon}
                onClick={() => deleteMethod(selected)}
              >
                {t("common:delete")}
              </Button>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default MethodsDetailPanel;
