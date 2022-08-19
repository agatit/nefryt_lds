import copy
from datetime import  datetime
import sys
from typing import Dict, List

from sqlalchemy import select, and_, insert

from .db import Session, global_session
from .trend import Trend
from database import lds

# from . import method
# from .method import MethodBalance, MethodWave, MethodMask, MethodCombine
# klasy zapisane stringiem, aby uniknąć cyklicznych importów - jak nie będzie to potrzebne to zminić na klasy
METHOD_CLASSES = {
    'WAVE': 'MethodWave',
    'BALANCE': 'MethodBalance',
    'MASK': 'MethodMask',
    'COMBINE': 'MethodCombine'    
}

 
class Event:
    def __init__(self, method_id, time, position) -> None:
        self._method_id = method_id
        self._time = datetime.fromtimestamp(time // 1000)
        self._position = position

    # Co jeżeli dwa razy zostanie wykryte te samo zdarzenie?
    # Obsługa takiej sytuacji
    def save(self) -> None:
        """save event to database"""
        session = Session()
        stmt = insert(lds.Event).values(EventDefID='LEAK', MethodID=20, BeginDate=self._time, Position=self._position)
        session.execute(stmt)
        session.commit()
        return


# TODO: Wygląda na to, żę brakuje parametrów pipeline!
# Np. która metoda/metody są aktywne, jakie są interwały, zdarzenia generowane dla poszczególnych metod, etc.
# może też progi, które są wymagane do wygenerowania zdarzenia
# Można to tez zapisać w configu, ale chyba będzie trudniej dla wielu pipelinów
class Pipeline:
    def __init__(self, plant, id, name) -> None:
        self._methods = {}
        self._nodes = {}
        self._active_methods = {}
        self._plant = plant
        self.id = id
        self.name = name
        
        self._read_params()
        self._build()

        self.begin_pos = self._params.get('BEGIN_POS',0)
        self.length_resolution = int(self._params.get('LENGTH_RESOLUTION', 1))
        self.time_resolution = int(self._params.get('TIME_RESOLUTION', 1))
        
        for id in self._params.get('ACTIVE_METHODS', '').split(','):
            self._active_methods[int(id)] = self._methods[int(id)]

        self.method_events = self._params.get('METHOD_EVENTS', '').split(',')
        # TODO: obsługa wymagalności parametrów metod


    def _build(self) -> None:
        
        stmt = select(lds.PipelineNode).where(lds.PipelineNode.PipelineID == self.id)
        for node, in global_session.execute(stmt):
            self._nodes[node.NodeID] = self._plant.nodes[node.NodeID]

        stmt = select(lds.Method).where(lds.Method.PipelineID == self.id)
        for method, in global_session.execute(stmt):            
            method_class = getattr(sys.modules["leak_detector.method"], METHOD_CLASSES[method.MethodDefID.strip()])
            self._methods[method.ID] = method_class(self, method.ID, method.Name)

    def _read_params(self):
        stmt = select([lds.PipelineParam, lds.PipelineParamDef]) \
            .select_from(lds.PipelineParamDef) \
            .outerjoin(lds.PipelineParam, \
                    and_(lds.PipelineParamDef.ID == lds.PipelineParam.PipelineParamDefID, lds.PipelineParam.PipelineID == self.id) \
                )  

        self._params = {}
        for param, param_def in global_session.execute(stmt):
            if param is not None:
                self._params[param_def.ID.strip()] = param.Value
            # else:
            # TODO: obsługa defaultowych wartości parametrów

    @property
    def plant(self) -> dict:
        return self._plant

    @property
    def methods(self) -> dict:
        return self._methods


    def get_probability(self, begin, end) -> dict:
        result = {}
        for id, method in self._active_methods.items():
            result[id] = method.get_probability(begin, end)

        return result



    def find_leaks_in_range(self, begin, end) -> dict:
        """ Wersja bezstanowa, wykrywająca wycieki w zadanym przedziale czasowym
            wykonuje metodę get_probability() dla każdej aktywnej metody
            zawsze zwraca alarmy, które wykryła w zadanym okresie czasowym
        """
        events = {}
        for id, method in self._active_methods.items():
            events[id] = method.find_leaks_in_range(begin, end)

        return events


    def find_leaks_to(self, end) -> List[Event]:
        """ Wersja stanowa, wykrywająca wycieki na podstawie danych zebranych wcześniej
            składa zapamiętane prawdopodobieństwa z nowymi obliczonymi metodą find_leaks_in_range()
            nie zwraca alarmów, które już zwróciła wcześniej
        """
        pass    


class Node:
    def __init__(self, id, type, name) -> None:
        self.id = id
        self.type = type
        self.name = name


class Link:
    def __init__(self, id, length, begin_node : Node, end_node : Node) -> None:
        self.id = id
        self.length = length
        self.begin_node = begin_node
        self.end_node = end_node


class Plant:
    def __init__(self) -> None:
        self._nodes = {}
        self._links = {}
        self._pipelines = {}
        self._trends = {}
        self._build_mesh()
        self._build_pipelines()


    def _build_mesh(self) -> None:
        """ Wczytuje liniki i nody z bazy danych"""
        stmt = select(lds.Node)
        for node, in  global_session.execute(stmt):
            self._nodes[node.ID] = Node(node.ID, node.Type.strip(), str(node.Name or ""))

        stmt = select(lds.Link)
        for link, in global_session.execute(stmt):
            self._links[link.ID] = Link(link.ID, link.Length, self.nodes[link.BeginNodeID], self.nodes[link.EndNodeID])

        stmt = select(lds.Trend)
        for trend, in global_session.execute(stmt):
            self._trends[trend.ID] = Trend(trend.ID, trend.NodeID)            


    def _build_pipelines(self) -> None:
        """ Wczytuje pipliny i metody z bazy danych """
        stmt = select(lds.Pipeline)
        for pipeline, in global_session.execute(stmt):
            self._pipelines[pipeline.ID] = Pipeline(self, pipeline.ID, pipeline.Name)


    @property
    def pipelines(self) -> dict:
        return self._pipelines


    @property
    def nodes(self) -> dict:
        return self._nodes


    @property
    def links(self) -> dict:
        return self._links

    @property
    def trends(self) -> dict:
        return self._trends


    def get_distances(self, node1: Node, node2: Node, visited=None) -> List[int]:
        """ Zwraca listę odległości między dwoma węzłami, różnymi drogami
            implementacja rekursywna
        """
        if (visited is None):
            visited = set()
            
        if (node1 == node2):
            return [0]

        distances = []
        visited.add(node1)
        for link in self.links.values():
            if (link.begin_node == node1 and link.end_node not in visited):
                distances.extend([int(link.length + dist) for dist in self.get_distances(link.end_node, node2, copy.copy(visited))])
                
            if (link.end_node == node1 and link.begin_node not in visited):
                distances.extend([int(link.length + dist) for dist in self.get_distances(link.begin_node, node2, copy.copy(visited))])        
        return distances