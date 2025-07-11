import {
  Chart,
  ChartCategoryAxis,
  ChartCategoryAxisItem,
  ChartNoDataOverlay,
  ChartPane,
  ChartPanes,
  ChartSeries,
  ChartSeriesItem,
  ChartValueAxis,
  ChartValueAxisItem,
  PlotAreaHoverEvent,
  SelectEndEvent,
  SelectStartEvent,
} from "@progress/kendo-react-charts";
import React from "react";
import ScaleScrollBar, {
  ScaleScrollBarChangeEvent,
} from "../../../../components/ScaleScrollBar";
import { throttle } from "../../../../lib/utilis";
import { AxisType, ChartSeriesTrendData } from "./TrendsPage";
import CursorBubble from "../../../../components/CursorBubble";
import { useResizeObserver } from "../../../../hooks/useResizeObserver";
import { Loader } from "@progress/kendo-react-indicators";
import { SvgIcon } from "@progress/kendo-react-common";
import { xCircleIcon } from "@progress/kendo-svg-icons";
import { useTranslation } from "react-i18next";

const chartScaleThrottleMs = 50;

interface MinMaxType {
  max: number;
  min: number;
}

interface ChartComponentProps {
  isLoadingTrendsData: boolean;
  trendData: ChartSeriesTrendData[];
  navigatorData: ChartSeriesTrendData[];
  axesState: AxisType[];
  trendMinMaxValue: MinMaxType;
  valueAxisState: MinMaxType[];
  handleSelectStart: (event: SelectStartEvent) => void;
  handleSelectEnd: (event: SelectEndEvent) => void;
  handleOnPlotHover: (event: PlotAreaHoverEvent) => void;
  startDate: Date;
  endDate: Date;
  navigationStartDate: Date;
  navigationEndDate: Date;
  isEmpty: boolean;
}

const ChartComponent = React.memo(function ChartComponent({
  isLoadingTrendsData,
  trendData,
  navigatorData,
  axesState,
  trendMinMaxValue,
  valueAxisState,
  handleSelectStart,
  handleSelectEnd,
  handleOnPlotHover,
  startDate,
  endDate,
  navigationStartDate,
  navigationEndDate,
  isEmpty,
}: ChartComponentProps) {
  const { t } = useTranslation(["common", "trends-page"]);

  const axisCrossingValue = React.useMemo(() => {
    const beforeStart = new Date(startDate);
    beforeStart.setDate(beforeStart.getDate() - 1);
    const afterEnd = new Date(endDate);
    afterEnd.setDate(afterEnd.getDate() + 1);

    const arr = [beforeStart];
    for (let i = 1; i < axesState.length; i++) arr.push(afterEnd);

    return arr;
  }, [axesState, startDate, endDate]);

  const mainChartAxesItems = React.useMemo(() => {
    return axesState.map((axis, i) => {
      return (
        <ChartValueAxisItem
          key={i}
          labels={{ content: (e) => e.value + " " + axis.Unit }}
          max={
            valueAxisState[i] ? valueAxisState[i].max : trendMinMaxValue.max //react does not offer syncing state with prop change rerender
          }
          min={
            valueAxisState[i] ? valueAxisState[i].min : trendMinMaxValue.min //react does not offer syncing state with prop change rerender
          }
          title={{ text: axis.Name, margin: { left: 10, right: 10 } }}
          axisCrossingValue={trendMinMaxValue.min}
          name={axis.Name}
        />
      );
    });
  }, [axesState, valueAxisState, trendMinMaxValue]);

  const mainChartSeriesItems = React.useMemo(() => {
    return trendData.map((trend) => {
      const axis = axesState.find((axis) => axis.TrendIDs.includes(trend.id));
      return (
        <ChartSeriesItem
          key={trend.id}
          type="line"
          field="value"
          categoryField="timestamp"
          data={trend.data}
          markers={{ visible: false }}
          color={trend.color}
          axis={axis?.Name}
        />
      );
    });
  }, [trendData, axesState]);

  const navigationChartSeriesItems = React.useMemo(() => {
    return navigatorData.map((trend) => {
      return (
        <ChartSeriesItem
          key={trend.id + 1000}
          type="line"
          style="smooth"
          markers={{ visible: false }}
          field="value"
          categoryField="timestamp"
          data={trend.data}
          axis="valueNavigatorAxis"
          categoryAxis="navigatorAxis"
          color={trend.color}
        />
      );
    });
  }, [navigatorData]);

  const select = React.useMemo(() => {
    return {
      from: startDate,
      to: endDate,
    };
  }, [startDate, endDate]);

  return (
    <React.Fragment>
      <Chart
        key={"main-chart"}
        //   key={chartKeyRef.current}
        // ref={chartRef}
        className="main-chart"
        renderAs="svg"
        transitions={false}
      >
        <ChartCategoryAxis>
          <ChartCategoryAxisItem
            baseUnit={"auto"}
            maxDivisions={25}
            rangeLabels={{ format: "dd/MM/yy HH:mm:ss", visible: true }}
            min={startDate}
            max={endDate}
            axisCrossingValue={axisCrossingValue}
          />
        </ChartCategoryAxis>
        <ChartValueAxis>{mainChartAxesItems}</ChartValueAxis>
        <ChartSeries>{mainChartSeriesItems}</ChartSeries>
        {isEmpty && (
          <ChartNoDataOverlay>
            <div>
              <SvgIcon
                icon={xCircleIcon}
                themeColor="error"
                size="xxlarge"
              ></SvgIcon>
              <p style={{ paddingTop: "8px" }}>
                {t("trends-page:no_data_in_range")}
              </p>
            </div>
          </ChartNoDataOverlay>
        )}
      </Chart>
      <Chart
        key={"navigation-chart"}
        className="navigation-chart"
        renderAs="svg"
        onSelectStart={handleSelectStart}
        onSelectEnd={handleSelectEnd}
        onPlotAreaHover={handleOnPlotHover}
        transitions={false}
        style={{ height: "15vh" }}
      >
        <ChartCategoryAxis>
          <ChartCategoryAxisItem
            baseUnit={"auto"}
            maxDivisions={20}
            labels={{ visible: false }}
            name="navigatorAxis"
            // select={select}
            min={navigationStartDate}
            max={navigationEndDate}
          />
        </ChartCategoryAxis>
        <ChartValueAxis>
          <ChartValueAxisItem
            name="valueNavigatorAxis"
            labels={{ visible: false }}
          />
        </ChartValueAxis>
        <ChartSeries>{navigationChartSeriesItems}</ChartSeries>
      </Chart>
      {isLoadingTrendsData && (
        <Loader
          className="chart-loader"
          size="medium"
          type={"infinite-spinner"}
        />
      )}
    </React.Fragment>
  );
});

