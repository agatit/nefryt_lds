import React from "react";
import { AuthContext } from "../../../../contexts/authContext";
import {
  Trend,
  TrendApi,
  TrendDef,
  TrendDefApi,
  Template,
  Unit,
  TemplateApi,
  TrendDataMultiple,
  TrendDataApi,
  TemplateCreate,
} from "../../../../services/api";

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
import { useHandleApiResponse } from "../../../../hooks/useHandleApiResponse";
import { AppContext } from "../../../../contexts/appContext";
import {
  AxisType,
  ChartSeriesTrendData,
  ChartTrendData,
  generateValue,
} from "./utils";

const mainChartSampleSize = 750;
const navigationChartSampleSize = 200;

type TrendLoadStatus = {
  mainDataLoaded: boolean;
  navDataLoaded: boolean;
};

export default function TrendsPage() {
  const auth = React.useContext(AuthContext);
  const handleApiResponse = useHandleApiResponse();
  const { t } = useTranslation(["common", "trends-page"]);
  const appContext = React.useContext(AppContext);

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

  const [isLoadingTemplates, setIsLoadingTemplates] =
    React.useState<boolean>(false);

  const handleTemplateStateChange = React.useCallback((value: Template[]) => {
    if (value) setTemplates(value);
  }, []);

  const handleSelectedTemplateChange = React.useCallback(
    (template: Template) => {
      if (template.Axes == null || template.Axes.length == 0) {
        appContext.showNotification({
          notificationType: { icon: true, style: "warning" },
          message: t("trends-page:selected_template_is_empty"),
        });
        setTimeout(appContext.closeNotification.bind(appContext), 5000);
        return;
      }

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
    setIsLoadingTemplates(true);
    try {
      const response = await handleApiResponse(
        templateApi.listTemplatesTemplateGet.bind(templateApi)
      );
      console.log(response);
      if (response?.data) setTemplates(response.data.items);
    } catch (error) {
      console.log(error);
    }
    setIsLoadingTemplates(false);
  }, []);

  React.useEffect(() => {
    if (!useMockup) loadTemplates();
  }, [useMockup]);

  const handleAxesStateChange = React.useCallback((value: AxisType[]) => {
    if (value) setAxesState(value);
  }, []);

  const handleCreateNewTemplate = React.useCallback(
    async (name: string) => {
      let newTemplate: TemplateCreate = {
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
        const response = await handleApiResponse(
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
  const trendDataApi = React.useRef<TrendDataApi>(
    new TrendDataApi(auth?.config, host, axiosInstance)
  );
  const [trendsData, setTrendsData] = React.useState<ChartSeriesTrendData[]>(
    []
  );
  const [navigatorData, setNavigatorData] = React.useState<
    ChartSeriesTrendData[]
  >([]);
  const isLoadingTrendsDataRef = React.useRef<TrendLoadStatus>({
    mainDataLoaded: false,
    navDataLoaded: false,
  });
  const isLoadingTrendsData = React.useMemo(() => {
    return (
      !isLoadingTrendsDataRef.current.mainDataLoaded &&
      !isLoadingTrendsDataRef.current.navDataLoaded
    );
  }, [isLoadingTrendsDataRef.current]);

  const loadNavTrendsdata = React.useCallback(
    async (trendIdList: string, trendIdArr: number[]) => {
      try {
        const response = await handleApiResponse(
          trendDataApi.current.getTrendDataTrendTrendIdListDataBeginEndSamplesGet.bind(
            trendDataApi.current
          ),
          trendIdList,
          Math.floor(navigationStartDate.getTime() / 1000),
          Math.floor(navigationEndDate.getTime() / 1000),
          navigationChartSampleSize,
          1,
          navigationChartSampleSize
        );
        console.log(response);

        const newNavTrendsData: ChartSeriesTrendData[] = trendIdArr.map(
          (id) => {
            return {
              data: [],
              id: id,
              color: ldsContex!.trends.find((trend) => trend.ID == id)?.Color!,
            };
          }
        );

        response?.data.items.forEach((item: TrendDataMultiple) => {
          const timestamp = new Date(item.Timestamp * 1000);
          item.Data?.forEach((dataitem) => {
            const index = newNavTrendsData.findIndex(
              (td) => td.id == dataitem.ID
            );
            newNavTrendsData[index].data.push({
              timestamp: timestamp,
              value: dataitem.Value ? dataitem.Value : null,
            });
          });
        });

        setNavigatorData(newNavTrendsData);
        isLoadingTrendsDataRef.current = {
          mainDataLoaded: isLoadingTrendsDataRef.current.mainDataLoaded,
          navDataLoaded: true,
        };
      } catch (error) {
        console.log(error);
      }
    },
    [trendDataApi.current, ldsContex, navigationStartDate, navigationEndDate]
  );

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
      isLoadingTrendsDataRef.current = {
        mainDataLoaded: true,
        navDataLoaded: true,
      };
      return;
    }

    loadNavTrendsdata(trendIdList, trendIdArr);

    try {
      const response = await handleApiResponse(
        trendDataApi.current.getTrendDataTrendTrendIdListDataBeginEndSamplesGet.bind(
          trendDataApi.current
        ),
        trendIdList,
        Math.floor(startDate.getTime() / 1000),
        Math.floor(endDate.getTime() / 1000),
        mainChartSampleSize,
        1,
        mainChartSampleSize
      );
      console.log(response);

      if (response.status == 404) {
        isLoadingTrendsDataRef.current = {
          mainDataLoaded: true,
          navDataLoaded: true,
        };

        return;
      }

      const newTrendsData: ChartSeriesTrendData[] = trendIdArr.map((id) => {
        return {
          data: [],
          id: id,
          color: ldsContex!.trends.find((trend) => trend.ID == id)?.Color!,
        };
      });

      response?.data.items.forEach((item: TrendDataMultiple) => {
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
      isLoadingTrendsDataRef.current = {
        mainDataLoaded: true,
        navDataLoaded: isLoadingTrendsDataRef.current.navDataLoaded,
      };
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
    isLoadingTrendsDataRef.current = {
      mainDataLoaded: true,
      navDataLoaded: true,
    };
  }, [startDate, endDate, ldsContex?.trends, axesState]);

  React.useEffect(() => {
    setTemplates(useMockup ? mockupTemplates : []);
    setAxesState(useMockup ? mockupAxes : []);
  }, [useMockup]);

  React.useEffect(() => {
    isLoadingTrendsDataRef.current = {
      mainDataLoaded: false,
      navDataLoaded: false,
    };
    useMockup ? generateTestData() : loadTrendsData();
  }, [useMockup, startDate, endDate, axesState, generateTestData]);

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
            navigationChart={true}
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
          dateManipulation={true}
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
