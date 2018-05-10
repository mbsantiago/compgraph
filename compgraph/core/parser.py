from __future__ import print_function
from __future__ import division

import math
from lark import Lark
from compgraph.core.shapes import Shape

GRAMMAR = '''
expression: shape
    | numeric

shape.100 : ATOMIC -> atomic
    | shape op shape -> operation
    | "(" shape op shape ")" -> operation
    | shape ":" shape -> shape_concat
    | shape "[" slice "]" -> shape_slice
    | numeric op shape -> operation
    | shape op numeric -> operation
    | func "(" shape ")" -> func
    | shape "[" list "]" -> shape_list
    | shape "[" shape "]" -> shape_list
    | "(" shape ")" -> parens
    | "[" list "]" -> constant_shape
    | "[" numeric "]" -> constant_shape

list: (numeric ",")+ numeric

slice : numeric ":" numeric -> normal_slice
    | numeric ":" -> start_slice
    | ":" numeric -> end_slice
    | numeric ":" numeric ":" numeric -> full_strided_slice
    | ":" numeric ":" numeric -> end_strided_slice
    | numeric "::" numeric -> start_strided_slice
    | "::" numeric -> strided_slice

numeric : SIGNED_NUMBER -> atomic_number
    | shape "[" numeric "]" -> shape_get
    | numeric op numeric -> operation
    | func "(" numeric ")" -> func
    | numfunc "(" shape ")" -> func
    | ATOMIC_NUM -> atomic
    | ATOMIC "==" LITERAL -> literal_match
    | ATOMIC_NUM "==" LITERAL -> literal_match
    | "(" numeric ")" -> parens

func: "floor" -> floor
    | "ceil" -> ceiling

numfunc: "prod" -> product
    | "sum" -> sum
    | "dim" -> dim

op: "/" -> div
    | "*" -> prod
    | "%" -> mod
    | "+" -> add
    | "-" -> sub

ATOMIC : "$" /\w+/
ATOMIC_NUM : "#" /\w+/
LITERAL : /\w+/
%import common.SIGNED_NUMBER
%import common.WS
%ignore WS
'''


def make_parser():
    parser = Lark(GRAMMAR, start='expression')
    return parser


def parse_transformation(parser, edge_description):
    for output_name, transformation in edge_description.shape_transformations.items():
        pass


def evaluate_node(node, **kwargs):
    node_type = node.data
    childs = node.children

    if node_type == 'expression':
        return evaluate_node(childs[0], **kwargs)

    if node_type == 'atomic':
        value = kwargs[childs[0].value[1:]]
        if isinstance(value, (list, tuple)):
            value = Shape(value)
        else:
            value = float(value)
        return value

    if node_type == 'operation':
        argument1 = evaluate_node(childs[0], **kwargs)
        argument2 = evaluate_node(childs[2], **kwargs)
        operation = childs[1]
        if operation.data == 'add':
            return argument1 + argument2
        if operation.data == 'prod':
            return argument1 * argument2
        if operation.data == 'sub':
            return argument1 - argument2
        if operation.data == 'div':
            return argument1 / argument2
        if operation.data == 'mod':
            return argument1 % argument2

    if node_type == 'list':
        values = [
            evaluate_node(child, **kwargs)
            for child in childs
        ]
        return Shape(values)

    if node_type == 'shape_list':
        shape = evaluate_node(childs[0], **kwargs)
        shape_list = evaluate_node(childs[1], **kwargs)
        return Shape([shape[x] for x in shape_list])

    if node_type == 'atomic_number':
        return int(childs[0].value)

    if node_type == 'shape_slice':
        shape = evaluate_node(childs[0], **kwargs)
        shape_slice = evaluate_node(childs[1], **kwargs)
        return Shape(shape[shape_slice])

    if node_type == 'normal_slice':
        start = evaluate_node(childs[0], **kwargs)
        end = evaluate_node(childs[1], **kwargs)
        return slice(start, end)

    if node_type == 'start_slice':
        start = evaluate_node(childs[0], **kwargs)
        return slice(start, None)

    if node_type == 'end_slice':
        end = evaluate_node(childs[0], **kwargs)
        return slice(None, end)

    if node_type == 'full_strided_slice':
        start = evaluate_node(childs[0], **kwargs)
        end = evaluate_node(childs[1], **kwargs)
        stride = evaluate_node(childs[2], **kwargs)
        return slice(start, end, stride)

    if node_type == 'strided_slice':
        stride = evaluate_node(childs[0], **kwargs)
        return slice(None, None, stride)

    if node_type == 'end_strided_slice':
        end = evaluate_node(childs[0], **kwargs)
        stride = evaluate_node(childs[1], **kwargs)
        return slice(None, end, stride)

    if node_type == 'start_strided_slice':
        start = evaluate_node(childs[0], **kwargs)
        stride = evaluate_node(childs[1], **kwargs)
        return slice(start, None, stride)

    if node_type == 'func':
        func = childs[0].data
        argument = evaluate_node(childs[1], **kwargs)
        if func == 'floor':
            if isinstance(argument, (int, float)):
                return int(math.floor(argument))
            if isinstance(argument, Shape):
                return [int(math.floor(dim)) for dim in argument]
        if func == 'sum':
            return int(sum(argument))
        if func == 'dim':
            return len(argument)
        if func == 'ceiling':
            if isinstance(argument, (int, float)):
                return int(math.ceil(argument))
            if isinstance(argument, Shape):
                return [int(math.ceil(dim)) for dim in argument]
        if func == 'product':
            product = 1
            for dim in argument:
                product *= dim
            return product

    if node_type == 'shape_concat':
        shape1 = evaluate_node(childs[0], **kwargs)
        shape2 = evaluate_node(childs[1], **kwargs)
        return Shape.concat(shape1, shape2)

    if node_type == 'constant_shape':
        return evaluate_node(childs[0], **kwargs)

    if node_type == 'shape_get':
        shape = evaluate_node(childs[0], **kwargs)
        index = evaluate_node(childs[1], **kwargs)
        return shape[index]

    if node_type == 'parens':
        return evaluate_node(childs[0], **kwargs)

    if node_type == 'literal_match':
        variable = childs[0].value[1:]
        literal = childs[1].value
        return kwargs[variable] == literal


def make_transformation_from_string(parser, string):
    tree = parser.parse(string)
    variables = [atom.children[0].value[1:] for atom in tree.find_data('atomic')]
    def transformation(**kwargs):
        return evaluate_node(tree, **kwargs)
    return variables, transformation


PARSER = make_parser()
