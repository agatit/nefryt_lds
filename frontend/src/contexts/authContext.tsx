import React, { PropsWithChildren } from "react";
import { AuthApi, Configuration, LoginPermissions } from "../services/api";
import { axiosInstance, host } from "../lib/apiUtilities";
import { AxiosResponse } from "axios";
import { useCookies } from "react-cookie";
import { useNavigate } from "react-router-dom";

export type AuthContextType = {
  data: LoginPermissions;
  setAuth: (newAuth: LoginPermissions) => void;
  refreshAccess: () => void;
  config: Configuration;
};

export const AuthContext = React.createContext<AuthContextType | null>(null);

export const AuthContextProvider = (props: PropsWithChildren) => {
  const [cookies, setCookie, removeCookie] = useCookies(["auth"]);
  if (typeof cookies.auth == "undefined")
    throw new TypeError("Auth cookie is undefined");
  const [auth, setAuth] = React.useState<LoginPermissions>(cookies.auth);
  const [config, setConfig] = React.useState<Configuration>(
    new Configuration({ accessToken: cookies.auth.token })
  );

  const navigate = useNavigate();

  async function refreshAccess() {
    if (
      new Date(auth.refreshTokenExpiration).getTime() < new Date().getTime()
    ) {
      removeCookie("auth", { path: "/" }); //if refresh token expired remove auth cookie in order to redirect to login page
      navigate("/login");
      location.reload();
      return;
    }
    const authApi = new AuthApi(
      new Configuration({ accessToken: auth.refreshToken }),
      host,
      axiosInstance
    );
    const response = await authApi.authRefreshAuthRefreshPost();
    setAuth(response.data);
    setConfig(new Configuration({ accessToken: response.data.token }));
    setCookie("auth", JSON.stringify(response.data));
    location.reload();
  }

  return (
    <AuthContext.Provider
      value={{ data: auth, setAuth, refreshAccess, config }}
    >
      {props.children}
    </AuthContext.Provider>
  );
};
