import { AxiosResponse, AxiosError } from "axios";
import { AuthContext } from "../contexts/authContext";
import React from "react";

export function useRefreshableRequest() {
  const auth = React.useContext(AuthContext);

  async function refreshableRequest<T, Args extends any[]>(
    request: (...args: Args) => Promise<AxiosResponse<T>>,
    ...args: Args
  ) {
    try {
      const response = await request(...args);
      return response;
    } catch (err: any) {
      if (err.status == 401) {
        await auth?.refreshAccess();
      }
    }
  }
  return refreshableRequest;
}
