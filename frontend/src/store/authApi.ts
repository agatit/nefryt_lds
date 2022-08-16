import { api } from "./emptyApi";
const injectedRtkApi = api.injectEndpoints({
  endpoints: (build) => ({
    authLogin: build.mutation<AuthLoginApiResponse, AuthLoginApiArg>({
      query: (queryArg) => ({
        url: `/auth/login`,
        method: "POST",
        body: queryArg.login,
      }),
    }),
    authRefresh: build.mutation<AuthRefreshApiResponse, AuthRefreshApiArg>({
      query: () => ({ url: `/auth/refresh`, method: "POST" }),
    }),
  }),
  overrideExisting: false,
});
export { injectedRtkApi as enhancedApi };
export type AuthLoginApiResponse = /** status 200 OK */ LoginPermissions;
export type AuthLoginApiArg = {
  login: Login;
};
export type AuthRefreshApiResponse = /** status 200 OK */ LoginPermissions;
export type AuthRefreshApiArg = void;
export type LoginPermissions = {
  username?: string;
  success?: boolean;
  token: string;
  refreshToken: string;
  refreshTokenExpiration: string;
  permissions?: {
    [key: string]: any;
  }[];
};
export type Login = {
  username: string;
  password: string;
  deviceId?: string;
  deviceName?: string;
};
export const { useAuthLoginMutation, useAuthRefreshMutation } = injectedRtkApi;
