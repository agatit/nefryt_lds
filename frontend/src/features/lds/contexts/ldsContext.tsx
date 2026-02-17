import React, { PropsWithChildren } from "react";
import {
  Trend,
  TrendApi,
  TrendDef,
  TrendGroup,
  TrendGroupApi,
  TrendParamApi,
  TrendParamDef,
  Unit,
  UnitApi,
  Event,
  Link,
  EventDef,
  EventDefApi,
  Node,
  LinkCreate,
  LinkUpdate,
  EventDefUpdate,
  EventDefCreate,
  NodeCreate,
  NodeUpdate,
  Pipeline,
  PipelineCreate,
  PipelineUpdate,
  PipelineParam,
  PipelineParamCreate,
  Method,
  MethodCreate,
  MethodUpdate,
  MethodDef,
  MethodParam,
  MethodParamCreate,
  MethodParamDef,
  Template,
  TemplateCreate,
  TemplateUpdate,
} from "../../../services/api";

export type LDSContextType = {
  trendDefs: TrendDef[];
  trendApi: TrendApi;
  trends: Trend[];
  setTrends: (value: Trend[]) => void;
  addTrend: (value: Trend) => Promise<Trend>;
  updateTrend: (value: Trend) => Promise<void>;
  deleteTrend: (value: Trend) => Promise<void>;
  trendParamApi: TrendParamApi;
  trendParamDefs: TrendParamDef[];
  trendGroupApi: TrendGroupApi;
  trendGroups: TrendGroup[];
  setTrendGroups: (value: TrendGroup[]) => void;
  addTrendGroup: (value: TrendGroup) => Promise<void>;
  updateTrendGroup: (value: TrendGroup) => Promise<void>;
  deleteTrendGroup: (value: TrendGroup) => Promise<void>;
  unitApi: UnitApi;
  units: Unit[];
  setUnits: (value: Unit[]) => void;
  addUnit: (value: Unit) => Promise<void>;
  updateUnit: (value: Unit) => Promise<void>;
  deleteUnit: (value: Unit) => Promise<void>;
  events: Event[];
  setEvents: (value: Event[]) => void;
  ackEvent: (eventId: number) => Promise<void>;
  links: Link[];
  addLink: (value: LinkCreate) => Promise<Link>;
  updateLink: (id: number, value: LinkUpdate) => Promise<void>;
  deleteLink: (value: Link) => Promise<void>;
  setLinks: (value: Link[]) => void;
  eventDefs: EventDef[];
  eventDefApi: EventDefApi;
  updateEventDef: (id: string, value: EventDefUpdate) => Promise<void>;
  deleteEventDef: (value: EventDef) => Promise<void>;
  addEventDef: (value: EventDefCreate) => Promise<void>;
  nodes: Node[];
  addNode: (value: NodeCreate) => Promise<Node>;
  updateNode: (id: number, value: NodeUpdate) => Promise<void>;
  deleteNode: (value: Node) => Promise<void>;
  pipelines: Pipeline[];
  addPipeline: (value: PipelineCreate) => Promise<Pipeline>;
  updatePipeline: (id: number, value: PipelineUpdate) => Promise<void>;
  deletePipeline: (value: Pipeline) => Promise<void>;
  pipelineParams: PipelineParam[];
  addPipelineParams: (
    value: PipelineParamCreate,
    pipelineID: number,
  ) => Promise<PipelineParam>;
  deletePipelineParams: (value: PipelineParam) => Promise<void>;
  loadPipelineParamsByPipeline: (pipelineID: number) => Promise<void>;
  updatePipelineParam: (
    pipelineID: number,
    pipelineParamDefID: string,
    value: string,
  ) => Promise<void>;
  pipelineParamDefs: PipelineParam[];
  loadPipelineParamDefs: (pipelineID: number) => Promise<void>;
  methods: Method[];
  methodDefs: MethodDef[];
  addMethod: (value: MethodCreate) => Promise<Method>;
  updateMethod: (id: number, value: MethodUpdate) => Promise<void>;
  deleteMethod: (value: Method) => Promise<void>;
  methodParams: MethodParam[];
  methodParamDefs: MethodParamDef[];
  addMethodParam: (methodID: number, value: MethodParamCreate) => Promise<void>;
  updateMethodParam: (
    methodID: number,
    methodParamDefID: string,
    value: string,
  ) => Promise<void>;
  deleteMethodParam: (
    methodID: number,
    methodParamDefID: string,
  ) => Promise<void>;
  loadMethodParamsByMethod: (methodID: number) => Promise<void>;
  templates: Template[];
  addTemplate: (template: TemplateCreate) => Promise<void>;
  updateTemplate: (id: number, template: TemplateUpdate) => Promise<void>;
  deleteTemplate: (id: number) => Promise<void>;
};

