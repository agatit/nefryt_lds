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
import CursorBubble from "../../../../components/CursorBubble";
import { useResizeObserver } from "../../../../hooks/useResizeObserver";
import { Loader } from "@progress/kendo-react-indicators";
import { SvgIcon } from "@progress/kendo-react-common";
import { xCircleIcon } from "@progress/kendo-svg-icons";
import { useTranslation } from "react-i18next";
import { AxisType, ChartSeriesTrendData } from "./utils";

const chartScaleThrottleMs = 50;

interface MinMaxType {
  max: number;
  min: number;
}

interface ChartComponentProps {
  isLoadingTrendsData: boolean;
  trendData: ChartSeriesTrendData[];
  navigationChart: boolean;
  navigatorData?: ChartSeriesTrendData[];
  axesState: AxisType[];
  trendMinMaxValue: MinMaxType;
  valueAxisState: MinMaxType[];
  handleOnPlotHover: (event: PlotAreaHoverEvent) => void;
  startDate: Date;
  endDate: Date;
  navigationStartDate?: Date;
  navigationEndDate?: Date;
  isEmpty: boolean;
  highlightedTrendID: number | null;
}

const ChartComponent = React.memo(function ChartComponent({
  isLoadingTrendsData,
  trendData,
  navigationChart,
  navigatorData,
  axesState,
  trendMinMaxValue,
  valueAxisState,
  handleOnPlotHover,
  startDate,
  endDate,
  navigationStartDate,
  navigationEndDate,
  isEmpty,
  highlightedTrendID,
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
    const opacity = highlightedTrendID !== null ? 0.25 : null;
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
          opacity={opacity ? (trend.id == highlightedTrendID ? 1 : opacity) : 1}
        />
      );
    });
  }, [trendData, axesState, highlightedTrendID]);

  const navigationChartSeriesItems = React.useMemo(() => {
    if (!navigationChart || navigatorData == undefined) return;
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
          highlight={{
            visible: false,
          }}
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
      {navigationChart && (
        <Chart
          key={"navigation-chart"}
          className="navigation-chart"
          renderAs="svg"
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
      )}
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

enum HandleType {
  LEFT,
  RIGHT,
}

interface NavigationSelectComponentProps {
  onSelectStart: (handle: HandleType) => void;
  onSelectEnd: () => void;
}

const NavigationSelectComponent = React.memo(
  function NavigationSelectComponent({
    onSelectStart,
    onSelectEnd,
  }: NavigationSelectComponentProps) {
    const leftHandleRef = React.useRef<HTMLDivElement>(null);
    const rightHandleRef = React.useRef<HTMLDivElement>(null);
    const [navigationChartRect, setNavigationChartRect] =
      React.useState<DOMRect>();
    const [selectStart, setSelectStart] = React.useState<number>(33.3);
    const [selectEnd, setSelectEnd] = React.useState<number>(66.6);
    const [isDragging, setIsDragging] = React.useState<boolean>(false);
    const grabbedHandle = React.useRef<HandleType>(HandleType.LEFT);
    const startingX = React.useRef<number>(0);
    const startingSelect = React.useRef<number>(0);

    React.useLayoutEffect(() => {
      // todo add some windows resizing observers
      setNavigationChartRect(
        document
          .getElementsByClassName("navigation-chart")[0]
          ?.getElementsByTagName("svg")[0]
          ?.children[1]?.children[2]?.getBoundingClientRect()
      );
    }, []);

    const selectWidth = React.useMemo(() => {
      if (navigationChartRect == undefined) return 0;

      return ((selectEnd - selectStart) * navigationChartRect.width) / 100;
    }, [navigationChartRect, selectStart, selectEnd]);

    const leftMaskWidth = React.useMemo(() => {
      if (navigationChartRect == undefined) return 0;

      return ((selectStart - 0) * navigationChartRect.width) / 100;
    }, [selectStart, navigationChartRect]);
    const rightMaskWidth = React.useMemo(() => {
      if (navigationChartRect == undefined) return 0;

      return ((100 - selectEnd) * navigationChartRect.width) / 100;
    }, [selectEnd, navigationChartRect]);

    const perPixelStep = React.useMemo(() => {
      if (navigationChartRect == undefined) return 0;

      return 100 / navigationChartRect.width;
    }, [navigationChartRect]);

    const handleMouseDown = React.useCallback(
      (event: React.MouseEvent, handle: HandleType) => {
        onSelectStart(handle);
        setIsDragging(true);
        grabbedHandle.current = handle;
        startingX.current = event.clientX;
        startingSelect.current =
          handle == HandleType.LEFT ? selectStart : selectEnd;
      },
      [onSelectStart]
    );

    const handleMouseMove = React.useCallback(
      (event: MouseEvent) => {
        if (!isDragging) return;

        const pixelShift = event.clientX - startingX.current;
        switch (grabbedHandle.current) {
          case HandleType.LEFT:
            setSelectStart(startingSelect.current + perPixelStep * pixelShift);
            break;
          case HandleType.RIGHT:
            setSelectEnd(startingSelect.current + perPixelStep * pixelShift);
            break;
        }
      },
      [selectStart, isDragging]
    );

    const handleMouseUp = React.useCallback(() => {
      if (!isDragging) return;

      onSelectEnd();
      setIsDragging(false);
      setSelectStart(33.3);
      setSelectEnd(66.6);
    }, [onSelectEnd, isDragging]);

    React.useEffect(() => {
      document.addEventListener("mouseup", handleMouseUp);
      document.addEventListener("mousemove", handleMouseMove);

      return () => {
        document.removeEventListener("mouseup", handleMouseUp);
        document.removeEventListener("mousemove", handleMouseMove);
      };
    }, [handleMouseUp, handleMouseMove]);

    if (navigationChartRect == undefined) return <></>;
    return (
      <div
        className={"navigation-selection-container"}
        style={{
          top: navigationChartRect.top,
          left: navigationChartRect.left,
          width: navigationChartRect.width,
          height: navigationChartRect.height,
        }}
      >
        <div className="mask" style={{ width: leftMaskWidth }} />
        <div className="selection" style={{ width: selectWidth }}>
          <div
            ref={rightHandleRef}
            className={"right-handle" + (isDragging ? " pass-events" : "")}
            onMouseDown={(event) => handleMouseDown(event, HandleType.RIGHT)}
          />
          <div
            ref={leftHandleRef}
            className={"left-handle" + (isDragging ? " pass-events" : "")}
            onMouseDown={(event) => handleMouseDown(event, HandleType.LEFT)}
          />
        </div>
        <div className="mask" style={{ width: rightMaskWidth }} />
      </div>
    );
  }
);

export interface TrendChartProps {
  isLoadingTrendsData: boolean;
  startDate: Date;
  endDate: Date;
  navigationChart: boolean;
  navigationStartDate?: Date;
  navigationEndDate?: Date;
  trendData: ChartSeriesTrendData[];
  navigatorData?: ChartSeriesTrendData[];
  axesState: AxisType[];
  onStartDateChange?: (value: Date) => void;
  onEndDateChange?: (value: Date) => void;
  onShowCursorBubbleChange: (value: boolean) => void;
  onCursorBubbleTextChange: (value: string) => void;
  highlightedTrendID: number | null;
}

const TrendChart = React.memo(function TrendChart({
  isLoadingTrendsData,
  startDate,
  endDate,
  navigationChart = false,
  navigationStartDate,
  navigationEndDate,
  trendData,
  navigatorData,
  axesState,
  onStartDateChange,
  onEndDateChange,
  onShowCursorBubbleChange,
  onCursorBubbleTextChange,
  highlightedTrendID,
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

  const [triggerRerender, setTriggerRerender] = React.useState<boolean>(false);
  React.useEffect(() => {
    handleSSBarsLeftPositioning();
  }, [axesState, triggerRerender]);

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
    if (ssBarStyles.length !== valueAxisState.length) {
      setTriggerRerender(!triggerRerender);
      return;
    }

    return ssBarStyles.map((style, i) => {
      return (
        <ScaleScrollBar
          key={i}
          style={{
            position: "absolute",
            top: ssBarVerticalStyle.current.top,
            left: style.left,
            height: ssBarVerticalStyle.current.height,
            display: isEmpty || chartRenderCounter.current < 1 ? "none" : "",
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

  const grabbedHandle = React.useRef<HandleType>(HandleType.LEFT);
  const selectStartDate = React.useRef<Date>(startDate);
  const selectEndDate = React.useRef<Date>(endDate);

  const handleSelectStart = React.useCallback(
    (handle: HandleType) => {
      if (!navigationChart) return;
      onShowCursorBubbleChange(true);
      grabbedHandle.current = handle;
      selectStartDate.current = startDate;
      selectEndDate.current = endDate;
    },
    [startDate, endDate]
  );

  const handleSelectEnd = React.useCallback(() => {
    if (!navigationChart) return;
    onShowCursorBubbleChange(false);
    onStartDateChange!(selectStartDate.current);
    onEndDateChange!(selectEndDate.current);
  }, []);

  const handleOnPlotHover = React.useCallback((e: PlotAreaHoverEvent) => {
    if (e.category) {
      if (grabbedHandle.current == HandleType.LEFT) {
        selectStartDate.current = e.category;
      } else {
        selectEndDate.current = e.category;
      }
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
    }
  }, []);

  return (
    <React.Fragment>
      <div className="chart-container" ref={chartContainerRef}>
        <ChartComponent
          isLoadingTrendsData={isLoadingTrendsData}
          trendData={isEmpty ? [] : trendData}
          navigationChart={navigationChart}
          navigatorData={navigatorData}
          axesState={axesState}
          trendMinMaxValue={trendMinMaxValue}
          valueAxisState={valueAxisState}
          handleOnPlotHover={handleOnPlotHover}
          startDate={startDate}
          endDate={endDate}
          navigationStartDate={navigationStartDate}
          navigationEndDate={navigationEndDate}
          isEmpty={isEmpty}
          highlightedTrendID={highlightedTrendID}
        />
      </div>
      {scaleScrollBars}
      {navigationChart && (
        <NavigationSelectComponent
          onSelectStart={handleSelectStart}
          onSelectEnd={handleSelectEnd}
        />
      )}
    </React.Fragment>
  );
});

export default TrendChart;
