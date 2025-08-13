import {
  DrawerItem,
  DrawerItemProps,
  DrawerSelectEvent,
} from "@progress/kendo-react-layout";
import {
  chartLineIcon,
  chevronDownIcon,
  chevronRightIcon,
  dropletIcon,
  homeIcon,
  kpiStatusOpenIcon,
  lockIcon,
  planIcon,
  unlockIcon,
  wrenchIcon,
} from "@progress/kendo-svg-icons";
import React from "react";
import { useTranslation } from "react-i18next";
import { Route, Routes, useLocation, useNavigate } from "react-router-dom";
import { AuthContext, AuthContextProvider } from "../../contexts/authContext";
import {
  DrawerRouterContainer,
  DrawerRouterItemProps,
} from "onyks_shared_kendo";
import KendoLocalizationWrapper from "../../components/KendoLocalizationWrapper";
import TrendsPage from "./features/trends_page/TrendsPage";
import TrendConfigurationPage from "./features/trends_configuration/TrendConfigurationPage";
import LeakProbabilityPage from "./features/LeakProbabilityPage";
import EventsPage from "./features/EventsPage";
import HomePage from "./features/HomePage";
import { Button } from "@progress/kendo-react-buttons";
import "../../styles/features/lds/lds.scss";
import { SwitchChangeEvent } from "@progress/kendo-react-inputs";
import { NavbarContext } from "../../contexts/navbarContext";
import { LDSContextProvider } from "./contexts/ldsContext";
import {
  Trend,
  TrendApi,
  TrendDefApi,
  TrendDefBase,
  TrendGroup,
  TrendGroupApi,
  Unit,
  UnitApi,
} from "../../services/api";
import { axiosInstance, host } from "../../lib/apiUtilities";
import { useRefreshableRequest } from "../../hooks/useRefreshableRequest";
import { error } from "console";
import {
  mockupTrendDefs,
  mockupTrendGroups,
  mockupTrends,
  mockupUnits,
} from "../../data/mockup-data";
import { Loader } from "@progress/kendo-react-indicators";

