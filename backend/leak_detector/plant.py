import sys
import logging
from typing import List

from sqlalchemy import select
from .db import global_session
from database import lds
from .method import base, wave

# klasy zapisane stringiem, aby uniknąć cyklicznych importów 
METHOD_CLASSES = {
    'WAVE': 'MethodWave',
    'BALANCE': 'MethodBalance',
    'MASK': 'MethodMask',
    'COMBINE': 'MethodCombine'    
}

 
class Event:
    def __init__(self) -> None:
        pass

    def save() -> None:
        """save event to database"""
        pass


# TODO: Wygląda na to, żę brakuje parametrów pipeline!
# Np. która metoda/metody są aktywne, jakie są interwały, zdarzenia generowane dla poszczególnych metod, etc.
# może też progi, które są wymagane do wygenerowania zdarzenia
# Można to tez zapisać w configu, ale chyba będzie trudniej dla wielu pipelinów
class Pipeline:
    def __init__(self, plant, id, name, begin_pos) -> None:
        self._methods = {}
        self._nodes = {}
        self._active_methods = {}
        self._plant = plant
        self.id = id
        self.name = name
        self.begin_pos = begin_pos
        self._build() 


    def _build(self) -> None:
        
        stmt = select(lds.PipelineNode).where(lds.PipelineNode.PipelineID == self.id)
        for node, in global_session.execute(stmt):
            self._nodes[node.NodeID] = self._plant.nodes[node.NodeID]

        stmt = select(lds.Method).where(lds.Method.PipelineID == self.id)
        for method, in global_session.execute(stmt):            
            method_class = getattr(sys.modules["leak_detector.method"], METHOD_CLASSES[method.MethodDefID.strip()])
            self._methods[method.ID] = method_class(self.id, method.ID, method.Name)

    @property
    def plants(self) -> dict:
        return self._plants


    def get_probablity(self, timestamp, step) -> List[float]:
        result = []
        for method in self.methods:
            result.append(method.get_probablity(timestamp, step))


    def find_leaks_in_range(self, begin, end, time_resolution, length_resolution) -> List[Event]:
        """ Wersja bezstanowa, wykrywająca wycieki w zadanym przedziale czasowym
            wykonuje metodę get_probablity() dla każdej aktywnej metody
            zawsze zwraca alarmy, które wykryła w zadanym okresie czasowym
        """
        pass


    def find_leaks_to(self, end, time_resolution, length_resolution) -> List[Event]:
        """ Wersja stanowa, wykrywająca wycieki na podstawie danych zebranych wcześniej
            składa zapamiętane prawdopodobieństwa z nowymi obliczonymi metodą find_leaks_in_range()
            nie zwraca alarmów, które już zwróciła wcześniej
        """
        pass    


class Link:
    def __init__(self, id, length, begin_node, end_node) -> None:
        self.id = id
        self.length = length
        self.begin_node = begin_node
        self.end_node = end_node


class Node:
    def __init__(self, id, type, name):
        self.id = id
        self.type = type
        self.name = name


class Plant:
    def __init__(self) -> None:
        self._nodes = {}
        self._links = {}
        self._pipelines = {}
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


    def _build_pipelines(self) -> None:
        """ Wczytuje pipliny i metody z bazy danych """
        stmt = select(lds.Pipeline)
        for pipeline, in global_session.execute(stmt):
            self._pipelines[pipeline.ID] = Pipeline(self, pipeline.ID, pipeline.Name, pipeline.BeginPos)


    @property
    def pipelines(self) -> dict:
        return self._pipelines


    @property
    def nodes(self) -> dict:
        return self._nodes


    @property
    def links(self) -> dict:
        return self._links


    def get_distances(self, node1: Node, node2: Node) -> List[int]:
        """ Zwraca listę odległości między dwoma węzłami, różnymi drogami
            implementacja rekursywna
        """
        pass