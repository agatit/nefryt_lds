import { DrawerSelectEvent } from "@progress/kendo-react-layout";
import {
  chartLineIcon,
  chartLineStackedMarkersIcon,
  dropletIcon,
  graphIcon,
  homeIcon,
  lockIcon,
  planIcon,
  unlockIcon,
  wrenchIcon,
  linkIcon,
  shareIcon,
  trackChangesIcon,
} from "@progress/kendo-svg-icons";
import React from "react";
import { useTranslation } from "react-i18next";
import { Route, Routes, useLocation, useNavigate } from "react-router-dom";
import { AuthContext } from "../../../contexts/authContext";
import {
  DrawerRouterContainer,
  DrawerRouterItemProps,
} from "onyks_shared_kendo";
import KendoLocalizationWrapper from "../../../components/KendoLocalizationWrapper";
import TrendsPage from "../features/trends/TrendsPage";
import TrendConfigurationPage from "../features/trends_configuration";
import LeakProbabilityPage from "../features/leaks_probability";
import EventsPage from "../features/events";
import LinksPage from "../features/links";
import NodesPage from "../features/nodes";
import PipelinesPage from "../features/pipelines";
import HomePage from "../features/home/HomePage";
import { Button } from "@progress/kendo-react-buttons";
import "./lds.scss";
import { NavbarContext } from "../../../contexts/navbarContext";
import { LDSContextProvider } from "../contexts/ldsContext";
import {
  Trend,
  TrendApi,
  TrendDefApi,
  TrendDef,
  TrendGroup,
  TrendGroupApi,
  Unit,
  UnitApi,
  TrendParamApi,
  TrendParamDef,
  Event,
  EventApi,
  EventDef,
  EventDefApi,
  Link,
  LinkApi,
  Node,
  NodeApi,
  LinkCreate,
  LinkUpdate,
  EventDefUpdate,
  EventDefCreate,
  NodeCreate,
  NodeUpdate,
  Pipeline,
  PipelineCreate,
  PipelineUpdate,
  PipelineApi,
  PipelineParam,
  PipelineParamApi,
  PipelineParamCreate,
  Method,
  MethodCreate,
  MethodUpdate,
  MethodDef,
  MethodApi,
  MethodDefApi,
  MethodParam,
  MethodParamCreate,
  MethodParamDef,
  MethodParamApi,
  Template,
  TemplateCreate,
  TemplateApi,
  TemplateUpdate,
} from "../../../services/api";
import { axiosInstance, host } from "../../../lib/apiUtilities";
import {
  mockupTrendDefs,
  mockupTrendGroups,
  mockupTrendParamDefs,
  mockupTrends,
  mockupUnits,
  mockupEvents,
  mockupLinks,
  mockupEventDefs,
  mockupNodes,
  mockupPipelines,
  mockupPipelineParams,
  mockupMethods,
  mockupMethodDefs,
  mockupMethodParamDef,
  mockupMethodParams,
  mockupTemplates,
} from "../../../data/mockup-data";
import { Loader } from "@progress/kendo-react-indicators";
import { useHandleApiResponse } from "../../../hooks/useHandleApiResponse";
import TrendsCurrentPage from "../features/trends/TrendsCurrentPage";
import SimulatorPage from "../features/simulator";
import MethodsPage from "../features/methods";
import TemplatePage from "../features/templates";
export default function LDS() {
  const { t } = useTranslation(["common", "titles", "nav", "kendo"]);
  const { pathname } = useLocation();
  const navigate = useNavigate();
  const nav = React.useContext(NavbarContext);

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
      {
        text: t("nav:links"),
        svgIcon: linkIcon,
        selected: pathname == "/links",
        route: "/links",
      },
      {
        separator: true,
      },
      {
        text: t("nav:nodes"),
        svgIcon: shareIcon,
        selected: pathname == "/nodes",
        route: "/nodes",
      },
      {
        separator: true,
      },
      {
        text: t("nav:pipelines"),
        svgIcon: trackChangesIcon,
        selected: pathname == "/pipelines",
        route: "/pipelines",
      },
      {
        separator: true,
      },
      {
        text: t("nav:methods"),
        svgIcon: trackChangesIcon,
        selected: pathname == "/methods",
        route: "/methods",
      },
      {
        separator: true,
      },
      {
        text: t("nav:templates"),
        svgIcon: trackChangesIcon,
        selected: pathname == "/templates",
        route: "/templates",
      },
      {
        separator: true,
      },
    ],
  );

  React.useEffect(() => {
    setRouterItems(
      routerItems.map((item) => {
        return {
          ...item,
          selected:
            item.route == "/" ? pathname == "/" : pathname.includes(item.route),
        };
      }),
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
    [nav],
  );

  const auth = React.useContext(AuthContext);
  const handleApiResponse = useHandleApiResponse();

  const trendDefApi = React.useMemo(
    () => new TrendDefApi(auth?.config, host, axiosInstance),
    [auth],
  );

  const trendGroupApi = React.useMemo(
    () => new TrendGroupApi(auth?.config, host, axiosInstance),
    [auth],
  );

  const unitApi = React.useMemo(
    () => new UnitApi(auth?.config, host, axiosInstance),
    [auth],
  );

  const eventDefApi = React.useMemo(
    () => new EventDefApi(auth?.config, host, axiosInstance),
    [auth],
  );

  const eventApi = React.useMemo(
    () => new EventApi(auth?.config, host, axiosInstance),
    [auth],
  );

  const linkApi = React.useMemo(
    () => new LinkApi(auth?.config, host, axiosInstance),
    [auth],
  );

  const nodeApi = React.useMemo(
    () => new NodeApi(auth?.config, host, axiosInstance),
    [auth],
  );

  const pipelineApi = React.useMemo(
    () => new PipelineApi(auth?.config, host, axiosInstance),
    [auth],
  );

  const pipelineParamApi = React.useMemo(
    () => new PipelineParamApi(auth?.config, host, axiosInstance),
    [auth],
  );

  const methodApi = React.useMemo(
    () => new MethodApi(auth?.config, host, axiosInstance),
    [auth],
  );

  const methodDefApi = React.useMemo(
    () => new MethodDefApi(auth?.config, host, axiosInstance),
    [auth],
  );

  const methodParamApi = React.useMemo(
    () => new MethodParamApi(auth?.config, host, axiosInstance),
    [auth],
  );

  const trendApi = React.useMemo(
    () => new TrendApi(auth?.config, host, axiosInstance),
    [auth],
  );

  const trendParamApi = React.useMemo(
    () => new TrendParamApi(auth?.config, host, axiosInstance),
    [auth],
  );

  const templateApi = React.useMemo(
    () => new TemplateApi(auth?.config, host, axiosInstance),
    [auth],
  );

  const [trendDefs, setTrendDefs] = React.useState<TrendDef[]>(
    nav.useMockup ? mockupTrendDefs : [],
  );

  const [trendGroups, setTrendGroups] = React.useState<TrendGroup[]>(
    nav.useMockup ? mockupTrendGroups : [],
  );

  const [units, setUnits] = React.useState<Unit[]>(
    nav.useMockup ? mockupUnits : [],
  );

  const [trends, setTrends] = React.useState<Trend[]>(
    nav.useMockup ? mockupTrends : [],
  );

  const [trendParamDefs, setTrendParamDefs] = React.useState<TrendParamDef[]>(
    nav.useMockup ? mockupTrendParamDefs : [],
  );

  const [events, setEvents] = React.useState<Event[]>(
    nav.useMockup ? mockupEvents : [],
  );

  const [links, setLinks] = React.useState<Link[]>(
    nav.useMockup ? mockupLinks : [],
  );

  const [nodes, setNodes] = React.useState<Node[]>(
    nav.useMockup ? mockupNodes : [],
  );

  const [pipelines, setPipelines] = React.useState<Pipeline[]>(
    nav.useMockup ? mockupPipelines : [],
  );

  const [methods, setMethods] = React.useState<Method[]>(
    nav.useMockup ? mockupMethods : [],
  );

  const [methodDefs, setMethodDefs] = React.useState<MethodDef[]>(
    nav.useMockup ? mockupMethodDefs : [],
  );

  const [methodParams, setMethodParams] = React.useState<MethodParam[]>(
    nav.useMockup ? mockupMethodParams : [],
  );

  const [methodParamDefs, setMethodParamDefs] = React.useState<
    MethodParamDef[]
  >(nav.useMockup ? mockupMethodParamDef : []);

  const [pipelineParams, setPipelineParams] = React.useState<PipelineParam[]>(
    nav.useMockup ? mockupPipelineParams : [],
  );

  const [pipelineParamDefs, setPipelineParamDefs] = React.useState<
    PipelineParam[]
  >([]);

  const [templates, setTemplates] = React.useState<Template[]>(
    nav.useMockup ? mockupTemplates : [],
  );

  const [eventDefs, setEventDefs] = React.useState<EventDef[]>(
    nav.useMockup ? mockupEventDefs : [],
  );

  React.useEffect(() => {
    setTrendDefs(nav.useMockup ? mockupTrendDefs : []);
    setTrendGroups(nav.useMockup ? mockupTrendGroups : []);
    setUnits(nav.useMockup ? mockupUnits : []);
    setTrends(nav.useMockup ? mockupTrends : []);
    setTrendParamDefs(nav.useMockup ? mockupTrendParamDefs : []);
    setEvents(nav.useMockup ? mockupEvents : []);
    setLinks(nav.useMockup ? mockupLinks : []);
    setNodes(nav.useMockup ? mockupNodes : []);
    setEventDefs(nav.useMockup ? mockupEventDefs : []);
    setPipelines(nav.useMockup ? mockupPipelines : []);
    setPipelineParams(nav.useMockup ? mockupPipelineParams : []);
    setMethods(nav.useMockup ? mockupMethods : []);
    setMethodDefs(nav.useMockup ? mockupMethodDefs : []);
    setMethodParams(nav.useMockup ? mockupMethodParams : []);
    setMethodParamDefs(nav.useMockup ? mockupMethodParamDef : []);
    setTemplates(nav.useMockup ? mockupTemplates : []);
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
          value,
        );

        if (response?.data) {
          setTrends([...trends, response.data]);
          return response.data;
        }
      } catch (error) {
        console.log(error);
      }
    },
    [nav, trends, trendApi],
  );

  const updateTrend = React.useCallback(
    async (value: Trend) => {
      if (nav.useMockup) {
        setTrends(
          trends.map((trend) => {
            if (trend.ID == value.ID) return value;
            return trend;
          }),
        );
        return;
      }

      const { ID, ...updateTrend } = value;
      try {
        const response = await handleApiResponse(
          trendApi.updateTrendTrendTrendIdPut.bind(trendApi),
          ID,
          updateTrend,
        );

        if (response?.data)
          setTrends(
            trends.map((trend) => {
              if (trend.ID == response.data.ID) return response.data;
              return trend;
            }),
          );
      } catch (error) {
        console.log(error);
      }
    },
    [nav, trends, trendApi],
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
          value.ID,
        );

        setTrends((prev) => prev.filter((link) => link.ID !== value.ID));
      } catch (error) {
        console.log(error);
      }
    },
    [nav, trends, trendApi],
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
          value,
        );

        if (response?.data) setTrendGroups([...trendGroups, response.data]);
      } catch (error) {
        console.log(error);
      }
    },
    [nav, trendGroups, trendGroupApi],
  );

  const updateTrendGroup = React.useCallback(
    async (value: TrendGroup) => {
      if (nav.useMockup) {
        setTrendGroups(
          trendGroups.map((trendGroup) => {
            if (trendGroup.ID == value.ID) return value;
            return trendGroup;
          }),
        );
        return;
      }

      const { ID, ...updateTrendGroup } = value;
      try {
        const response = await handleApiResponse(
          trendGroupApi.updateTrendGroupTrendGroupTrendGroupIdPut.bind(
            trendGroupApi,
          ),
          ID,
          updateTrendGroup,
        );

        if (response?.data)
          setTrendGroups(
            trendGroups.map((trendGroup) => {
              if (trendGroup.ID == response.data.ID) return response.data;
              return trendGroup;
            }),
          );
      } catch (error) {
        console.log(error);
      }
    },
    [nav, trendGroups, trendGroupApi],
  );

  const deleteTrendGroup = React.useCallback(
    async (value: TrendGroup) => {
      if (nav.useMockup) {
        setTrendGroups(
          trendGroups.filter((trendGroup) => trendGroup.ID !== value.ID),
        );
        return;
      }

      try {
        const response = await handleApiResponse(
          trendGroupApi.deleteTrendGroupByIdTrendGroupTrendGroupIdDelete.bind(
            trendGroupApi,
          ),
          value.ID,
        );

        setTrendGroups(
          trendGroups.filter((trendGroup) => trendGroup.ID !== value.ID),
        );
      } catch (error) {
        console.log(error);
      }
    },
    [nav, trendGroups, trendGroupApi],
  );

  const ackEvent = React.useCallback(
    async (eventId: number) => {
      if (nav.useMockup) {
        setEvents((prev) =>
          prev.map((e) =>
            e.ID === eventId ? { ...e, AckDate: new Date().toISOString() } : e,
          ),
        );
        return;
      }

      try {
        await handleApiResponse(
          eventApi.ackEventEventEventIdAckPost.bind(eventApi),
          eventId,
        );

        setEvents((prev) =>
          prev.map((e) =>
            e.ID === eventId ? { ...e, AckDate: new Date().toISOString() } : e,
          ),
        );
      } catch (error) {
        console.log(error);
      }
    },
    [nav, eventApi],
  );

  const addEventDef = React.useCallback(
    async (value: EventDefCreate) => {
      if (nav.useMockup) {
        const mock: EventDef = {
          ...value,
        };
        setEventDefs((prev) => [...prev, mock]);
        return mock;
      }

      const response = await handleApiResponse(
        eventDefApi.createEventDefEventDefPost.bind(eventDefApi),
        value,
      );

      if (response?.data) {
        setEventDefs((prev) => [...prev, response.data]);
        return response.data;
      }
    },
    [nav, eventDefApi],
  );

  const updateEventDef = React.useCallback(
    async (id: string, value: EventDefUpdate) => {
      if (nav.useMockup) {
        const cleanUpdate = Object.fromEntries(
          Object.entries(value).filter(([, v]) => v !== null),
        );

        setEventDefs((prev) =>
          prev.map((d) => (d.ID === id ? { ...d, ...cleanUpdate } : d)),
        );

        return;
      }

      const response = await handleApiResponse(
        eventDefApi.updateEventDefEventDefEventDefIdPut.bind(eventDefApi),
        id,
        value,
      );

      if (response?.data) {
        setEventDefs((prev) =>
          prev.map((d) => (d.ID === response.data.ID ? response.data : d)),
        );
      }
    },
    [nav, eventDefApi],
  );

  const deleteEventDef = React.useCallback(
    async (value: EventDef) => {
      if (nav.useMockup) {
        setEventDefs((prev) => prev.filter((d) => d.ID !== value.ID));
        return;
      }
      try {
        await handleApiResponse(
          eventDefApi.deleteEventDefByIdEventDefEventDefIdDelete.bind(
            eventDefApi,
          ),
          value.ID,
        );

        setEventDefs((prev) => prev.filter((d) => d.ID !== value.ID));
      } catch (error) {
        console.log(error);
      }
    },
    [nav, eventDefApi],
  );

  const addPipeline = React.useCallback(
    async (value: PipelineCreate) => {
      if (nav.useMockup) {
        const mock: Pipeline = {
          ID: Date.now(),
          Name: value.Name,
        };

        setPipelines((prev) => [...prev, mock]);
        return mock;
      }

      try {
        const response = await handleApiResponse(
          pipelineApi.createPipelinePipelinePost.bind(pipelineApi),
          value,
        );

        if (response?.data) {
          setPipelines((prev) => [...prev, response.data]);
          return response.data;
        }
      } catch (error) {
        console.log(error);
      }
    },
    [nav, pipelineApi],
  );

  const updatePipeline = React.useCallback(
    async (id: number, value: PipelineUpdate) => {
      if (nav.useMockup) {
        setPipelines((prev) =>
          prev.map((p) =>
            p.ID === id ? { ...p, Name: value.Name ?? p.Name } : p,
          ),
        );
        return;
      }

      try {
        const response = await handleApiResponse(
          pipelineApi.updatePipelinePipelinePipelineIdPut.bind(pipelineApi),
          id,
          value,
        );

        if (response?.data) {
          setPipelines((prev) =>
            prev.map((p) => (p.ID === response.data.ID ? response.data : p)),
          );
        }
      } catch (error) {
        console.log(error);
      }
    },
    [nav, pipelineApi],
  );

  const deletePipeline = React.useCallback(
    async (value: Pipeline) => {
      if (nav.useMockup) {
        setPipelines((prev) => prev.filter((p) => p.ID !== value.ID));
        return;
      }

      try {
        await handleApiResponse(
          pipelineApi.deletePipelineByIdPipelinePipelineIdDelete.bind(
            pipelineApi,
          ),
          value.ID,
        );

        setPipelines((prev) => prev.filter((p) => p.ID !== value.ID));
      } catch (error) {
        console.log(error);
      }
    },
    [nav, pipelineApi],
  );

  const addMethod = React.useCallback(
    async (value: MethodCreate) => {
      if (nav.useMockup) {
        const mock: Method = {
          ID: Math.max(0, ...methods.map((m) => m.ID)) + 1,
          ...value,
        };

        setMethods((prev) => [...prev, mock]);
        return mock;
      }

      try {
        const response = await handleApiResponse(
          methodApi.createMethodMethodPost.bind(methodApi),
          value,
        );

        if (response?.data) {
          setMethods((prev) => [...prev, response.data]);
          return response.data;
        }
      } catch (error) {
        console.log(error);
      }
    },
    [nav, methodApi],
  );

  const updateMethod = React.useCallback(
    async (id: number, value: MethodUpdate) => {
      if (nav.useMockup) {
        setMethods((prev) =>
          prev.map((m) =>
            m.ID === id
              ? {
                  ...m,
                  MethodDefID: value.MethodDefID ?? m.MethodDefID,
                  PipelineID: value.PipelineID ?? m.PipelineID,
                  Name: value.Name ?? m.Name,
                }
              : m,
          ),
        );
        return;
      }

      try {
        const response = await handleApiResponse(
          methodApi.updateMethodMethodMethodIdPut.bind(methodApi),
          id,
          value,
        );

        if (response?.data) {
          setMethods((prev) =>
            prev.map((m) => (m.ID === id ? response.data : m)),
          );
        }
      } catch (error) {
        console.log(error);
      }
    },
    [methodApi],
  );

  const deleteMethod = React.useCallback(
    async (value: Method) => {
      if (nav.useMockup) {
        setMethods((prev) => prev.filter((m) => m.ID !== value.ID));
        return;
      }

      try {
        await handleApiResponse(
          methodApi.deleteMethodByIdMethodMethodIdDelete.bind(methodApi),
          value.ID,
        );

        setMethods((prev) => prev.filter((m) => m.ID !== value.ID));
      } catch (error) {
        console.log(error);
      }
    },
    [nav, methodApi],
  );

  const addLink = React.useCallback(
    async (value: LinkCreate) => {
      if (nav.useMockup) {
        const mockLink: Link = {
          ID: Math.max(0, ...links.map((l) => l.ID)) + 1,
          ...value,
          Length: value.Length != null ? String(value.Length) : null,
        };

        setLinks((prev) => [...prev, mockLink]);
        return mockLink;
      }

      try {
        const response = await handleApiResponse(
          linkApi.createLinkLinkPost.bind(linkApi),
          value,
        );

        if (response?.data) {
          setLinks((prev) => [...prev, response.data]);
          return response.data;
        }
      } catch (error) {
        console.log(error);
      }
    },
    [nav, linkApi],
  );

  const updateLink = React.useCallback(
    async (id: number, value: LinkUpdate) => {
      if (nav.useMockup) {
        setLinks((prev) =>
          prev.map((link) =>
            link.ID === id
              ? {
                  ...link,
                  ...value,
                  Length: value.Length == null ? null : String(value.Length),
                }
              : link,
          ),
        );

        return;
      }

      try {
        const response = await handleApiResponse(
          linkApi.updateLinkLinkLinkIdPut.bind(linkApi),
          id,
          value,
        );

        if (response?.data) {
          setLinks((prev) =>
            prev.map((link) =>
              link.ID === response.data.ID ? response.data : link,
            ),
          );
        }
      } catch (error) {
        console.log(error);
      }
    },
    [nav, linkApi],
  );

  const deleteLink = React.useCallback(
    async (value: Link) => {
      if (nav.useMockup) {
        setLinks((prev) => prev.filter((link) => link.ID !== value.ID));
        return;
      }

      try {
        await handleApiResponse(
          linkApi.deleteLinkByIdLinkLinkIdDelete.bind(linkApi),
          value.ID,
        );

        setLinks((prev) => prev.filter((link) => link.ID !== value.ID));
      } catch (error) {
        console.log(error);
      }
    },
    [nav, linkApi],
  );

  const addPipelineParams = React.useCallback(
    async (value: PipelineParamCreate, pipelineID: number) => {
      if (nav.useMockup) {
        const mock: PipelineParam = {
          PipelineParamDefID: value.PipelineParamDefID,
          Value: value.Value,
          PipelineID: pipelineID,
        };

        setPipelineParams((prev) => [...prev, mock]);
        return mock;
      }

      try {
        const response = await handleApiResponse(
          pipelineParamApi.createPipelineParamPipelinePipelineIdParamPost.bind(
            pipelineParamApi,
          ),
          pipelineID,
          value,
        );

        if (response?.data) {
          setPipelineParams((prev) => [...prev, response.data]);
          return response.data;
        }
      } catch (error) {
        console.log(error);
      }
    },
    [nav, pipelineParamApi],
  );

  const updatePipelineParam = React.useCallback(
    async (pipelineID: number, pipelineParamDefID: string, value: string) => {
      try {
        const response = await handleApiResponse(
          pipelineParamApi.updatePipelineParamPipelinePipelineIdParamPipelineParamDefIdPut.bind(
            pipelineParamApi,
          ),
          pipelineID,
          pipelineParamDefID,
          value,
        );

        if (response?.data) {
          setPipelineParams((prev) =>
            prev.map((p) =>
              p.PipelineID === pipelineID &&
              p.PipelineParamDefID === pipelineParamDefID
                ? response.data
                : p,
            ),
          );
        }
      } catch (error) {
        console.log(error);
      }
    },
    [pipelineParamApi],
  );

  const loadPipelineParamDefs = React.useCallback(
    async (pipelineID: number) => {
      try {
        const response = await handleApiResponse(
          pipelineParamApi.listRequiredPipelineParamsByPipelineIdPipelinePipelineIdParamAllGet.bind(
            pipelineParamApi,
          ),
          pipelineID,
        );

        if (response?.data?.items) {
          setPipelineParamDefs(response.data.items);
        }
      } catch (err) {
        console.log(err);
      }
    },
    [pipelineParamApi],
  );

  const deletePipelineParam = React.useCallback(
    async (value: PipelineParam) => {
      if (nav.useMockup) {
        setPipelineParams((prev) =>
          prev.filter(
            (p) =>
              !(
                p.PipelineID === value.PipelineID &&
                p.PipelineParamDefID === value.PipelineParamDefID
              ),
          ),
        );
        return;
      }

      try {
        await handleApiResponse(
          pipelineParamApi.deletePipelineParamByIdPipelinePipelineIdParamPipelineParamDefIdDelete.bind(
            pipelineParamApi,
          ),
          value.PipelineID,
          value.PipelineParamDefID,
        );

        setPipelineParams((prev) =>
          prev.filter(
            (p) =>
              !(
                p.PipelineID === value.PipelineID &&
                p.PipelineParamDefID === value.PipelineParamDefID
              ),
          ),
        );
      } catch (error) {
        console.log(error);
      }
    },
    [nav, pipelineParamApi],
  );

  const addNode = React.useCallback(
    async (value: NodeCreate) => {
      if (nav.useMockup) {
        const mock: Node = {
          ID: Math.max(0, ...nodes.map((n) => n.ID ?? 0)) + 1,
          ...value,
        };

        setNodes((prev) => [...prev, mock]);
        return mock;
      }

      try {
        const response = await handleApiResponse(
          nodeApi.createNodeNodePost.bind(nodeApi),
          value,
        );

        if (response?.data) {
          setNodes((prev) => [...prev, response.data]);
          return response.data;
        }
      } catch (error) {
        console.log(error);
      }
    },
    [nav, nodeApi],
  );

  const updateNode = React.useCallback(
    async (id: number, value: NodeUpdate) => {
      if (nav.useMockup) {
        const cleanUpdate = Object.fromEntries(
          Object.entries(value).filter(([, v]) => v != null),
        );

        setNodes((prev) =>
          prev.map((node) =>
            node.ID === id ? { ...node, ...cleanUpdate } : node,
          ),
        );
        return;
      }

      try {
        const response = await handleApiResponse(
          nodeApi.updateNodeNodeNodeIdPut.bind(nodeApi),
          id,
          value,
        );

        if (response?.data) {
          setNodes((prev) =>
            prev.map((node) =>
              node.ID === response.data.ID ? response.data : node,
            ),
          );
        }
      } catch (error) {
        console.log(error);
      }
    },
    [nav, nodeApi],
  );

  const deleteNode = React.useCallback(
    async (value: Node) => {
      if (nav.useMockup) {
        setNodes((prev) => prev.filter((node) => node.ID !== value.ID));
        return;
      }

      try {
        await handleApiResponse(
          nodeApi.deleteNodeByIdNodeNodeIdDelete.bind(nodeApi),
          value.ID!,
        );

        setNodes((prev) => prev.filter((node) => node.ID !== value.ID));
      } catch (error) {
        console.log(error);
      }
    },
    [nav, nodeApi],
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
          value,
        );

        if (response?.data) setUnits([...units, response.data]);
      } catch (error) {
        console.log(error);
      }
    },
    [nav, units, unitApi],
  );

  const updateUnit = React.useCallback(
    async (value: Unit) => {
      if (nav.useMockup) {
        setUnits(
          units.map((unit) => {
            if (unit.ID == value.ID) return value;
            return unit;
          }),
        );
        return;
      }

      const { ID, ...updateUnit } = value;
      try {
        const response = await handleApiResponse(
          unitApi.updateUnitUnitUnitIdPut.bind(unitApi),
          ID,
          updateUnit,
        );

        if (response?.data)
          setUnits(
            units.map((unit) => {
              if (unit.ID == response.data.ID) return response.data;
              return unit;
            }),
          );
      } catch (error) {
        console.log(error);
      }
    },
    [nav, units, unitApi],
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
          value.ID,
        );

        setUnits(units.filter((unit) => unit.ID !== value.ID));
      } catch (error) {
        console.log(error);
      }
    },
    [nav, units, unitApi],
  );

  const addMethodParam = React.useCallback(
    async (methodID: number, value: MethodParamCreate) => {
      try {
        const response = await handleApiResponse(
          methodParamApi.createMethodParamMethodMethodIdParamPost.bind(
            methodParamApi,
          ),
          methodID,
          value,
        );

        if (response?.data) {
          setMethodParams((prev) => [...prev, response.data]);
        }
      } catch (err) {
        console.log(err);
      }
    },
    [methodParamApi],
  );

  const updateMethodParam = React.useCallback(
    async (methodID: number, methodParamDefID: string, value: string) => {
      try {
        const response = await handleApiResponse(
          methodParamApi.updateMethodParamMethodMethodIdParamMethodParamDefIdPut.bind(
            methodParamApi,
          ),
          methodID,
          methodParamDefID,
          value,
        );

        if (response?.data) {
          setMethodParams((prev) =>
            prev.map((p) =>
              p.MethodID === methodID && p.MethodParamDefID === methodParamDefID
                ? response.data
                : p,
            ),
          );
        }
      } catch (err) {
        console.log(err);
      }
    },
    [methodParamApi],
  );

  const deleteMethodParam = React.useCallback(
    async (methodID: number, methodParamDefID: string) => {
      try {
        await handleApiResponse(
          methodParamApi.deleteMethodParamByIdMethodMethodIdParamMethodParamDefIdDelete.bind(
            methodParamApi,
          ),
          methodID,
          methodParamDefID,
        );

        setMethodParams((prev) =>
          prev.filter(
            (p) =>
              !(
                p.MethodID === methodID &&
                p.MethodParamDefID === methodParamDefID
              ),
          ),
        );
      } catch (err) {
        console.log(err);
      }
    },
    [methodParamApi],
  );

  const loadMethodParamsByMethod = React.useCallback(
    async (methodID: number) => {
      try {
        const response = await handleApiResponse(
          methodParamApi.listMethodParamsByMethodIdMethodMethodIdParamGet.bind(
            methodParamApi,
          ),
          methodID,
        );

        if (response?.data) {
          setMethodParams(response.data.items);
        }
      } catch (err) {
        console.log(err);
      }
    },
    [methodParamApi],
  );

  const addTemplate = React.useCallback(
    async (value: TemplateCreate) => {
      if (nav.useMockup) {
        const mock: Template = {
          ID: Math.max(0, ...templates.map((t) => t.ID ?? 0)) + 1,
          ...value,
        };

        setTemplates((prev) => [...prev, mock]);
        return mock;
      }

      try {
        const response = await handleApiResponse(
          templateApi.createTemplateTemplatePost.bind(templateApi),
          value,
        );

        if (response?.data) {
          setTemplates((prev) => [...prev, response.data]);
          return response.data;
        }
      } catch (error) {
        console.log(error);
      }
    },
    [nav, templates, templateApi],
  );

  const updateTemplate = React.useCallback(
    async (id: number, value: TemplateUpdate) => {
      if (nav.useMockup) {
        setTemplates((prev) =>
          prev.map((t) =>
            t.ID === id
              ? {
                  ...t,
                  Name: value.Name ?? t.Name ?? "",
                  Axes: value.Axes ?? t.Axes,
                }
              : t,
          ),
        );
        return;
      }

      try {
        const response = await handleApiResponse(
          templateApi.updateTemplateTemplateTemplateIdPut.bind(templateApi),
          id,
          value,
        );

        if (response?.data) {
          setTemplates((prev) =>
            prev.map((t) =>
              t.ID === id
                ? {
                    ...response.data,
                    Name: response.data.Name ?? "",
                  }
                : t,
            ),
          );
        }
      } catch (error) {
        console.log(error);
      }
    },
    [templateApi],
  );

  const deleteTemplate = React.useCallback(
    async (id: number) => {
      if (nav.useMockup) {
        setTemplates((prev) => prev.filter((t) => t.ID !== id));
        return;
      }

      try {
        await handleApiResponse(
          templateApi.deleteTemplateByIdTemplateTemplateIdDelete.bind(
            templateApi,
          ),
          id,
        );

        setTemplates((prev) => prev.filter((t) => t.ID !== id));
      } catch (error) {
        console.log(error);
      }
    },
    [nav, templateApi],
  );

  const [isLoading, setIsLoading] = React.useState(true);

  const LoadData = React.useCallback(async () => {
    setIsLoading(true);

    try {
      await Promise.all([
        handleApiResponse(
          trendDefApi.listTrendDefsTrendDefGet.bind(trendDefApi),
        ).then((res) => res?.data && setTrendDefs(res.data.items)),

        handleApiResponse(
          eventDefApi.listEventDefsEventDefGet.bind(eventDefApi),
        ).then((res) => res?.data && setEventDefs(res.data.items)),

        handleApiResponse(
          trendGroupApi.listTrendGroupsTrendGroupGet.bind(trendGroupApi),
        ).then((res) => res?.data && setTrendGroups(res.data.items)),

        handleApiResponse(unitApi.listUnitsUnitGet.bind(unitApi)).then(
          (res) => res?.data && setUnits(res.data.items),
        ),

        handleApiResponse(eventApi.listEventsEventGet.bind(eventApi)).then(
          (res) => res?.data && setEvents(res.data.items),
        ),

        handleApiResponse(
          methodDefApi.listMethodDefsMethodDefGet.bind(methodDefApi),
        ).then((res) => res?.data && setMethodDefs(res.data.items)),

        handleApiResponse(methodApi.listMethodsMethodGet.bind(methodApi)).then(
          (res) => res?.data && setMethods(res.data.items),
        ),

        handleApiResponse(
          methodParamApi.listMethodParamDefsMethodParamDefGet.bind(
            methodParamApi,
          ),
        ).then((res) => res?.data && setMethodParamDefs(res.data.items)),

        handleApiResponse(linkApi.listLinksLinkGet.bind(linkApi)).then(
          (res) => res?.data && setLinks(res.data.items),
        ),

        handleApiResponse(nodeApi.listNodesNodeGet.bind(nodeApi)).then(
          (res) => res?.data && setNodes(res.data.items),
        ),

        handleApiResponse(
          pipelineApi.listPipelinesPipelineGet.bind(pipelineApi),
        ).then((res) => res?.data && setPipelines(res.data.items)),

        handleApiResponse(trendApi.listTrendsTrendGet.bind(trendApi)).then(
          (res) => res?.data && setTrends(res.data.items),
        ),

        handleApiResponse(
          templateApi.listTemplatesTemplateGet.bind(templateApi),
        ).then((res) => res?.data && setTemplates(res.data.items)),

        handleApiResponse(
          trendParamApi.listTrendParamDefsTrendParamDefGet.bind(trendParamApi),
        ).then((res) => res?.data && setTrendParamDefs(res.data.items)),
      ]);
    } catch (err) {
      console.log(err);
    } finally {
      setIsLoading(false);
    }
  }, [
    trendDefApi,
    trendGroupApi,
    unitApi,
    trendApi,
    trendParamApi,
    eventApi,
    linkApi,
    nodeApi,
    pipelineApi,
    eventDefApi,
    methodApi,
    methodParamApi,
    templateApi,
  ]);

  React.useEffect(() => {
    if (!nav.useMockup) LoadData();
  }, [nav.useMockup]);
  
  const isLoadingContext = isLoading;

  const loadPipelineParamsByPipeline = React.useCallback(
    async (pipelineID: number) => {
      try {
        const response = await handleApiResponse(
          pipelineParamApi.listPipelineParamsByPipelineIdPipelinePipelineIdParamGet.bind(
            pipelineParamApi,
          ),
          pipelineID,
        );

        if (response?.data) {
          setPipelineParams(response.data.items);
        }
      } catch (error) {
        console.log(error);
      }
    },
    [pipelineParamApi],
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
              trendParamApi={trendParamApi}
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
              events={events}
              setEvents={setEvents}
              ackEvent={ackEvent}
              links={links}
              setLinks={setLinks}
              eventDefs={eventDefs}
              updateEventDef={updateEventDef}
              deleteEventDef={deleteEventDef}
              eventDefApi={eventDefApi}
              addEventDef={addEventDef}
              addLink={addLink}
              deleteLink={deleteLink}
              updateLink={updateLink}
              nodes={nodes}
              addNode={addNode}
              deleteNode={deleteNode}
              updateNode={updateNode}
              pipelines={pipelines}
              addPipeline={addPipeline}
              updatePipeline={updatePipeline}
              deletePipeline={deletePipeline}
              pipelineParams={pipelineParams}
              addPipelineParams={addPipelineParams}
              deletePipelineParams={deletePipelineParam}
              loadPipelineParamsByPipeline={loadPipelineParamsByPipeline}
              updatePipelineParam={updatePipelineParam}
              loadPipelineParamDefs={loadPipelineParamDefs}
              pipelineParamDefs={pipelineParamDefs}
              methods={methods}
              addMethod={addMethod}
              deleteMethod={deleteMethod}
              updateMethod={updateMethod}
              methodDefs={methodDefs}
              methodParams={methodParams}
              methodParamDefs={methodParamDefs}
              addMethodParam={addMethodParam}
              deleteMethodParam={deleteMethodParam}
              updateMethodParam={updateMethodParam}
              loadMethodParamsByMethod={loadMethodParamsByMethod}
              templates={templates}
              addTemplate={addTemplate}
              deleteTemplate={deleteTemplate}
              updateTemplate={updateTemplate}
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
                <Route path="/links" element={<LinksPage />} />
                <Route path="/nodes" element={<NodesPage />} />
                <Route path="/pipelines" element={<PipelinesPage />} />
                <Route path="/methods" element={<MethodsPage />} />
                <Route path="/templates" element={<TemplatePage />} />
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
