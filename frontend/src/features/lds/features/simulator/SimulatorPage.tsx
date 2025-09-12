import React from "react";
import "../../../../styles/features/lds/features/simulatorPage.scss";
import { AuthContext } from "../../../../contexts/authContext";

import { LDSContext } from "../../contexts/ldsContext";
import { NavbarContext } from "../../../../contexts/navbarContext";
import { useTranslation } from "react-i18next";

import { useHandleApiResponse } from "../../../../hooks/useHandleApiResponse";
import { AppContext } from "../../../../contexts/appContext";
import {
  Simulation,
  SimulationApi,
  SimulationDataApi,
  SimulationDef,
  SimulationDefApi,
  SimulationParam,
  SimulationParamApi,
  SimulationParamDef,
} from "../../../../services/api";
import { axiosInstance, host } from "../../../../lib/apiUtilities";
import { SvgIcon, Typography } from "@progress/kendo-react-common";
import { arrowRightIcon } from "@progress/kendo-svg-icons";
import SimulatorDetailPanel from "./SimulatorDetailPanel";
import SimulatorChart from "./SimulatorChart";
import { Loader } from "@progress/kendo-react-indicators";
import PipelineVisualisation from "./PipelineVisualisation";

export interface SimulationData {
  Distance: number;
  Data: number;
}

