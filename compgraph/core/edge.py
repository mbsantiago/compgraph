import abc
import os
import glob
import uuid
import json

from six import iteritems
from six import itervalues

import compgraph as cg
from compgraph.utils import make_namespace_from_dict
from compgraph.core.parser import make_transformation_from_string
from compgraph.core.parser import PARSER as parser

MANDATORY_FIELDS = [
    'name',
    'inputs',
    'outputs',
    'shape_transformations',
    'attributes',
    'description'
]

OPTIONAL_FIELDS = [
    'defaults',
    'variables'
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
            # if isinstance(value, dict):
            #     value = make_namespace_from_dict(value)
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


def build_init(description):
    # Attributes field contain information
    # required for edge construction
    attributes = sorted(description.attributes)
    inputs = sorted(description.inputs)

    # Check for defaults
    try:
        defaults = description.defaults
    except:
        defaults = {}

    # Separating optional and required arguments
    # for construction
    optional_arguments = sorted(defaults.keys())
    required_arguments = inputs + sorted([
        attr for attr in attributes
        if attr not in optional_arguments])
    num_args = len(required_arguments)

    # Making usage string
    name = description.name
    usage_string = "{}(".format(name)
    for arg in required_arguments:
        usage_string += "{}, ".format(arg)
    for arg in optional_arguments[:-1]:
        usage_string += "{}=None, ".format(arg)
    if len(optional_arguments) > 0:
        arg = optional_arguments[-1]
        usage_string += "{}=None".format(arg)
    usage_string += ")"

    # Making the docstring for init function
    # Making arguments list
    args_string = ''
    for arg in required_arguments:
        if arg in inputs:
            args_string += '    {} (Node): Edge input.\n'.format(arg)
        else:
            args_string += '    {}: Edge configuration.\n'.format(arg)

    kwargs_string = ''
    if len(optional_arguments) > 0:
        kwargs_string += '\nOptional arguments:\n'
        for arg in optional_arguments:
            kwargs_string += '    {}: Edge configuration\n'.format(arg)

    doc_string = """{name} edge construction.

Args:
{args}
{kwargs}
Returns:
    {name} Object
""".format(name=name, args=args_string, kwargs=kwargs_string)

    def init(self, *args, **kwargs):
        if len(args) != num_args:
            msg = "Incorrect number of arguments for "
            msg += "{} construction. Usage:\n".format(name)
            msg += usage_string
            raise ValueError(msg)

        for user_arg, attr in zip(args, required_arguments):
            setattr(self, attr, user_arg)

        for opt_arg in optional_arguments:
            try:
                setattr(self, opt_art, kwargs[opt_arg])
            except KeyError:
                default = parse_defaults()
                setattr(self, opt_art, default)

    init.__doc__ = doc_string

    return init


def parse_defaults():
    return None


def build_class_from_description(description):
    # Build docstring from description
    docstring = '''{} edge.

{}
'''.format(description.name, description.description)

    # Build get_output_shape method
    vars_and_transformations = {
        output: make_transformation_from_string(parser, string)
        for output, string in iteritems(description.shape_transformations)
    }

    variables = [
        variable for pair in itervalues(vars_and_transformations)
        for variable in pair[0]]

    init_func = build_init(description)

    name = str(description.name)
    methods = {
        '__init__': init_func,
        '__doc__': docstring
    }
    newclass = type(name, (object,), methods)
    Edge.register(newclass)
    setattr(cg, name, newclass)


# def parse_transformations(path):
#     descriptions = load_edges_from_directory(path)
#     parser = make_parser()
#
#     for description in descriptions:
#         parse_transformation(parser, description)


def load_edges_from_directory(path):
    all_edges_in_path = glob.glob(os.path.join(path, '*.json'))
    edge_descriptions = []
    for file in all_edges_in_path:
        with open(file, 'r') as jsonfile:
            description = json.load(jsonfile)
        edge_descriptions.append(EdgeDescription(description))
    return edge_descriptions


def add_edge_from_description(dict_description):
    description = EdgeDescription(dict_description)


def initialize_edge_module():
    # TODO check for user defined edge directories
    pass

