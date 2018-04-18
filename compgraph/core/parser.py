from __future__ import print_function
from __future__ import division

import math
from lark import Lark
from compgraph.core.shapes import Shape

GRAMMAR = '''
start: expresion
    | numeric

expresion.100 : ATOMIC -> atomic
    | expresion op expresion -> expresion_op
    | "(" expresion op expresion ")" -> expresion_op_braces
    | expresion ":" expresion -> expresion_concat
    | expresion "[" slice "]" -> expresion_slice
    | numeric op expresion -> expresion_nl_op
    | expresion op numeric -> expresion_nr_op
    | func "(" expresion ")" -> func
    | "[" list "]" -> constant_shape

list: [list ","] numeric

slice : expresion -> slice_from_expresion
    | list -> slice_from_expresion
    | numeric ":" numeric -> normal_slice
    | numeric ":" -> start_slice
    | ":" numeric -> end_slice
    | numeric ":" numeric ":" numeric -> full_strided_slice
    | ":" numeric ":" numeric -> end_strided_slice
    | numeric "::" numeric -> start_strided_slice
    | "::" numeric -> strided_slice

numeric : SIGNED_NUMBER -> atomic_number
    | expresion "[" numeric "]" -> expresion_get
    | numeric op numeric -> numeric_op
    | func "(" numeric ")" -> func
    | ATOMIC -> atomic
    | ATOMIC "==" LITERAL -> literal_match
    | "(" numeric ")" -> braced_numeric

func: "floor" -> floor
    | "ceil" -> ceiling
    | "prod" -> product
    | "sum" -> sum

op: "/" -> div
    | "*" -> prod
    | "%" -> mod
    | "+" -> add
    | "-" -> sub

ATOMIC : "$" /\w+/

LITERAL : "#" /\w+/
%import common.SIGNED_NUMBER
%import common.WS
%ignore WS
'''


def make_parser():
    parser = Lark(GRAMMAR)
    return parser


def parse_transformation(parser, edge_description):
    for output_name, transformation in edge_description.shape_transformations.items():
        print(parser.parse(transformation))


def evaluate_node(node, **kwargs):
    if node.data == 'start':
        return evaluate_node(node.children[0], **kwargs)

    if node.data == 'atomic':
        value = kwargs[node.children[0].value[1:]]
        if isinstance(value, (list, tuple)):
            value = Shape(value)
        return value
    if '_op' in node.data:
        argument1 = evaluate_node(node.children[0], **kwargs)
        argument2 = evaluate_node(node.children[2], **kwargs)
        operation = node.children[1]
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

    if node.data == 'list':
        current = node
        values = [evaluate_node(current.children[-1], **kwargs)]
        while len(current.children) > 1:
            current = current.children[0]
            values.append(evaluate_node(current.children[-1], **kwargs))
        return Shape(values[::-1])

    if node.data == 'atomic_number':
        return int(node.children[0].value)

    if node.data == 'expresion_slice':
        argument1 = evaluate_node(node.children[0], **kwargs)
        argument2 = evaluate_node(node.children[1], **kwargs)

        if isinstance(argument2, Shape):
            return Shape([argument1[x] for x in argument2])

        if isinstance(argument2, slice):
            return Shape(argument1[argument2])

    if node.data == 'slice_from_expresion':
        return evaluate_node(node.children[0], **kwargs)

    if node.data == 'normal_slice':
        argument1 = evaluate_node(node.children[0], **kwargs)
        argument2 = evaluate_node(node.children[1], **kwargs)
        return slice(argument1, argument2)

    if node.data == 'start_slice':
        argument1 = evaluate_node(node.children[0], **kwargs)
        return slice(argument1, None)

    if node.data == 'end_slice':
        argument1 = evaluate_node(node.children[0], **kwargs)
        return slice(None, argument1)

    if node.data == 'full_strided_slice':
        argument1 = evaluate_node(node.children[0], **kwargs)
        argument2 = evaluate_node(node.children[1], **kwargs)
        argument3 = evaluate_node(node.children[2], **kwargs)
        return slice(argument1, argument2, argument3)

    if node.data == 'strided_slice':
        argument1 = evaluate_node(node.children[0], **kwargs)
        return slice(None, None, argument1)

    if node.data == 'end_strided_slice':
        argument1 = evaluate_node(node.children[0], **kwargs)
        argument2 = evaluate_node(node.children[1], **kwargs)
        return slice(None, argument1, argument2)

    if node.data == 'start_strided_slice':
        argument1 = evaluate_node(node.children[0], **kwargs)
        argument2 = evaluate_node(node.children[1], **kwargs)
        return slice(argument1, None, argument2)

    if node.data == 'func':
        func = node.children[0].data
        argument = evaluate_node(node.children[1], **kwargs)
        if func == 'floor':
            if isinstance(argument, (int, float)):
                return int(math.floor(argument))
            if isinstance(argument, Shape):
                return [int(math.floor(dim)) for dim in argument]
        if func == 'sum':
            return int(sum(argument))
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

    if node.data == 'expresion_concat':
        argument1 = evaluate_node(node.children[0], **kwargs)
        argument2 = evaluate_node(node.children[1], **kwargs)
        return Shape.concat(argument1, argument2)

    if node.data == 'constant_shape':
        return evaluate_node(node.children[0], **kwargs)

    if node.data == 'expresion_get':
        argument1 = evaluate_node(node.children[0], **kwargs)
        argument2 = evaluate_node(node.children[1], **kwargs)
        return argument1[argument2]

    if node.data == 'braced_numeric':
        return evaluate_node(node.children[0], **kwargs)

    if node.data == 'literal_match':
        variable = node.children[0].value[1:]
        literal = node.children[1].value[1:]
        return kwargs[variable] == literal


def make_transformation_from_tree(tree):
    variables = [atom.children[0].value[1:] for atom in tree.find_data('atomic')]

    def transformation(**kwargs):
        return evaluate_node(tree, **kwargs)

    return transformation
