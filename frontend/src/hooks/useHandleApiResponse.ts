import { AxiosResponse } from "axios";
import React from "react";
import { useTranslation } from "react-i18next";
import { AppContext, NotificationDataType } from "../contexts/appContext";
import { useRefreshableRequest } from "./useRefreshableRequest";

const timeToCloseNotification = 10000;
const successType: NotificationDataType["notificationType"] = {
  icon: true,
  style: "success",
};
const errorType: NotificationDataType["notificationType"] = {
  icon: true,
  style: "error",
};

export function useHandleApiResponse() {
  const { t } = useTranslation(["api"]);
  const appContext = React.useContext(AppContext);
  const refreshableRequest = useRefreshableRequest();

  const timerRef = React.useRef<NodeJS.Timeout | undefined>(undefined);

  async function handleApiResponse<T, Args extends any[]>(
    request: (...args: Args) => Promise<AxiosResponse<T>>,
    ...args: Args
  ) {
    try {
      clearTimeout(timerRef.current);
      const response = await refreshableRequest(request, ...args);
      switch (response!.config.method) {
        case "post":
          appContext.showNotification({
            notificationType: successType,
            message: t("api:element_created_successfully"),
          });
          break;
        case "put":
          appContext.showNotification({
            notificationType: successType,
            message: t("api:element_updated_successfully"),
          });
          break;
        case "delete":
          appContext.showNotification({
            notificationType: successType,
            message: t("api:element_deleted_successfully"),
          });
          break;
      }
      timerRef.current = setTimeout(() => {
        appContext.closeNotification();
      }, timeToCloseNotification);

      return response;
    } catch (err: any) {
      switch (err.status) {
        // Client errors
        case 400:
          appContext.showNotification({
            notificationType: errorType,
            message: t("api:failed_request_reload_and_try_again"),
          });
          break;
        case 403:
          appContext.showNotification({
            notificationType: errorType,
            message: t("api:failed_request_you_dont_have_permission_action"),
          });
          break;
        case 404:
          appContext.showNotification({
            notificationType: errorType,
            message: t("api:failed_request_something_went_wrong"),
          });
          break;
        case 418:
          appContext.showNotification({
            notificationType: { icon: true, style: "warning" },
            message: t("api:server_is_teapot_you_little_dum_dum"),
          });
          break;
        // Server errors
        case 500:
          appContext.showNotification({
            notificationType: errorType,
            message: t("api:failed_request_internal_server_error"),
          });
          break;
        case 503:
          appContext.showNotification({
            notificationType: errorType,
            message: t("api:failed_request_server_is_not_responding"),
          });
          break;
        default:
          appContext.showNotification({
            notificationType: errorType,
            message: t("api:encountered_unknown_error_while_fetching_data"),
          });
          break;
      }

      console.log(err);
      timerRef.current = setTimeout(() => {
        appContext.closeNotification();
      }, timeToCloseNotification);

      return;
    }
  }
  return handleApiResponse;
}
