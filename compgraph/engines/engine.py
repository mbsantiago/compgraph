import os
import abc
import functools


def discover_engines():
    engines = [name for name in os.listdir('.') if not os.path.isfile(name)]
    return engines


def select_engine(engine_name):
    if not os.path.exists(engine_name):
        msg = 'Engine selected {} is mis-named or does not exist.\n'
        msg = msg.format(engine_name)
        msg = 'Select one of the following:'
        for engine_name in discover_engines():
            msg += '\t- {}\n'.format(engine_name)
        IOError(msg)
    return Engine(engine_name)


class Operation(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, name):
        self.name = name


class Engine(object):
    def __init__(self, engine_name, config=None):
        self.engine_name = engine_name
        self.config = config

    def render(self, graph):
        def compute(**kwargs):
            return None
        return compute

