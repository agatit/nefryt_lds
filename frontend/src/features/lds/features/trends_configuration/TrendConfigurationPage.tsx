import React from "react";
import "../../../../styles/layouts/detail-panel.scss";
import "../../../../styles/features/lds/features/trendConfiguration.scss";
import { DetailPanel } from "onyks_shared_kendo";
import {
  mockupTrendDefs,
  mockupTrendGroups,
  mockupTrends,
  MockupTrendType,
  mockupUnits,
} from "../../../../data/mockup-data";
import { AuthContext } from "../../../../contexts/authContext";
import { useRefreshableRequest } from "../../../../hooks/useRefreshableRequest";
import { useTranslation } from "react-i18next";
import { Typography } from "@progress/kendo-react-common";

import { TrendDefBase, TrendGroup, Unit } from "../../../../services/api";
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

export interface ParsedTrendType extends MockupTrendType {
  trendType: string;
  trendGroup: string;
}

const TrendConfigurationPage = React.memo(function TrendConfigurationPage() {
  const auth = React.useContext(AuthContext);
  const refreshableRequest = useRefreshableRequest();
  const { t } = useTranslation(["common", "config-page"]);

  const [trendDefs, setTrendDefs] =
    React.useState<TrendDefBase[]>(mockupTrendDefs);
  const [trendGroups, setTrendGroups] =
    React.useState<TrendGroup[]>(mockupTrendGroups);
  const [units, setUnits] = React.useState<Unit[]>(mockupUnits);
  const [trends, setTrends] = React.useState<MockupTrendType[]>(mockupTrends);

  const [selected, setSelected] = React.useState<ParsedTrendType | null>(null);

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

  const [showAddNewTrendDefDialog, setShowAddNewTrendDefDialog] =
    React.useState<boolean>(false);
  const openAddNewTrendDefDialog = React.useCallback(() => {
    setShowAddNewTrendDefDialog(true);
  }, []);
  const closeAddNewTrendDefDialog = React.useCallback(() => {
    setShowAddNewTrendDefDialog(false);
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
            trendDefs={trendDefs}
            trendGroups={trendGroups}
            units={units}
            trends={trends}
            setTrends={setTrends}
            setSelected={setSelected}
          />

          <TabStrip
            className="config-trend-stuff-tab"
            selected={tabSelected}
            onSelect={handleTabSelect}
          >
            <TabStripTab title={t("config-page:trends_types")}>
              <TrendDefConfiguration
                showDialog={showAddNewTrendDefDialog}
                openDialog={openAddNewTrendDefDialog}
                closeDialog={closeAddNewTrendDefDialog}
                trendDefs={trendDefs}
                setTrendDefs={setTrendDefs}
              />
            </TabStripTab>
            <TabStripTab title={t("config-page:trends_groups")}>
              <TrendGroupConfiguration
                showDialog={showAddNewTrendGroupDialog}
                openDialog={openAddNewTrendGroupDialog}
                closeDialog={closeAddNewTrendGroupDialog}
                trendGroups={trendGroups}
                setTrendGroups={setTrendGroups}
              />
            </TabStripTab>
            <TabStripTab title={t("config-page:trends_units")}>
              <TrendUnitConfiguration
                showDialog={showAddNewUnitDialog}
                openDialog={openAddNewUnitDialog}
                closeDialog={closeAddNewUnitDialog}
                units={units}
                setUnits={setUnits}
              />
            </TabStripTab>
          </TabStrip>
        </Splitter>
        <DetailPanel
          className={
            "config-detail-panel" + (selected !== null ? "" : " no-selected")
          }
          flexGrow={1}
          extandable={false}
        >
          {selected !== null ? (
            <TrendConfigurationDetailPanel
              trendDefs={trendDefs}
              trendGroups={trendGroups}
              units={units}
              trends={trends}
              setTrends={setTrends}
              selected={selected}
              enterAddNewTrend={openAddNewTrendDialog}
            />
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