export const LDSContext = React.createContext<LDSContextType | null>(null);

interface LDSContextProviderProps extends PropsWithChildren {
  trendDefs: TrendDef[];
  trendApi: TrendApi;
  trends: Trend[];
  setTrends: (value: Trend[]) => void;
  addTrend: (value: Trend) => Promise<Trend>;
  updateTrend: (value: Trend) => Promise<void>;
  deleteTrend: (value: Trend) => Promise<void>;
  trendParamApi: TrendParamApi;
  trendParamDefs: TrendParamDef[];
  trendGroupApi: TrendGroupApi;
  trendGroups: TrendGroup[];
  setTrendGroups: (value: TrendGroup[]) => void;
  addTrendGroup: (value: TrendGroup) => Promise<void>;
  updateTrendGroup: (value: TrendGroup) => Promise<void>;
  deleteTrendGroup: (value: TrendGroup) => Promise<void>;
  unitApi: UnitApi;
  units: Unit[];
  setUnits: (value: Unit[]) => void;
  addUnit: (value: Unit) => Promise<void>;
  updateUnit: (value: Unit) => Promise<void>;
  deleteUnit: (value: Unit) => Promise<void>;
  events: Event[];
  setEvents: (value: Event[]) => void;
  ackEvent: (eventId: number) => Promise<void>;
  links: Link[];
  addLink: (value: LinkCreate) => Promise<Link>;
  updateLink: (id: number, value: LinkUpdate) => Promise<void>;
  deleteLink: (value: Link) => Promise<void>;
  setLinks: (value: Link[]) => void;
  eventDefs: EventDef[];
  eventDefApi: EventDefApi;
  updateEventDef: (id: string, value: EventDefUpdate) => Promise<void>;
  deleteEventDef: (value: EventDef) => Promise<void>;
  addEventDef: (value: EventDefCreate) => Promise<void>;
  nodes: Node[];
  addNode: (value: NodeCreate) => Promise<Node>;
  updateNode: (id: number, value: NodeUpdate) => Promise<void>;
  deleteNode: (value: Node) => Promise<void>;
  pipelines: Pipeline[];
  addPipeline: (value: PipelineCreate) => Promise<Pipeline>;
  updatePipeline: (id: number, value: PipelineUpdate) => Promise<void>;
  deletePipeline: (value: Pipeline) => Promise<void>;
  pipelineParams: PipelineParam[];
  addPipelineParams: (
    value: PipelineParamCreate,
    pipelineID: number,
  ) => Promise<PipelineParam>;
  deletePipelineParams: (value: PipelineParam) => Promise<void>;
  loadPipelineParamsByPipeline: (pipelineID: number) => Promise<void>;
  updatePipelineParam: (
    pipelineID: number,
    pipelineParamDefID: string,
    value: string,
  ) => Promise<void>;
  pipelineParamDefs: PipelineParam[];
  loadPipelineParamDefs: (pipelineID: number) => Promise<void>;
  methods: Method[];
  methodDefs: MethodDef[];
  addMethod: (value: MethodCreate) => Promise<Method>;
  updateMethod: (id: number, value: MethodUpdate) => Promise<void>;
  deleteMethod: (value: Method) => Promise<void>;
  addMethodParam: (methodID: number, value: MethodParamCreate) => Promise<void>;
  updateMethodParam: (
    methodID: number,
    methodParamDefID: string,
    value: string,
  ) => Promise<void>;
  deleteMethodParam: (
    methodID: number,
    methodParamDefID: string,
  ) => Promise<void>;
  methodParams: MethodParam[];
  methodParamDefs: MethodParamDef[];
  loadMethodParamsByMethod: (methodID: number) => Promise<void>;
  templates: Template[];
  addTemplate: (template: TemplateCreate) => Promise<void>;
  updateTemplate: (id: number, template: TemplateUpdate) => Promise<void>;
  deleteTemplate: (id: number) => Promise<void>;
}

