import { DrawerItemProps } from "@progress/kendo-react-layout";
import {
  homeIcon,
  kpiStatusOpenIcon,
  lockIcon,
  unlockIcon,
} from "@progress/kendo-svg-icons";
import React from "react";
import { useTranslation } from "react-i18next";
import { Route, Routes, useLocation, useNavigate } from "react-router-dom";
import { AuthContextProvider } from "../../contexts/authContext";
import { DrawerRouterContainer } from "onyks_shared_kendo";
import KendoLocalizationWrapper from "../../components/KendoLocalizationWrapper";
import TrendsPage from "./features/trends_page/TrendsPage";
import TrendConfigurationPage from "./features/TrendConfigurationPage";
import LeakProbabilityPage from "./features/LeakProbabilityPage";
import EventsPage from "./features/EventsPage";
import HomePage from "./features/HomePage";
import { Button } from "@progress/kendo-react-buttons";
import "../../styles/features/lds/lds.scss";

export default function LDS() {
  const { t } = useTranslation(["common", "titles", "nav", "kendo"]);
  const { pathname } = useLocation();
  const navigate = useNavigate();

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
      text: t("nav:trends_mockup"),
      svgIcon: kpiStatusOpenIcon,
      selected: pathname == "/trends-mockup",
      route: "/trends-mockup",
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

  const [isMenuPinned, setIsMenuPinned] = React.useState<boolean>(true);
  const toggleMenuPinned = React.useCallback(() => {
    setIsMenuPinned(!isMenuPinned);
  }, [isMenuPinned]);

  return (
    <AuthContextProvider>
      <DrawerRouterContainer
        items={routerItems}
        navigate={navigate}
        expandOnHover={!isMenuPinned}
        expanded={true}
        position="start"
        mode="push"
        mini
      >
        <KendoLocalizationWrapper>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route
              path="/trends-mockup"
              element={<TrendsPage key={1} useMockup={true} />}
            />
            <Route
              path="/trends"
              element={<TrendsPage key={2} useMockup={false} />}
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
        </KendoLocalizationWrapper>
      </DrawerRouterContainer>
      <Button
        className="router-lock-button"
        svgIcon={isMenuPinned ? lockIcon : unlockIcon}
        onClick={toggleMenuPinned}
      />
    </AuthContextProvider>
  );
}
