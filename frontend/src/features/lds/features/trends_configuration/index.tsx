import React from "react";
import "../../../../styles/layouts/detail-panel.scss";
import "./trendConfiguration.scss";
import { DetailPanel } from "onyks_shared_kendo";
import {
  mockupTrendDefs,
  mockupTrendGroups,
  mockupTrends,
  mockupUnits,
} from "../../../../data/mockup-data";
import { useTranslation } from "react-i18next";
import { Typography } from "@progress/kendo-react-common";

import {
  Trend,
  TrendDef,
  TrendGroup,
  TrendParam,
  TrendParamCreate,
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
import TrendParamDefConfiguration from "./components/TrendParamDefConfiguration/TrendParamDefConfiguration";
import TrendParamDefConfigurationDetailPanel from "./components/TrendParamDefConfiguration/TrendParamDefConfigurationDetailPanel";
import { useHandleApiResponse } from "../../../../hooks/useHandleApiResponse";

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
  const handleApiResponse = useHandleApiResponse();

  const ldsContext = React.useContext(LDSContext);
  React.useMemo(() => {
    if (ldsContext == null)
      throw new Error(
        "LDS Context cannot be null to use TrendConfigurationPage",
      );
  }, [ldsContext]);

  const [verticalPanes, setVerticalPanes] = React.useState<SplitterPaneProps[]>(
    [{ size: "66%" }, {}],
  );
  const handleVerticalChange = (event: SplitterOnChangeEvent) => {
    setVerticalPanes(event.newState);
  };

  const [tabSelected, setTabSelected] = React.useState<number>(0);
  const handleTabSelect = React.useCallback(
    (e: TabStripSelectEventArguments) => {
      setTabSelected(e.selected);
    },
    [],
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
    trendParamDef: null,
    trendDef: null,
    trendGroup: null,
    unit: null,
  });
  const isSelected = React.useMemo(
    () =>
      selection.trend !== null ||
      selection.trendParamDef !== null ||
      selection.trendDef !== null ||
      selection.trendGroup !== null ||
      selection.unit !== null,
    [selection],
  );

  const handleSelectedTrendChange = React.useCallback(
    (value: ParsedTrendType) => {
      setSelection({
        trend: value,
        trendParamDef: null,
        trendDef: null,
        trendGroup: null,
        unit: null,
      });
    },
    [],
  );

  const handleSelectedTrendParamDefChange = React.useCallback(
    (value: TrendParamDef) => {
      setSelection({
        trend: null,
        trendParamDef: value,
        trendDef: null,
        trendGroup: null,
        unit: null,
      });
    },
    [],
  );

  const handleSelectedTrendDefChange = React.useCallback((value: TrendDef) => {
    setSelection({
      trend: null,
      trendParamDef: null,
      trendDef: value,
      trendGroup: null,
      unit: null,
    });
  }, []);

  const handleSelectedTrendGroupChange = React.useCallback(
    (value: TrendGroup) => {
      setSelection({
        trend: null,
        trendParamDef: null,
        trendDef: null,
        trendGroup: value,
        unit: null,
      });
    },
    [],
  );

  const handleSelectedUnitChange = React.useCallback((value: Unit) => {
    setSelection({
      trend: null,
      trendParamDef: null,
      trendDef: null,
      trendGroup: null,
      unit: value,
    });
  }, []);

  const handleSelectedTrendDeletion = React.useCallback(
    async (value: Trend) => {
      // try {
      //   const trendParams: TrendParam[] = (
      //     await handleApiResponse(
      //       ldsContext!.trendParamApi.listTrendParamsByTrendIdTrendTrendIdParamGet.bind(
      //         ldsContext!.trendParamApi
      //       ),
      //       value.ID
      //     )
      //   ).data.items;
      await ldsContext!.deleteTrend(value);
      //   for (let param of trendParams) {
      //     try {
      //       await handleApiResponse(
      //         ldsContext!.trendParamApi.deleteTrendParamByIdTrendTrendIdParamTrendParamDefIdDelete.bind(
      //           ldsContext!.trendParamApi
      //         ),
      //         value.ID,
      //         param.TrendParamDefID
      //       );
      //     } catch (error) {
      //       console.log(error);
      //     }
      //   }
      // } catch (error) {
      //   console.log(error);
      // }
      setSelection({
        trend: null,
        trendParamDef: null,
        trendDef: null,
        trendGroup: null,
        unit: null,
      });
    },
    [],
  );

  const handleSelectedTrendGroupDeletion = React.useCallback(
    async (value: TrendGroup) => {
      await ldsContext!.deleteTrendGroup(value);
      setSelection({
        trend: null,
        trendParamDef: null,
        trendDef: null,
        trendGroup: null,
        unit: null,
      });
    },
    [],
  );

  const handleSelectedUnitDeletion = React.useCallback(async (value: Unit) => {
    await ldsContext!.deleteUnit(value);
    setSelection({
      trend: null,
      trendParamDef: null,
      trendDef: null,
      trendGroup: null,
      unit: null,
    });
  }, []);

  const SelectedDetailPanel = React.useCallback((): React.JSX.Element => {
    if (selection.trend)
      return (
        <TrendConfigurationDetailPanel
          trendDefs={ldsContext!.trendDefs}
          trendGroups={ldsContext!.trendGroups}
          trendParamDefs={ldsContext!.trendParamDefs}
          units={ldsContext!.units}
          editTrend={ldsContext!.updateTrend}
          deleteTrend={handleSelectedTrendDeletion}
          selected={selection.trend}
          enterAddNewTrend={openAddNewTrendDialog}
        />
      );
    if (selection.trendParamDef)
      return (
        <TrendParamDefConfigurationDetailPanel
          selected={selection.trendParamDef}
        />
      );
    if (selection.trendDef)
      return <TrendDefConfigurationDetailPanel selected={selection.trendDef} />;
    if (selection.trendGroup)
      return (
        <TrendGroupConfigurationDetailPanel
          editTrendGroup={ldsContext!.updateTrendGroup}
          deleteTrendGroup={handleSelectedTrendGroupDeletion}
          selected={selection.trendGroup}
          enterAddNewTrendGroup={openAddNewTrendGroupDialog}
        />
      );
    if (selection.unit)
      return (
        <TrendUnitConfigurationDetailPanel
          editUnit={ldsContext!.updateUnit}
          deleteUnit={handleSelectedUnitDeletion}
          selected={selection.unit}
          enterAddNewUnit={openAddNewUnitDialog}
        />
      );
    return <></>;
  }, [selection]);

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
            trendDefs={ldsContext!.trendDefs}
            trendGroups={ldsContext!.trendGroups}
            trendParamDefs={ldsContext!.trendParamDefs}
            units={ldsContext!.units}
            trends={ldsContext!.trends}
            addTrend={ldsContext!.addTrend}
            deleteTrend={handleSelectedTrendDeletion}
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
                trendDefs={ldsContext!.trendDefs}
                selected={selection.trendDef}
                setSelected={handleSelectedTrendDefChange}
              />
            </TabStripTab>
            <TabStripTab title={t("config-page:trends_params")}>
              <TrendParamDefConfiguration
                trendParamDefs={ldsContext!.trendParamDefs}
                selected={selection.trendParamDef}
                setSelected={handleSelectedTrendParamDefChange}
              />
            </TabStripTab>
            <TabStripTab title={t("config-page:trends_groups")}>
              <TrendGroupConfiguration
                showDialog={showAddNewTrendGroupDialog}
                openDialog={openAddNewTrendGroupDialog}
                closeDialog={closeAddNewTrendGroupDialog}
                trendGroups={ldsContext!.trendGroups}
                addTrendGroup={ldsContext!.addTrendGroup}
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
                units={ldsContext!.units}
                addUnit={ldsContext!.addUnit}
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
