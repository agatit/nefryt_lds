import React from "react";
import "./App.scss";
import Navbar from "./layouts/Navbar";
import { Route, Routes, useLocation, useNavigate } from "react-router-dom";
import { DrawerRouterContainer, LoadingPanel } from "onyks_shared_kendo";
import KendoLocalizationWrapper from "./components/KendoLocalizationWrapper";
import { useTranslation } from "react-i18next";
import { DrawerItemProps } from "@progress/kendo-react-layout";
import { homeIcon, kpiStatusOpenIcon } from "@progress/kendo-svg-icons";
import { NavbarContextProvider } from "./contexts/navbarContext";
import PrivateRoute from "./components/PrivateRoute";
import Login from "./features/auth/login";
import HomePage from "./features/lds/HomePage";
import TrendsPage from "./features/lds/features/TrendsPage";
import TrendConfigurationPage from "./features/lds/features/TrendConfigurationPage";
import LeakProbabilityPage from "./features/lds/features/LeakProbabilityPage";
import EventsPage from "./features/lds/features/EventsPage";
import { AuthContextProvider } from "./contexts/authContext";
import { useCookies } from "react-cookie";

function App() {
  const { t } = useTranslation(["common", "titles", "nav"]);
  const { pathname } = useLocation();
  const navigate = useNavigate();
  const [cookies, setCookie] = useCookies([
    "token",
    "permissions",
    "refreshToken",
  ]);
  const [token, setToken] = React.useState<string | null>(cookies.token);
  const [permissions, setPermissions] = React.useState<string[] | null>(
    cookies.permissions
  );

  // Navbar stuff if any
  const [title, setTitle] = React.useState<string>(t("titles:" + pathname));

  // Build drawer router components
  const [routerItems, setRouterItems] = React.useState<DrawerItemProps[]>([
    {
      text: t("nav:home"),
      svgIcon: homeIcon,
      selected: pathname == "/",
      route: "/",
    },
    {
      separator: true,
    },
    {
      text: t("nav:trends"),
      svgIcon: kpiStatusOpenIcon,
      selected: pathname == "/trends",
      route: "/trends",
    },
    {
      separator: true,
    },
    {
      text: t("nav:trend_configuration"),
      svgIcon: kpiStatusOpenIcon,
      selected: pathname == "/trend-configuration",
      route: "/trend-configuration",
    },
    {
      separator: true,
    },
    {
      text: t("nav:leak_probability_map"),
      svgIcon: kpiStatusOpenIcon,
      selected: pathname == "/leak-probability-map",
      route: "/leak-probability-map",
    },
    {
      separator: true,
    },
    {
      text: t("nav:events"),
      svgIcon: kpiStatusOpenIcon,
      selected: pathname == "/events",
      route: "/events",
    },
    {
      separator: true,
    },
  ]);

  React.useEffect(() => {
    setRouterItems(
      routerItems.map((item) => {
        return {
          ...item,
          selected:
            item.route == "/" ? pathname == "/" : pathname.includes(item.route),
        };
      })
    );
  }, [pathname]);

  return (
    <div className="App">
      <Navbar title={title} />
      <React.Suspense fallback={<LoadingPanel querySelectorString=".App" />}>
        {token ? (
          <AuthContextProvider token={token} permissions={permissions}>
            <NavbarContextProvider setTitle={setTitle}>
              <DrawerRouterContainer
                items={routerItems}
                navigate={navigate}
                expandOnHover={true}
                position="start"
                mode="push"
                mini
              >
                <KendoLocalizationWrapper>
                  <Routes>
                    {/* <Route
                      path="/login"
                      element={
                        <Login
                          setToken={setToken}
                          setPermissions={setPermissions}
                        />
                      }
                    /> */}

                    <Route
                      path="/"
                      element={
                        <PrivateRoute>
                          <HomePage />
                        </PrivateRoute>
                      }
                    />
                    <Route
                      path="/trends"
                      element={
                        <PrivateRoute>
                          <TrendsPage />
                        </PrivateRoute>
                      }
                    />
                    <Route
                      path="/trend-configuration"
                      element={
                        <PrivateRoute>
                          <TrendConfigurationPage />
                        </PrivateRoute>
                      }
                    />
                    <Route
                      path="/leak-probability-map"
                      element={
                        <PrivateRoute>
                          <LeakProbabilityPage />
                        </PrivateRoute>
                      }
                    />
                    <Route
                      path="/events"
                      element={
                        <PrivateRoute>
                          <EventsPage />
                        </PrivateRoute>
                      }
                    />
                  </Routes>
                </KendoLocalizationWrapper>
              </DrawerRouterContainer>
            </NavbarContextProvider>
          </AuthContextProvider>
        ) : (
          <Login setToken={setToken} setPermissions={setPermissions} />
        )}
      </React.Suspense>
    </div>
  );
}

export default App;
