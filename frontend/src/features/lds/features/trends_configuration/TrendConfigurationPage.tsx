import React from "react";
import "../../../../styles/layouts/detail-panel.scss";
import "../../../../styles/features/lds/features/trendConfiguration.scss";
import { DetailPanel } from "onyks_shared_kendo";
import {
  mockupTrendDefs,
  mockupTrendGroups,
  mockupTrends,
  mockupUnits,
} from "../../../../data/mockup-data";
import { AuthContext } from "../../../../contexts/authContext";
import { useRefreshableRequest } from "../../../../hooks/useRefreshableRequest";
import { useTranslation } from "react-i18next";
import { Typography } from "@progress/kendo-react-common";

import {
  Trend,
  TrendDefBase,
  TrendGroup,
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
import TrendConfigurationDetailPanel from "./TrendConfigurationDetailPanel";
import TrendConfiguration from "./TrendConfiguration";
import TrendDefConfiguration from "./TrendDefConfiguration";
import TrendGroupConfiguration from "./TrendGroupConfiguration";
import TrendUnitConfiguration from "./TrendUnitConfiguration";
import TrendDefConfigurationDetailPanel from "./TrendDefConfigurationDetailPanel";
import TrendGroupConfigurationDetailPanel from "./TrendGroupConfigurationDetailPanel";
import TrendUnitConfigurationDetailPanel from "./TrendUnitConfigurationDetailPanel";
import { LDSContext } from "../../contexts/ldsContext";
import { NavbarContext } from "../../../../contexts/navbarContext";

export interface SelectionType {
  trend: ParsedTrendType | null;
  trendDef: TrendDefBase | null;
  trendGroup: TrendGroup | null;
  unit: Unit | null;
}

export interface ParsedTrendType extends Trend {
  trendType: string;
  trendGroup: string;
  // unit: string; //waiting for unit api fix
}

const TrendConfigurationPage = React.memo(function TrendConfigurationPage() {
  const auth = React.useContext(AuthContext);
  const refreshableRequest = useRefreshableRequest();
  const { t } = useTranslation(["common", "config-page"]);

  const ldsContex = React.useContext(LDSContext);
  React.useMemo(() => {
    if (ldsContex == null)
      throw new Error(
        "LDS Context cannot be null to use TrendConfigurationPage"
      );
  }, [ldsContex]);

  const [verticalPanes, setVerticalPanes] = React.useState<SplitterPaneProps[]>(
    [{ size: "66%" }, {}]
  );
  const handleVerticalChange = (event: SplitterOnChangeEvent) => {
    setVerticalPanes(event.newState);
  };

  const [tabSelected, setTabSelected] = React.useState<number>(0);
  const handleTabSelect = React.useCallback(
    (e: TabStripSelectEventArguments) => {
      setTabSelected(e.selected);
    },
    []
  );

  // Dialogs controls
  const [showAddNewTrendDialog, setShowAddNewTrendDialog] =
    React.useState<boolean>(false);
  const openAddNewTrendDialog = React.useCallback(() => {
    setShowAddNewTrendDialog(true);
  }, []);
  const closeAddNewTrendDialog = React.useCallback(() => {
    setShowAddNewTrendDialog(false);
  }, []);

  const [showAddNewTrendGroupDialog, setShowAddNewTrendGroupDialog] =
    React.useState<boolean>(false);
  const openAddNewTrendGroupDialog = React.useCallback(() => {
    setShowAddNewTrendGroupDialog(true);
  }, []);
  const closeAddNewTrendGroupDialog = React.useCallback(() => {
    setShowAddNewTrendGroupDialog(false);
  }, []);

  const [showAddNewUnitDialog, setShowAddNewUnitDialog] =
    React.useState<boolean>(false);
  const openAddNewUnitDialog = React.useCallback(() => {
    setShowAddNewUnitDialog(true);
  }, []);
  const closeAddNewUnitDialog = React.useCallback(() => {
    setShowAddNewUnitDialog(false);
  }, []);

  // Selection
  const [selection, setSelection] = React.useState<SelectionType>({
    trend: null,
    trendDef: null,
    trendGroup: null,
    unit: null,
  });
  const isSelected = React.useMemo(
    () =>
      selection.trend !== null ||
      selection.trendDef !== null ||
      selection.trendGroup !== null ||
      selection.unit !== null,
    [selection]
  );

  const handleSelectedTrendChange = React.useCallback(
    (value: ParsedTrendType) => {
      setSelection({
        trend: value,
        trendDef: null,
        trendGroup: null,
        unit: null,
      });
    },
    []
  );

  const handleSelectedTrendDefChange = React.useCallback(
    (value: TrendDefBase) => {
      setSelection({
        trend: null,
        trendDef: value,
        trendGroup: null,
        unit: null,
      });
    },
    []
  );

  const handleSelectedTrendGroupChange = React.useCallback(
    (value: TrendGroup) => {
      setSelection({
        trend: null,
        trendDef: null,
        trendGroup: value,
        unit: null,
      });
    },
    []
  );

  const handleSelectedUnitChange = React.useCallback((value: Unit) => {
    setSelection({
      trend: null,
      trendDef: null,
      trendGroup: null,
      unit: value,
    });
  }, []);

  const SelectedDetailPanel = React.useCallback((): React.JSX.Element => {
    if (selection.trend)
      return (
        <TrendConfigurationDetailPanel
          trendDefs={ldsContex!.trendDefs}
          trendGroups={ldsContex!.trendGroups}
          units={ldsContex!.units}
          editTrend={ldsContex!.updateTrend}
          selected={selection.trend}
          enterAddNewTrend={openAddNewTrendDialog}
        />
      );
    if (selection.trendDef)
      return (
        <TrendDefConfigurationDetailPanel
          trendDefs={ldsContex!.trendDefs}
          selected={selection.trendDef}
        />
      );
    if (selection.trendGroup)
      return (
        <TrendGroupConfigurationDetailPanel
          editTrendGroup={ldsContex!.updateTrendGroup}
          selected={selection.trendGroup}
          enterAddNewTrendGroup={openAddNewTrendGroupDialog}
        />
      );
    if (selection.unit)
      return (
        <TrendUnitConfigurationDetailPanel
          editUnit={ldsContex!.updateUnit}
          selected={selection.unit}
          enterAddNewUnit={openAddNewUnitDialog}
        />
      );
    return <></>;
  }, [selection, ldsContex, openAddNewTrendDialog]);

  return (
    <React.Fragment>
      <main className="config-page">
        <Splitter
          className="config-grid-container"
          panes={verticalPanes}
          orientation="vertical"
          onChange={handleVerticalChange}
        >
          <TrendConfiguration
            showDialog={showAddNewTrendDialog}
            openDialog={openAddNewTrendDialog}
            closeDialog={closeAddNewTrendDialog}
            trendDefs={ldsContex!.trendDefs}
            trendGroups={ldsContex!.trendGroups}
            units={ldsContex!.units}
            trends={ldsContex!.trends}
            addTrend={ldsContex!.addTrend}
            selected={selection.trend}
            setSelected={handleSelectedTrendChange}
          />

          <TabStrip
            className="config-trend-stuff-tab"
            selected={tabSelected}
            onSelect={handleTabSelect}
          >
            <TabStripTab title={t("config-page:trends_types")}>
              <TrendDefConfiguration
                trendDefs={ldsContex!.trendDefs}
                selected={selection.trendDef}
                setSelected={handleSelectedTrendDefChange}
              />
            </TabStripTab>
            <TabStripTab title={t("config-page:trends_groups")}>
              <TrendGroupConfiguration
                showDialog={showAddNewTrendGroupDialog}
                openDialog={openAddNewTrendGroupDialog}
                closeDialog={closeAddNewTrendGroupDialog}
                trendGroups={ldsContex!.trendGroups}
                addTrendGroup={ldsContex!.addTrendGroup}
                selected={selection.trendGroup}
                setSelected={handleSelectedTrendGroupChange}
              />
            </TabStripTab>
            <TabStripTab title={t("config-page:trends_units")}>
              <TrendUnitConfiguration
                showDialog={showAddNewUnitDialog}
                openDialog={openAddNewUnitDialog}
                closeDialog={closeAddNewUnitDialog}
                units={ldsContex!.units}
                addUnit={ldsContex!.addUnit}
                selected={selection.unit}
                setSelected={handleSelectedUnitChange}
              />
            </TabStripTab>
          </TabStrip>
        </Splitter>
        <DetailPanel
          className={"config-detail-panel" + (isSelected ? "" : " no-selected")}
          flexGrow={1}
          extandable={false}
        >
          {isSelected ? (
            <SelectedDetailPanel />
          ) : (
            <Typography.p style={{ marginBottom: 0 }}>
              {t("config-page:select_element_to_edit")}
            </Typography.p>
          )}
        </DetailPanel>
      </main>
    </React.Fragment>
  );
});

export default TrendConfigurationPage;
