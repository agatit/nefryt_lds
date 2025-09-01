import React from "react";
import {
  Simulation,
  SimulationDef,
  SimulationParam,
  SimulationParamDef,
} from "../../../../services/api";
import { DetailPanel } from "onyks_shared_kendo";
import { useTranslation } from "react-i18next";
import { TabStripSelectEventArguments } from "@progress/kendo-react-layout";
import { Loader } from "@progress/kendo-react-indicators";
import { TreeViewDataItem } from "../trends/utils";
import {
  processTreeViewItems,
  TreeView,
  TreeViewItemClickEvent,
} from "@progress/kendo-react-treeview";
import { SvgIcon, Typography } from "@progress/kendo-react-common";
import { arrowUpIcon } from "@progress/kendo-svg-icons";

export interface SimulatorDetailPanelProps {
  isLoading: boolean;
  isLoadingSimulationParams: boolean;
  simulationDefs: SimulationDef[];
  simulations: Simulation[];
  simulationParamDefs: SimulationParamDef[];
  simulationParams: SimulationParam[];
  dateTime: Date;
  selectedSimulation: Simulation | undefined;
  onSelectedSimulationChange: (value: Simulation) => void;
}

const SimulatorDetailPanel = React.memo(function SimulatorDetailPanel({
  isLoading,
  isLoadingSimulationParams,
  simulationDefs,
  simulations,
  simulationParamDefs,
  simulationParams,
  selectedSimulation,
  dateTime,
  onSelectedSimulationChange,
}: SimulatorDetailPanelProps) {
  const { t } = useTranslation(["common", "simulator-page"]);

  const pipelineLength = React.useMemo(() => {
    let lengthParam = simulationParams.find(
      (param) => param.SimulationParamDefID == "LENGTH"
    );
    return Number(lengthParam?.Value) ?? 0;
  }, [simulationParams]);

  const simulationTree: TreeViewDataItem[] = React.useMemo(() => {
    return simulations.map((simulation) => {
      return {
        text: simulation.Name,
        id: simulation.ID,
      };
    });
  }, [simulations]);

  const [simulationSelect, setSimulationSelect] = React.useState<string[]>([
    "",
  ]);
  const handleSimulationClick = React.useCallback(
    (event: TreeViewItemClickEvent) => {
      setSimulationSelect([event.itemHierarchicalIndex]);
      onSelectedSimulationChange(
        simulations.find((simulation) => simulation.ID == event.item.id)!
      );
    },
    [simulations]
  );

  return (
    <DetailPanel className="chart-detail-panel" flexGrow={1} extandable={false}>
      {!isLoading ? (
        <div className="detail-panel-content">
          <div className="item">
            <div className="item-row">
              <Typography.p style={{ marginBottom: 0 }}>
                {t("simulator-page:available_simulations")}
              </Typography.p>
            </div>
            <div className="item-row">
              <TreeView
                data={processTreeViewItems(simulationTree, {
                  select: simulationSelect,
                })}
                onItemClick={handleSimulationClick}
                className="simulation-treeview"
              />
            </div>
          </div>
          <div className="separator" />
          {selectedSimulation !== undefined ? (
            <React.Fragment>
              <div className="item">
                <div className="item-row">
                  <Typography.p style={{ marginBottom: 0 }}>
                    {t("simulator-page:current_simulation_date_time")}
                  </Typography.p>
                </div>
                <div className="item-row">{dateTime.toLocaleString()}</div>
              </div>
              <div className="item">
                <div className="item-row">
                  <Typography.p style={{ marginBottom: 0 }}>
                    {t("simulator-page:refresh_time")}
                  </Typography.p>
                </div>
                <div className="item-row">
                  {selectedSimulation.RefreshTimeSeconds + " s"}
                </div>
              </div>
              <div className="separator" />
              <div className="item">
                <div className="item-row">
                  <Typography.p style={{ marginBottom: 0 }}>
                    {t("simulator-page:pipeline_length")}
                  </Typography.p>
                </div>
                <div className="item-row">{pipelineLength} m</div>
              </div>
            </React.Fragment>
          ) : (
            <div className="item">
              <div className="item-row" style={{ alignItems: "center" }}>
                <Typography.p style={{ marginBottom: 0 }}>
                  {t("simulator-page:select_simulation")}
                </Typography.p>
                <SvgIcon icon={arrowUpIcon} />
              </div>
            </div>
          )}
        </div>
      ) : (
        <Loader size="medium" type={"infinite-spinner"} />
      )}
    </DetailPanel>
  );
});

export default SimulatorDetailPanel;
