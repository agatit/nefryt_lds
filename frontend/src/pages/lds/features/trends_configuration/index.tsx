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

const TrendConfigurationPage = React.memo(function TrendConfigurationPage() {
  const { t } = useTranslation(["common", "config-page"]);
  const ldsContext = useContext(LDSContext);

  if (!ldsContext) return null;

  const [verticalPanes, setVerticalPanes] = useState<SplitterPaneProps[]>([
    { size: "66%" },
    {},
  ]);
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
  const [panelOpen, setPanelOpen] = useState(false);
  const [addMode, setAddMode] = useState(false);
  const [tabSelected, setTabSelected] = useState(0);
  const [showAddNewTrendGroupDialog, setShowAddNewTrendGroupDialog] =
    useState(false);
  const [showAddNewUnitDialog, setShowAddNewUnitDialog] = useState(false);
  const [showDeleteDialog, setShowDeleteDialog] = useState(false);
  const [selected, setSelected] = useState<ParsedTrendType | null>(null);

  const [selection, setSelection] = useState<SelectionType>({
    trend: null,
    trendParamDef: null,
    trendDef: null,
    trendGroup: null,
    unit: null,
  });

  const handleVerticalChange = (event: SplitterOnChangeEvent) => {
    setVerticalPanes(event.newState);
  };

  const openAddNewTrendGroupDialog = () => setShowAddNewTrendGroupDialog(true);

  const closeAddNewTrendGroupDialog = () =>
    setShowAddNewTrendGroupDialog(false);

  const openAddNewUnitDialog = () => setShowAddNewUnitDialog(true);

  const closeAddNewUnitDialog = () => setShowAddNewUnitDialog(false);

  const handleTabSelect = useCallback((e: TabStripSelectEventArguments) => {
    setTabSelected(e.selected);
  }, []);

  const requestDelete = useCallback((trend: ParsedTrendType) => {
    setSelected(trend);
    setShowDeleteDialog(true);
  }, []);

  const confirmDelete = useCallback(async () => {
    if (!selected) return;

    try {
      await deleteTrend(selected);
      setSelected(null);
      setPanelOpen(false);
    } finally {
      setShowDeleteDialog(false);
    }
  }, [selected, deleteTrend]);

  const openAddNewTrendPanel = () => {
    setSelection({
      trend: null,
      trendParamDef: null,
      trendDef: null,
      trendGroup: null,
      unit: null,
    });

    setAddMode(true);
    setPanelOpen(true);
  };

  const handleSelectedTrendChange = (value: ParsedTrendType) => {
    setAddMode(false);
    setSelection({
      trend: value,
      trendParamDef: null,
      trendDef: null,
      trendGroup: null,
      unit: null,
    });
    setPanelOpen(true);
  };

  const handleSelectedTrendDefChange = (value: TrendDef) => {
    setSelection({
      trend: null,
      trendParamDef: null,
      trendDef: value,
      trendGroup: null,
      unit: null,
    });
    setPanelOpen(true);
  };

  const handleSelectedTrendGroupChange = (value: TrendGroup) => {
    setSelection({
      trend: null,
      trendParamDef: null,
      trendDef: null,
      trendGroup: value,
      unit: null,
    });
    setPanelOpen(true);
  };

  const handleSelectedUnitChange = (value: Unit) => {
    setSelection({
      trend: null,
      trendParamDef: null,
      trendDef: null,
      trendGroup: null,
      unit: value,
    });
    setPanelOpen(true);
  };

  const handleSelectedTrendDeletion = async (value: Trend) => {
    await ldsContext.deleteTrend(value);
    setSelection({
      trend: null,
      trendParamDef: null,
      trendDef: null,
      trendGroup: null,
      unit: null,
    });
    setPanelOpen(false);
  };

  const handleSelectedTrendGroupDeletion = async (value: TrendGroup) => {
    await ldsContext.deleteTrendGroup(value);
    setSelection({
      trend: null,
      trendParamDef: null,
      trendDef: null,
      trendGroup: null,
      unit: null,
    });
    setPanelOpen(false);
  };

  const handleSelectedUnitDeletion = async (value: Unit) => {
    await ldsContext.deleteUnit(value);
    setSelection({
      trend: null,
      trendParamDef: null,
      trendDef: null,
      trendGroup: null,
      unit: null,
    });
    setPanelOpen(false);
  };

  const isSelected =
    addMode ||
    selection.trend ||
    selection.trendDef ||
    selection.trendGroup ||
    selection.unit;

  const SelectedDetailPanel = () => {
    if (selection.trend || addMode) {
      return (
        <TrendConfigurationDetailPanel
          trendDefs={trendDefs}
          trendGroups={trendGroups}
          units={units}
          editTrend={updateTrend}
          addTrend={addTrend}
          deleteTrend={handleSelectedTrendDeletion}
          selected={selection.trend}
          addMode={addMode}
          setAddMode={setAddMode}
          requestDelete={requestDelete}
        />
      );
    }

    if (selection.trendDef)
      return <TrendDefConfigurationDetailPanel selected={selection.trendDef} />;

    if (selection.trendGroup)
      return (
        <TrendGroupConfigurationDetailPanel
          editTrendGroup={updateTrendGroup}
          deleteTrendGroup={handleSelectedTrendGroupDeletion}
          selected={selection.trendGroup}
          enterAddNewTrendGroup={openAddNewTrendGroupDialog}
        />
      );

    if (selection.unit)
      return (
        <TrendUnitConfigurationDetailPanel
          editUnit={updateUnit}
          deleteUnit={handleSelectedUnitDeletion}
          selected={selection.unit}
          enterAddNewUnit={openAddNewUnitDialog}
        />
      );

    return <></>;
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
          enterAddNewTrend={openAddNewTrendPanel}
          requestDelete={requestDelete}
        />

        <TabStrip
          className="config-trend-stuff-tab"
          selected={tabSelected}
          onSelect={handleTabSelect}
        >
          <TabStripTab title={t("config-page:trends_types")}>
            <TrendDefConfiguration
              trendDefs={trendDefs}
              selected={selection.trendDef}
              setSelected={handleSelectedTrendDefChange}
            />
          </TabStripTab>

          <TabStripTab title={t("config-page:trends_groups")}>
            <TrendGroupConfiguration
              showDialog={showAddNewTrendGroupDialog}
              openDialog={openAddNewTrendGroupDialog}
              closeDialog={closeAddNewTrendGroupDialog}
              trendGroups={trendGroups}
              addTrendGroup={addTrendGroup}
              deleteTrendGroup={handleSelectedTrendGroupDeletion}
              selected={selection.trendGroup}
              setSelected={handleSelectedTrendGroupChange}
            />
          </TabStripTab>

          <TabStripTab title={t("config-page:trends_units")}>
            <TrendUnitConfiguration
              showDialog={showAddNewUnitDialog}
              openDialog={openAddNewUnitDialog}
              closeDialog={closeAddNewUnitDialog}
              units={units}
              addUnit={addUnit}
              deleteUnit={handleSelectedUnitDeletion}
              selected={selection.unit}
              setSelected={handleSelectedUnitChange}
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

      {showDeleteDialog && (
        <Dialog
          title={t("common:confirm_deletion")}
          onClose={() => setShowDeleteDialog(false)}
        >
          {t("config-page:sure_you_want_delete_trend")}
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
    </main>
  );
});

export default TrendConfigurationPage;