export default function LDS() {
  const { t } = useTranslation(["common", "titles", "nav", "kendo"]);
  const { pathname } = useLocation();
  const navigate = useNavigate();
  const nav = React.useContext(NavbarContext);

  // Building drawer router components (that why inside component)
  const [routerItems, setRouterItems] = React.useState<DrawerRouterItemProps[]>(
    [
      {
        id: 1,
        text: t("nav:home"),
        svgIcon: homeIcon,
        selected: pathname == "/",
        route: "/",
      },
      {
        separator: true,
      },
      {
        id: 2,
        text: t("nav:trends"),
        svgIcon: chartLineIcon,
        selected: pathname == "/trends",
        route: "/trends",
      },
      {
        separator: true,
      },
      {
        id: 3,
        text: t("nav:trend_configuration"),
        svgIcon: wrenchIcon,
        selected: pathname == "/trend-configuration",
        route: "/trend-configuration",
      },
      {
        separator: true,
      },
      {
        text: t("nav:leak_probability_map"),
        svgIcon: dropletIcon,
        selected: pathname == "/leak-probability-map",
        route: "/leak-probability-map",
      },
      {
        separator: true,
      },
      {
        id: 5,
        text: t("nav:events"),
        svgIcon: planIcon,
        selected: pathname == "/events",
        route: "/events",
      },
      {
        separator: true,
      },
    ]
  );

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

  const [isMenuPinned, setIsMenuPinned] = React.useState<boolean>(true);
  const toggleMenuPinned = React.useCallback(() => {
    setIsMenuPinned(!isMenuPinned);
  }, [isMenuPinned]);

  const setTitleOnDrawerSelect = React.useCallback(
    (event: DrawerSelectEvent) => {
      nav.setTitle(event.itemTarget.props.text ?? t("titles:missing_title"));
    },
    [nav]
  );

  // LDS context and data loading
  const auth = React.useContext(AuthContext);
  const refreshableRequest = useRefreshableRequest();

  const trendDefApi = React.useMemo(
    () => new TrendDefApi(auth?.config, host, axiosInstance),
    [auth]
  );
  const trendGroupApi = React.useMemo(
    () => new TrendGroupApi(auth?.config, host, axiosInstance),
    [auth]
  );
  const unitApi = React.useMemo(
    () => new UnitApi(auth?.config, host, axiosInstance),
    [auth]
  );
  const trendApi = React.useMemo(
    () => new TrendApi(auth?.config, host, axiosInstance),
    [auth]
  );

  const [trendDefs, setTrendDefs] = React.useState<TrendDefBase[]>(
    nav.useMockup ? mockupTrendDefs : []
  );
  const [trendGroups, setTrendGroups] = React.useState<TrendGroup[]>(
    nav.useMockup ? mockupTrendGroups : []
  );
  const [units, setUnits] = React.useState<Unit[]>(
    nav.useMockup ? mockupUnits : []
  );
  const [trends, setTrends] = React.useState<Trend[]>(
    nav.useMockup ? mockupTrends : []
  );

  React.useEffect(() => {
    setTrendDefs(nav.useMockup ? mockupTrendDefs : []);
    setTrendGroups(nav.useMockup ? mockupTrendGroups : []);
    setUnits(nav.useMockup ? mockupUnits : []);
    setTrends(nav.useMockup ? mockupTrends : []);
  }, [nav.useMockup]);

  const LoadData = React.useCallback(async () => {
    //maybe split into separate function to avoid .then() mess
    refreshableRequest(trendDefApi.listTrendDefsTrendDefGet.bind(trendDefApi))
      .then((response) => {
        console.log(response);
        if (response?.data) setTrendDefs(response?.data.items);
      })
      .catch((error) => {
        console.log(error);
      });

    refreshableRequest(
      trendGroupApi.listTrendGroupsTrendGroupGet.bind(trendGroupApi)
    )
      .then((response) => {
        console.log(response);
        if (response?.data) setTrendGroups(response?.data.items);
      })
      .catch((error) => {
        console.log(error);
      });

    refreshableRequest(unitApi.listUnitsUnitGet.bind(unitApi))
      .then((response) => {
        console.log(response);
        if (response?.data) setUnits(response?.data.items);
      })
      .catch((error) => {
        console.log(error);
      });

    refreshableRequest(trendApi.listTrendsTrendGet.bind(trendApi))
      .then((response) => {
        console.log(response);
        if (response?.data) setTrends(response?.data.items);
      })
      .catch((error) => {
        console.log(error);
      });
  }, [trendDefApi, trendGroupApi, unitApi, trendApi]);
  React.useEffect(() => {
    if (!nav.useMockup) LoadData();
  }, []);

  const isLoadingContext = React.useMemo(
    () =>
      trendDefs.length == 0 ||
      trendGroups.length == 0 ||
      units.length == 0 ||
      trends.length == 0,
    [trendDefs, trendGroups, units, trends]
  );

  return (
    <React.Fragment>
      <DrawerRouterContainer
        items={routerItems}
        navigate={navigate}
        expandOnHover={!isMenuPinned}
        expanded={true}
        position="start"
        mode="push"
        mini
        width={260}
        onSelect={setTitleOnDrawerSelect}
      >
        {!isLoadingContext ? (
          <KendoLocalizationWrapper>
            <LDSContextProvider
              trendDefs={trendDefs}
              trendGroupApi={trendGroupApi}
              trendGroups={trendGroups}
              setTrendGroups={setTrendGroups}
              unitApi={unitApi}
              units={units}
              setUnits={setUnits}
              trendApi={trendApi}
              trends={trends}
              setTrends={setTrends}
            >
              <Routes>
                <Route path="/" element={<HomePage key={"home-page"} />} />
                <Route
                  path="/trends"
                  element={<TrendsPage key={"trends-page"} />}
                />
                <Route
                  path="/trend-configuration"
                  element={<TrendConfigurationPage />}
                />
                <Route
                  path="/leak-probability-map"
                  element={<LeakProbabilityPage />}
                />
                <Route path="/events" element={<EventsPage />} />
              </Routes>
            </LDSContextProvider>
          </KendoLocalizationWrapper>
        ) : (
          <div className="content-loader">
            <Loader
              style={{
                position: "absolute",
                top: "50%",
                left: "50%",
                translate: "-50% -50%",
              }}
              size="large"
              type={"infinite-spinner"}
            />
          </div>
        )}
      </DrawerRouterContainer>
      <Button
        className="router-lock-button"
        svgIcon={isMenuPinned ? lockIcon : unlockIcon}
        onClick={toggleMenuPinned}
      />
    </React.Fragment>
  );
}
