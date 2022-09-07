import { api } from "./emptyApi";
const injectedRtkApi = api.injectEndpoints({
  endpoints: (build) => ({
    listEvents: build.query<ListEventsApiResponse, ListEventsApiArg>({
      query: () => ({ url: `/event` }),
    }),
    getEventById: build.query<GetEventByIdApiResponse, GetEventByIdApiArg>({
      query: (queryArg) => ({ url: `/event/${queryArg.eventId}` }),
    }),
    ackEvent: build.mutation<AckEventApiResponse, AckEventApiArg>({
      query: (queryArg) => ({
        url: `/event/${queryArg.eventId}/ack`,
        method: "POST",
      }),
    }),
  }),
  overrideExisting: false,
});
export { injectedRtkApi as enhancedApi };
export type ListEventsApiResponse = /** status 200 A array of events */ Event[];
export type ListEventsApiArg = void;
export type GetEventByIdApiResponse =
  /** status 200 Expected response to a valid request */ Event;
export type GetEventByIdApiArg = {
  /** The id of the event to retrieve */
  eventId: number;
};
export type AckEventApiResponse = /** status 200 Updated */ Information;
export type AckEventApiArg = {
  /** The id of the event to retrieve */
  eventId: number;
};
export type Event = {
  ID?: number;
  EventDefID: number;
  MethodID: number;
  BeginDate: string;
  AckDate?: string;
  EndDate?: string;
  Details?: string;
  Position?: number;
  Caption?: string;
  Verbosity?: string;
  Silient?: boolean;
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
export const { useListEventsQuery, useGetEventByIdQuery, useAckEventMutation } =
  injectedRtkApi;
