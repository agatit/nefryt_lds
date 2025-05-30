import React from "react";
import { AuthContext } from "../../../../contexts/authContext";
import {
  Trend,
  TrendApi,
  TrendDef,
  TrendDefApi,
} from "../../../../services/api";
import {
  PlotAreaHoverEvent,
  SelectEndEvent,
  SelectStartEvent,
} from "@progress/kendo-react-charts";
import { useRefreshableRequest } from "../../../../hooks/useRefreshableRequest";
import { axiosInstance, host } from "../../../../lib/apiUtilities";
import { Loader } from "@progress/kendo-react-indicators";
import "../../../../styles/features/lds/features/trendPage.scss";
import {
  Checkbox,
  CheckboxChangeEvent,
  TextBox,
  TextBoxChangeEvent,
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
import { Label } from "@progress/kendo-react-labels";
import {
  DateTimePicker,
  DateTimePickerChangeEvent,
} from "@progress/kendo-react-dateinputs";
import CursorBubble from "../../../../components/CursorBubble";
import { DetailPanel } from "onyks_shared_kendo";
import { chartLegendIcon } from "../../components/chartLegendIcon";
import { pencilIcon, saveIcon } from "@progress/kendo-svg-icons";
import { Button } from "@progress/kendo-react-buttons";
import { Dialog, DialogActionsBar } from "@progress/kendo-react-dialogs";
import {
  ItemRenderProps,
  processTreeViewItems,
  TreeView,
  TreeViewDragAnalyzer,
  TreeViewDragClue,
  TreeViewExpandChangeEvent,
  TreeViewItemDragEndEvent,
  TreeViewItemDragOverEvent,
  TreeViewItemDragStartEvent,
  TreeViewOperationDescriptor,
} from "@progress/kendo-react-treeview";
import TrendChart, { ChartSeriesTrendData, ChartTrendData } from "./TrendChart";
import TrendsDetailPanel from "./TrendsDetailPanel";
import ChartEditDialog from "./ChartEditDialog";

const mainChartSampleSize = 400;
const navigationChartSampleSize = 100;

export type MockupTrendType = {
  ID: number;
  TrendGroupID: number;
  Color: string;
  TrendDefID: string;
  Name: string;
  Unit: string;
};

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

export interface TreeViewDataItem {
  id?: number;
  text: string;
  expanded?: boolean;
  checked?: boolean;
  selected?: boolean;
  items?: TreeViewDataItem[];
}

const mockupTrendDefs: TrendDef[] = [
  {
    ID: "P01",
    Name: "Pressure",
  },
  {
    ID: "DP01",
    Name: "Pressure Derivative",
  },
  {
    ID: "T01",
    Name: "Temperature",
  },
  {
    ID: "DT01",
    Name: "Temperature Derivative",
  },
];

const mockupTrends: MockupTrendType[] = [
  {
    ID: 0,
    TrendGroupID: 1,
    Color: "#ff6358",
    TrendDefID: "P01",
    Name: "Ciśnienie 1",
    Unit: "MPa",
  },
  {
    ID: 1,
    TrendGroupID: 1,
    Color: "#ffe162",
    TrendDefID: "P01",
    Name: "Ciśnienie 2",
    Unit: "MPa",
  },
  {
    ID: 2,
    TrendGroupID: 1,
    Color: "#4cd180",
    TrendDefID: "P01",
    Name: "Ciśnienie 3",
    Unit: "MPa",
  },
  {
    ID: 3,
    TrendGroupID: 2,
    Color: "#4b5ffa",
    TrendDefID: "DP01",
    Name: "Pochodna Ciśnienia 1",
    Unit: "",
  },
  {
    ID: 4,
    TrendGroupID: 2,
    Color: "#ac58ff",
    TrendDefID: "DP01",
    Name: "Pochodna Ciśnienia 2",
    Unit: "",
  },
  {
    ID: 5,
    TrendGroupID: 3,
    Color: "#ff5892",
    TrendDefID: "P01",
    Name: "Temperatura 1",
    Unit: "°C",
  },
  {
    ID: 6,
    TrendGroupID: 3,
    Color: "#59ffc4",
    TrendDefID: "P01",
    Name: "Temperatura 2",
    Unit: "°C",
  },
  {
    ID: 7,
    TrendGroupID: 4,
    Color: "#ffc459",
    TrendDefID: "P01",
    Name: "Pochodna Temperatury 1",
    Unit: "",
  },
  {
    ID: 8,
    TrendGroupID: 4,
    Color: "#4b9dd1",
    TrendDefID: "P01",
    Name: "Pochodna Temperatury 2",
    Unit: "",
  },
];

const mockupTrendTreeData: TreeViewDataItem[] = [
  {
    id: 1,
    text: "Ciśnienie",
    items: [
      {
        id: 2,
        text: "Pomiary",
        items: [
          { text: mockupTrends[0].Name, id: mockupTrends[0].ID },
          { text: mockupTrends[1].Name, id: mockupTrends[1].ID },
          { text: mockupTrends[2].Name, id: mockupTrends[2].ID },
        ],
      },
      {
        id: 3,
        text: "Pochodne",
        items: [
          { text: mockupTrends[3].Name, id: mockupTrends[3].ID },
          { text: mockupTrends[4].Name, id: mockupTrends[4].ID },
        ],
      },
    ],
  },
  {
    id: 4,
    text: "Temperatura",
    items: [
      {
        id: 5,
        text: "Pomiary",
        items: [
          { text: mockupTrends[5].Name, id: mockupTrends[5].ID },
          { text: mockupTrends[6].Name, id: mockupTrends[6].ID },
        ],
      },
      {
        id: 6,
        text: "Pochodne",
        items: [
          { text: mockupTrends[7].Name, id: mockupTrends[7].ID },
          { text: mockupTrends[8].Name, id: mockupTrends[8].ID },
        ],
      },
    ],
  },
];

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

export default function TrendsPage() {
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

  const [isChartInEdit, setIsChartInEdit] = React.useState<boolean>(false);

  const handleChartEditButtonClick = React.useCallback(
    (e: React.MouseEvent) => {
      setIsChartInEdit(!isChartInEdit);
    },
    [isChartInEdit]
  );

  const endChartEdit = React.useCallback(() => {
    setIsChartInEdit(false);
  }, []);

  const axisTreeRef = React.useRef<any>(null);

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
  const [trendsState, setTrendsState] = React.useState<
    Trend[] | MockupTrendType[]
  >(mockupTrends);
  const [isLoadingTrends, setIsLoadingTrends] = React.useState<boolean>(false);
  // const trendLoadStatusRef = React.useRef<TrendLoadStatus>({
  //   defsLoaded: false,
  //   trendsLoaded: false,
  // });

  const [axesState, setAxesState] = React.useState<AxisType[]>([
    {
      Name: "Ciśnienie pomiary MPa",
      Unit: "MPa",
      TrendIDs: [0, 1, 2],
      ScaleMax: 9,
      ScaleMin: -1,
    },
  ]);

  const handleAxesStateChange = React.useCallback((value: AxisType[]) => {
    if (value) setAxesState(value);
  }, []);

  const [trendsTree, setTrendsTree] =
    React.useState<TreeViewDataItem[]>(mockupTrendTreeData);
  const axisTree: TreeViewDataItem[] = React.useMemo(() => {
    return axesState.map((axis) => {
      return {
        text: axis.Name,
        items: axis.TrendIDs.map((id) => {
          const trend = trendsState.find((trend) => trend.ID == id);
          return {
            id: id,
            text: trend!.Name!,
          };
        }),
      };
    });
  }, [axesState]);

  const TreeCustomItem = React.useCallback(
    (props: ItemRenderProps, depth: number) => {
      const trend = trendsState.find((trend) => trend.ID == props.item.id);
      return props.itemHierarchicalIndex.split("_").length > depth ? (
        <React.Fragment>
          {trend && (
            <SvgIcon
              icon={chartLegendIcon}
              size="xlarge"
              style={{ stroke: (trend as MockupTrendType).Color }}
            />
          )}
          <span>{props.item.text}</span>
        </React.Fragment>
      ) : (
        <span>{props.item.text}</span>
      );
    },
    [trendsState]
  );

  const TrendsTreeCustomItem = React.useCallback(
    (props: ItemRenderProps) => {
      return TreeCustomItem(props, 2);
    },
    [TreeCustomItem]
  );

  const AxisTreeCustomItem = React.useCallback(
    (props: ItemRenderProps) => {
      return TreeCustomItem(props, 1);
    },
    [TreeCustomItem]
  );

  // Trends Data
  const [trendsData, setTrendsData] = React.useState<ChartSeriesTrendData[]>(
    []
  );
  const [navigatorData, setNavigatorData] = React.useState<
    ChartSeriesTrendData[]
  >([]);
  // const [isLoadingTrendsData, setIsLoadingTrendsData] =
  //   React.useState<boolean>(false);

  // Loading from api

  // function checkIfTrendsLoaded() {
  //   if (
  //     trendLoadStatusRef.current.defsLoaded &&
  //     trendLoadStatusRef.current.trendsLoaded
  //   )
  //     setIsLoadingTrends(false);
  // }

  // async function loadTrends() {
  //   trendLoadStatusRef.current = { defsLoaded: false, trendsLoaded: false };

  //   refreshableRequest(
  //     trendDefApi.listTrendDefsTrendDefGet.bind(trendDefApi)
  //   ).then((response) => {
  //     trendLoadStatusRef.current.defsLoaded = true;
  //     if (response?.data) setTrendDefs(response?.data.items);
  //     checkIfTrendsLoaded();
  //   });

  //   refreshableRequest(trendApi.listTrendsTrendGet.bind(trendApi)).then(
  //     (response) => {
  //       trendLoadStatusRef.current.trendsLoaded = true;
  //       if (response?.data)
  //         setTrendsState({ trends: response.data.items, activeTrendsIDs: [] });
  //       checkIfTrendsLoaded();
  //     }
  //   );
  // }

  // mockup data testing

  const generateTestData = React.useCallback(async () => {
    if (startDate == null || endDate == null) return;

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
  }, [startDate, endDate, trendsState, axesState]);

  React.useEffect(() => {
    generateTestData();
  }, [startDate, endDate, axesState]);

  return (
    <React.Fragment>
      <main>
        <TrendChart
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
        />
        <TrendsDetailPanel
          isLoadingTrends={isLoadingTrends}
          axisTreeRef={axisTreeRef}
          axisTree={axisTree}
          TreeCustomItem={AxisTreeCustomItem}
          isChartInEdit={isChartInEdit}
          onChartEditButtonClick={handleChartEditButtonClick}
          startDate={startDate}
          endDate={endDate}
          onStartDateChange={handleStartDateChange}
          onEndDateChange={handleEndDateChange}
        />
      </main>
      {isChartInEdit && (
        <ChartEditDialog
          trendsTree={trendsTree}
          TrendsTreeCustomItem={TrendsTreeCustomItem}
          AxisTreeCustomItem={AxisTreeCustomItem}
          axisTreeRef={axisTreeRef}
          axisTree={axisTree}
          onCancelButtonClick={endChartEdit}
          onSaveButtonClick={endChartEdit}
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
