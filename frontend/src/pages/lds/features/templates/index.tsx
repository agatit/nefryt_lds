import React from "react";
import "./templatePage.scss";
import { useTranslation } from "react-i18next";
import Templates from "./components/Templates";
import TemplatesDetailPanel from "./components/TemplatesDetailPage";
import { LDSContext } from "../../contexts/ldsContext";
import { DetailPanel } from "onyks_shared_kendo";
import { Typography } from "@progress/kendo-react-common";
import { Dialog, DialogActionsBar } from "@progress/kendo-react-dialogs";
import { TextBox, TextBoxChangeEvent } from "@progress/kendo-react-inputs";
import { Button } from "@progress/kendo-react-buttons";
import { Axis } from "../../../../services/api";
import { Template } from "../../../../services/api";
import { Label } from "@progress/kendo-react-labels";
import {
  DropDownList,
  DropDownListChangeEvent,
} from "@progress/kendo-react-dropdowns";
import { UNITS } from "./components/constants";
import {
  NumericTextBox,
  NumericTextBoxChangeEvent,
} from "@progress/kendo-react-inputs";
import { AppContext } from "../../../../contexts/appContext";

const TemplatePage = () => {
  const { t } = useTranslation(["common", "nodes-page"]);
  const appContext = React.useContext(AppContext);
  const lds = React.useContext(LDSContext);
  if (!appContext || !lds) return null;

  const { templates, addTemplate, updateTemplate, deleteTemplate } = lds;
  const [selected, setSelected] = React.useState<Template | null>(null);
  const [showAddDialog, setShowAddDialog] = React.useState(false);
  const [name, setName] = React.useState("");
  const [axes, setAxes] = React.useState<Axis[]>([]);

  const handleAxisTitleChange = (index: number) => (e: TextBoxChangeEvent) => {
    setAxes((prev) =>
      prev.map((axis, i) =>
        i === index ? { ...axis, Title: String(e.value ?? "") } : axis,
      ),
    );
  };

  const handleAxisUnitChange =
    (index: number) => (e: DropDownListChangeEvent) => {
      setAxes((prev) =>
        prev.map((axis, i) =>
          i === index ? { ...axis, UnitID: String(e.value ?? "") } : axis,
        ),
      );
    };

  const handleAxisMinChange =
    (index: number) => (e: NumericTextBoxChangeEvent) => {
      setAxes((prev) =>
        prev.map((axis, i) =>
          i === index ? { ...axis, ScaledMin: e.value ?? 0 } : axis,
        ),
      );
    };

  const handleAxisMaxChange =
    (index: number) => (e: NumericTextBoxChangeEvent) => {
      setAxes((prev) =>
        prev.map((axis, i) =>
          i === index ? { ...axis, ScaledMax: e.value ?? 0 } : axis,
        ),
      );
    };

  const handleNameChange = React.useCallback(
    (e: TextBoxChangeEvent) => setName(String(e.value ?? "")),
    [],
  );

  const handleAddAxis = () => {
    setAxes((prev) => [
      ...prev,
      {
        Title: "",
        UnitID: "",
        ScaledMin: 0,
        ScaledMax: 0,
        TrendsID: [],
      },
    ]);
  };

  const confirmAdd = async () => {
    const showError = (message: string) =>
      appContext.showNotification({
        notificationType: { icon: true, style: "error" },
        message,
      });

    if (!name.trim()) {
      showError("Template name required");
      return;
    }

    if (!axes.length) {
      showError("Add at least one axis");
      return;
    }

    if (axes.some((a) => !a.Title || !a.UnitID)) {
      showError("Axis title and unit required");
      return;
    }

    if (axes.some((a) => !a.UnitID?.trim())) {
      showError("Axis unit required");
      return;
    }

    await addTemplate({
      Name: name,
      Axes: axes,
    });

    setShowAddDialog(false);
    setName("");
    setAxes([]);
  };

  return (
    <main className="templates-page">
      <div className="links-grid-container">
        <Templates
          templates={templates}
          selected={selected}
          onSelectTemplate={setSelected}
          openAddDialog={() => setShowAddDialog(true)}
        />
      </div>

      <DetailPanel
        className={"templates-detail-panel" + (selected ? "" : " no-selected")}
        flexGrow={1}
        extandable={false}
      >
        {selected ? (
          <TemplatesDetailPanel
            selected={selected}
            updateTemplate={updateTemplate}
            deleteTemplate={deleteTemplate}
            openAddDialog={() => setShowAddDialog(true)}
          />
        ) : (
          <Typography.p>
            {t("template-page:select_element_to_edit")}
          </Typography.p>
        )}
      </DetailPanel>

      {showAddDialog && (
        <Dialog
          title="Add New Template"
          onClose={() => setShowAddDialog(false)}
          className="templates-dialog"
        >
          <TextBox
            placeholder="Template Name"
            value={name}
            onChange={handleNameChange}
          />

          <Button
            themeColor="primary"
            onClick={handleAddAxis}
            className="template-button"
          >
            Add Axis
          </Button>

          {axes.map((axis, index) => (
            <div key={index} className="axis-row">
              <Label>Title</Label>
              <TextBox
                value={axis.Title}
                onChange={handleAxisTitleChange(index)}
              />

              <Label>Unit</Label>
              <DropDownList
                data={UNITS}
                value={axis.UnitID}
                onChange={handleAxisUnitChange(index)}
              />

              <Label>Min</Label>
              <NumericTextBox
                value={axis.ScaledMin}
                onChange={handleAxisMinChange(index)}
              />

              <Label>Max</Label>
              <NumericTextBox
                value={axis.ScaledMax}
                onChange={handleAxisMaxChange(index)}
              />
            </div>
          ))}

          <DialogActionsBar>
            <Button onClick={() => setShowAddDialog(false)}>Cancel</Button>
            <Button themeColor="primary" onClick={confirmAdd}>
              Confirm
            </Button>
          </DialogActionsBar>
        </Dialog>
      )}
    </main>
  );
};

export default TemplatePage;
