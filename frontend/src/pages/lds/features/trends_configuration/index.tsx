import React, { useCallback, useState, useContext } from "react";
import "../../../../styles/layouts/detail-panel.scss";
import "./trendConfiguration.scss";
import { DetailPanel } from "onyks_shared_kendo";
import { Button } from "@progress/kendo-react-buttons";
import { Dialog, DialogActionsBar } from "@progress/kendo-react-dialogs";
import { useTranslation } from "react-i18next";
import {
  Trend,
  TrendDef,
  TrendGroup,
  TrendParamDef,
  Unit,
} from "../../../../services/api";
import {
  Splitter,
  SplitterOnChangeEvent,
  SplitterPaneProps,
  TabStrip,
  TabStripSelectEventArguments,
  TabStripTab,
} from "@progress/kendo-react-layout";
import TrendConfigurationDetailPanel from "./components/TrendConfiguration/TrendConfigurationDetailPanel";
import TrendConfiguration from "./components/TrendConfiguration/TrendConfiguration";
import TrendDefConfiguration from "./components/TrendDefConfiguration/TrendDefConfiguration";
import TrendGroupConfiguration from "./components/TrendGroupConfiguration/TrendGroupConfiguration";
import TrendUnitConfiguration from "./components/TrendUnitConfiguration/TrendUnitConfiguration";
import TrendDefConfigurationDetailPanel from "./components/TrendDefConfiguration/TrendDefConfigurationDetailPanel";
import TrendGroupConfigurationDetailPanel from "./components/TrendGroupConfiguration/TrendGroupConfigurationDetailPanel";
import TrendUnitConfigurationDetailPanel from "./components/TrendUnitConfiguration/TrendUnitConfigurationDetailPanel";
import { LDSContext } from "../../contexts/ldsContext";

export interface SelectionType {
  trend: ParsedTrendType | null;
  trendParamDef: TrendParamDef | null;
  trendDef: TrendDef | null;
  trendGroup: TrendGroup | null;
  unit: Unit | null;
}

export interface ParsedTrendType extends Trend {
  trendType: string;
  trendGroup: string;
  unit: string;
}

type AddModeType = "trend" | "trendGroup" | "unit" | null;

type DeleteTarget =
  | { type: "trend"; item: ParsedTrendType }
  | { type: "trendGroup"; item: TrendGroup }
  | { type: "unit"; item: Unit }
  | null;

