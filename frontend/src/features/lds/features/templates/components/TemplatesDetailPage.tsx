import React from "react";
import { Label } from "@progress/kendo-react-labels";
import { TextBox, TextBoxChangeEvent } from "@progress/kendo-react-inputs";
import { Button } from "@progress/kendo-react-buttons";
import { Dialog, DialogActionsBar } from "@progress/kendo-react-dialogs";
import {
  pencilIcon,
  cancelIcon,
  trashIcon,
  saveIcon,
  plusIcon,
} from "@progress/kendo-svg-icons";
import { UNITS } from "./constants";
import {
  DropDownList,
  DropDownListChangeEvent,
} from "@progress/kendo-react-dropdowns";
import { Template, TemplateUpdate, Axis } from "../../../../../services/api";
import { useTranslation } from "react-i18next";

interface Props {
  selected: Template;
  updateTemplate: (id: number, value: TemplateUpdate) => Promise<void>;
  deleteTemplate: (id: number) => Promise<void>;
  openAddDialog: () => void;
}

const TemplatesDetailPanel = React.memo(function TemplatesDetailPanel({
  selected,
  updateTemplate,
  deleteTemplate,
  openAddDialog,
}: Props) {
  const { t } = useTranslation(["common", "template-page"]);
  const [inEdit, setInEdit] = React.useState(false);
  const [showDeleteDialog, setShowDeleteDialog] = React.useState(false);
  const [name, setName] = React.useState("");
  const [axes, setAxes] = React.useState<Axis[]>([]);

  const handleAxisUnitChange =
    (index: number) => (e: DropDownListChangeEvent) => {
      updateAxis(index, "UnitID", String(e.value ?? ""));
    };

  const handleAxisMinChange = (index: number) => (e: TextBoxChangeEvent) => {
    updateAxis(index, "ScaledMin", Number(e.value ?? 0));
  };

  const handleAxisMaxChange = (index: number) => (e: TextBoxChangeEvent) => {
    updateAxis(index, "ScaledMax", Number(e.value ?? 0));
  };
  
  const handleAxisTitleChange = (index: number) => (e: TextBoxChangeEvent) => {
    updateAxis(index, "Title", String(e.value ?? ""));
  };

  const handleNameChange = React.useCallback((e: TextBoxChangeEvent) => {
    setName(String(e.value ?? ""));
  }, []);

  const updateAxis = <K extends keyof Axis>(
    index: number,
    field: K,
    value: Axis[K],
  ) => {
    setAxes((prev) =>
      prev.map((a, i) => (i === index ? { ...a, [field]: value } : a)),
    );
  };

  const addAxis = () => {
    setAxes((prev) => [
      ...prev,
      {
        TrendsID: [],
        Title: "",
        UnitID: "",
        ScaledMin: 0,
        ScaledMax: 0,
      },
    ]);
  };

  const saveEdit = async () => {
    await updateTemplate(selected.ID, {
      Name: name,
      Axes: axes,
    });

    setInEdit(false);
  };

  const cancelEdit = () => {
    setName(selected.Name);
    setAxes(selected.Axes ?? []);
    setInEdit(false);
  };

  const confirmDelete = async () => {
    await deleteTemplate(selected.ID);
    setShowDeleteDialog(false);
  };

  React.useEffect(() => {
    if (!selected) return;

    setName(selected.Name);
    setAxes(selected.Axes ?? []);
    setInEdit(false);
  }, [selected]);

  return (
    <div className="detail-panel-content">
      <div className="item-column">
        <Label>ID</Label>
        <TextBox value={selected.ID.toString()} disabled />

        <Label>{t("template-page:name")}</Label>
        <TextBox value={name} disabled={!inEdit} onChange={handleNameChange} />
      </div>

      <div className="axes-container">
        {axes.map((axis, i) => (
          <div key={i} className="axis-card">
            <Label>Title</Label>
            <TextBox
              value={axis.Title}
              disabled={!inEdit}
              onChange={handleAxisTitleChange(i)}
            />

            <Label>Unit</Label>
            <DropDownList
              data={UNITS}
              value={axis.UnitID}
              disabled={!inEdit}
              onChange={handleAxisUnitChange(i)}
            />

            <Label>Min</Label>
            <TextBox
              value={axis.ScaledMin}
              disabled={!inEdit}
              onChange={handleAxisMinChange(i)}
            />

            <Label>Max</Label>
            <TextBox
              value={axis.ScaledMax}
              disabled={!inEdit}
              onChange={handleAxisMaxChange(i)}
            />
          </div>
        ))}
      </div>

      <div className="item-row">
        {!inEdit ? (
          <>
            <Button svgIcon={pencilIcon} onClick={() => setInEdit(true)}>
              {t("common:edit")}
            </Button>

            <Button svgIcon={plusIcon} onClick={openAddDialog}>
              Add template
            </Button>
          </>
        ) : (
          <>
            <Button svgIcon={cancelIcon} onClick={cancelEdit}>
              {t("common:cancel")}
            </Button>

            <Button svgIcon={saveIcon} themeColor="primary" onClick={saveEdit}>
              {t("common:save")}
            </Button>

            <Button
              svgIcon={trashIcon}
              onClick={() => setShowDeleteDialog(true)}
            >
              {t("common:delete")}
            </Button>

            <Button svgIcon={plusIcon} onClick={addAxis}>
              Add axis
            </Button>
          </>
        )}
      </div>

      {showDeleteDialog && (
        <Dialog
          title={t("common:confirm_deletion")}
          onClose={() => setShowDeleteDialog(false)}
        >
          Delete template?
          <DialogActionsBar>
            <Button onClick={() => setShowDeleteDialog(false)}>
              {t("common:cancel")}
            </Button>

            <Button themeColor="primary" onClick={confirmDelete}>
              {t("common:delete")}
            </Button>
          </DialogActionsBar>
        </Dialog>
      )}
    </div>
  );
});

export default TemplatesDetailPanel;
