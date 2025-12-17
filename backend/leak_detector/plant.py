from __future__ import annotations
import importlib
import logging
import copy
from typing import TYPE_CHECKING
from sqlalchemy import select
from sqlalchemy.orm import Session
from config import Settings
from db import get_engine
from .trend import Trend
from .event import Event
from database import lds

if TYPE_CHECKING:
    from method import MethodBase

METHOD_CLASSES = {
    'WAVE': 'MethodWaveSigned',
    'BALANCE': 'MethodBalance',
    'MASK': 'MethodMask',
    'COMBINE': 'MethodCombine',
    'TOF': 'MethodTOF'
}

class Node:
    def __init__(self, id_: int, type_: str, name: str):
        self.id = id_
        self.type = type_
        self.name = name

        logging.debug(f"Node {self.id}: {self.type} {self.name} created.")


class Link:
    def __init__(self, id_: int, length: float, begin_node: Node, end_node: Node):
        self.id = id_
        self.begin_node = begin_node
        self.end_node = end_node
        self.length = length

        logging.debug(f"Link {self.id}: {self.begin_node.id} {self.end_node.id} {self.length} created.")


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

        logging.debug(f"Pipeline {self.id}: {self.name} created.")

    def _build(self) -> None:        
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

    def _get_params(self) -> None:
        self.length_resolution = int(self._params.get('LENGTH_RESOLUTION', 10))
        self.time_resolution = int(self._params.get('TIME_RESOLUTION', 10))

    def _get_methods(self) -> None:
        for method_id in self._params.get('ACTIVE_METHODS', '').split(',') if not Settings.optimizer_method_id else [Settings.optimizer_method_id]:
            self._active_methods[int(method_id)] = self._methods[int(method_id)]

        self.method_events = self._params.get('METHOD_EVENTS', '').split(',')

    def find_leaks_in_range(self, begin: int, end: int) -> dict[int, list[Event]]:
        events = {}
        for method_id, method in self._active_methods.items():
            events[method_id] = method.find_leaks_in_range(begin, end)

        return events

    # TODO: find_leaks_to().
    def find_leaks_to(self, to: int) -> list[Event]:
        """ Wersja stanowa, wykrywająca wycieki na podstawie danych zebranych wcześniej
            składa zapamiętane prawdopodobieństwa z nowymi obliczonymi metodą find_leaks_in_range()
            nie zwraca alarmów, które już zwróciła wcześniej
        """
        pass

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

    def get_leakage_alarm_delta(self) -> int:
        return max([method.get_leakage_alarm_delta() for method in self._active_methods.values()])


class Plant:
    def __init__(self):
        self._nodes = {}
        self._links = {}
        self._pipelines = {}
        self._trends = {}
        self._build_mesh()
        self._build_pipelines()

        logging.debug(f"Plant created.")

    def _build_mesh(self) -> None:
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

    def _build_pipelines(self) -> None:
        statement = select(lds.Pipeline)
        with Session(get_engine()) as session:
            pipelines = session.scalars(statement).all()
        for pipeline in pipelines:
            if not Settings.optimizer_pipeline_id or pipeline.ID == Settings.optimizer_pipeline_id:
                self._pipelines[int(pipeline.ID)] = Pipeline(self, pipeline.ID, pipeline.Name)

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

    def get_leakage_alarm_delta(self) -> int:
        return max([pipeline.get_leakage_alarm_delta() for pipeline in self._pipelines.values()])