const TrendConfigurationPage = React.memo(function TrendConfigurationPage() {
  const { t } = useTranslation(["common", "config-page"]);
  const ldsContext = useContext(LDSContext);
  if (!ldsContext) return null;

  const {
    trends,
    deleteTrend,
    addTrend,
    updateTrend,
    trendDefs,
    trendGroups,
    units,
    updateTrendGroup,
    updateUnit,
    addTrendGroup,
    addUnit,
  } = ldsContext;

  const { unitSymbols } = ldsContext;

  const [verticalPanes, setVerticalPanes] = useState<SplitterPaneProps[]>([
    { size: "66%" },
    {},
  ]);

  const [panelOpen, setPanelOpen] = useState(false);
  const [addMode, setAddMode] = useState<AddModeType>(null);
  const [tabSelected, setTabSelected] = useState(0);
  const [deleteTarget, setDeleteTarget] = useState<DeleteTarget>(null);

  const [selection, setSelection] = useState<SelectionType>({
    trend: null,
    trendParamDef: null,
    trendDef: null,
    trendGroup: null,
    unit: null,
  });

  const clearSelection = () =>
    setSelection({
      trend: null,
      trendParamDef: null,
      trendDef: null,
      trendGroup: null,
      unit: null,
    });

  const openAddMode = (mode: AddModeType) => {
    clearSelection();
    setAddMode(mode);
    setPanelOpen(true);
  };

  const handleVerticalChange = (event: SplitterOnChangeEvent) => {
    setVerticalPanes(event.newState);
  };

  const handleTabSelect = useCallback((e: TabStripSelectEventArguments) => {
    setTabSelected(e.selected);
  }, []);

  const handleSelectedTrendChange = (value: ParsedTrendType | null) => {
    setAddMode(null);
    clearSelection();
    if (value) {
      setSelection((prev) => ({ ...prev, trend: value }));
      setPanelOpen(true);
    }
  };

  const handleSelectedTrendDefChange = (value: TrendDef | null) => {
    setAddMode(null);
    clearSelection();
    if (value) {
      setSelection((prev) => ({ ...prev, trendDef: value }));
      setPanelOpen(true);
    }
  };

  const handleSelectedTrendGroupChange = (value: TrendGroup | null) => {
    setAddMode(null);
    clearSelection();
    if (value) {
      setSelection((prev) => ({ ...prev, trendGroup: value }));
      setPanelOpen(true);
    }
  };

  const handleSelectedUnitChange = (value: Unit | null) => {
    setAddMode(null);
    clearSelection();
    if (value) {
      setSelection((prev) => ({ ...prev, unit: value }));
      setPanelOpen(true);
    }
  };

  const requestDeleteTrend = (trend: ParsedTrendType) =>
    setDeleteTarget({ type: "trend", item: trend });

  const requestDeleteTrendGroup = (group: TrendGroup) =>
    setDeleteTarget({ type: "trendGroup", item: group });

  const requestDeleteUnit = (unit: Unit) =>
    setDeleteTarget({ type: "unit", item: unit });

  const confirmDelete = async () => {
    if (!deleteTarget) return;

    try {
      switch (deleteTarget.type) {
        case "trend":
          await deleteTrend(deleteTarget.item);
          break;

        case "trendGroup":
          await ldsContext.deleteTrendGroup(deleteTarget.item);
          break;

        case "unit":
          await ldsContext.deleteUnit(deleteTarget.item);
          break;
      }

      clearSelection();
      setPanelOpen(false);
    } finally {
      setDeleteTarget(null);
    }
  };

  const isSelected =
    addMode !== null ||
    selection.trend ||
    selection.trendDef ||
    selection.trendGroup ||
    selection.unit;

  const SelectedDetailPanel = () => {
    if (selection.trend || addMode === "trend") {
      return (
        <TrendConfigurationDetailPanel
          trendDefs={trendDefs}
          trendGroups={trendGroups}
          units={units}
          editTrend={updateTrend}
          addTrend={addTrend}
          deleteTrend={deleteTrend}
          selected={selection.trend}
          addMode={addMode === "trend"}
          setAddMode={(v) => setAddMode(v ? "trend" : null)}
          requestDelete={requestDeleteTrend}
        />
      );
    }

    if (selection.trendDef) {
      return <TrendDefConfigurationDetailPanel selected={selection.trendDef} />;
    }

    if (selection.trendGroup || addMode === "trendGroup") {
      return (
        <TrendGroupConfigurationDetailPanel
          editTrendGroup={updateTrendGroup}
          deleteTrendGroup={ldsContext.deleteTrendGroup}
          addTrendGroup={addTrendGroup}
          selected={selection.trendGroup}
          addMode={addMode === "trendGroup"}
          setAddMode={(v) => setAddMode(v ? "trendGroup" : null)}
        />
      );
    }

    if (selection.unit || addMode === "unit") {
      return (
        <TrendUnitConfigurationDetailPanel
          editUnit={updateUnit}
          addUnit={addUnit}
          requestDelete={requestDeleteUnit}
          selected={selection.unit}
          addMode={addMode === "unit"}
          setAddMode={(v) => setAddMode(v ? "unit" : null)}
          symbols={unitSymbols}
        />
      );
    }

    return null;
  };

  return (
    <main className="config-page">
      <Splitter
        className="config-grid-container"
        panes={verticalPanes}
        orientation="vertical"
        onChange={handleVerticalChange}
      >
        <TrendConfiguration
          trendDefs={trendDefs}
          trendGroups={trendGroups}
          units={units}
          trends={trends}
          selected={selection.trend}
          setSelected={handleSelectedTrendChange}
          enterAddNewTrend={() => openAddMode("trend")}
          requestDelete={requestDeleteTrend}
        />

        <TabStrip selected={tabSelected} onSelect={handleTabSelect}>
          <TabStripTab title={t("config-page:trends_types")}>
            <TrendDefConfiguration
              trendDefs={trendDefs}
              selected={selection.trendDef}
              setSelected={handleSelectedTrendDefChange}
            />
          </TabStripTab>

          <TabStripTab title={t("config-page:trends_groups")}>
            <TrendGroupConfiguration
              trendGroups={trendGroups}
              selected={selection.trendGroup}
              setSelected={handleSelectedTrendGroupChange}
              requestDelete={requestDeleteTrendGroup}
              enterAddNewTrendGroup={() => openAddMode("trendGroup")}
            />
          </TabStripTab>

          <TabStripTab title={t("config-page:trends_units")}>
            <TrendUnitConfiguration
              units={units}
              selected={selection.unit}
              setSelected={handleSelectedUnitChange}
              deleteUnit={requestDeleteUnit}
              enterAddNewUnit={() => openAddMode("unit")}
            />
          </TabStripTab>
        </TabStrip>
      </Splitter>

      <DetailPanel
        className={"config-detail-panel" + (isSelected ? "" : " no-selected")}
        flexGrow={1}
        extandable
        extended={panelOpen}
        onExtendedChange={setPanelOpen}
      >
        {isSelected && <SelectedDetailPanel />}
      </DetailPanel>

      {deleteTarget && (
        <Dialog
          title={t("common:confirm_deletion")}
          onClose={() => setDeleteTarget(null)}
        >
          {deleteTarget.type === "trend" &&
            t("config-page:sure_you_want_delete_trend")}
          {deleteTarget.type === "trendGroup" &&
            t("config-page:sure_you_want_delete_trend_group")}
          {deleteTarget.type === "unit" &&
            t("config-page:sure_you_want_delete_unit")}

          <DialogActionsBar>
            <Button onClick={() => setDeleteTarget(null)}>
              {t("common:cancel")}
            </Button>
            <Button themeColor="primary" onClick={confirmDelete}>
              {t("common:delete")}
            </Button>
          </DialogActionsBar>
        </Dialog>
      )}
    </main>
  );
});

export default TrendConfigurationPage;
