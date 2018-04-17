"""Module for Node definition"""
import abc
import uuid

from . import graph as grph


class BaseNode(object):
    __metaclass__ = abc.ABCMeta

    def __init__(
            self,
            name=None,
            device=None,
            shape=None,
            fix_shape=False,
            type=None,
            graph=None):

        self.graph = grph.DEFAULT_GRAPH if graph is None else graph
        self.name = uuid.uuid4() if name is None else name
        self.device = device
        self._shape = shape
        self._fix_shape = fix_shape

        # Add node to graph
        self.graph.add_node(self)

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, new_shape):
        if self._fix_shape:
            raise self.FixedShapeError
        self._shape = new_shape

    def fix_shape(self):
        self._fix_shape = True

    def toggle_fix_shape(self):
        self._fix_shape = not self._fix_shape

    def set_device(self, device):
        self.device = device

    def __repr__(self):
        node_type = '{} Object'.format(self.type)
        msg = '{:^15}:: Name : {}'.format(node_type, self.name)
        msg += ' ' * 18 + 'Shape : {}'.format(self.shape)
        msg += ' ' * 18 + '@ Graph : {}'.format(self.graph.name)
        return msg

    class FixedShapeError(Exception):
        pass


class Node(BaseNode):
    type = 'Node'


class InputNode(BaseNode):
    type = 'Input'


class OutputNode(BaseNode):
    type = 'Output'
