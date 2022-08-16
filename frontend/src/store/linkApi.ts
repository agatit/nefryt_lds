import { api } from "./emptyApi";
const injectedRtkApi = api.injectEndpoints({
  endpoints: (build) => ({
    listLinks: build.query<ListLinksApiResponse, ListLinksApiArg>({
      query: () => ({ url: `/link` }),
    }),
    createLink: build.mutation<CreateLinkApiResponse, CreateLinkApiArg>({
      query: (queryArg) => ({
        url: `/link`,
        method: "POST",
        body: queryArg.link,
      }),
    }),
    getLinkById: build.query<GetLinkByIdApiResponse, GetLinkByIdApiArg>({
      query: (queryArg) => ({ url: `/link/${queryArg.linkId}` }),
    }),
    updateLink: build.mutation<UpdateLinkApiResponse, UpdateLinkApiArg>({
      query: (queryArg) => ({
        url: `/link/${queryArg.linkId}`,
        method: "PUT",
        body: queryArg.link,
      }),
    }),
    deleteLinkById: build.mutation<
      DeleteLinkByIdApiResponse,
      DeleteLinkByIdApiArg
    >({
      query: (queryArg) => ({
        url: `/link/${queryArg.linkId}`,
        method: "DELETE",
      }),
    }),
  }),
  overrideExisting: false,
});
export { injectedRtkApi as enhancedApi };
export type ListLinksApiResponse = /** status 200 A array of links */ Link[];
export type ListLinksApiArg = void;
export type CreateLinkApiResponse =
  /** status 201 Expected response to a valid request */ Link;
export type CreateLinkApiArg = {
  link: Link;
};
export type GetLinkByIdApiResponse =
  /** status 200 Expected response to a valid request */ Link;
export type GetLinkByIdApiArg = {
  /** The id of the link to retrieve */
  linkId: number;
};
export type UpdateLinkApiResponse =
  /** status 200 Expected response to a valid request */ Link;
export type UpdateLinkApiArg = {
  /** The id of the link to retrieve */
  linkId: number;
  link: Link;
};
export type DeleteLinkByIdApiResponse = /** status 204 Deleted */ Information;
export type DeleteLinkByIdApiArg = {
  /** The id of the link to retrieve */
  linkId: number;
};
export type Link = {
  ID: number;
  BeginNodeID?: number;
  EndNodeID?: number;
  Length?: number;
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
  useListLinksQuery,
  useCreateLinkMutation,
  useGetLinkByIdQuery,
  useUpdateLinkMutation,
  useDeleteLinkByIdMutation,
} = injectedRtkApi;
