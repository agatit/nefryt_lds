import React from "react";
import "./App.scss";
import Navbar from "./components/Navbar";
import { Route, Routes, useLocation } from "react-router-dom";
import { LoadingPanel } from "onyks_shared_kendo";
import { useTranslation } from "react-i18next";
import Login from "./features/auth/Login";
import LDS from "./features/lds/LDS";
import { NavbarContextProvider } from "./contexts/navbarContext";
import PrivateRoute from "./components/PrivateRoute";
import { SwitchChangeEvent } from "@progress/kendo-react-inputs";
import { AuthContextProvider } from "./contexts/authContext";
import { useCookies } from "react-cookie";
import { Fade } from "@progress/kendo-react-animation";
import {
  AppContextProvider,
  NotificationDataType,
} from "./contexts/appContext";
import {
  Notification,
  NotificationGroup,
} from "@progress/kendo-react-notification";

function App() {
  const { t } = useTranslation(["common", "titles"]);
  const { pathname } = useLocation();

  // Navbar stuff if any
  const [title, setTitle] = React.useState<string>(t("titles:" + pathname));
  const [cookies, setCookies] = useCookies(["useMockup"]);
  const [useMockup, setUseMockup] = React.useState<boolean>(() => {
    if (typeof cookies.useMockup == "undefined") {
      setCookies("useMockup", false);
      return false;
    } else {
      return cookies.useMockup;
    }
  });
  const handleUseMockupChange = React.useCallback(
    (event: SwitchChangeEvent) => {
      setUseMockup(event.value);
      setCookies("useMockup", event.value);
    },
    [],
  );

  // Notification
  const [notificationState, setNotificationState] = React.useState<{
    visible: boolean;
    notificationData: NotificationDataType;
  }>({
    visible: false,
    notificationData: {
      notificationType: { icon: true, style: "none" },
      message: "",
    },
  });
  const showNotification = React.useCallback(
    (notificationData: NotificationDataType) => {
      setNotificationState({ visible: true, notificationData });
    },
    [],
  );
  const closeNotification = React.useCallback(() => {
    setNotificationState({
      visible: false,
      notificationData: {
        notificationType: { icon: true, style: "none" },
        message: "",
      },
    });
  }, []);

  return (
    <div className="App">
      <AppContextProvider
        showNotification={showNotification}
        closeNotification={closeNotification}
      >
        <Navbar
          title={title}
          useMockup={useMockup}
          handleOnUseMockupChange={handleUseMockupChange}
        />
        <React.Suspense fallback={<LoadingPanel querySelectorString=".App" />}>
          <NavbarContextProvider setTitle={setTitle} useMockup={useMockup}>
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route
                path="/*"
                element={
                  <PrivateRoute>
                    <LDS />
                  </PrivateRoute>
                }
              />
            </Routes>
          </NavbarContextProvider>
        </React.Suspense>
      </AppContextProvider>
      <Fade style={{ position: "fixed", right: "1%", bottom: "1%" }}>
        {notificationState.visible && (
          <Notification
            type={notificationState.notificationData.notificationType}
            closable={true}
            onClose={closeNotification}
          >
            <span>{notificationState.notificationData.message}</span>
          </Notification>
        )}
      </Fade>
    </div>
  );
}

export default App;
