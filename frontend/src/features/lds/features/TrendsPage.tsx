import React from "react";
import { AuthContext } from "../../../contexts/authContext";
import {
  Configuration,
  PageTrend,
  PageTrendDef,
  Trend,
  TrendApi,
  TrendApiFactory,
  TrendDef,
  TrendDefApi,
} from "../../../services/api";
import {
  Chart,
  ChartCategoryAxis,
  ChartCategoryAxisItem,
  ChartPane,
  ChartPanes,
  ChartSeries,
  ChartSeriesItem,
  ChartTooltip,
  ChartValueAxis,
  ChartValueAxisItem,
  PlotAreaHoverEvent,
  RenderEvent,
  SelectEndEvent,
  SelectStartEvent,
  TitleVisualArgs,
} from "@progress/kendo-react-charts";
import { useRefreshableRequest } from "../../../hooks/useRefreshableRequest";
import { axiosInstance, host } from "../../../lib/apiUtilities";
import { Loader } from "@progress/kendo-react-indicators";
import "../../../styles/features/lds/features/trendPage.scss";
import TrendCheckbox from "../components/TrendCheckbox";
import {
  Checkbox,
  CheckboxChangeEvent,
  RangeSlider,
  RangeSliderChangeEvent,
  Switch,
} from "@progress/kendo-react-inputs";
import {
  PanelBar,
  PanelBarItem,
  TabStrip,
  TabStripSelectEventArguments,
  TabStripTab,
} from "@progress/kendo-react-layout";
import { useTranslation } from "react-i18next";
import { SvgIcon, Typography } from "@progress/kendo-react-common";
import { DropDownList } from "@progress/kendo-react-dropdowns";
import { Label } from "@progress/kendo-react-labels";
import {
  DateTimePicker,
  DateTimePickerChangeEvent,
} from "@progress/kendo-react-dateinputs";
import CursorBubble from "../../../components/CursorBubble";
import { DetailPanel } from "onyks_shared_kendo";
import { chartLegendIcon } from "../components/chartLegendIcon";
import { pencilIcon, saveIcon } from "@progress/kendo-svg-icons";
import { Button } from "@progress/kendo-react-buttons";
import ScaleScrollBar, {
  ScaleScrollBarChangeEvent,
} from "../../../components/ScaleScrollBar";
import { throttle } from "../../../lib/utilis";

type ChartTrendData = {
  timestamp: Date;
  value: number;
};

type ChartSeriesTrendData = {
  data: ChartTrendData[];
  id: number;
};

type MockupTrendType = {
  ID: number;
  TrendGroupID: number;
  Color: string;
  TrendDefID: string;
  Name: string;
};

type TrendsState = {
  trends: Trend[] | MockupTrendType[];
  activeTrendsIDs: number[];
};

type TrendLoadStatus = {
  defsLoaded: boolean;
  trendsLoaded: boolean;
};

const mockupTrendDefs: TrendDef[] = [
  {
    ID: "P01",
    Name: "Pressure",
  },
];

const mockupTrends: MockupTrendType[] = [
  {
    ID: 0,
    TrendGroupID: 1,
    Color: "#ff6358",
    TrendDefID: "P01",
    Name: "Ciśnienie 1",
  },
  {
    ID: 1,
    TrendGroupID: 1,
    Color: "#ffe162",
    TrendDefID: "P01",
    Name: "Ciśnienie 2",
  },
  {
    ID: 2,
    TrendGroupID: 1,
    Color: "#4cd180",
    TrendDefID: "P01",
    Name: "Ciśnienie 3",
  },
];

