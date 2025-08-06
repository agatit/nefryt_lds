import React from "react";
import { AuthContext } from "../../../../contexts/authContext";
import {
  Trend,
  TrendApi,
  TrendDefBase,
  TrendDefApi,
  Template,
  Unit,
} from "../../../../services/api";

import { useRefreshableRequest } from "../../../../hooks/useRefreshableRequest";
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
  MockupTrendType,
  mockupUnits,
} from "../../../../data/mockup-data";

const mainChartSampleSize = 500;
const navigationChartSampleSize = 50;

type TrendLoadStatus = {
  defsLoaded: boolean;
  trendsLoaded: boolean;
};

export type AxisType = {
  Name: string;
  Unit: string;
  TrendIDs: number[];
  ScaleMax: number;
  ScaleMin: number;
};

export interface ChartTrendData {
  timestamp: Date;
  value: number | null;
}

export interface ChartSeriesTrendData {
  data: ChartTrendData[];
  id: number;
  color: string;
}

export interface TreeViewDataItem {
  id?: number | string;
  text: string;
  expanded?: boolean;
  checked?: boolean;
  selected?: boolean;
  items?: TreeViewDataItem[];
}

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

export interface TrendsPageProps {
  useMockup: boolean;
}

export default function TrendsPage({ useMockup }: TrendsPageProps) {
  const auth = React.useContext(AuthContext);
  const refreshableRequest = useRefreshableRequest();

  // UI STUFF
  const [startDate, setStartDate] = React.useState<Date>(() => {
    var date = new Date();
    date.setDate(date.getDate() - 1);
    return date;
  });
  const [endDate, setEndDate] = React.useState<Date>(new Date());

  const handleChartStartDateChange = React.useCallback((value: Date) => {
    if (value) setStartDate(value);
  }, []);
  const handleChartEndDateChange = React.useCallback((value: Date) => {
    if (value) setEndDate(value);
  }, []);

  const navigationStartDate = React.useMemo(() => {
    return new Date(
      startDate.getTime() - (endDate.getTime() - startDate.getTime())
    );
  }, [startDate, endDate]);
  const navigationEndDate = React.useMemo(() => {
    return new Date(
      endDate.getTime() + (endDate.getTime() - startDate.getTime())
    );
  }, [startDate, endDate]);

  const handleStartDateChange = React.useCallback(
    (e: DateTimePickerChangeEvent) => {
      if (e.value) setStartDate(e.value);
    },
    []
  );
  const handleEndDateChange = React.useCallback(
    (e: DateTimePickerChangeEvent) => {
      if (e.value) setEndDate(e.value);
    },
    []
  );

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

  const trendDefApi = React.useMemo(
    () => new TrendDefApi(auth?.config, host, axiosInstance),
    [auth]
  );
  const trendApi = React.useMemo(
    () => new TrendApi(auth?.config, host, axiosInstance),
    [auth]
  );

  // Trends and trend defs
  const [trendDefs, setTrendDefs] =
    React.useState<TrendDefBase[]>(mockupTrendDefs);
  const [trendsState, setTrendsState] = React.useState<
    Trend[] | MockupTrendType[]
  >(mockupTrends);
  const [isLoadingTrends, setIsLoadingTrends] = React.useState<boolean>(false);
  const trendLoadStatusRef = React.useRef<TrendLoadStatus>({
    defsLoaded: false,
    trendsLoaded: false,
  });

  const [axesState, setAxesState] = React.useState<AxisType[]>(
    useMockup
      ? mockupAxes
      : [
          {
            Name: "Ciśnienia",
            Unit: "MPa",
            TrendIDs: [1, 2, 3, 4],
            ScaleMax: 0,
            ScaleMin: 0,
          },
        ]
  );

  const handleAxesStateChange = React.useCallback((value: AxisType[]) => {
    if (value) setAxesState(value);
  }, []);

  const [unitsState, setUnitsState] = React.useState<Unit[]>(
    useMockup ? mockupUnits : []
  );

  const [templatesState, setTemplatesState] = React.useState<Template[]>(
    useMockup ? mockupTemplates : []
  );
  const handleTemplateStateChange = React.useCallback((value: Template[]) => {
    if (value) setTemplatesState(value);
  }, []);

  const handleSelectedTemplateChange = React.useCallback(
    (template: Template) => {
      if (template.Axes == null || template.Axes.length == 0) return;

      const newAxesState: AxisType[] = [];
      for (let axis of template.Axes) {
        const unit = unitsState.find((u) => u.ID == axis.UnitID);
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
    [unitsState]
  );

  const handleCreateNewTemplate = React.useCallback(
    (name: string) => {
      // TODO: connect to api
      let newTemplate: Template = {
        Name: name,
        Axes: axesState.map((axis) => {
          const unit = unitsState.find((u) => u.Symbol == axis.Unit);
          return {
            TrendsID: axis.TrendIDs,
            Title: axis.Name,
            UnitID: unit!.ID,
            ScaledMin: axis.ScaleMin,
            ScaledMax: axis.ScaleMax,
          };
        }),
        ID: templatesState.length, //tmp set id
      };

      setTemplatesState([...templatesState, newTemplate]);
    },
    [templatesState, axesState]
  );

  // Trends Data
  const [trendsData, setTrendsData] = React.useState<ChartSeriesTrendData[]>(
    []
  );
  const [navigatorData, setNavigatorData] = React.useState<
    ChartSeriesTrendData[]
  >([]);
  const [isLoadingTrendsData, setIsLoadingTrendsData] =
    React.useState<boolean>(true);
  const trendsDataLoadStatusRef = React.useRef<boolean>(false);

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
        if (response?.data) setTrendsState(response.data.items);
        checkIfTrendsLoaded();
      }
    );
  }

  function checkIfTrendsDataLoaded() {
    if (trendsDataLoadStatusRef) setIsLoadingTrendsData(false);
  }

  async function loadTrendsData() {
    trendsDataLoadStatusRef.current = false;

    var trendIdList: string = "";
    const trendIdArr: number[] = [];

    axesState.forEach((axis) => {
      trendIdArr.push(...axis.TrendIDs);
    });

    trendIdArr.forEach((id) => {
      trendIdList += id.toString() + ",";
    });

    refreshableRequest(
      trendApi.getTrendDataTrendTrendIdListDataBeginEndSamplesGet.bind(
        trendApi
      ),
      trendIdList,
      startDate.getTime(),
      endDate.getTime(),
      mainChartSampleSize,
      1,
      1000
    )
      .then((response) => {
        const newTrendsData: ChartSeriesTrendData[] = trendIdArr.map((id) => {
          return {
            data: [],
            id: id,
            color: trendsState.find((trend) => trend.ID == id)?.Color!,
          };
        });
        response?.data.items.forEach((item) => {
          const timestamp = new Date(item.Timestamp * 1000);
          item.Data?.forEach((dataitem) => {
            const index = newTrendsData.findIndex((td) => td.id == dataitem.ID);
            newTrendsData[index].data.push({
              timestamp: timestamp,
              value: dataitem.Value ? dataitem.Value : null,
            });
          });
        });

        trendsDataLoadStatusRef.current = true;
        checkIfTrendsDataLoaded();

        setTrendsData(newTrendsData);
      })
      .catch((err) => {
        if (err.status == 404) {
          console.log("no data");
        }
      });
  }

  // mockup data testing

  const generateTestData = React.useCallback(async () => {
    if (startDate == null || endDate == null) return;

    trendLoadStatusRef.current = { defsLoaded: false, trendsLoaded: false };
    trendsDataLoadStatusRef.current = false;

    const timeDiff = endDate.getTime() - startDate.getTime();
    const step = Math.floor(timeDiff / mainChartSampleSize);
    const newTrendsData: ChartSeriesTrendData[] = [];

    const navStartDate = new Date(startDate.getTime() - timeDiff);
    const navEndDate = new Date(endDate.getTime() + timeDiff);
    const newNavData: ChartSeriesTrendData[] = [];
    const step2 = Math.floor(
      (navEndDate.getTime() - navStartDate.getTime()) /
        navigationChartSampleSize
    );

    const activeTrendsIDs: number[] = [];
    for (let axis of axesState) {
      for (let id of axis.TrendIDs) {
        activeTrendsIDs.push(id);
      }
    }

    for (let trend of trendsState!) {
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

      const navData: ChartTrendData[] = [];
      for (let i = 0; i < navigationChartSampleSize; i++) {
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

      newTrendsData.push({
        data: generatedData,
        id: trend.ID!,
        color: trend.Color! as string,
      });
      newNavData.push({
        data: navData,
        id: trend.ID!,
        color: trend.Color! as string,
      });
    }

    setTrendsData(newTrendsData);
    setNavigatorData(newNavData);

    trendLoadStatusRef.current = { defsLoaded: true, trendsLoaded: true };
    checkIfTrendsLoaded();
    trendsDataLoadStatusRef.current = true;
    checkIfTrendsDataLoaded();
  }, [startDate, endDate, trendsState, axesState]);

  React.useEffect(() => {
    useMockup ? generateTestData() : loadTrends();
  }, [startDate, endDate, axesState]);

  React.useEffect(() => {
    if (!isLoadingTrends && !useMockup) loadTrendsData();
  }, [isLoadingTrends, axesState]);

  return (
    <React.Fragment>
      <main className="trends-page">
        <TrendChart
          isLoadingTrendsData={isLoadingTrendsData}
          startDate={startDate}
          endDate={endDate}
          navigationStartDate={navigationStartDate}
          navigationEndDate={navigationEndDate}
          trendData={trendsData}
          navigatorData={navigatorData}
          axesState={axesState}
          onStartDateChange={handleChartStartDateChange}
          onEndDateChange={handleChartEndDateChange}
          onShowCursorBubbleChange={handleShowCursorBubbleChange}
          onCursorBubbleTextChange={handleCursorBubbleTextChange}
          highlightedTrendID={highlightedTrendID}
        />
        <TrendsDetailPanel
          isLoadingTrends={isLoadingTrends}
          trends={trendsState}
          axesState={axesState}
          onAxesStateChange={handleAxesStateChange}
          onChartEditButtonClick={openChartEdit}
          startDate={startDate}
          endDate={endDate}
          onStartDateChange={handleStartDateChange}
          onEndDateChange={handleEndDateChange}
          templates={templatesState}
          onSelectedTemplateChange={handleSelectedTemplateChange}
          handleCreateNewTemplate={handleCreateNewTemplate}
          onHighlightedTrendIDChange={setHighlightedTrendID}
        />
      </main>
      {showChartEdit && (
        <ChartEditDialog
          useMockup={useMockup}
          closeDialog={closeChartEdit}
          trendDefs={trendDefs}
          trendGroups={mockupTrendGroupFromDB}
          mockupTrendTreeData={mockupTrendTreeData}
          trendsState={trendsState}
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
