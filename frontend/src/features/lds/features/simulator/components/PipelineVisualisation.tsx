import React from "react";
import { Simulation, SimulationParam } from "../../../../../services/api";
import { SimulationData } from "../index";
import { SvgIcon } from "@progress/kendo-react-common";
import {
  chevronDoubleLeftIcon,
  chevronDoubleRightIcon,
} from "@progress/kendo-svg-icons";

export interface PipelineVisualisationProps {
  simulation: Simulation;
  simulationParams: SimulationParam[];
  simulationData: SimulationData[];
}

const PipelineVisualisation: React.FC<PipelineVisualisationProps> = ({
  simulation,
  simulationParams,
  simulationData,
}) => {
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

  const pipelineLength = React.useMemo(() => {
    let lengthParam = simulationParams.find(
      (param) => param.SimulationParamDefID == "LENGTH"
    );
    return Number(lengthParam?.Value) ?? 0;
  }, [simulationParams]);

  return (
    <div className="pipeline-visualisation">
      {simulationData.map((simData, index) => {
        var empty = 100 - (simData.Data * 100) / maxSimulationValue;
        return (
          <React.Fragment>
            {index !== 0 && (
              <div className="pipe">
                {/* <div
                  className="pipe-empty"
                  style={{ height: "calc(" + empty + "% - 4px)" }}
                />
                <div className="pipe-fill" /> */}
                {simulationData[index - 1].Data !== simData.Data && (
                  <SvgIcon
                    icon={
                      simulationData[index - 1].Data > simData.Data
                        ? chevronDoubleRightIcon
                        : chevronDoubleLeftIcon
                    }
                    size="small"
                  />
                )}
              </div>
            )}
            <div className="sensors">
              <span className="sensors-distance">{simData.Distance}</span>
              <div className="sensors-empty" style={{ height: empty + "%" }} />
              <div className="sensors-fill" />
            </div>
          </React.Fragment>
        );
      })}
    </div>
  );
};

export default PipelineVisualisation;