export default function TrendsCurrentPage() {
  const auth = React.useContext(AuthContext);
  const handleApiResponse = useHandleApiResponse();
  const { t } = useTranslation(["common", "trends-page"]);
  const appContext = React.useContext(AppContext);

  // UI STUFF
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

  const simulationDefApi = React.useRef(
    new SimulationDefApi(auth?.config, host, axiosInstance)
  );
  const [simulationDefs, setSimulationDefs] = React.useState<SimulationDef[]>(
    []
  );

  const simulationApi = React.useRef(
    new SimulationApi(auth?.config, host, axiosInstance)
  );
  const [simulations, setSimulations] = React.useState<Simulation[]>([]);

  const simulationParamApi = React.useRef(
    new SimulationParamApi(auth?.config, host, axiosInstance)
  );
  const [simulationParamDefs, setSimulationParamDefs] = React.useState<
    SimulationParamDef[]
  >([]);

  const simulationLoadedStatus = React.useRef({
    simdefsLoaded: false,
    simsLoaded: false,
    simParamDefsLoaded: false,
  });
  const isLoadingSimulations = React.useMemo(() => {
    console.log("BAJO JAJO");
    return (
      !simulationLoadedStatus.current.simdefsLoaded &&
      !simulationLoadedStatus.current.simsLoaded &&
      !simulationLoadedStatus.current.simParamDefsLoaded
    );
  }, [
    simulationLoadedStatus.current.simdefsLoaded,
    simulationLoadedStatus.current.simParamDefsLoaded,
    simulationLoadedStatus.current.simsLoaded,
  ]);

  const loadSimulationDefs = React.useCallback(async () => {
    try {
      const response = await handleApiResponse(
        simulationDefApi.current.listSimulationDefsSimulationDefGet.bind(
          simulationDefApi.current
        )
      );
      console.log(response);
      if (response.data) setSimulationDefs(response.data.items);
      simulationLoadedStatus.current.simdefsLoaded = true;
    } catch (error) {
      console.log(error);
    }
  }, []);

  const loadSimulations = React.useCallback(async () => {
    try {
      const response = await handleApiResponse(
        simulationApi.current.listSimulationsSimulationGet.bind(
          simulationApi.current
        )
      );
      console.log(response);
      if (response.data) setSimulations(response.data.items);
      simulationLoadedStatus.current.simsLoaded = true;
    } catch (error) {
      console.log(error);
    }
  }, []);

  const loadSimulationParamDefs = React.useCallback(async () => {
    try {
      const response = await handleApiResponse(
        simulationParamApi.current.listSimulationParamDefsSimulationParamDefGet.bind(
          simulationParamApi.current
        )
      );
      console.log(response);
      if (response.data) setSimulationParamDefs(response.data.items);
      simulationLoadedStatus.current.simParamDefsLoaded = true;
    } catch (error) {
      console.log(error);
    }
  }, []);

  React.useEffect(() => {
    simulationLoadedStatus.current = {
      simdefsLoaded: false,
      simsLoaded: false,
      simParamDefsLoaded: false,
    };
    loadSimulationDefs();
    loadSimulations();
    loadSimulationParamDefs();
  }, [useMockup]);

  const [selectedSimulation, setSelectedSimulation] =
    React.useState<Simulation>();

  const [simulationParams, setSimulationParams] = React.useState<
    SimulationParam[]
  >([]);
  const [isLoadingSimulationParams, setIsLoadingSimulationParams] =
    React.useState<boolean>(false);

  const loadSimulationParams = React.useCallback(async () => {
    if (selectedSimulation == undefined) return;
    setIsLoadingSimulationParams(true);
    try {
      const response = await handleApiResponse(
        simulationParamApi.current.listSimulationParamsBySimulationIdSimulationSimulationIdParamGet.bind(
          simulationParamApi.current
        ),
        selectedSimulation.ID
      );
      console.log(response);
      if (response.data) setSimulationParams(response.data.items);
    } catch (error) {
      console.log(error);
    }
    setIsLoadingSimulationParams(false);
  }, [selectedSimulation]);

  const simulationDataApi = React.useRef(
    new SimulationDataApi(auth?.config, host, axiosInstance)
  );
  const [simulationData, setSimulationData] = React.useState<SimulationData[]>(
    []
  );
  const [simulationCurrentDateTime, setSimulationCurrentDateTime] =
    React.useState<Date>(new Date());

  const loadSimulationData = React.useCallback(async () => {
    if (selectedSimulation == undefined) return;

    try {
      const response = await handleApiResponse(
        simulationDataApi.current.getSimulationDataSimulationSimulationIdDataGet.bind(
          simulationDataApi.current
        ),
        1
      );
      console.log(response);
      setTimeToRefresh(selectedSimulation.RefreshTimeSeconds);
      if (response.data) {
        setSimulationData(response.data.items[0].Data);
        setSimulationCurrentDateTime(
          new Date(response.data.items[0].Time * 1000)
        );
      }
    } catch (error) {
      console.log(error);
    }
  }, [selectedSimulation]);

  const handleSelectedSimulationChange = React.useCallback(
    (simulation: Simulation) => {
      setSelectedSimulation(simulation);
    },
    []
  );

  const [timeToRefresh, setTimeToRefresh] = React.useState(0);

  React.useEffect(() => {
    if (selectedSimulation == undefined) return;

    loadSimulationParams();

    loadSimulationData();
    const interval = setInterval(
      loadSimulationData,
      selectedSimulation.RefreshTimeSeconds * 1000
    );

    return () => clearInterval(interval);
  }, [selectedSimulation]);

  // mockup data testing

  return (
    <React.Fragment>
      <main className="simulator-page">
        {selectedSimulation == undefined ? (
          <div className="no-simulation-container">
            <Typography.p style={{ marginBottom: 0 }} fontSize="large">
              {t("simulator-page:select_simulation")}
            </Typography.p>
            <SvgIcon icon={arrowRightIcon} size="large" />
          </div>
        ) : (
          <div className="chart-container">
            {simulationData.length > 0 ? (
              <React.Fragment>
                <SimulatorChart simulationData={simulationData} />
                <PipelineVisualisation
                  simulation={selectedSimulation}
                  simulationParams={simulationParams}
                  simulationData={simulationData}
                />
              </React.Fragment>
            ) : (
              <Loader
                className="chart-loader"
                size="medium"
                type={"infinite-spinner"}
              />
            )}
          </div>
        )}
        <SimulatorDetailPanel
          isLoading={isLoadingSimulations}
          isLoadingSimulationParams={isLoadingSimulationParams}
          simulationDefs={simulationDefs}
          simulations={simulations}
          simulationParamDefs={simulationParamDefs}
          simulationParams={simulationParams}
          dateTime={simulationCurrentDateTime}
          selectedSimulation={selectedSimulation}
          onSelectedSimulationChange={handleSelectedSimulationChange}
          startTimeToRefresh={timeToRefresh}
        />
      </main>
    </React.Fragment>
  );
}
