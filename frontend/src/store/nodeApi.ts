import { api } from "./emptyApi";
const injectedRtkApi = api.injectEndpoints({
  endpoints: (build) => ({
    listNodes: build.query<ListNodesApiResponse, ListNodesApiArg>({
      query: () => ({ url: `/node` }),
    }),
    createNode: build.mutation<CreateNodeApiResponse, CreateNodeApiArg>({
      query: (queryArg) => ({
        url: `/node`,
        method: "POST",
        body: queryArg.node,
      }),
    }),
    getNodeById: build.query<GetNodeByIdApiResponse, GetNodeByIdApiArg>({
      query: (queryArg) => ({ url: `/node/${queryArg.nodeId}` }),
    }),
    updateNode: build.mutation<UpdateNodeApiResponse, UpdateNodeApiArg>({
      query: (queryArg) => ({
        url: `/node/${queryArg.nodeId}`,
        method: "PUT",
        body: queryArg.node,
      }),
    }),
    deleteNodeById: build.mutation<
      DeleteNodeByIdApiResponse,
      DeleteNodeByIdApiArg
    >({
      query: (queryArg) => ({
        url: `/node/${queryArg.nodeId}`,
        method: "DELETE",
      }),
    }),
  }),
  overrideExisting: false,
});
export { injectedRtkApi as enhancedApi };
export type ListNodesApiResponse = /** status 200 A array of nodes */ Node[];
export type ListNodesApiArg = void;
export type CreateNodeApiResponse =
  /** status 201 Expected response to a valid request */ Node;
export type CreateNodeApiArg = {
  node: Node;
};
export type GetNodeByIdApiResponse =
  /** status 200 Expected response to a valid request */ Node;
export type GetNodeByIdApiArg = {
  /** The id of the node to retrieve */
  nodeId: number;
};
export type UpdateNodeApiResponse =
  /** status 200 Expected response to a valid request */ Node;
export type UpdateNodeApiArg = {
  /** The id of the node to retrieve */
  nodeId: number;
  node: Node;
};
export type DeleteNodeByIdApiResponse = /** status 204 Deleted */ Information;
export type DeleteNodeByIdApiArg = {
  /** The id of the node to retrieve */
  nodeId: number;
};
export type EditorNode = {
  PosX: number;
  PosY: number;
};
export type Node = {
  ID: number;
  Type: string;
  TrendID?: number | null;
  Name?: string;
  EditorParams?: EditorNode;
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
export const {
  useListNodesQuery,
  useCreateNodeMutation,
  useGetNodeByIdQuery,
  useUpdateNodeMutation,
  useDeleteNodeByIdMutation,
} = injectedRtkApi;
