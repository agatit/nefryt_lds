import { api } from "./emptyApi";
const injectedRtkApi = api.injectEndpoints({
  endpoints: (build) => ({
    listTrends: build.query<ListTrendsApiResponse, ListTrendsApiArg>({
      query: (queryArg) => ({
        url: `/trend`,
        params: { $filter: queryArg.$filter },
      }),
    }),
    createTrend: build.mutation<CreateTrendApiResponse, CreateTrendApiArg>({
      query: (queryArg) => ({
        url: `/trend`,
        method: "POST",
        body: queryArg.trend,
      }),
    }),
    getTrendById: build.query<GetTrendByIdApiResponse, GetTrendByIdApiArg>({
      query: (queryArg) => ({ url: `/trend/${queryArg.trendId}` }),
    }),
    updateTrend: build.mutation<UpdateTrendApiResponse, UpdateTrendApiArg>({
      query: (queryArg) => ({
        url: `/trend/${queryArg.trendId}`,
        method: "PUT",
        body: queryArg.trend,
      }),
    }),
    deleteTrendById: build.mutation<
      DeleteTrendByIdApiResponse,
      DeleteTrendByIdApiArg
    >({
      query: (queryArg) => ({
        url: `/trend/${queryArg.trendId}`,
        method: "DELETE",
      }),
    }),
    listTrendParams: build.query<
      ListTrendParamsApiResponse,
      ListTrendParamsApiArg
    >({
      query: (queryArg) => ({
        url: `/trend/${queryArg.trendId}/param`,
        params: { $filter: queryArg.$filter },
      }),
    }),
    getTrendParamById: build.query<
      GetTrendParamByIdApiResponse,
      GetTrendParamByIdApiArg
    >({
      query: (queryArg) => ({
        url: `/trend/${queryArg.trendId}/param/${queryArg.trendParamDefId}`,
      }),
    }),
    updateTrendParam: build.mutation<
      UpdateTrendParamApiResponse,
      UpdateTrendParamApiArg
    >({
      query: (queryArg) => ({
        url: `/trend/${queryArg.trendId}/param/${queryArg.trendParamDefId}`,
        method: "PUT",
        body: queryArg.trendParam,
      }),
    }),
    getTrendData: build.query<GetTrendDataApiResponse, GetTrendDataApiArg>({
      query: (queryArg) => ({
        url: `/trend/${queryArg.trendIdList}/data/${queryArg.begin}/${queryArg.end}/${queryArg.samples}`,
      }),
    }),
    getTrendCurrentData: build.query<
      GetTrendCurrentDataApiResponse,
      GetTrendCurrentDataApiArg
    >({
      query: (queryArg) => ({
        url: `/trend/${queryArg.trendIdList}/current_data/${queryArg.period}/${queryArg.samples}`,
      }),
    }),
    listTrendDefs: build.query<ListTrendDefsApiResponse, ListTrendDefsApiArg>({
      query: (queryArg) => ({
        url: `/trend_def`,
        params: { $filter: queryArg.$filter },
      }),
    }),
  }),
  overrideExisting: false,
});
export { injectedRtkApi as enhancedApi };
export type ListTrendsApiResponse = /** status 200 A array of trends */ Trend[];
export type ListTrendsApiArg = {
  /** Query filter in OData standard */
  $filter?: string;
};
export type CreateTrendApiResponse =
  /** status 201 Expected response to a valid request */ Trend;
export type CreateTrendApiArg = {
  trend: Trend;
};
export type GetTrendByIdApiResponse =
  /** status 200 Expected response to a valid request */ Trend;
export type GetTrendByIdApiArg = {
  /** The id of the trend to retrieve */
  trendId: number;
};
export type UpdateTrendApiResponse =
  /** status 200 Expected response to a valid request */ Trend;
export type UpdateTrendApiArg = {
  /** The id of the trend to retrieve */
  trendId: number;
  trend: Trend;
};
export type DeleteTrendByIdApiResponse = /** status 204 Deleted */ Information;
export type DeleteTrendByIdApiArg = {
  /** The id of the trend to retrieve */
  trendId: number;
};
export type ListTrendParamsApiResponse =
  /** status 200 A array of params */ TrendParam[];
export type ListTrendParamsApiArg = {
  /** Query filter in OData standard */
  $filter?: string;
  /** The id of the trend to retrieve */
  trendId: number;
};
export type GetTrendParamByIdApiResponse =
  /** status 200 Expected response to a valid request */ TrendParam;
export type GetTrendParamByIdApiArg = {
  /** The id of the trend to retrieve */
  trendId: number;
  /** The id of the param to retrieve */
  trendParamDefId: string;
};
export type UpdateTrendParamApiResponse =
  /** status 200 Expected response to a valid request */ TrendParam;
export type UpdateTrendParamApiArg = {
  /** The id of the trend to retrieve */
  trendId: number;
  /** The id of the param to retrieve */
  trendParamDefId: string;
  trendParam: TrendParam;
};
export type GetTrendDataApiResponse =
  /** status 200 A array of trend data */ TrendData[];
export type GetTrendDataApiArg = {
  /** Lost of ids of the trend to retrieve */
  trendIdList: number[];
  /** start of date to take from data (timestamp UTC) */
  begin: number;
  /** end of date to take from data (timestamp UTC) */
  end: number;
  /** number of data samples to take (resolution) */
  samples: number;
};
export type GetTrendCurrentDataApiResponse =
  /** status 200 A array of trend data */ TrendData[];
export type GetTrendCurrentDataApiArg = {
  /** Lost of ids of the trend to retrieve */
  trendIdList: number[];
  /** period of data to take since currnet time (timestamp UTC) */
  period: number;
  /** number of data samples to take (resolution) */
  samples: number;
};
export type ListTrendDefsApiResponse =
  /** status 200 A array of trend defs */ TrendDef[];
export type ListTrendDefsApiArg = {
  /** Query filter in OData standard */
  $filter?: string;
};
export type Trend = {
  ID?: number;
  Name?: string;
  TrendGroupID?: number;
  TrendDefID: string;
  NodeID?: number;
  TimeExponent?: number;
  Format?: string;
  Unit?: string;
  Color?: string;
  Symbol?: string;
  RawMin: number;
  RawMax: number;
  ScaledMin: number;
  ScaledMax: number;
};
export type Error = {
  code: number;
  message: string;
};
export type Information = {
  status: number;
  affected: number;
  message: string | null;
};
export type TrendParam = {
  TrendID: number;
  TrendParamDefID: string;
  Name?: string;
  DataType?: string;
  Value: string;
};
export type TrendData = {
  Timestamp: number;
  TimestampMs: number;
  [key: string]: number;
};
export type TrendDef = {
  ID: string;
  Name: string;
};
export const {
  useListTrendsQuery,
  useCreateTrendMutation,
  useGetTrendByIdQuery,
  useUpdateTrendMutation,
  useDeleteTrendByIdMutation,
  useListTrendParamsQuery,
  useGetTrendParamByIdQuery,
  useUpdateTrendParamMutation,
  useGetTrendDataQuery,
  useGetTrendCurrentDataQuery,
  useListTrendDefsQuery,
} = injectedRtkApi;
