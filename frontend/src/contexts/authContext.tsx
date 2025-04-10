import React, { PropsWithChildren } from "react";
import { AuthApi, Configuration, LoginPermissions } from "../services/api";
import { axiosInstance, host } from "../lib/apiUtilities";
import { AxiosResponse } from "axios";

export type AuthContextType = {
  getToken: () => string | null;
  permissions: string[] | null;
  refreshAccess: (refreshToken: string) => Promise<void>;
  getConfig: () => Configuration;
};

export const AuthContext = React.createContext<AuthContextType | null>(null);

interface AuthContextProviderProps extends PropsWithChildren {
  token: string | null;
  permissions: string[] | null;
}

export const AuthContextProvider = (props: AuthContextProviderProps) => {
  const tokenRef = React.useRef<string | null>(props.token);
  const [permissions, setPermissions] = React.useState<string[] | null>(
    props.permissions
  );
  const configRef = React.useRef<Configuration>(
    new Configuration({ accessToken: props.token ? props.token : undefined })
  );

  async function refreshAccess(refreshToken: string) {
    new AuthApi(
      new Configuration({ accessToken: refreshToken }),
      host,
      axiosInstance
    )
      .authRefreshAuthRefreshPost()
      .then((response: AxiosResponse<LoginPermissions>) => {
        if (response.data.permissions)
          setPermissions(response.data.permissions);
        configRef.current = new Configuration({
          accessToken: response.data.token,
        });
      });
  }

  function getConfig(): Configuration {
    return configRef.current;
  }

  function getToken(): string | null {
    return tokenRef.current;
  }

  return (
    <AuthContext.Provider
      value={{ getToken, permissions, refreshAccess, getConfig }}
    >
      {props.children}
    </AuthContext.Provider>
  );
};
