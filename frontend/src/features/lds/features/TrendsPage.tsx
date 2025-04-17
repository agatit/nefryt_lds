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

type ChartTrendData = {
  timestamp: Date;
  value: number;
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

  const [trendDefs, setTrendDefs] = React.useState<TrendDef[]>([]);
  const [trends, setTrends] = React.useState<Trend[]>([]);
  const [trendsData, setTrendsData] = React.useState<ChartTrendData[][]>([]);

  const [beginDate, setBeginDate] = React.useState(new Date(1741958666));
  const [endDate, setEndDate] = React.useState(new Date(1741959745));
  const [samples, setSamples] = React.useState(1000);

  React.useEffect(() => {
    async function loadData() {
      const trendDefsListResponse = await refreshableRequest(
        trendDefApi.listTrendDefsTrendDefGet.bind(trendDefApi)
      );
      const trendsListResponse = await refreshableRequest(
        trendApi.listTrendsTrendGet.bind(trendApi)
      );

      const trendsData: ChartTrendData[][] = [];

      for (let trend of trendsListResponse!.data.items) {
        const trendData: ChartTrendData[] = [];
        for (
          let page = 1;
          page <= (samples >= 100 ? samples / 100 : 1);
          page++
        ) {
          (
            await refreshableRequest(
              trendApi.getSingleTrendDataTrendTrendIdSingleDataBeginEndSamplesGet.bind(
                trendApi
              ),
              trend.ID!.toString(),
              beginDate.getTime(),
              endDate.getTime(),
              samples,
              page,
              100
            )
          )?.data.items.forEach((item) => {
            trendData.push({
              timestamp: new Date(item.Timestamp * 1000 + item.TimestampMs),
              value: item.Value,
            });
          });
        }
        trendsData.push(trendData);
      }

      setTrendDefs(
        trendDefsListResponse?.data.items
          ? trendDefsListResponse.data.items
          : []
      );
      setTrends(
        trendsListResponse?.data.items ? trendsListResponse.data.items : []
      );
      console.log(trendsData);
      setTrendsData(trendsData);
    }
    loadData();
  }, [auth]);

  return (
    <React.Fragment>
      <main>
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
      </main>
    </React.Fragment>
  );
}
