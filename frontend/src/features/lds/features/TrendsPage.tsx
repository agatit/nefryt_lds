import React from "react";
import { AuthContext } from "../../../contexts/authContext";
import {
  Configuration,
  PageTrend,
  Trend,
  TrendApi,
  TrendApiFactory,
} from "../../../services/api";
import { useRefreshableRequest } from "../../../hooks/useRefreshableRequest";
import { axiosInstance, host } from "../../../lib/apiUtilities";

export default function TrendsPage() {
  const auth = React.useContext(AuthContext);
  const refreshableRequest = useRefreshableRequest();
  const trendApi = React.useMemo(() => {
    return new TrendApi(auth?.config, host, axiosInstance);
  }, [auth]);

  const [trends, setTrends] = React.useState<Trend[]>([]);

  React.useEffect(() => {
    async function loadData() {
      const trendsListResponse = await refreshableRequest<PageTrend>(
        trendApi.listTrendsTrendGet.bind(trendApi)
      );
      setTrends(
        trendsListResponse?.data.items ? trendsListResponse.data.items : []
      );
    }
    loadData();
  }, [auth]);

  return <p>{trends.length}</p>;
}
