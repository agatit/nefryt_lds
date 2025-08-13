import React from "react";
import { Navigate } from "react-router-dom";
import { useCookies } from "react-cookie";
import { AuthContextProvider } from "../contexts/authContext";

export default function PrivateRoute(props: React.PropsWithChildren) {
  const [cookies, setCookie] = useCookies(["auth"]);

  if (typeof cookies.auth == "undefined") return <Navigate to="/login" />;

  return <AuthContextProvider>{props.children}</AuthContextProvider>;
}