export const LDSContextProvider: React.FC<LDSContextProviderProps> = ({
  children,
  trendDefs,
  trendApi,
  trends,
  setTrends,
  addTrend,
  updateTrend,
  deleteTrend,
  trendParamApi,
  trendParamDefs,
  trendGroupApi,
  trendGroups,
  setTrendGroups,
  addTrendGroup,
  updateTrendGroup,
  deleteTrendGroup,
  unitApi,
  units,
  setUnits,
  addUnit,
  updateUnit,
  deleteUnit,
  events,
  setEvents,
  ackEvent,
  links,
  addLink,
  updateLink,
  deleteLink,
  setLinks,
  eventDefs,
  eventDefApi,
  updateEventDef,
  deleteEventDef,
  addEventDef,
  nodes,
  addNode,
  updateNode,
  deleteNode,
  pipelines,
  addPipeline,
  updatePipeline,
  deletePipeline,
  pipelineParams,
  addPipelineParams,
  deletePipelineParams,
  loadPipelineParamsByPipeline,
  updatePipelineParam,
  pipelineParamDefs,
  loadPipelineParamDefs,
  methods,
  methodDefs,
  addMethod,
  updateMethod,
  deleteMethod,
  addMethodParam,
  updateMethodParam,
  deleteMethodParam,
  methodParams,
  methodParamDefs,
  loadMethodParamsByMethod,
  templates,
  addTemplate,
  updateTemplate,
  deleteTemplate,
}: LDSContextProviderProps) => {
  const value = React.useMemo(
    () => ({
      trendDefs,
      trendApi,
      trends,
      setTrends,
      addTrend,
      updateTrend,
      deleteTrend,
      trendParamApi,
      trendParamDefs,
      trendGroupApi,
      trendGroups,
      setTrendGroups,
      addTrendGroup,
      updateTrendGroup,
      deleteTrendGroup,
      unitApi,
      units,
      setUnits,
      addUnit,
      updateUnit,
      deleteUnit,
      events,
      setEvents,
      ackEvent,
      links,
      addLink,
      updateLink,
      deleteLink,
      setLinks,
      eventDefs,
      eventDefApi,
      updateEventDef,
      deleteEventDef,
      addEventDef,
      nodes,
      addNode,
      updateNode,
      deleteNode,
      pipelines,
      addPipeline,
      updatePipeline,
      deletePipeline,
      pipelineParams,
      addPipelineParams,
      deletePipelineParams,
      loadPipelineParamsByPipeline,
      updatePipelineParam,
      pipelineParamDefs,
      loadPipelineParamDefs,
      methods,
      methodDefs,
      addMethod,
      updateMethod,
      deleteMethod,
      addMethodParam,
      updateMethodParam,
      deleteMethodParam,
      methodParams,
      methodParamDefs,
      loadMethodParamsByMethod,
      templates,
      addTemplate,
      updateTemplate,
      deleteTemplate,
    }),
    [
      trendDefs,
      trendApi,
      trends,
      addTrend,
      updateTrend,
      deleteTrend,
      trendParamApi,
      trendParamDefs,
      trendGroupApi,
      trendGroups,
      addTrendGroup,
      updateTrendGroup,
      deleteTrendGroup,
      unitApi,
      units,
      addUnit,
      updateUnit,
      deleteUnit,
      ackEvent,
      links,
      addLink,
      updateLink,
      deleteLink,
      setLinks,
      eventDefs,
      updateEventDef,
      deleteEventDef,
      addEventDef,
      nodes,
      addNode,
      updateNode,
      deleteNode,
      pipelines,
      addPipeline,
      updatePipeline,
      deletePipeline,
      pipelineParams,
      addPipelineParams,
      deletePipelineParams,
      loadPipelineParamsByPipeline,
      updatePipelineParam,
      pipelineParamDefs,
      loadPipelineParamDefs,
      methods,
      methodDefs,
      addMethod,
      updateMethod,
      deleteMethod,
      addMethodParam,
      updateMethodParam,
      deleteMethodParam,
      methodParams,
      methodParamDefs,
      loadMethodParamsByMethod,
      templates,
      addTemplate,
      updateTemplate,
      deleteTemplate,
    ],
  );

  return <LDSContext.Provider value={value}>{children}</LDSContext.Provider>;
};
