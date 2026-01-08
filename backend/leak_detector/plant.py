from __future__ import annotations
import importlib
import logging
import copy
from typing import TYPE_CHECKING
from sqlalchemy import select
from sqlalchemy.orm import Session
from db import get_engine
from .config import LeakDetectorSettings
from .trend import Trend
from .event import Event
from database import lds

if TYPE_CHECKING:
    from method import MethodBase

METHOD_CLASSES = {
    'WAVE': 'MethodWave',
    'TOF': 'MethodTOF'
}

logger = logging.getLogger(__name__)

class Node:
    def __init__(self, id_: int, type_: str, name: str):
        self.id = id_
        self.type = type_
        self.name = name

        logger.debug(f"Node: Created with id = {self.id}")


class Link:
    def __init__(self, id_: int, length: float, begin_node: Node, end_node: Node):
        self.id = id_
        self.begin_node = begin_node
        self.end_node = end_node
        self.length = length

        logger.debug(f"Link: Created with id = {self.id}")


class Pipeline:
    def __init__(self, plant: Plant, id_: int, name: str):
        self._plant = plant
        self._nodes = {}
        self._first_node = None
        self._methods = {}
        self._active_methods: dict[int, MethodBase] = {}
        self.id = id_
        self.name = name

        self._params = {}
        self._read_params()
        self._get_params()
        self._build()
        self._get_methods()

        logger.debug(f"Pipeline: Created with id = {self.id}")

    def _build(self) -> None:
        logger.debug(f"Pipeline: Started building pipeline with id = {self.id}")
        stmt = (select(lds.PipelineNode)
                .where(lds.PipelineNode.PipelineID == self.id)) # noqa
        with Session(get_engine()) as session:
            nodes = session.scalars(stmt).all()
        for node in nodes:
            self._nodes[node.NodeID] = self._plant.nodes[node.NodeID]
            if node.First:
                self._first_node = self._nodes[node.NodeID]

        stmt = (select(lds.Method)
                .where(lds.Method.PipelineID == self.id)) # noqa
        with Session(get_engine()) as session:
            methods = session.scalars(stmt).all()
        for method in methods:
            method_class = getattr(importlib.import_module("leak_detector.method"), METHOD_CLASSES[method.MethodDefID.strip()])
            self._methods[method.ID] = method_class(self, method.ID, method.Name)
        logger.debug(f"Pipeline: Finished building pipeline with id = {self.id}")

    def _read_params(self) -> None:
        statement = (select(lds.PipelineParam)
                     .join(lds.Pipeline, lds.PipelineParam.PipelineID == lds.Pipeline.ID) # noqa
                     .join(lds.PipelineParamDef, lds.PipelineParam.PipelineParamDefID == lds.PipelineParamDef.ID)
                     .where(lds.PipelineParam.PipelineID == self.id))
        with Session(get_engine()) as session:
            params = session.scalars(statement).all()
        for param in params:
            self._params[param.PipelineParamDefID.strip()] = param.Value
        self.begin_pos = float(self._params.get('BEGIN_POS', 0))
        logger.info(f"Pipeline with id = {self.id} initialized (params={self._params})")

    def _get_params(self) -> None:
        self.length_resolution = int(self._params.get('LENGTH_RESOLUTION', 10))
        self.time_resolution = int(self._params.get('TIME_RESOLUTION', 10))

    def _get_methods(self) -> None:
        for method_id in self._params.get('ACTIVE_METHODS', '').split(',') if not LeakDetectorSettings.optimizer_method_id else [LeakDetectorSettings.optimizer_method_id]:
            self._active_methods[int(method_id)] = self._methods[int(method_id)]

        self.method_events = self._params.get('METHOD_EVENTS', '').split(',')
        self._max_trend_time_delta = max(([method.get_max_trend_time_delta() for method in self._active_methods.values()]))
        self._max_leakage_alarm_delta = max([method.get_leakage_alarm_delta() for method in self._active_methods.values()])

    def find_leaks_in_range(self, begin: int, end: int) -> dict[int, list[Event]]:
        logger.debug(f'Pipeline with id = {self.id} detect leaks in range {begin}-{end}')
        events = {}
        for method_id, method in self._active_methods.items():
            events[method_id] = method.find_leaks_in_range(begin, end)

        return events

    @property
    def plant(self) -> Plant:
        return self._plant

    @property
    def nodes(self) -> dict[int, Node]:
        return self._nodes

    @property
    def methods(self) -> dict[int, MethodBase]:
        return self._methods
    
    @property
    def active_methods(self) -> dict[int, MethodBase]:
        return self._active_methods

    @property
    def first_node(self) -> Node:
        return self._first_node

    @property
    def max_leakage_alarm_delta(self) -> int:
        return self._max_leakage_alarm_delta

    @property
    def max_trend_time_delta(self) -> int:
        return self._max_trend_time_delta


