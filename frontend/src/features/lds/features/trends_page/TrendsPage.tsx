import React from "react";
import { AuthContext } from "../../../../contexts/authContext";
import {
  Trend,
  TrendApi,
  TrendDefBase,
  TrendDefApi,
  Template,
  Unit,
  TemplateApi,
  TemplateBase,
} from "../../../../services/api";

import { useRefreshableRequest } from "../../../../hooks/useRefreshableRequest";
import { axiosInstance, host } from "../../../../lib/apiUtilities";
import "../../../../styles/layouts/detail-panel.scss";
import "../../../../styles/features/lds/features/trendPage.scss";

import { DateTimePickerChangeEvent } from "@progress/kendo-react-dateinputs";
import CursorBubble from "../../../../components/CursorBubble";
import TrendChart from "./TrendChart";
import TrendsDetailPanel from "./TrendsDetailPanel";
import ChartEditDialog from "./ChartEditDialog";
import {
  mockupAxes,
  mockupTemplates,
  mockupTrendDefs,
  mockupTrendGroupFromDB,
  mockupTrends,
  mockupTrendTreeData,
  mockupUnits,
} from "../../../../data/mockup-data";
import { LDSContext } from "../../contexts/ldsContext";
import { NavbarContext } from "../../../../contexts/navbarContext";
import { SvgIcon, Typography } from "@progress/kendo-react-common";
import { useTranslation } from "react-i18next";
import { arrowRightIcon } from "@progress/kendo-svg-icons";

const mainChartSampleSize = 500;
const navigationChartSampleSize = 50;

type TrendLoadStatus = {
  defsLoaded: boolean;
  trendsLoaded: boolean;
};

export type AxisType = {
  Name: string;
  Unit: string;
  TrendIDs: number[];
  ScaleMax: number;
  ScaleMin: number;
};

export interface ChartTrendData {
  timestamp: Date;
  value: number | null;
}

export interface ChartSeriesTrendData {
  data: ChartTrendData[];
  id: number;
  color: string;
}

export interface TreeViewDataItem {
  id?: number | string;
  text: string;
  expanded?: boolean;
  checked?: boolean;
  selected?: boolean;
  items?: TreeViewDataItem[];
}

function generateValue(date: Date, chart: number): number {
  switch (chart) {
    case 0:
      return (
        Math.sin((date.getTime() / Math.pow(10, 8)) * 2) +
        date.getMonth() +
        Math.sin(date.getHours() / 2) +
        Math.random() * (1.5 - 0.5) +
        0.5
      );
    case 1:
      return (
        Math.cos((date.getTime() / Math.pow(10, 8)) * 2) +
        date.getDate() / 2 +
        Math.cos(date.getHours() / 2) +
        Math.random() * (1.5 - 0.5) -
        5
      );
    case 2:
      return (
        Math.sin(date.getTime() / Math.pow(10, 7)) +
        date.getMonth() +
        Math.cos(date.getMinutes() / 25) +
        Math.random() * (1.5 - 0.5) +
        0.5
      );
  }
  return (
    Math.sin((date.getTime() / Math.pow(10, 8)) * 2) +
    date.getMonth() +
    Math.sin(date.getHours() / 2) +
    Math.random() * (2 - 1) +
    1
  );
}

