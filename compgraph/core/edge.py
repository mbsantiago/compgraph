import abc
import os
import glob
import uuid
import json

from compgraph.utils import make_namespace_from_dict
from compgraph.core.parser import make_parser
from compgraph.core.parser import parse_transformation

MANDATORY_FIELDS = [
    'name',
    'inputs',
    'outputs',
    'shape_transformations',
    'parameters',
    'description'
]


class Edge(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, type, name=None, device=None, inputs=None, outputs=None):
        self.type = type
        self.inputs = inputs
        self.outputs = outputs

        self.name = uuid.uuid4() if name is None else name
        self.device = device

    @abc.abstractmethod
    def output_shape(self, input_shape):
        pass

    @abc.abstractmethod
    def shape_transform(self):
        pass

    @abc.abstractmethod
    def perceptual_field(self):
        pass


class EdgeDescription(object):
    def __init__(self, dictionary):
        type(self).check_field_validity(dictionary)

        for key in MANDATORY_FIELDS:
            setattr(self, key, dictionary[key])

        other_keys = [
            key for key in dictionary
            if key not in MANDATORY_FIELDS]

        for key in other_keys:
            value = dictionary[key]
            if isinstance(value, dict):
                value = make_namespace_from_dict(value)
            setattr(self, key, value)

    def parse_output_transformation(self, output):
        if output not in self.outputs:
            raise ValueError('Output {} is not part of Edge description'.format(output))

    def __repr__(self):
        msg = 'Edge {}:\n\t{}'.format(self.name, self.description)
        return msg

    class InvalidDescription(Exception):
        pass

    @staticmethod
    def check_field_validity(dictionary):
        for field in MANDATORY_FIELDS:
            if not field in dictionary:
                msg = '{} field is missing from '.format(field)
                msg += 'edge description: \n'
                msg += '\t{}'.format(dictionary)
                raise EdgeDescription.InvalidDescription(msg)


def build_class_from_description(description):
    def output_shape(self, input_shape):
        #TODO define method based on description
        pass

    def shape_transform(self):
        #TODO define method based on description
        pass

    def perceptual_field(self):
        #TODO define method based on description
        pass

    name = description.name
    methods = {
        'output_shape': output_shape,
        'shape_transform': shape_transform,
        'perceptual_field': perceptual_field
    }
    newclass = type(name, (Edge,), methods)
    return newclass

def parse_transformations(path):
    descriptions = load_edges_from_directory(path)
    parser = make_parser()

    for description in descriptions:
        parse_transformation(parser, description)


def load_edges_from_directory(path):
    all_edges_in_path = glob.glob(os.path.join(path, '*.json'))
    edge_descriptions = []
    for file in all_edges_in_path:
        with open(file, 'r') as jsonfile:
            description = json.load(jsonfile)
        edge_descriptions.append(EdgeDescription(description))
    return edge_descriptions

parse_transformations('../edges/')
