import {
  Chart,
  ChartCategoryAxis,
  ChartCategoryAxisItem,
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
import { AxisType } from "./TrendsPage";

interface MinMaxType {
  max: number;
  min: number;
}

export interface ChartTrendData {
  timestamp: Date;
  value: number;
}

export interface ChartSeriesTrendData {
  data: ChartTrendData[];
  id: number;
  color: string;
}

export interface TrendChartProps {
  startDate: Date;
  endDate: Date;
  navigationStartDate: Date;
  navigationEndDate: Date;
  trendData: ChartSeriesTrendData[];
  navigatorData: ChartSeriesTrendData[];
  axesState: AxisType[];
  onSelectStart: (event: SelectStartEvent) => void;
  onSelectEnd: (event: SelectEndEvent) => void;
  onPlotAreaHover: (event: PlotAreaHoverEvent) => void;
}

const TrendChart = React.memo(function TrendChart({
  startDate,
  endDate,
  navigationStartDate,
  navigationEndDate,
  trendData,
  navigatorData,
  axesState,
  onSelectStart,
  onSelectEnd,
  onPlotAreaHover,
}: TrendChartProps) {
  // const chartRef = React.useRef<Chart>(null);
  // const chartKeyRef = React.useRef<number>(0);
  // chartRef.current?.chartInstance.destroy(); //tmp help with cleaning after chart
  // chartKeyRef.current += 1;

  const trendMinMaxValue: MinMaxType = React.useMemo(() => {
    if (trendData.length == 0) return { max: 0, min: 0 };

    let min = trendData[0].data[0].value;
    let max = trendData[0].data[0].value;

    for (let trend of trendData) {
      for (let data of trend.data) {
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

  const axisCrossingValue = React.useMemo(() => {
    const beforeStart = new Date(startDate);
    beforeStart.setDate(beforeStart.getDate() - 1);
    const afterEnd = new Date(endDate);
    afterEnd.setDate(afterEnd.getDate() + 1);

    const arr = [beforeStart];
    for (let i = 1; i < axesState.length; i++) arr.push(afterEnd);

    return arr;
  }, [axesState, startDate, endDate]);

  const updateValueAxisState = React.useCallback(
    (newMinMax: MinMaxType, index: number) => {
      const arr = [...valueAxisState];
      arr.splice(index, 1, newMinMax);
      setValueAxisState(arr);
    },
    [valueAxisState]
  );

  const throttledValueAxisChange = React.useMemo(
    () => throttle(updateValueAxisState, 166),
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

  const mainChartAxesItems = React.useMemo(() => {
    return axesState.map((axis, i) => {
      return (
        <ChartValueAxisItem
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
  }, [trendData]);

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
  React.useLayoutEffect(() => {
    const chartRect = document
      .getElementsByClassName("main-chart")[0]
      ?.getElementsByTagName("svg")[0]
      ?.children[1]?.children[2]?.getBoundingClientRect();

    const axesElements = document
      .getElementsByClassName("main-chart")[0]
      ?.getElementsByTagName("svg")[0]?.children[1]?.children[2]?.children;

    const ssBarStyles = [];
    let counter = 0;
    for (let i = 0; i < axesElements.length; i++) {
      const axis = axesState.find(
        (axis) => axis.Name == axesElements[i].lastElementChild?.innerHTML
      );

      if (axis == undefined) continue;

      counter++;

      const axisRect = axesElements[i].getBoundingClientRect();
      ssBarStyles.push({
        left: axisRect.left + (counter == 1 ? 15 : -20),
      });
    }

    if (chartRect && ssBarStyles.length > 0) setSSBarStyles(ssBarStyles);
  }, [mainChartAxesItems]);

  const scaleScrollBars = React.useMemo(() => {
    return ssBarStyles.map((style, i) => {
      return (
        <ScaleScrollBar
          style={{
            position: "absolute",
            top: ssBarVerticalStyle.current.top,
            left: style.left,
            height: ssBarVerticalStyle.current.height,
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

  return (
    <React.Fragment>
      <div className="chart-container">
        <Chart
          //   key={chartKeyRef.current}
          // ref={chartRef}
          className="main-chart"
          renderAs="svg"
          onSelectStart={onSelectStart}
          onSelectEnd={onSelectEnd}
          onPlotAreaHover={onPlotAreaHover}
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
              axisCrossingValue={axisCrossingValue}
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
            {/* <ChartValueAxisItem
              labels={{ content: (e) => e.value + " MPa" }}
              max={valueAxisState.max}
              min={valueAxisState.min}
              title={{ text: "Ciśnienie MPa", margin: { left: 10, right: 10 } }}
              axisCrossingValue={trendMinMaxValue.min}
            /> */}
            {mainChartAxesItems}
            <ChartValueAxisItem name="valueNavigatorAxis" pane="navigator" />
          </ChartValueAxis>
          <ChartSeries>
            {mainChartSeriesItems}
            {navigationChartSeriesItems}
          </ChartSeries>
        </Chart>
      </div>
      {scaleScrollBars}
      {/* <ScaleScrollBar
        style={{
          position: "absolute",
          top: ssBarStyle.top,
          left: ssBarStyle.left,
          height: ssBarStyle.height,
        }}
        max={trendMinMaxValue.max}
        min={trendMinMaxValue.min} //
        vertical={true}
        value={{
          start: valueAxisState.min,
          end: valueAxisState.max,
        }}
        onChange={handleScaleScrollBarChange}
      /> */}
    </React.Fragment>
  );
});

export default TrendChart;
