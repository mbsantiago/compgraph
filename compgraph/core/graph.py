import uuid
from contextlib import contextmanager

from compgraph import engines

class Graph(object):
    graphs = {}

    def __init__(self, name=None):
        self.nodes = {}
        self.edges = {}
        self.name = uuid.uuid4() if name is None else name

        Graph.graphs[self.name] = name

    def add_node(self, node):
        if self.name_in_graph(node=node.name):
            raise Graph.NameCollisionError('Node {} already used in graph'.format(node.name))
        self.nodes[node.name] = node

    def add_edge(self, edge):
        if self.name_in_graph(edge=edge.name):
            raise Graph.NameCollisionError('Edge {} already used in graph'.format(edge.name))
        self.edges[edge.name] = edge

    @contextmanager
    def as_default(self):
        global DEFAULT_GRAPH
        temp = DEFAULT_GRAPH
        DEFAULT_GRAPH = self
        yield
        DEFAULT_GRAPH = temp

    @staticmethod
    def get_default():
        return DEFAULT_GRAPH

    @staticmethod
    def clear_default():
        """TODO: Docstring for clear_default.
        """
        global DEFAULT_GRAPH
        DEFAULT_GRAPH = Graph('default')

    def name_in_graph(self, node=None, edge=None):
        if node is not None:
            return node in self.nodes
        elif edge is not None:
            return edge in self.edges
        else:
            msg = 'User must specify node or edges argument'
            raise ValueError(msg)

    def collect_inputs(self):
        inputs = {
            node.name: node
            for node in self.nodes
            if node.type == 'Input'}
        return inputs

    def collect_outputs(self):
        outputs = {
            node.name: node
            for node in self.nodes
            if node.type == 'Output'}
        return outputs

    def render(self, engine='tensorflow'):
        engine = engines.select_engine(engine)
        compute = engine.render(self)
        return compute

    class NameCollisionError(Exception):
        pass


DEFAULT_GRAPH = Graph('default')
