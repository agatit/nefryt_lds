import React from "react";
import { Navigate } from "react-router-dom";
import { AuthContext } from "../contexts/authContext";

export default function PrivateRoute(props: React.PropsWithChildren) {
  const auth = React.useContext(AuthContext);

  console.log(auth?.permissions);

  if (auth?.getToken() == null) return <Navigate to="/login" />;

  return props.children;
}
