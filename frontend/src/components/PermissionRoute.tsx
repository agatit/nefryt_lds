import React from "react";
import { Navigate } from "react-router-dom";
import { AuthContext } from "../contexts/authContext";

export interface PermissionRouteProps extends React.PropsWithChildren {
  requiredPermission: string;
  fallbackRoute: string;
}

export default function PermissionRoute(props: PermissionRouteProps) {
  const auth = React.useContext(AuthContext);

  if (!auth?.data.permissions?.includes(props.requiredPermission))
    return <Navigate to={props.fallbackRoute} />;

  return props.children;
}
