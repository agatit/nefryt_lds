import { api } from "./emptyApi";
const injectedRtkApi = api.injectEndpoints({
  endpoints: (build) => ({
    listPipelines: build.query<ListPipelinesApiResponse, ListPipelinesApiArg>({
      query: (queryArg) => ({
        url: `/pipeline`,
        params: { $filter: queryArg.$filter },
      }),
    }),
    createPipeline: build.mutation<
      CreatePipelineApiResponse,
      CreatePipelineApiArg
    >({
      query: (queryArg) => ({
        url: `/pipeline`,
        method: "POST",
        body: queryArg.pipeline,
      }),
    }),
    getPipelineById: build.query<
      GetPipelineByIdApiResponse,
      GetPipelineByIdApiArg
    >({
      query: (queryArg) => ({ url: `/pipeline/${queryArg.pipelineId}` }),
    }),
    updatePipeline: build.mutation<
      UpdatePipelineApiResponse,
      UpdatePipelineApiArg
    >({
      query: (queryArg) => ({
        url: `/pipeline/${queryArg.pipelineId}`,
        method: "PUT",
        body: queryArg.pipeline,
      }),
    }),
    deletePipelineById: build.mutation<
      DeletePipelineByIdApiResponse,
      DeletePipelineByIdApiArg
    >({
      query: (queryArg) => ({
        url: `/pipeline/${queryArg.pipelineId}`,
        method: "DELETE",
      }),
    }),
    listPipelineParams: build.query<
      ListPipelineParamsApiResponse,
      ListPipelineParamsApiArg
    >({
      query: (queryArg) => ({
        url: `/pipeline/${queryArg.pipelineId}/param`,
        params: { $filter: queryArg.$filter },
      }),
    }),
    updatePipelineParam: build.mutation<
      UpdatePipelineParamApiResponse,
      UpdatePipelineParamApiArg
    >({
      query: (queryArg) => ({
        url: `/pipeline/${queryArg.pipelineId}/param/${queryArg.pipelineParamDefId}`,
        method: "PUT",
        body: queryArg.body,
      }),
    }),
  }),
  overrideExisting: false,
});
export { injectedRtkApi as enhancedApi };
export type ListPipelinesApiResponse =
  /** status 200 A array of pipelines */ Pipeline[];
export type ListPipelinesApiArg = {
  /** Query filter in OData standard */
  $filter?: string;
};
export type CreatePipelineApiResponse =
  /** status 201 Expected response to a valid request */ Pipeline;
export type CreatePipelineApiArg = {
  pipeline: Pipeline;
};
export type GetPipelineByIdApiResponse =
  /** status 200 Expected response to a valid request */ Pipeline;
export type GetPipelineByIdApiArg = {
  /** The id of the pipeline to retrieve */
  pipelineId: number;
};
export type UpdatePipelineApiResponse =
  /** status 200 Expected response to a valid request */ Pipeline;
export type UpdatePipelineApiArg = {
  /** The id of the pipeline to retrieve */
  pipelineId: number;
  pipeline: Pipeline;
};
export type DeletePipelineByIdApiResponse =
  /** status 204 Deleted */ Information;
export type DeletePipelineByIdApiArg = {
  /** The id of the pipeline to retrieve */
  pipelineId: number;
};
export type ListPipelineParamsApiResponse =
  /** status 200 A array of  pipelines params */ PipelineParam[];
export type ListPipelineParamsApiArg = {
  /** Query filter in OData standard */
  $filter?: string;
  /** The id of the pipeline to retrieve */
  pipelineId: number;
};
export type UpdatePipelineParamApiResponse =
  /** status 201 Updated */ Information;
export type UpdatePipelineParamApiArg = {
  /** The id of the pipeline to retrieve */
  pipelineId: number;
  /** The id of the param to retrieve */
  pipelineParamDefId: string;
  body: PipelineParam[];
};
export type EditorPipeline = {
  AreaWidth: number;
  AreaHeight: number;
  AreaWidthDivision: number;
  AreaHeightDivision: number;
};
export type Pipeline = {
  ID?: number;
  Name?: string;
  BeginPos?: number;
  EditorParams?: EditorPipeline;
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
export type PipelineParam = {
  PipelineID: number;
  PipelineParamDefID?: number;
  DataType?: string;
  Name?: string;
  Value?: string;
};
export const {
  useListPipelinesQuery,
  useCreatePipelineMutation,
  useGetPipelineByIdQuery,
  useUpdatePipelineMutation,
  useDeletePipelineByIdMutation,
  useListPipelineParamsQuery,
  useUpdatePipelineParamMutation,
} = injectedRtkApi;