class Plant:
    def __init__(self, past_leak_detector: bool):
        self._nodes = {}
        self._links = {}
        self._pipelines = {}
        self._trends = {}
        self._build_mesh()
        self._build_pipelines()
        self._past_leak_detector = past_leak_detector

        logger.debug(f"Plant: Created")

    def _build_mesh(self) -> None:
        logger.debug(f"Plant: Started building mesh")
        statement = select(lds.Node)
        with Session(get_engine()) as session:
            results = session.scalars(statement).all()
        for node in results:
            self._nodes[int(node.ID)] = Node(node.ID, node.Type.strip(), str(node.Name or ""))

        statement = select(lds.Link)
        with Session(get_engine()) as session:
            links = session.scalars(statement).all()
        for link in links:
            self._links[int(link.ID)] = Link(link.ID, float(link.Length), self.nodes[link.BeginNodeID], self.nodes[link.EndNodeID])

        statement = select(lds.Trend)
        with Session(get_engine()) as session:
            trends = session.scalars(statement).all()
        for trend in trends:
            self._trends[int(trend.ID)] = Trend(trend)
        logger.debug(f"Plant: Finished building mesh")

    def _build_pipelines(self) -> None:
        logger.debug(f"Plant: Started building pipelines")
        statement = select(lds.Pipeline)
        with Session(get_engine()) as session:
            pipelines = session.scalars(statement).all()
        for pipeline in pipelines:
            if not LeakDetectorSettings.optimizer_pipeline_id or pipeline.ID == LeakDetectorSettings.optimizer_pipeline_id:
                self._pipelines[int(pipeline.ID)] = Pipeline(self, pipeline.ID, pipeline.Name)

        self._max_leakage_alarm_delta = max([pipeline.max_leakage_alarm_delta for pipeline in self._pipelines.values()])
        self._max_trend_time_delta = max(([pipeline.max_trend_time_delta for pipeline in self._pipelines.values()]))
        logger.debug(f"Plant: Finished building pipelines")

    def get_distances(self, node1: Node, node2: Node, visited=None) -> list[float]:
        if visited is None:
            visited = set()

        if node1 == node2:
            return [0]

        distances = []
        visited.add(node1)
        for link in self.links.values():
            if link.begin_node == node1 and link.end_node not in visited:
                distances.extend([link.length + dist for dist in self.get_distances(link.end_node, node2, copy.copy(visited))])

            if link.end_node == node1 and link.begin_node not in visited:
                distances.extend([link.length + dist for dist in self.get_distances(link.begin_node, node2, copy.copy(visited))])        

        return distances

    @property
    def pipelines(self) -> dict[int, Pipeline]:
        return self._pipelines

    @property
    def nodes(self) -> dict[int, Node]:
        return self._nodes

    @property
    def links(self) -> dict[int, Link]:
        return self._links

    @property
    def trends(self) -> dict[int, Trend]:
        return self._trends

    @property
    def max_leakage_alarm_delta(self) -> int:
        return self._max_leakage_alarm_delta

    @property
    def max_trend_time_delta(self) -> int:
        return self._max_trend_time_delta

    @property
    def past_leak_detector(self) -> bool:
        return self._past_leak_detector