export default function TrendsPage() {
  const { t } = useTranslation(["common", "trends-page"]);

  const auth = React.useContext(AuthContext);
  const refreshableRequest = useRefreshableRequest();

  // UI STUFF
  const [tabSelected, setTabSelected] = React.useState<number>(0);

  const [startDate, setStartDate] = React.useState<Date | null>(() => {
    var date = new Date();
    date.setDate(date.getDate() - 1);
    return date;
  });
  const [endDate, setEndDate] = React.useState<Date | null>(new Date());
  const [navigationStartDate, setNavigationStartDate] =
    React.useState<Date | null>(null);
  const [navigationEndDate, setNavigationEndDate] = React.useState<Date | null>(
    null
  );

  const [isChartInEdit, setIsChartInEdit] = React.useState<boolean>(false);

  const [isNavigating, setIsNavigating] = React.useState<boolean>(false);
  const [cursorBubbleText, setCursorBubbleText] = React.useState("");

  const [valueAxisState, setValueAxisState] = React.useState<{
    max: number | null;
    min: number | null;
  }>({ max: null, min: null });

  const [axisSliderStyle, setAxisSliderStyle] = React.useState<{
    top: number;
    left: number;
    height: number;
  }>({ top: 0, left: 0, height: 0 });

  const [axisSliderState, setAxisSliderState] = React.useState<{
    max: number;
    min: number;
  }>({ max: 0, min: 0 });

  function handleTabSelect(e: TabStripSelectEventArguments) {
    setTabSelected(e.selected);
  }

  function handleStartDateChange(e: DateTimePickerChangeEvent) {
    setStartDate(e.value);
  }
  function handleEndDateChange(e: DateTimePickerChangeEvent) {
    setEndDate(e.value);
  }

  function handleSelectStart(e: SelectStartEvent) {
    setIsNavigating(true);
  }

  function handleSelectEnd(e: SelectEndEvent) {
    setIsNavigating(false);
    setStartDate(e.from);
    setEndDate(e.to);
  }

  function handleChartEditButtonClick(e: React.MouseEvent) {
    setIsChartInEdit(!isChartInEdit);
  }

  function handleOnPlotHover(e: PlotAreaHoverEvent) {
    if (e.category)
      setCursorBubbleText(
        e.category.toLocaleDateString("pl-PL", {
          hourCycle: "h24",
          weekday: "short",
          month: "short",
          day: "2-digit",
          hour: "2-digit",
          minute: "2-digit",
          seconds: "2-digit",
          fractionalSecondDigits: "3",
        })
      );
  }

  const throttledValueAxisChange = React.useMemo(
    () => throttle(setValueAxisState, 166),
    []
  );

  function handleScaleScrollBarChange(e: ScaleScrollBarChangeEvent) {
    throttledValueAxisChange({
      max: Math.round(e.value.end * 100) / 100,
      min: Math.round(e.value.start * 100) / 100,
    });
  }

  // DATA STUFF

  const trendDefApi = React.useMemo(
    () => new TrendDefApi(auth?.config, host, axiosInstance),
    [auth]
  );
  const trendApi = React.useMemo(
    () => new TrendApi(auth?.config, host, axiosInstance),
    [auth]
  );

  // Trends and trend defs
  const [trendDefs, setTrendDefs] = React.useState<TrendDef[]>(mockupTrendDefs);
  const [trendsState, setTrendsState] = React.useState<TrendsState>({
    trends: mockupTrends,
    activeTrendsIDs: [0, 1, 2],
  });
  const [isLoadingTrends, setIsLoadingTrends] = React.useState<boolean>(false);
  const trendLoadStatusRef = React.useRef<TrendLoadStatus>({
    defsLoaded: false,
    trendsLoaded: false,
  });

  // Trends Data
  const [trendsData, setTrendsData] = React.useState<ChartSeriesTrendData[]>(
    []
  );
  const [isLoadingTrendsData, setIsLoadingTrendsData] =
    React.useState<boolean>(false);
  const [navigatorData, setNavigatorData] = React.useState<
    ChartSeriesTrendData[]
  >([]);

  function handleActiveTrendsCheckboxChange(
    e: CheckboxChangeEvent,
    id: number
  ) {
    if (e.value) {
      setTrendsState({
        trends: trendsState.trends,
        activeTrendsIDs: [...trendsState.activeTrendsIDs, id].sort(
          (a, b) => a - b
        ),
      });
    } else {
      setTrendsState({
        trends: trendsState.trends,
        activeTrendsIDs: trendsState.activeTrendsIDs.filter(
          (item) => item !== id
        ),
      });
    }
  }

  // Loading from api

  function checkIfTrendsLoaded() {
    if (
      trendLoadStatusRef.current.defsLoaded &&
      trendLoadStatusRef.current.trendsLoaded
    )
      setIsLoadingTrends(false);
  }

  async function loadTrends() {
    trendLoadStatusRef.current = { defsLoaded: false, trendsLoaded: false };

    refreshableRequest(
      trendDefApi.listTrendDefsTrendDefGet.bind(trendDefApi)
    ).then((response) => {
      trendLoadStatusRef.current.defsLoaded = true;
      if (response?.data) setTrendDefs(response?.data.items);
      checkIfTrendsLoaded();
    });

    refreshableRequest(trendApi.listTrendsTrendGet.bind(trendApi)).then(
      (response) => {
        trendLoadStatusRef.current.trendsLoaded = true;
        if (response?.data)
          setTrendsState({ trends: response.data.items, activeTrendsIDs: [] });
        checkIfTrendsLoaded();
      }
    );
  }

  // mockup data testing

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

  async function generateTestData() {
    if (startDate == null || endDate == null) return;

    const timeDiff = endDate.getTime() - startDate.getTime();
    const step = Math.floor(timeDiff / 500);
    const newTrendsData: ChartSeriesTrendData[] = [];

    const navStartDate = new Date(startDate.getTime() - timeDiff);
    const navEndDate = new Date(endDate.getTime() + timeDiff);
    const newNavData: ChartSeriesTrendData[] = [];
    const step2 = Math.floor(
      (navEndDate.getTime() - navStartDate.getTime()) / 150
    );

    let max;
    let min;

    for (let trend of trendsState!.trends) {
      if (!trendsState!.activeTrendsIDs.includes(trend.ID!)) continue;

      const generatedData: ChartTrendData[] = [];
      for (let i = 0; i < 500; i++) {
        const timestamp = new Date(startDate.getTime() + i * step);
        const value = generateValue(timestamp, trend.ID!);

        if (max == undefined && min == undefined) {
          max = value;
          min = value;
        }
        if (value > max!) max = value;
        if (value < min!) min = value;

        generatedData.push({
          timestamp: timestamp,
          value: value,
        });
      }

      const navData: ChartTrendData[] = [];
      for (let i = 0; i < 150; i++) {
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

      newTrendsData.push({ data: generatedData, id: trend.ID! });
      newNavData.push({ data: navData, id: trend.ID! });
    }

    const valueAxisStep = Math.abs(max! - min!) / 5;
    setValueAxisState({
      max: Math.round(max! + valueAxisStep),
      min: Math.round(min! - valueAxisStep),
    });

    setAxisSliderState({
      max: Math.round(max! + valueAxisStep),
      min: Math.round(min! - valueAxisStep),
    });

    setTrendsData(newTrendsData);
    setNavigatorData(newNavData);
    setNavigationStartDate(navStartDate);
    setNavigationEndDate(navEndDate);
  }

  React.useEffect(() => {
    generateTestData();
  }, [startDate, endDate, trendsState.activeTrendsIDs]);

  const chartRef = React.useRef<Chart>(null);
  const chartKeyRef = React.useRef<number>(0);
  const ChartComponent = React.useMemo(() => {
    chartRef.current?.chartInstance.destroy(); //tmp help with cleaning after chart
    chartKeyRef.current += 1;
    return (
      <div className="chart-container">
        <Chart
          key={chartKeyRef.current}
          ref={chartRef}
          className="main-chart"
          renderAs="svg"
          onSelectStart={handleSelectStart}
          onSelectEnd={handleSelectEnd}
          onPlotAreaHover={handleOnPlotHover}
          transitions={false}
          style={{ height: "100%" }}
        >
          <ChartCategoryAxis>
            <ChartCategoryAxisItem
              baseUnit={"auto"}
              maxDivisions={25}
              rangeLabels={{ format: "dd/MM/yy HH:mm:ss", visible: true }}
              min={startDate}
              max={endDate}
            />
            <ChartCategoryAxisItem
              baseUnit={"auto"}
              maxDivisions={20}
              rangeLabels={{ format: "dd/MM/yy HH:mm:ss", visible: true }}
              name="navigatorAxis"
              pane="navigator"
              select={{ from: startDate, to: endDate }}
              min={navigationStartDate}
              max={navigationEndDate}
            />
          </ChartCategoryAxis>
          <ChartPanes>
            <ChartPane />
            <ChartPane name={"navigator"} height={200} />
          </ChartPanes>
          <ChartValueAxis>
            <ChartValueAxisItem
              labels={{ content: (e) => e.value + " MPa" }}
              max={valueAxisState.max}
              min={valueAxisState.min}
              title={{ text: "Ciśnienie MPa", margin: { left: 10, right: 10 } }}
            />
            <ChartValueAxisItem name="valueNavigatorAxis" pane="navigator" />
          </ChartValueAxis>
          <ChartSeries>
            {trendsData.map((trend, i) => {
              return (
                <ChartSeriesItem
                  key={i}
                  type="line"
                  field="value"
                  categoryField="timestamp"
                  data={trend.data}
                  markers={{ visible: false }}
                  color={
                    trendsState?.trends.find((item) => item.ID == trend.id)
                      ?.Color
                  }
                />
              );
            })}
            {navigatorData.map((trend, i) => {
              return (
                <ChartSeriesItem
                  key={i + 1000}
                  type="line"
                  style="smooth"
                  markers={{ visible: false }}
                  field="value"
                  categoryField="timestamp"
                  data={trend.data}
                  axis="valueNavigatorAxis"
                  categoryAxis="navigatorAxis"
                  color={
                    trendsState?.trends.find((item) => item.ID == trend.id)
                      ?.Color
                  }
                />
              );
            })}
          </ChartSeries>
        </Chart>
      </div>
    );
  }, [trendsData, valueAxisState]);

  React.useLayoutEffect(() => {
    const axisTitleRect = document
      .getElementsByClassName("main-chart")[0]
      ?.getElementsByTagName("svg")[0]
      ?.children[1]?.children[2].lastElementChild?.getBoundingClientRect();

    const axisRect = document
      .getElementsByClassName("main-chart")[0]
      ?.getElementsByTagName("svg")[0]
      ?.children[1]?.children[2]?.getBoundingClientRect();

    if (axisTitleRect && axisRect)
      setAxisSliderStyle({
        top: axisRect.top,
        left: axisTitleRect.left + 15,
        height: axisRect.bottom - axisRect.top,
      });
  }, [axisSliderState]);

  return (
    <React.Fragment>
      <main>
        {ChartComponent}
        <DetailPanel className="chart-detail-panel" flexGrow={1}>
          <TabStrip
            className="detail-panel-tabs"
            keepTabsMounted={true}
            selected={tabSelected}
            onSelect={handleTabSelect}
          >
            <TabStripTab title={t("trends-page:chart_config")}>
              {!isLoadingTrends ? (
                <div className="chart-config-content">
                  {isChartInEdit ? (
                    <PanelBar className="detail-panel-panel-bar">
                      {trendDefs.map((trendDef, i) => {
                        return (
                          <PanelBarItem
                            title={trendDef.Name}
                            expanded={i == 0 ? true : false}
                            selected={i == 0 ? true : false}
                          >
                            {trendsState?.trends.map((trend) => {
                              if (trend.TrendDefID == trendDef.ID)
                                return (
                                  <div className="item">
                                    <Checkbox
                                      value={trendsState.activeTrendsIDs.includes(
                                        trend.ID!
                                      )}
                                      onChange={(e) =>
                                        handleActiveTrendsCheckboxChange(
                                          e,
                                          trend.ID!
                                        )
                                      }
                                    />
                                    <SvgIcon
                                      icon={chartLegendIcon}
                                      size="xlarge"
                                      style={{ stroke: trend?.Color }}
                                    />
                                    {trend?.Name}
                                  </div>
                                );
                            })}
                          </PanelBarItem>
                        );
                      })}
                    </PanelBar>
                  ) : (
                    <div className="item">
                      <Typography.p fontSize="large" margin={0}>
                        {t("trends-page:legend")}
                      </Typography.p>
                      <div className="legend-container">
                        {trendsState?.activeTrendsIDs.map((id) => {
                          const trend = trendsState.trends.find(
                            (trend) => trend.ID == id
                          );
                          return (
                            <div>
                              <SvgIcon
                                icon={chartLegendIcon}
                                size="xlarge"
                                style={{ stroke: trend?.Color }}
                              />
                              {trend?.Name}
                            </div>
                          );
                        })}
                      </div>
                    </div>
                  )}
                  <div className="item">
                    <Button
                      svgIcon={isChartInEdit ? undefined : pencilIcon}
                      onClick={handleChartEditButtonClick}
                    >
                      {isChartInEdit ? t("common:save") : t("common:edit")}
                    </Button>
                  </div>
                  <div className="item">
                    <Typography.p fontSize="large" margin={0}>
                      {t("trends-page:time_interval")}
                    </Typography.p>
                    <div className="item-row">
                      <div>
                        <Label>{t("common:from")}</Label>
                        <DateTimePicker
                          format={"dd/MM/yy HH:mm:ss"}
                          value={startDate}
                          onChange={handleStartDateChange}
                        />
                      </div>
                      <div>
                        <Label>{t("common:to")}</Label>
                        <DateTimePicker
                          format={"dd/MM/yy HH:mm:ss"}
                          value={endDate}
                          onChange={handleEndDateChange}
                        />
                      </div>
                    </div>
                  </div>
                  <div className="item">
                    <Button svgIcon={saveIcon}>
                      {t("trends-page:save_as_template")}
                    </Button>
                  </div>
                </div>
              ) : (
                <Loader size="medium" type={"infinite-spinner"} />
              )}
            </TabStripTab>
            <TabStripTab title={t("trends-page:templates")}></TabStripTab>
          </TabStrip>
        </DetailPanel>
        <ScaleScrollBar
          style={{
            position: "absolute",
            top: axisSliderStyle.top,
            left: axisSliderStyle.left,
            height: axisSliderStyle.height,
          }}
          max={axisSliderState.max}
          min={axisSliderState.min}
          vertical={true}
          value={{
            start: valueAxisState.min ? valueAxisState.min : 0,
            end: valueAxisState.max ? valueAxisState.max : 0,
          }}
          onChange={handleScaleScrollBarChange}
        />
      </main>
      {isNavigating && <CursorBubble text={cursorBubbleText} />}
    </React.Fragment>
  );
}
