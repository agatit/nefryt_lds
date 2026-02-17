import React from "react";
import {
  Chart,
  ChartCategoryAxis,
  ChartCategoryAxisItem,
  ChartSeries,
  ChartSeriesItem,
  ChartValueAxis,
  ChartValueAxisItem,
} from "@progress/kendo-react-charts";
import { Simulation, SimulationParam } from "../../../../../services/api";
import { SimulationData } from "..";

const chartScaleThrottleMs = 10;

export interface SimulatorChartProps {
  //   simulation: Simulation;
  //   simulationParams: SimulationParam[];
  simulationData: SimulationData[];
}

const SimulatorChart: React.FC<SimulatorChartProps> = ({
  //   simulation,
  //   simulationParams,
  simulationData,
}: SimulatorChartProps) => {
  const maxSimulationValueRef = React.useRef(0);
  const maxSimulationValue: number = React.useMemo(() => {
    let max = 0;
    simulationData.forEach((data) => {
      if (data.Data > max) max = data.Data;
    });
    max += Math.floor(max / 10);
    if (max > maxSimulationValueRef.current)
      maxSimulationValueRef.current = max;
    return maxSimulationValueRef.current;
  }, [simulationData]);

  //   const pipelineLength = React.useMemo(() => {
  //     let lengthParam = simulationParams.find(
  //       (param) => param.SimulationParamDefID == "LENGTH"
  //     );
  //     return Number(lengthParam?.Value) ?? 0;
  //   }, [simulationParams]);

  //   const distanceArr = React.useMemo(() => {
  //     let distanceArr = [];
  //     for (let i = 0; i <= pipelineLength; i += simulation.ResolutionMeters) {
  //       distanceArr.push(i);
  //     }
  //     return distanceArr;
  //   }, [simulation, pipelineLength]);

  return (
    <Chart
      key={"simulator-chart"}
      className="simulator-chart"
      renderAs="svg"
      transitions={false}
    >
      {/* <ChartCategoryAxis>
            <ChartCategoryAxisItem
                categories={distanceArr}
                min={0}
                max={pipelineLength}
                />
        </ChartCategoryAxis> */}
      <ChartValueAxis>
        <ChartValueAxisItem min={0} max={maxSimulationValue} />
      </ChartValueAxis>
      <ChartSeries>
        <ChartSeriesItem
          type="line"
          field="Data"
          categoryField="Distance"
          data={simulationData}
        />
      </ChartSeries>
    </Chart>
  );
};

export default SimulatorChart;
