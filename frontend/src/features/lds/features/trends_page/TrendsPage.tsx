import React from "react";
import { AuthContext } from "../../../../contexts/authContext";
import {
  Trend,
  TrendApi,
  TrendDefBase,
  TrendDefApi,
  Template,
  Axis,
  Unit,
} from "../../../../services/api";

import { useRefreshableRequest } from "../../../../hooks/useRefreshableRequest";
import { axiosInstance, host } from "../../../../lib/apiUtilities";
import "../../../../styles/features/lds/features/trendPage.scss";

import { SvgIcon, Typography } from "@progress/kendo-react-common";
import { DateTimePickerChangeEvent } from "@progress/kendo-react-dateinputs";
import CursorBubble from "../../../../components/CursorBubble";
import { chartLegendIcon } from "../../components/chartLegendIcon";
import { SVGIcon, xIcon } from "@progress/kendo-svg-icons";
import { Button } from "@progress/kendo-react-buttons";
import { ItemRenderProps } from "@progress/kendo-react-treeview";
import TrendChart from "./TrendChart";
import TrendsDetailPanel from "./TrendsDetailPanel";
import ChartEditDialog from "./ChartEditDialog";

const mainChartSampleSize = 500;
const navigationChartSampleSize = 50;

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

const mockupTrendDefs: TrendDefBase[] = [
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
    Unit: "MPa/s",
  },
  {
    ID: 4,
    TrendGroupID: 2,
    Color: "#ac58ff",
    TrendDefID: "DP01",
    Name: "Pochodna Ciśnienia 2",
    Unit: "MPa/s",
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
    Unit: "°C/s",
  },
  {
    ID: 8,
    TrendGroupID: 4,
    Color: "#4b9dd1",
    TrendDefID: "P01",
    Name: "Pochodna Temperatury 2",
    Unit: "°C/s",
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

const mockupAxes: AxisType[] = [
  {
    Name: "Ciśnienie pomiary MPa",
    Unit: "MPa",
    TrendIDs: [0, 1, 2],
    ScaleMax: 9,
    ScaleMin: -1,
  },
];

const mockupUnits: Unit[] = [
  {
    ID: "C",
    Name: "Temperatura",
    Symbol: "°C",
    BaseID: "C",
    Multiplier: "1.0",
  },
  {
    ID: "MPa",
    Name: "Ciśnienie",
    Symbol: "MPa",
    BaseID: "MPa",
    Multiplier: "1.0",
  },
  {
    ID: "C_s",
    Name: "Pochodna temperatury",
    Symbol: "°C/s",
    BaseID: "C_s",
    Multiplier: "1.0",
  },
  {
    ID: "MPa_s",
    Name: "Pochodna ciśnienia",
    Symbol: "MPa/s",
    BaseID: "MPa_s",
    Multiplier: "1.0",
  },
];

const mockupTemplates: Template[] = [
  {
    Name: "Pomiary ciśnień",
    Axes: [
      {
        TrendsID: [0, 1, 2],
        Title: "Ciśnienie",
        UnitID: "MPa",
        ScaledMin: -4,
        ScaledMax: 12,
      },
    ],
    ID: 0,
  },
  {
    Name: "Ciśnienia wszystko",
    Axes: [
      {
        TrendsID: [0, 1, 2],
        Title: "Ciśnienie",
        UnitID: "MPa",
        ScaledMin: -4,
        ScaledMax: 12,
      },
      {
        TrendsID: [3, 4],
        Title: "Pochodna",
        UnitID: "MPa_s",
        ScaledMin: -4,
        ScaledMax: 12,
      },
    ],
    ID: 1,
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

interface MockupTrendGroupType {
  ID: number;
  Name: string;
  AnalisisOnly?: boolean;
}

const mockupTrendGroupFromDB: MockupTrendGroupType[] = [
  {
    ID: 1,
    Name: "Przepływ",
  },
  {
    ID: 2,
    Name: "Temperatura",
  },
  {
    ID: 3,
    Name: "Gęstość",
  },
  {
    ID: 4,
    Name: "Ciśnienie",
  },
  {
    ID: 6,
    Name: "Przepływ",
  },
  {
    ID: 7,
    Name: "Temperatura",
  },
  {
    ID: 8,
    Name: "Gęstość",
  },
  {
    ID: 9,
    Name: "Ciśnienie",
  },
  {
    ID: 10,
    Name: "Automatyka",
  },
  {
    ID: 11,
    Name: "Automatyka",
  },
];

export interface TrendsPageProps {
  useMockup: boolean;
}

export default function TrendsPage({ useMockup }: TrendsPageProps) {
  React.useLayoutEffect(() => {
    const axesElements = document
      .getElementsByClassName("main-chart")[0]
      ?.getElementsByTagName("svg")[0]?.children[1]?.children[2]?.children;
  });

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

  const trendsTree: TreeViewDataItem[] = React.useMemo(() => {
    if (useMockup) return mockupTrendTreeData;

    const trendsTree: TreeViewDataItem[] = mockupTrendGroupFromDB.map(
      (item) => {
        return {
          id: item.ID,
          text: item.Name,
          items: [],
        };
      }
    );

    for (let trend of trendsState) {
      const index = trendsTree.findIndex(
        (item) => item.id == trend.TrendGroupID
      );
      const trendDef = trendDefs.find((item) => item.ID == trend.TrendDefID);

      const indexTrendDef = trendsTree[index].items?.findIndex(
        (item) => item.id == trend.TrendDefID
      );

      if (indexTrendDef == -1) {
        trendsTree[index].items?.push({
          id: trend.TrendDefID,
          text: trendDef?.Name!,
          items: [
            {
              id: trend.ID,
              text: trend.Name!,
            },
          ],
        });

        continue;
      }

      trendsTree[index].items![indexTrendDef!].items?.push({
        id: trend.ID,
        text: trend.Name!,
      });
    }

    return trendsTree;
  }, [trendsState, mockupTrendGroupFromDB]);

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
  }, [axesState, trendsState]);

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
    []
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

  // Treeview stuff

  const TreeCustomItem = React.useCallback(
    (
      props: ItemRenderProps,
      depth: number,
      buttonIcon?: SVGIcon,
      buttonOnClick?: React.MouseEventHandler<HTMLButtonElement>
    ) => {
      const trend = trendsState.find((trend) => trend.ID == props.item.id);
      const correctDepth =
        props.itemHierarchicalIndex.split("_").length > depth;
      return (
        <React.Fragment>
          {trend && correctDepth && (
            <SvgIcon
              icon={chartLegendIcon}
              size="xlarge"
              style={{ stroke: (trend as MockupTrendType).Color }}
            />
          )}
          {correctDepth ? (
            <span>{props.item.text}</span>
          ) : (
            <span style={{ fontWeight: "bold" }}>{props.item.text}</span>
          )}
          {buttonIcon !== undefined && (
            <Button
              svgIcon={buttonIcon}
              onClick={buttonOnClick}
              fillMode="flat"
            />
          )}
        </React.Fragment>
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

  const AxisEditTreeCustomItem = React.useCallback(
    (props: ItemRenderProps) => {
      return TreeCustomItem(props, 1);
    },
    [TreeCustomItem]
  );

  const removeFromAxes = React.useCallback(
    (props: ItemRenderProps) => {
      const indexArray = props.itemHierarchicalIndex.split("_");

      if (indexArray.length == 1) {
        setAxesState(axesState.filter((axis) => axis.Name !== props.item.text));
        return;
      }

      setAxesState(
        axesState.map((axis, i) => {
          if (i !== parseInt(indexArray[0])) return axis;
          return {
            ...axis,
            TrendIDs: axis.TrendIDs.filter(
              (ids, index) => index !== parseInt(indexArray[1])
            ),
          };
        })
      );
    },
    [axesState]
  );

  const AxisLegendTreeCustomItem = React.useCallback(
    (props: ItemRenderProps) => {
      return TreeCustomItem(props, 1, xIcon, () => removeFromAxes(props));
    },
    [TreeCustomItem, removeFromAxes]
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
      <main>
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
        />
        <TrendsDetailPanel
          isLoadingTrends={isLoadingTrends}
          axisTreeRef={axisTreeRef}
          axisTree={axisTree}
          TreeCustomItem={AxisLegendTreeCustomItem}
          isChartInEdit={isChartInEdit}
          onChartEditButtonClick={handleChartEditButtonClick}
          startDate={startDate}
          endDate={endDate}
          onStartDateChange={handleStartDateChange}
          onEndDateChange={handleEndDateChange}
          templates={templatesState}
          onSelectedTemplateChange={handleSelectedTemplateChange}
          handleCreateNewTemplate={handleCreateNewTemplate}
        />
      </main>
      {isChartInEdit && (
        <ChartEditDialog
          trendsTree={trendsTree}
          TrendsTreeCustomItem={TrendsTreeCustomItem}
          AxisTreeCustomItem={AxisLegendTreeCustomItem}
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
