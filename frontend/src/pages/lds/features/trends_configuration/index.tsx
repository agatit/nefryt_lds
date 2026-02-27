import React from "react";
import "../../../../styles/layouts/detail-panel.scss";
import "./trendConfiguration.scss";
import { DetailPanel } from "onyks_shared_kendo";
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
  const ldsContext = React.useContext(LDSContext);

  if (!ldsContext) return null;

  const [verticalPanes, setVerticalPanes] = React.useState<SplitterPaneProps[]>(
    [{ size: "66%" }, {}],
  );
  const [panelOpen, setPanelOpen] = React.useState(false);
  const [addMode, setAddMode] = React.useState(false);
  const [tabSelected, setTabSelected] = React.useState(0);
  const [showAddNewTrendGroupDialog, setShowAddNewTrendGroupDialog] =
    React.useState(false);
  const [showAddNewUnitDialog, setShowAddNewUnitDialog] = React.useState(false);

  const handleVerticalChange = (event: SplitterOnChangeEvent) => {
    setVerticalPanes(event.newState);
  };

  const handleTabSelect = React.useCallback(
    (e: TabStripSelectEventArguments) => {
      setTabSelected(e.selected);
    },
    [],
  );

  const openAddNewTrendGroupDialog = () => setShowAddNewTrendGroupDialog(true);

  const closeAddNewTrendGroupDialog = () =>
    setShowAddNewTrendGroupDialog(false);

  const openAddNewUnitDialog = () => setShowAddNewUnitDialog(true);

  const closeAddNewUnitDialog = () => setShowAddNewUnitDialog(false);

  const [selection, setSelection] = React.useState<SelectionType>({
    trend: null,
    trendParamDef: null,
    trendDef: null,
    trendGroup: null,
    unit: null,
  });

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

  const selectedDetailPanel = React.useMemo(() => {
    if (selection.trend || addMode) {
      return (
        <TrendConfigurationDetailPanel
          trendDefs={ldsContext.trendDefs}
          trendGroups={ldsContext.trendGroups}
          trendParamDefs={ldsContext.trendParamDefs}
          units={ldsContext.units}
          selected={selection.trend}
          editTrend={ldsContext.updateTrend}
          addTrend={ldsContext.addTrend}
          deleteTrend={handleSelectedTrendDeletion}
          addMode={addMode}
          setAddMode={setAddMode}
          closePanel={() => setPanelOpen(false)}
        />
      );
    }

    if (selection.trendDef)
      return <TrendDefConfigurationDetailPanel selected={selection.trendDef} />;

    if (selection.trendGroup)
      return (
        <TrendGroupConfigurationDetailPanel
          editTrendGroup={ldsContext.updateTrendGroup}
          deleteTrendGroup={handleSelectedTrendGroupDeletion}
          selected={selection.trendGroup}
          enterAddNewTrendGroup={openAddNewTrendGroupDialog}
        />
      );

    if (selection.unit)
      return (
        <TrendUnitConfigurationDetailPanel
          editUnit={ldsContext.updateUnit}
          deleteUnit={handleSelectedUnitDeletion}
          selected={selection.unit}
          enterAddNewUnit={openAddNewUnitDialog}
        />
      );

    return <></>;
  }, [selection, addMode]);

  return (
    <main className="config-page">
      <Splitter
        className="config-grid-container"
        panes={verticalPanes}
        orientation="vertical"
        onChange={handleVerticalChange}
      >
        <TrendConfiguration
          trendDefs={ldsContext.trendDefs}
          trendGroups={ldsContext.trendGroups}
          trendParamDefs={ldsContext.trendParamDefs}
          units={ldsContext.units}
          trends={ldsContext.trends}
          deleteTrend={handleSelectedTrendDeletion}
          selected={selection.trend}
          setSelected={handleSelectedTrendChange}
          enterAddNewTrend={openAddNewTrendPanel}
        />

        <TabStrip
          className="config-trend-stuff-tab"
          selected={tabSelected}
          onSelect={handleTabSelect}
        >
          {/* <TabStripTab title={t("config-page:trends_types")}>
            <TrendDefConfiguration
              trendDefs={ldsContext.trendDefs}
              selected={selection.trendDef}
              setSelected={handleSelectedTrendDefChange}
            />
          </TabStripTab> */}

          <TabStripTab title={t("config-page:trends_groups")}>
            <TrendGroupConfiguration
              showDialog={showAddNewTrendGroupDialog}
              openDialog={openAddNewTrendGroupDialog}
              closeDialog={closeAddNewTrendGroupDialog}
              trendGroups={ldsContext.trendGroups}
              addTrendGroup={ldsContext.addTrendGroup}
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
              units={ldsContext.units}
              addUnit={ldsContext.addUnit}
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
        {isSelected && selectedDetailPanel}
      </DetailPanel>
    </main>
  );
});

export default TrendConfigurationPage;
