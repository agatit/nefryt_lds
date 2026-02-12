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
import { AuthContext } from "../../contexts/authContext";
import {
  DrawerRouterContainer,
  DrawerRouterItemProps,
} from "onyks_shared_kendo";
import KendoLocalizationWrapper from "../../components/KendoLocalizationWrapper";
import TrendsPage from "./features/trends/TrendsPage";
import TrendConfigurationPage from "./features/trends_configuration/TrendConfigurationPage";
import LeakProbabilityPage from "./features/LeakProbabilityPage";
import EventsPage from "./features/events/EventsPage";
import LinksPage from "./features/links/LinksPage";
import NodesPage from "./features/nodes/NodesPage";
import PipelinesPage from "./features/pipelines/PipelinesPage";
import HomePage from "./features/HomePage";
import { Button } from "@progress/kendo-react-buttons";
import "../../styles/features/lds/lds.scss";
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
} from "../../services/api";
import { axiosInstance, host } from "../../lib/apiUtilities";
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

  const trendApi = React.useMemo(
    () => new TrendApi(auth?.config, host, axiosInstance),
    [auth],
  );

  const trendParamApi = React.useMemo(
    () => new TrendParamApi(auth?.config, host, axiosInstance),
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

  const [pipelineParams, setPipelineParams] = React.useState<PipelineParam[]>(
    nav.useMockup ? mockupPipelineParams : [],
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

        setLinks((prev) => prev.filter((link) => link.ID !== value.ID));
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

  const LoadData = React.useCallback(async () => {
    handleApiResponse(trendDefApi.listTrendDefsTrendDefGet.bind(trendDefApi))
      .then((response) => {
        if (response?.data) setTrendDefs(response?.data.items);
      })
      .catch((error) => {
        console.log(error);
      });

    handleApiResponse(
      eventDefApi.listEventDefsEventDefGet.bind(eventDefApi),
    ).then((res) => {
      if (res?.data) setEventDefs(res.data.items);
    });

    handleApiResponse(
      trendGroupApi.listTrendGroupsTrendGroupGet.bind(trendGroupApi),
    )
      .then((response) => {
        if (response?.data) setTrendGroups(response?.data.items);
      })
      .catch((error) => {
        console.log(error);
      });

    handleApiResponse(unitApi.listUnitsUnitGet.bind(unitApi))
      .then((response) => {
        if (response?.data) setUnits(response?.data.items);
      })
      .catch((error) => {
        console.log(error);
      });

    handleApiResponse(eventApi.listEventsEventGet.bind(eventApi))
      .then((response) => {
        if (response?.data) setEvents(response?.data.items);
      })
      .catch((error) => {
        console.log(error);
      });

    handleApiResponse(linkApi.listLinksLinkGet.bind(linkApi))
      .then((response) => {
        if (response?.data) setLinks(response?.data.items);
      })
      .catch((error) => {
        console.log(error);
      });

    handleApiResponse(nodeApi.listNodesNodeGet.bind(nodeApi))
      .then((response) => {
        if (response?.data) setNodes(response?.data.items);
      })
      .catch((error) => {
        console.log(error);
      });

    handleApiResponse(pipelineApi.listPipelinesPipelineGet.bind(pipelineApi))
      .then((response) => {
        if (response?.data) setPipelines(response?.data.items);
      })
      .catch((error) => {
        console.log(error);
      });

    handleApiResponse(trendApi.listTrendsTrendGet.bind(trendApi))
      .then((response) => {
        if (response?.data) setTrends(response?.data.items);
      })
      .catch((error) => {
        console.log(error);
      });

    handleApiResponse(
      trendParamApi.listTrendParamDefsTrendParamDefGet.bind(trendParamApi),
    ).then((resposne) => {
      if (resposne.data) setTrendParamDefs(resposne.data.items);
    });
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
    pipelineParamApi,
  ]);

  React.useEffect(() => {
    if (!nav.useMockup) LoadData();
  }, [nav.useMockup]);

  const isLoadingContext = React.useMemo(
    () =>
      trendDefs.length == 0 ||
      trendGroups.length == 0 ||
      units.length == 0 ||
      trends.length == 0 ||
      links.length == 0 ||
      nodes.length == 0 ||
      //events.length == 0 ||
      eventDefs.length == 0 ||
      pipelines.length === 0,
    [
      trendDefs,
      trendGroups,
      units,
      trends,
      pipelines,
      links,
      nodes,
      events,
      eventDefs,
    ],
  );

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
