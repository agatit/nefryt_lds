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
  TrendValue,
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

const period = 1000; //in seconds so around 17 minutes
const mainChartSampleSize = 1000;

export default function TrendsCurrentPage() {
  const auth = React.useContext(AuthContext);
  const handleApiResponse = useHandleApiResponse();
  const { t } = useTranslation(["common", "trends-page"]);
  const appContext = React.useContext(AppContext);

  // UI STUFF
  const [endDate, setEndDate] = React.useState<Date>(new Date());
  const startDate = React.useMemo(() => {
    let date = new Date(endDate);
    date.setSeconds(date.getSeconds() - period);
    return date;
  }, [endDate]);

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
    try {
      const response = await handleApiResponse(
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

  const [isLoadingTrendsData, setIsLoadingTrendsData] =
    React.useState<boolean>(false);

  const trendIdArr = React.useMemo(() => {
    let trendIdArr: number[] = [];
    axesState.forEach((axis) => {
      trendIdArr.push(...axis.TrendIDs);
    });
    return trendIdArr;
  }, [axesState]);
  const trendIdList = React.useMemo(() => {
    let trendIdList: string = "";
    trendIdArr.forEach((id) => {
      trendIdList += id.toString() + ",";
    });
    return trendIdList;
  }, [trendIdArr]);

  const loadTrendsData = React.useCallback(async () => {
    if (trendIdList.length == 0) {
      // if no axes just leave
      setIsLoadingTrendsData(false);
      return;
    }

    try {
      const response = await handleApiResponse(
        trendDataApi.current.getTrendCurrentDataTrendTrendIdListCurrentDataPeriodSamplesGet.bind(
          trendDataApi.current
        ),
        trendIdList,
        period,
        mainChartSampleSize,
        1,
        mainChartSampleSize
      );
      console.log(response);

      if (response.status == 404) {
        setIsLoadingTrendsData(false);
        return;
      }

      const newTrendsData: ChartSeriesTrendData[] = trendIdArr.map((id) => {
        return {
          data: [],
          id: id,
          color: ldsContex!.trends.find((trend) => trend.ID == id)?.Color!,
        };
      });

      response?.data.items[0].Data.forEach((item: TrendDataMultiple) => {
        const timestamp = new Date(item.Timestamp * 1000);
        item.Data?.forEach((dataitem) => {
          const index = newTrendsData.findIndex((td) => td.id == dataitem.ID);
          newTrendsData[index].data.push({
            timestamp: timestamp,
            value: dataitem.Value ? dataitem.Value : null,
          });
        });
      });

      if (response?.data.items[0].LastTimestamp) {
        setEndDate(new Date(response.data.items[0].LastTimestamp * 1000));
      }

      setTrendsData(newTrendsData);
      setIsLoadingTrendsData(false);
    } catch (error) {
      console.log(error);
    }
  }, [ldsContex, trendIdArr, trendIdList]);

  async function loadLastSecondData() {
    if (trendIdList.length == 0) return;

    try {
      const response = await handleApiResponse(
        trendDataApi.current.getTrendCurrentDataTrendTrendIdListCurrentDataPeriodSamplesGet.bind(
          trendDataApi.current
        ),
        trendIdList,
        1,
        1,
        1,
        1
      );
      console.log(response);

      if (response.status == 404) {
        setIsLoadingTrendsData(false);
        return;
      }
      if (response?.data.items[0].Data) {
        const newTrendsData: ChartSeriesTrendData[] = [...trendsData];
        const timestamp = new Date(
          response?.data.items[0].Data[0].Timestamp * 1000
        );
        response?.data.items[0].Data[0].Data?.forEach(
          (dataitem: TrendValue) => {
            const index = newTrendsData.findIndex((td) => td.id == dataitem.ID);
            newTrendsData[index].data.shift();
            newTrendsData[index].data.push({
              timestamp: timestamp,
              value: dataitem.Value ? dataitem.Value : null,
            });
          }
        );

        setTrendsData(newTrendsData);
        setEndDate(new Date(response.data.items[0].LastTimestamp * 1000));
      }
    } catch (error) {
      console.log(error);
    }
  }

  // mockup data testing

  const generateTestData = React.useCallback(async () => {
    if (startDate == null || endDate == null) return;

    const timeDiff = endDate.getTime() - startDate.getTime();
    const step = Math.floor(timeDiff / mainChartSampleSize);
    const newTrendsData: ChartSeriesTrendData[] = [];

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

      newTrendsData.push({
        data: generatedData,
        id: trend.ID!,
        color: trend.Color! as string,
      });
    }

    setTrendsData(newTrendsData);
    setIsLoadingTrendsData(false);
  }, [startDate, endDate, ldsContex?.trends, axesState]);

  React.useEffect(() => {
    setTemplates(useMockup ? mockupTemplates : []);
    setAxesState(useMockup ? mockupAxes : []);
  }, [useMockup]);

  React.useEffect(() => {
    setIsLoadingTrendsData(true);
    useMockup ? generateTestData() : loadTrendsData();
  }, [useMockup, axesState]);

  React.useEffect(() => {
    const interval = setInterval(loadLastSecondData, 1000);
    return () => clearInterval(interval);
  }, [isLoadingTrendsData]);

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
            navigationChart={false}
            trendData={trendsData}
            axesState={axesState}
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
          dateManipulation={false}
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
