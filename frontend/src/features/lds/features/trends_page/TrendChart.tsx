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

interface MinMaxType {
  max: number;
  min: number;
}

interface ScaleScrollBarStyleType {
  top: number;
  left: number;
  height: number;
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
  const [valueAxisState, setValueAxisState] =
    React.useState<MinMaxType>(trendMinMaxValue);
  const [ssBarStyle, setSSBarStyle] = React.useState<ScaleScrollBarStyleType>({
    top: 0,
    left: 0,
    height: 0,
  });

  React.useLayoutEffect(() => {
    setValueAxisState(trendMinMaxValue);
  }, [trendData]);

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
      setSSBarStyle({
        top: axisRect.top,
        left: axisTitleRect.left + 15,
        height: axisRect.bottom - axisRect.top,
      });
  }, []);

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

  const mainChartSeriesItems = React.useMemo(() => {
    return trendData.map((trend) => {
      return (
        <ChartSeriesItem
          key={trend.id}
          type="line"
          field="value"
          categoryField="timestamp"
          data={trend.data}
          markers={{ visible: false }}
          color={trend.color}
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
            {mainChartSeriesItems}
            {navigationChartSeriesItems}
          </ChartSeries>
        </Chart>
      </div>
      <ScaleScrollBar
        style={{
          position: "absolute",
          top: ssBarStyle.top,
          left: ssBarStyle.left,
          height: ssBarStyle.height,
        }}
        max={trendMinMaxValue.max}
        min={trendMinMaxValue.min}
        vertical={true}
        value={{
          start: valueAxisState.min,
          end: valueAxisState.max,
        }}
        onChange={handleScaleScrollBarChange}
      />
    </React.Fragment>
  );
});

export default TrendChart;