export interface TrendChartProps {
  isLoadingTrendsData: boolean;
  startDate: Date;
  endDate: Date;
  navigationStartDate: Date;
  navigationEndDate: Date;
  trendData: ChartSeriesTrendData[];
  navigatorData: ChartSeriesTrendData[];
  axesState: AxisType[];
  onStartDateChange: (value: Date) => void;
  onEndDateChange: (value: Date) => void;
  onShowCursorBubbleChange: (value: boolean) => void;
  onCursorBubbleTextChange: (value: string) => void;
}

const TrendChart = React.memo(function TrendChart({
  isLoadingTrendsData,
  startDate,
  endDate,
  navigationStartDate,
  navigationEndDate,
  trendData,
  navigatorData,
  axesState,
  onStartDateChange,
  onEndDateChange,
  onShowCursorBubbleChange,
  onCursorBubbleTextChange,
}: TrendChartProps) {
  const isEmpty: boolean = React.useMemo(() => {
    for (let trend of trendData) {
      if (trend.data.length > 0) {
        return false;
      }
    }
    return true;
  }, [trendData]);

  const trendMinMaxValue: MinMaxType = React.useMemo(() => {
    if (trendData.length == 0) return { max: 0, min: 0 };

    let min;
    let max;

    for (let trend of trendData) {
      if (trend.data.length == 0) continue;
      if (min == undefined || max == undefined) {
        min = trend.data[0].value;
        max = trend.data[0].value;
      }
      for (let data of trend.data) {
        if (!data.value) continue;
        if (data.value > max!) max = data.value;
        if (data.value < min!) min = data.value;
      }
    }

    const step = Math.abs(max! - min!) / 5;
    min = Math.round(min! - step);
    max = Math.round(max! + step);

    return { min, max };
  }, [trendData]);
  const [valueAxisState, setValueAxisState] = React.useState<MinMaxType[]>(
    new Array(axesState.length).fill(trendMinMaxValue)
  );

  React.useEffect(() => {
    setValueAxisState(new Array(axesState.length).fill(trendMinMaxValue));
  }, [trendMinMaxValue, axesState]);

  const updateValueAxisState = React.useCallback(
    (newMinMax: MinMaxType, index: number) => {
      const arr = [...valueAxisState];
      arr.splice(index, 1, newMinMax);
      setValueAxisState(arr);
    },
    [valueAxisState]
  );

  const throttledValueAxisChange = React.useMemo(
    () => throttle(updateValueAxisState, chartScaleThrottleMs),
    [updateValueAxisState]
  );

  function handleScaleScrollBarChange(
    e: ScaleScrollBarChangeEvent,
    index: number
  ) {
    throttledValueAxisChange(
      {
        max: Math.round(e.value.end * 100) / 100,
        min: Math.round(e.value.start * 100) / 100,
      },
      index
    );
  }

  const ssBarVerticalStyle = React.useRef({ top: 0, height: 0 });
  React.useLayoutEffect(() => {
    const chartRect = document
      .getElementsByClassName("main-chart")[0]
      ?.getElementsByTagName("svg")[0]
      ?.children[1]?.children[2]?.getBoundingClientRect();

    ssBarVerticalStyle.current = {
      top: chartRect.top,
      height: chartRect.height - 16,
    };
  }, []);

  const [ssBarStyles, setSSBarStyles] = React.useState<any[]>([]);
  const handleSSBarsLeftPositioning = React.useCallback(() => {
    if (isLoadingTrendsData) return;
    const chartRect = document
      .getElementsByClassName("main-chart")[0]
      ?.getElementsByTagName("svg")[0]
      ?.children[1]?.children[2]?.getBoundingClientRect();

    const axesElements = document
      .getElementsByClassName("main-chart")[0]
      ?.getElementsByTagName("svg")[0]?.children[1]?.children[2]?.children;

    const ssBarStylesArr = [];
    let counter = 0;
    for (let i = 0; i < axesElements.length; i++) {
      const axis = axesState.find(
        (axis) => axis.Name == axesElements[i].lastElementChild?.innerHTML
      );

      if (axis == undefined) continue;
      counter++;

      const axisRect = axesElements[i].getBoundingClientRect();
      ssBarStylesArr.push({
        left: axisRect.left + (counter == 1 ? 15 : -20),
      });
    }
    if (chartRect && ssBarStylesArr.length > 0) setSSBarStyles(ssBarStylesArr);
  }, [ssBarStyles, isLoadingTrendsData]);

  React.useEffect(() => {
    handleSSBarsLeftPositioning();
  }, [axesState]);

  const chartRect = React.useRef({ width: 0, height: 0 });
  const chartRenderCounter = React.useRef(0);
  const chartContainerRef = useResizeObserver<HTMLDivElement>((size) => {
    chartRenderCounter.current++;
    if (chartRenderCounter.current < 3) {
      // on initial load with already set data we have proper position of axis at first rerender, fix later
      handleSSBarsLeftPositioning();
      return;
    }

    if (
      size.width == chartRect.current.width &&
      size.height == chartRect.current.height
    ) {
      chartRect.current = size;
      handleSSBarsLeftPositioning();
    }
  });

  const scaleScrollBars = React.useMemo(() => {
    return ssBarStyles.map((style, i) => {
      return (
        <ScaleScrollBar
          key={i}
          style={{
            position: "absolute",
            top: ssBarVerticalStyle.current.top,
            left: style.left,
            height: ssBarVerticalStyle.current.height,
            display: isEmpty || chartRenderCounter.current < 2 ? "none" : "",
          }}
          max={trendMinMaxValue.max}
          min={trendMinMaxValue.min}
          vertical={true}
          value={{
            start: valueAxisState[i].min,
            end: valueAxisState[i].max,
          }}
          onChange={(e) => handleScaleScrollBarChange(e, i)}
        />
      );
    });
  }, [ssBarStyles]);

  const handleSelectStart = React.useCallback((e: SelectStartEvent) => {
    onShowCursorBubbleChange(true);
  }, []);

  const handleSelectEnd = React.useCallback((e: SelectEndEvent) => {
    onShowCursorBubbleChange(false);
    onStartDateChange(e.from);
    onEndDateChange(e.to);
  }, []);

  const handleOnPlotHover = React.useCallback((e: PlotAreaHoverEvent) => {
    if (e.category)
      onCursorBubbleTextChange(
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
  }, []);

  return (
    <React.Fragment>
      <div className="chart-container" ref={chartContainerRef}>
        <ChartComponent
          isLoadingTrendsData={isLoadingTrendsData}
          trendData={isEmpty ? [] : trendData}
          navigatorData={navigatorData}
          axesState={axesState}
          trendMinMaxValue={trendMinMaxValue}
          valueAxisState={valueAxisState}
          handleSelectStart={handleSelectStart}
          handleSelectEnd={handleSelectEnd}
          handleOnPlotHover={handleOnPlotHover}
          startDate={startDate}
          endDate={endDate}
          navigationStartDate={navigationStartDate}
          navigationEndDate={navigationEndDate}
          isEmpty={isEmpty}
        />
      </div>
      {scaleScrollBars}
    </React.Fragment>
  );
});

export default TrendChart;