export default function TrendsPage() {
  const auth = React.useContext(AuthContext);
  const refreshableRequest = useRefreshableRequest();
  const { t } = useTranslation(["common", "trends-page"]);

  // UI STUFF
  const [startDate, setStartDate] = React.useState<Date>(() => {
    var date = new Date();
    date.setDate(date.getDate() - 1);
    return date;
  });
  const [endDate, setEndDate] = React.useState<Date>(new Date());

  const handleChartStartDateChange = React.useCallback((value: Date) => {
    if (value) setStartDate(value);
  }, []);
  const handleChartEndDateChange = React.useCallback((value: Date) => {
    if (value) setEndDate(value);
  }, []);

  const navigationStartDate = React.useMemo(() => {
    return new Date(
      startDate.getTime() - (endDate.getTime() - startDate.getTime())
    );
  }, [startDate, endDate]);
  const navigationEndDate = React.useMemo(() => {
    return new Date(
      endDate.getTime() + (endDate.getTime() - startDate.getTime())
    );
  }, [startDate, endDate]);

  const handleStartDateChange = React.useCallback(
    (e: DateTimePickerChangeEvent) => {
      if (e.value) setStartDate(e.value);
    },
    []
  );
  const handleEndDateChange = React.useCallback(
    (e: DateTimePickerChangeEvent) => {
      if (e.value) setEndDate(e.value);
    },
    []
  );

  const [showCursorBubble, setShowCursorBubble] =
    React.useState<boolean>(false);
  const [cursorBubbleText, setCursorBubbleText] = React.useState("");

  const handleShowCursorBubbleChange = React.useCallback((value: boolean) => {
    if (value !== undefined) setShowCursorBubble(value);
  }, []);
  const handleCursorBubbleTextChange = React.useCallback((value: string) => {
    if (value !== undefined) setCursorBubbleText(value);
  }, []);

  const [showChartEdit, setShowChartEdit] = React.useState<boolean>(false);
  const openChartEdit = React.useCallback(() => {
    setShowChartEdit(true);
  }, []);
  const closeChartEdit = React.useCallback(() => {
    setShowChartEdit(false);
  }, []);

  const [highlightedTrendID, setHighlightedTrendID] = React.useState<
    number | null
  >(null);

  // DATA STUFF
  const ldsContex = React.useContext(LDSContext);
  React.useMemo(() => {
    if (ldsContex == null)
      throw new Error("LDS Context cannot be null to use TrendsPage");
  }, [ldsContex]);
  const { useMockup } = React.useContext(NavbarContext);

  // templates data and axes
  const templateApi = React.useMemo(
    () => new TemplateApi(auth?.config, host, axiosInstance),
    [auth]
  );
  const [templates, setTemplates] = React.useState<Template[]>(
    useMockup ? mockupTemplates : []
  );

  const isLoadingTemplates = React.useMemo(
    () => templates.length == 0,
    [templates]
  );

  const handleTemplateStateChange = React.useCallback((value: Template[]) => {
    if (value) setTemplates(value);
  }, []);

  const handleSelectedTemplateChange = React.useCallback(
    (template: Template) => {
      if (template.Axes == null || template.Axes.length == 0) return;

      const newAxesState: AxisType[] = [];
      for (let axis of template.Axes) {
        const unit = ldsContex!.units.find((u) => u.ID == axis.UnitID);
        newAxesState.push({
          Name: axis.Title,
          Unit: unit ? unit.Symbol! : "",
          TrendIDs: axis.TrendsID ? axis.TrendsID : [],
          ScaleMin: axis.ScaledMin,
          ScaleMax: axis.ScaledMax,
        });
      }
      setAxesState(newAxesState);
    },
    [ldsContex?.units]
  );

  const [axesState, setAxesState] = React.useState<AxisType[]>(
    useMockup ? mockupAxes : []
  );

  const noAxes: boolean = React.useMemo(() => {
    return axesState.length == 0;
  }, [axesState]);

  const loadTemplates = React.useCallback(async () => {
    try {
      const response = await refreshableRequest(
        templateApi.listTemplatesTemplateGet.bind(templateApi)
      );
      console.log(response);
      if (response?.data) setTemplates(response.data.items);
    } catch (error) {
      console.log(error);
    }
  }, []);

  React.useEffect(() => {
    if (!useMockup) loadTemplates();
  }, [useMockup]);

  const handleAxesStateChange = React.useCallback((value: AxisType[]) => {
    if (value) setAxesState(value);
  }, []);

  const handleCreateNewTemplate = React.useCallback(
    async (name: string) => {
      let newTemplate: TemplateBase = {
        Name: name,
        Axes: axesState.map((axis) => {
          const unit = ldsContex!.units.find((u) => u.Symbol == axis.Unit);
          return {
            TrendsID: axis.TrendIDs,
            Title: axis.Name,
            UnitID: unit!.ID,
            ScaledMin: axis.ScaleMin,
            ScaledMax: axis.ScaleMax,
          };
        }),
      };
      if (useMockup)
        setTemplates([...templates, { ...newTemplate, ID: templates.length }]);

      try {
        const response = await refreshableRequest(
          templateApi.createTemplateTemplatePost.bind(templateApi),
          newTemplate
        );
        console.log(response);
        if (response?.data) setTemplates([...templates, response.data]);
      } catch (error) {
        console.log(error);
      }
    },
    [templates, axesState, useMockup]
  );

  // trends data
  const [trendsData, setTrendsData] = React.useState<ChartSeriesTrendData[]>(
    []
  );
  const [navigatorData, setNavigatorData] = React.useState<
    ChartSeriesTrendData[]
  >([]);
  const [isLoadingTrendsDataState, setLoadingTrendsDataState] = React.useState({
    mainDataLoaded: false,
    navDataLoaded: false,
  });
  const isLoadingTrendsData = React.useMemo(() => {
    return (
      !isLoadingTrendsDataState.mainDataLoaded &&
      !isLoadingTrendsDataState.navDataLoaded
    );
  }, [isLoadingTrendsDataState]);

  const loadTrendsData = React.useCallback(async () => {
    var trendIdList: string = "";
    const trendIdArr: number[] = [];

    axesState.forEach((axis) => {
      trendIdArr.push(...axis.TrendIDs);
    });

    trendIdArr.forEach((id) => {
      trendIdList += id.toString() + ",";
    });

    if (trendIdList.length == 0) {
      // if no axes just leave
      setLoadingTrendsDataState({ mainDataLoaded: true, navDataLoaded: true });
      return;
    }

    try {
      const response = await refreshableRequest(
        ldsContex!.trendApi.getTrendDataTrendTrendIdListDataBeginEndSamplesGet.bind(
          ldsContex!.trendApi
        ),
        trendIdList,
        startDate.getTime(),
        endDate.getTime(),
        mainChartSampleSize,
        1,
        1000
      );
      console.log(response);
      const newTrendsData: ChartSeriesTrendData[] = trendIdArr.map((id) => {
        return {
          data: [],
          id: id,
          color: ldsContex!.trends.find((trend) => trend.ID == id)?.Color!,
        };
      });
      response?.data.items.forEach((item) => {
        const timestamp = new Date(item.Timestamp * 1000);
        item.Data?.forEach((dataitem) => {
          const index = newTrendsData.findIndex((td) => td.id == dataitem.ID);
          newTrendsData[index].data.push({
            timestamp: timestamp,
            value: dataitem.Value ? dataitem.Value : null,
          });
        });
      });

      setTrendsData(newTrendsData);
      setLoadingTrendsDataState({ mainDataLoaded: true, navDataLoaded: true });
    } catch (error) {
      console.log(error);
    }
  }, [ldsContex, axesState]);

  // mockup data testing

  const generateTestData = React.useCallback(async () => {
    if (startDate == null || endDate == null) return;

    const timeDiff = endDate.getTime() - startDate.getTime();
    const step = Math.floor(timeDiff / mainChartSampleSize);
    const newTrendsData: ChartSeriesTrendData[] = [];

    const navStartDate = new Date(startDate.getTime() - timeDiff);
    const navEndDate = new Date(endDate.getTime() + timeDiff);
    const newNavData: ChartSeriesTrendData[] = [];
    const step2 = Math.floor(
      (navEndDate.getTime() - navStartDate.getTime()) /
        navigationChartSampleSize
    );

    const activeTrendsIDs: number[] = [];
    for (let axis of axesState) {
      for (let id of axis.TrendIDs) {
        activeTrendsIDs.push(id);
      }
    }

    for (let trend of ldsContex!.trends) {
      if (!activeTrendsIDs!.includes(trend.ID!)) continue;

      const generatedData: ChartTrendData[] = [];
      for (let i = 0; i < mainChartSampleSize; i++) {
        const timestamp = new Date(startDate.getTime() + i * step);
        const value = generateValue(timestamp, trend.ID!);

        generatedData.push({
          timestamp: timestamp,
          value: value,
        });
      }

      const navData: ChartTrendData[] = [];
      for (let i = 0; i < navigationChartSampleSize; i++) {
        const timestamp = new Date(navStartDate.getTime() + i * step2);
        navData.push({
          timestamp: timestamp,
          value: generateValue(timestamp, trend.ID!),
        });
      }

      // for select to work bounding dates has to be in nav data set
      navData.push({
        timestamp: startDate,
        value: generateValue(startDate, trend.ID!),
      });
      navData.push({
        timestamp: endDate,
        value: generateValue(endDate, trend.ID!),
      });

      navData.sort((a, b) => a.timestamp.getTime() - b.timestamp.getTime());

      newTrendsData.push({
        data: generatedData,
        id: trend.ID!,
        color: trend.Color! as string,
      });
      newNavData.push({
        data: navData,
        id: trend.ID!,
        color: trend.Color! as string,
      });
    }

    setTrendsData(newTrendsData);
    setNavigatorData(newNavData);
    setLoadingTrendsDataState({ mainDataLoaded: true, navDataLoaded: true });
  }, [startDate, endDate, ldsContex?.trends, axesState]);

  React.useEffect(() => {
    setTemplates(useMockup ? mockupTemplates : []);
    setAxesState(useMockup ? mockupAxes : []);
  }, [useMockup]);

  React.useEffect(() => {
    setLoadingTrendsDataState({ mainDataLoaded: false, navDataLoaded: false });
    useMockup ? generateTestData() : loadTrendsData();
  }, [
    useMockup,
    startDate,
    endDate,
    axesState,
    generateTestData,
    loadTrendsData,
  ]);

  return (
    <React.Fragment>
      <main className="trends-page">
        {noAxes ? (
          <div className="no-axes-container">
            <Typography.p style={{ marginBottom: 0 }} fontSize="large">
              {t("trends-page:add_trends_or_select_template")}
            </Typography.p>
            <SvgIcon icon={arrowRightIcon} size="large" />
          </div>
        ) : (
          <TrendChart
            isLoadingTrendsData={isLoadingTrendsData}
            startDate={startDate}
            endDate={endDate}
            navigationStartDate={navigationStartDate}
            navigationEndDate={navigationEndDate}
            trendData={trendsData}
            navigatorData={navigatorData}
            axesState={axesState}
            onStartDateChange={handleChartStartDateChange}
            onEndDateChange={handleChartEndDateChange}
            onShowCursorBubbleChange={handleShowCursorBubbleChange}
            onCursorBubbleTextChange={handleCursorBubbleTextChange}
            highlightedTrendID={highlightedTrendID}
          />
        )}
        <TrendsDetailPanel
          isLoading={isLoadingTemplates}
          trends={ldsContex!.trends}
          axesState={axesState}
          onAxesStateChange={handleAxesStateChange}
          onChartEditButtonClick={openChartEdit}
          startDate={startDate}
          endDate={endDate}
          onStartDateChange={handleStartDateChange}
          onEndDateChange={handleEndDateChange}
          templates={templates}
          onSelectedTemplateChange={handleSelectedTemplateChange}
          handleCreateNewTemplate={handleCreateNewTemplate}
          onHighlightedTrendIDChange={setHighlightedTrendID}
        />
      </main>
      {showChartEdit && (
        <ChartEditDialog
          useMockup={useMockup}
          closeDialog={closeChartEdit}
          trendDefs={ldsContex!.trendDefs}
          trendGroups={mockupTrendGroupFromDB}
          units={ldsContex!.units}
          mockupTrendTreeData={mockupTrendTreeData}
          trendsState={ldsContex!.trends}
          axesState={axesState}
          onAxesStateChange={handleAxesStateChange}
          onShowCursorBubbleChange={handleShowCursorBubbleChange}
          onCursorBubbleTextChange={handleCursorBubbleTextChange}
        />
      )}
      {showCursorBubble && <CursorBubble text={cursorBubbleText} />}
    </React.Fragment>
  );
}
