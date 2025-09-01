import {
  DrawerItem,
  DrawerItemProps,
  DrawerSelectEvent,
} from "@progress/kendo-react-layout";
import {
  chartLineIcon,
  chartLineStackedMarkersIcon,
  chevronDownIcon,
  chevronRightIcon,
  dropletIcon,
  graphIcon,
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
import TrendsPage from "./features/trends/TrendsPage";
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
  TrendDef,
  TrendGroup,
  TrendGroupApi,
  Unit,
  UnitApi,
} from "../../services/api";
import { axiosInstance, host } from "../../lib/apiUtilities";
import {
  mockupTrendDefs,
  mockupTrendGroups,
  mockupTrendParamDefs,
  MockupTrendParamDefType,
  mockupTrends,
  mockupUnits,
} from "../../data/mockup-data";
import { Loader } from "@progress/kendo-react-indicators";
import { useHandleApiResponse } from "../../hooks/useHandleApiResponse";
import TrendsCurrentPage from "./features/trends/TrendsCurrentPage";
import SimulatorPage from "./features/simulator/SimulatorPage";

export default function LDS() {
  const { t } = useTranslation(["common", "titles", "nav", "kendo"]);
  const { pathname } = useLocation();
  const navigate = useNavigate();
  const nav = React.useContext(NavbarContext);

  // Building drawer router components (that why inside component)
  const [routerItems, setRouterItems] = React.useState<DrawerRouterItemProps[]>(
    [
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
        text: t("nav:trends_current_readings"),
        svgIcon: graphIcon,
        selected: pathname == "/trends-current",
        route: "/trends-current",
      },
      {
        separator: true,
      },
      {
        text: t("nav:trends"),
        svgIcon: chartLineIcon,
        selected: pathname == "/trends",
        route: "/trends",
      },
      {
        separator: true,
      },
      {
        text: t("nav:simulator"),
        svgIcon: chartLineStackedMarkersIcon,
        selected: pathname == "/simulator",
        route: "/simulator",
      },
      {
        separator: true,
      },
      {
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
  const handleApiResponse = useHandleApiResponse();

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

  const [trendDefs, setTrendDefs] = React.useState<TrendDef[]>(
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
  const [trendParamDefs, setTrendParamDefs] =
    React.useState<MockupTrendParamDefType[]>(mockupTrendParamDefs);

  React.useEffect(() => {
    setTrendDefs(nav.useMockup ? mockupTrendDefs : []);
    setTrendGroups(nav.useMockup ? mockupTrendGroups : []);
    setUnits(nav.useMockup ? mockupUnits : []);
    setTrends(nav.useMockup ? mockupTrends : []);
    setTrendParamDefs(mockupTrendParamDefs);
  }, [nav.useMockup]);

  const addTrend = React.useCallback(
    async (value: Trend) => {
      if (nav.useMockup) {
        setTrends([...trends, value]);
        return;
      }

      try {
        const response = await handleApiResponse(
          trendApi.createTrendTrendPost.bind(trendApi),
          value
        );
        console.log(response);
        if (response?.data) setTrends([...trends, response.data]);
      } catch (error) {
        console.log(error);
      }
    },
    [nav, trends, trendApi]
  );

  const updateTrend = React.useCallback(
    async (value: Trend) => {
      if (nav.useMockup) {
        setTrends(
          trends.map((trend) => {
            if (trend.ID == value.ID) return value;
            return trend;
          })
        );
        return;
      }

      const { ID, ...updateTrend } = value;
      try {
        const response = await handleApiResponse(
          trendApi.updateTrendTrendTrendIdPut.bind(trendApi),
          ID,
          updateTrend
        );
        console.log(response);
        if (response?.data)
          setTrends(
            trends.map((trend) => {
              if (trend.ID == response.data.ID) return response.data;
              return trend;
            })
          );
      } catch (error) {
        console.log(error);
      }
    },
    [nav, trends, trendApi]
  );

  const deleteTrend = React.useCallback(
    async (value: Trend) => {
      if (nav.useMockup) {
        setTrends(trends.filter((trend) => trend.ID !== value.ID));
        return;
      }

      try {
        const response = await handleApiResponse(
          trendApi.deleteTrendByIdTrendTrendIdDelete.bind(trendApi),
          value.ID
        );
        console.log(response);
        setTrends(trends.filter((trend) => trend.ID !== value.ID));
      } catch (error) {
        console.log(error);
      }
    },
    [nav, trends, trendApi]
  );

  const addTrendGroup = React.useCallback(
    async (value: TrendGroup) => {
      if (nav.useMockup) {
        setTrendGroups([...trendGroups, value]);
        return;
      }

      try {
        const response = await handleApiResponse(
          trendGroupApi.createTrendGroupTrendGroupPost.bind(trendGroupApi),
          value
        );
        console.log(response);
        if (response?.data) setTrendGroups([...trendGroups, response.data]);
      } catch (error) {
        console.log(error);
      }
    },
    [nav, trendGroups, trendGroupApi]
  );

  const updateTrendGroup = React.useCallback(
    async (value: TrendGroup) => {
      if (nav.useMockup) {
        setTrendGroups(
          trendGroups.map((trendGroup) => {
            if (trendGroup.ID == value.ID) return value;
            return trendGroup;
          })
        );
        return;
      }

      const { ID, ...updateTrendGroup } = value;
      try {
        const response = await handleApiResponse(
          trendGroupApi.updateTrendGroupTrendGroupTrendGroupIdPut.bind(
            trendGroupApi
          ),
          ID,
          updateTrendGroup
        );
        console.log(response);
        if (response?.data)
          setTrendGroups(
            trendGroups.map((trendGroup) => {
              if (trendGroup.ID == response.data.ID) return response.data;
              return trendGroup;
            })
          );
      } catch (error) {
        console.log(error);
      }
    },
    [nav, trendGroups, trendGroupApi]
  );

  const deleteTrendGroup = React.useCallback(
    async (value: TrendGroup) => {
      if (nav.useMockup) {
        setTrendGroups(
          trendGroups.filter((trendGroup) => trendGroup.ID !== value.ID)
        );
        return;
      }

      try {
        const response = await handleApiResponse(
          trendGroupApi.deleteTrendGroupByIdTrendGroupTrendGroupIdDelete.bind(
            trendGroupApi
          ),
          value.ID
        );
        console.log(response);
        setTrendGroups(
          trendGroups.filter((trendGroup) => trendGroup.ID !== value.ID)
        );
      } catch (error) {
        console.log(error);
      }
    },
    [nav, trendGroups, trendGroupApi]
  );

  const addUnit = React.useCallback(
    async (value: Unit) => {
      if (nav.useMockup) {
        setUnits([...units, value]);
        return;
      }

      try {
        const response = await handleApiResponse(
          unitApi.createUnitUnitPost.bind(unitApi),
          value
        );
        console.log(response);
        if (response?.data) setUnits([...units, response.data]);
      } catch (error) {
        console.log(error);
      }
    },
    [nav, units, unitApi]
  );

  const updateUnit = React.useCallback(
    async (value: Unit) => {
      if (nav.useMockup) {
        setUnits(
          units.map((unit) => {
            if (unit.ID == value.ID) return value;
            return unit;
          })
        );
        return;
      }

      const { ID, ...updateUnit } = value;
      try {
        const response = await handleApiResponse(
          unitApi.updateUnitUnitUnitIdPut.bind(unitApi),
          ID,
          updateUnit
        );
        console.log(response);
        if (response?.data)
          setUnits(
            units.map((unit) => {
              if (unit.ID == response.data.ID) return response.data;
              return unit;
            })
          );
      } catch (error) {
        console.log(error);
      }
    },
    [nav, units, unitApi]
  );

  const deleteUnit = React.useCallback(
    async (value: Unit) => {
      if (nav.useMockup) {
        setUnits(units.filter((unit) => unit.ID !== value.ID));
        return;
      }

      try {
        const response = await handleApiResponse(
          unitApi.deleteUnitByIdUnitUnitIdDelete.bind(unitApi),
          value.ID
        );
        console.log(response);
        setUnits(units.filter((unit) => unit.ID !== value.ID));
      } catch (error) {
        console.log(error);
      }
    },
    [nav, units, unitApi]
  );

  const LoadData = React.useCallback(async () => {
    //maybe split into separate function to avoid .then() mess
    handleApiResponse(trendDefApi.listTrendDefsTrendDefGet.bind(trendDefApi))
      .then((response) => {
        console.log(response);
        if (response?.data) setTrendDefs(response?.data.items);
      })
      .catch((error) => {
        console.log(error);
      });

    handleApiResponse(
      trendGroupApi.listTrendGroupsTrendGroupGet.bind(trendGroupApi)
    )
      .then((response) => {
        console.log(response);
        if (response?.data) setTrendGroups(response?.data.items);
      })
      .catch((error) => {
        console.log(error);
      });

    handleApiResponse(unitApi.listUnitsUnitGet.bind(unitApi))
      .then((response) => {
        console.log(response);
        if (response?.data) setUnits(response?.data.items);
      })
      .catch((error) => {
        console.log(error);
      });

    handleApiResponse(trendApi.listTrendsTrendGet.bind(trendApi))
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
  }, [nav.useMockup]);

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
              addTrendGroup={addTrendGroup}
              updateTrendGroup={updateTrendGroup}
              deleteTrendGroup={deleteTrendGroup}
              trendParamDefs={trendParamDefs}
              unitApi={unitApi}
              units={units}
              setUnits={setUnits}
              addUnit={addUnit}
              updateUnit={updateUnit}
              deleteUnit={deleteUnit}
              trendApi={trendApi}
              trends={trends}
              setTrends={setTrends}
              addTrend={addTrend}
              updateTrend={updateTrend}
              deleteTrend={deleteTrend}
            >
              <Routes>
                <Route path="/" element={<HomePage key={"home-page"} />} />
                <Route
                  path="/trends-current"
                  element={<TrendsCurrentPage key={"trends-current-page"} />}
                />
                <Route
                  path="/trends"
                  element={<TrendsPage key={"trends-page"} />}
                />
                <Route
                  path="simulator"
                  element={<SimulatorPage key={"simulator-page"} />}
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
