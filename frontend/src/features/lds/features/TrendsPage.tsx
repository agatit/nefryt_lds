import React from "react";
import { AuthContext } from "../../../contexts/authContext";
import {
  Configuration,
  PageTrend,
  PageTrendDef,
  Trend,
  TrendApi,
  TrendApiFactory,
  TrendDef,
  TrendDefApi,
} from "../../../services/api";
import {
  Chart,
  ChartCategoryAxis,
  ChartCategoryAxisItem,
  ChartSeries,
  ChartSeriesItem,
  ChartTooltip,
} from "@progress/kendo-react-charts";
import { useRefreshableRequest } from "../../../hooks/useRefreshableRequest";
import { axiosInstance, host } from "../../../lib/apiUtilities";
import { Loader } from "@progress/kendo-react-indicators";
import "../../../styles/features/lds/features/trendPage.scss";
import TrendCheckbox from "../components/TrendCheckbox";
import { CheckboxChangeEvent } from "@progress/kendo-react-inputs";

type ChartTrendData = {
  timestamp: Date;
  value: number;
};

type TrendsState = {
  trends: Trend[];
  activeTrendsIDs: number[];
};

type TrendLoadStatus = {
  defsLoaded: boolean;
  trendsLoaded: boolean;
};

export default function TrendsPage() {
  const auth = React.useContext(AuthContext);
  const refreshableRequest = useRefreshableRequest();

  const trendDefApi = React.useMemo(
    () => new TrendDefApi(auth?.config, host, axiosInstance),
    [auth]
  );
  const trendApi = React.useMemo(
    () => new TrendApi(auth?.config, host, axiosInstance),
    [auth]
  );

  // Trends and trend defs
  const [trendDefs, setTrendDefs] = React.useState<TrendDef[]>([]);
  const [trendsState, setTrendsState] = React.useState<TrendsState>();
  const [isLoadingTrends, setIsLoadingTrends] = React.useState<boolean>(true);
  const trendLoadStatusRef = React.useRef<TrendLoadStatus>({
    defsLoaded: false,
    trendsLoaded: false,
  });

  // Trends Data
  const [trendsData, setTrendsData] = React.useState<ChartTrendData[][]>([]);
  const [isLoadingTrendsData, setIsLoadingTrendsData] =
    React.useState<boolean>(false);

  const [beginDate, setBeginDate] = React.useState(new Date(1741958666));
  const [endDate, setEndDate] = React.useState(new Date(1741959745));
  const [samples, setSamples] = React.useState(1000);

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
    setIsLoadingTrendsData(true);

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
        if (response?.data)
          setTrendsState({ trends: response.data.items, activeTrendsIDs: [] });
        checkIfTrendsLoaded();
      }
    );
  }

  React.useEffect(() => {
    loadTrends();
  }, [auth]);

  // function handleTrendCheckbox(event: CheckboxChangeEvent) {

  // }

  // React.useEffect(() => {
  //   async function loadData() {
  //     const trendsData: ChartTrendData[][] = [];

  //     // for (let trend of trendsListResponse!.data.items) {
  //     //   const trendData: ChartTrendData[] = [];
  //     //   for (
  //     //     let page = 1;
  //     //     page <= (samples >= 100 ? samples / 100 : 1);
  //     //     page++
  //     //   ) {
  //     //     (
  //     //       await refreshableRequest(
  //     //         trendApi.getSingleTrendDataTrendTrendIdSingleDataBeginEndSamplesGet.bind(
  //     //           trendApi
  //     //         ),
  //     //         trend.ID!.toString(),
  //     //         beginDate.getTime(),
  //     //         endDate.getTime(),
  //     //         samples,
  //     //         page,
  //     //         100
  //     //       )
  //     //     )?.data.items.forEach((item) => {
  //     //       trendData.push({
  //     //         timestamp: new Date(item.Timestamp * 1000 + item.TimestampMs),
  //     //         value: item.Value,
  //     //       });
  //     //     });
  //     //   }
  //     //   trendsData.push(trendData);
  //     // }
  //   }
  //   loadData();
  // }, [auth]);

  return (
    <React.Fragment>
      <main>
        <div className="chart-container">
          <Chart renderAs="canvas" pannable={true} zoomable={true}>
            <ChartTooltip />
            <ChartCategoryAxis>
              <ChartCategoryAxisItem
                baseUnit={"auto"}
                maxDivisions={30}
                rangeLabels={{ format: "HH:mm:ss", visible: true }}
              />
            </ChartCategoryAxis>
            <ChartSeries>
              {trendsData.map((trend) => {
                return (
                  <ChartSeriesItem
                    type="line"
                    field="value"
                    categoryField="timestamp"
                    data={trend}
                    markers={{ visible: false }}
                  />
                );
              })}
            </ChartSeries>
          </Chart>
        </div>
        <div className="trend-select-container">
          {trendLoadStatusRef.current.defsLoaded &&
          trendLoadStatusRef.current.trendsLoaded ? (
            trendsState?.trends.map((trend) => {
              return <TrendCheckbox trendName={trend.Name} />;
            })
          ) : (
            <Loader size="medium" type={"infinite-spinner"} />
          )}
        </div>
        <div className="date-time-select-container"></div>
      </main>
    </React.Fragment>
  );
}
