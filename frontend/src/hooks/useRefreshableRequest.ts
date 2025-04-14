import { AxiosResponse, AxiosError } from "axios";
import { AuthContext } from "../contexts/authContext";
import React from "react";

export function useRefreshableRequest() {
  const auth = React.useContext(AuthContext);

  async function refreshableRequest<T>(
    request: () => Promise<AxiosResponse<T>>
  ) {
    try {
      const response = await request();
      return response;
    } catch (err: any) {
      if (err.status == 401) {
        await auth?.refreshAccess();
      }
    }
  }
  return refreshableRequest;
}
