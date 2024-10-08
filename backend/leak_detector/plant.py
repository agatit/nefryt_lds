import logging
import sys
import copy
from typing import TYPE_CHECKING, Dict, List

from sqlalchemy import Float, select, and_

from .db import global_session
from .trend import Trend
from .event import Event
from database import lds

# Do importu type'ów:
if TYPE_CHECKING:
    from .method import MethodBase

# from . import method
# from .method import MethodBalance, MethodWave, MethodMask, MethodCombine
# klasy zapisane stringiem, aby uniknąć cyklicznych importów - jak nie będzie to potrzebne to zminić na klasy
METHOD_CLASSES = {
    'WAVE': 'MethodWave',
    'BALANCE': 'MethodBalance',
    'MASK': 'MethodMask',
    'COMBINE': 'MethodCombine'    
}

class Node:
    def __init__(self, id: int, type: str, name: str) -> None:
        self.id = id
        self.type = type
        self.name = name
        logging.debug(f"Node {self.id}: {self.type} {self.name} created.")


class Link:
    def __init__(self, id, length: float, begin_node: Node, end_node: Node) -> None:
        self.id = id
        self.begin_node = begin_node
        self.end_node = end_node
        self.length = length

        logging.debug(f"Link {self.id}: {self.begin_node.id} {self.end_node.id} {self.length} created.")


# TODO: Wygląda na to, żę brakuje parametrów pipeline!
# Np. która metoda/metody są aktywne, jakie są interwały, zdarzenia generowane dla poszczególnych metod, etc.
# może też progi, które są wymagane do wygenerowania zdarzenia
# Można to tez zapisać w configu, ale chyba będzie trudniej dla wielu pipelinów
class Pipeline:
    def __init__(self, plant: 'Plant', id: int, name: str) -> None:
        self._plant = plant
        self._nodes = {}
        self._first_node = None
        self._methods : Dict[int, 'MethodBase'] = {}
        self._active_methods : Dict[int, 'MethodBase'] = {}

        self.id = id
        self.name = name
        
        self._params = {}
        self._read_params()
        self._build()
        self._get_params()

        logging.debug(f"Pipeline {self.id}: {self.name} created.")

    def _build(self) -> None:        
        stmt = select(lds.PipelineNode).where(lds.PipelineNode.PipelineID == self.id)
        for node, in global_session.execute(stmt):
            self._nodes[node.NodeID] = self._plant.nodes[node.NodeID]
            if node.First:
                self._first_node = self._nodes[node.NodeID]
        logging.debug(stmt)

        stmt = select(lds.Method).where(lds.Method.PipelineID == self.id)
        for method, in global_session.execute(stmt):            
            method_class = getattr(sys.modules["leak_detector.method"], METHOD_CLASSES[method.MethodDefID.strip()])
            self._methods[method.ID] = method_class(self, method.ID, method.Name)
        logging.debug(stmt)

    def _read_params(self) -> None:
        stmt = select([lds.PipelineParam, lds.PipelineParamDef]) \
            .select_from(lds.PipelineParamDef) \
            .outerjoin(lds.PipelineParam, \
                    and_(lds.PipelineParamDef.ID == lds.PipelineParam.PipelineParamDefID, lds.PipelineParam.PipelineID == self.id) \
                )
        for param, param_def in global_session.execute(stmt):
            if param is not None:
                self._params[param_def.ID.strip()] = param.Value
        logging.debug(stmt)


    def _get_params(self) -> None:
        self.begin_pos = float(self._params.get('BEGIN_POS', 0))
        self.length_resolution = int(self._params.get('LENGTH_RESOLUTION', 1))
        self.time_resolution = int(self._params.get('TIME_RESOLUTION', 1))
        
        for id in self._params.get('ACTIVE_METHODS', '').split(','):
            self._active_methods[int(id)] = self._methods[int(id)]

        self.method_events = self._params.get('METHOD_EVENTS', '').split(',') 

    def get_probability(self, begin, end) -> Dict[int, List[List[Float]]]:
        result = {}
        for id, method in self._active_methods.items():
            result[id] = method.get_probability(begin, end)
        logging.info(f"Pipeline {self.id}: probabilities calculated.")

        return result

    def find_leaks_in_range(self, begin: int, end: int) -> Dict[int, List[Event]]:
        events = {}
        for id, method in self._active_methods.items():
            events[id] = method.find_leaks_in_range(begin, end)
        logging.info(f"Pipeline {self.id}: leaks detected.")

        return events

    # TODO:
    # - Metoda find_leaks_to().
    def find_leaks_to(self, to: int) -> List[Event]:
        """ Wersja stanowa, wykrywająca wycieki na podstawie danych zebranych wcześniej
            składa zapamiętane prawdopodobieństwa z nowymi obliczonymi metodą find_leaks_in_range()
            nie zwraca alarmów, które już zwróciła wcześniej
        """
        pass

    @property
    def plant(self) -> 'Plant':
        return self._plant

    @property
    def nodes(self) -> List[Node]:
        return self._nodes

    @property
    def methods(self) -> Dict[int, 'MethodBase']:
        return self._methods
    
    @property
    def active_methods(self) -> Dict[int, 'MethodBase']:
        return self._active_methods


class Plant:
    def __init__(self) -> None:
        self._nodes = {}
        self._links = {}
        self._pipelines = {}
        self._trends = {}
        self._build_mesh()
        self._build_pipelines()

        logging.debug(f"Plant created.")


    def _build_mesh(self) -> None:
        stmt = select(lds.Node)
        for node, in  global_session.execute(stmt):
            self._nodes[int(node.ID)] = Node(node.ID, node.Type.strip(), str(node.Name or ""))
        logging.debug(stmt)

        stmt = select(lds.Link)
        for link, in global_session.execute(stmt):
            self._links[int(link.ID)] = Link(link.ID, float(link.Length), self.nodes[link.BeginNodeID], self.nodes[link.EndNodeID])
        logging.debug(stmt)

        stmt = select(lds.Trend)
        for trend, in global_session.execute(stmt):
            self._trends[int(trend.ID)] = Trend(trend.ID, trend.NodeID)            
        logging.debug(stmt)

    def _build_pipelines(self) -> None:
        stmt = select(lds.Pipeline)
        for pipeline, in global_session.execute(stmt):
            self._pipelines[int(pipeline.ID)] = Pipeline(self, pipeline.ID, pipeline.Name)
        logging.debug(stmt)
    
    def get_distances(self, node1: Node, node2: Node, visited=None) -> List[float]:
        if (visited is None):
            visited = set()

        if (node1 == node2):
            return [0]

        distances = []
        visited.add(node1)
        for link in self.links.values():
            if (link.begin_node == node1 and link.end_node not in visited):
                distances.extend([link.length + dist for dist in self.get_distances(link.end_node, node2, copy.copy(visited))])

            if (link.end_node == node1 and link.begin_node not in visited):
                distances.extend([link.length + dist for dist in self.get_distances(link.begin_node, node2, copy.copy(visited))])        

        return distances

    @property
    def pipelines(self) -> Dict[int, Pipeline]:
        return self._pipelines

    @property
    def nodes(self) -> Dict[int, Node]:
        return self._nodes

    @property
    def links(self) -> Dict[int, Link]:
        return self._links

    @property
    def trends(self) -> Dict[int, Trend]:
        return self._trends
