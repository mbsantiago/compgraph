import unittest
import os

from compgraph.core.parser import make_parser
from compgraph.core.parser import make_transformation_from_string

class ParserTests(unittest.TestCase):
    def setUp(self):
        self.parser = make_parser()

    def test_parser_all_grammar(self):
        # Atomic
        input = [0, 1, 2]
        string = '$input'
        _, transformation = make_transformation_from_string(self.parser, string)
        output = transformation(input=input)
        self.assertEqual(output, input)

        # Numeric with braces
        input = 1
        string = '(#input)'
        _, transformation = make_transformation_from_string(self.parser, string)
        output = transformation(input=input)
        self.assertEqual(output, input)


        # Expresion concatenation
        input1 = [0, 1, 2]
        input2 = [3, 4, 5]
        string = '$input1:$input2'
        _, transformation = make_transformation_from_string(self.parser, string)
        output = transformation(input1=input1, input2=input2)
        self.assertEqual(output, input1 + input2)

        # Expresion operation
        # add
        input1 = [0, 1, 2]
        input2 = [3, 4, 5]
        string = '$input1 + $input2'
        _, transformation = make_transformation_from_string(self.parser, string)
        output = transformation(input1=input1, input2=input2)
        self.assertEqual(output, [3, 5, 7])

        # prod
        string = '$input1 * $input2'
        _, transformation = make_transformation_from_string(self.parser, string)
        output = transformation(input1=input1, input2=input2)
        self.assertEqual(output, [0, 4, 10])

        # mod
        input1 = [4, 6, 8]
        input2 = [2, 4, 3]
        string = '$input1 % $input2'
        _, transformation = make_transformation_from_string(self.parser, string)
        output = transformation(input1=input1, input2=input2)
        self.assertEqual(output, [0, 2, 2])

        # sub
        input1 = [4, 6, 8]
        input2 = [2, 4, 3]
        string = '$input1 - $input2'
        _, transformation = make_transformation_from_string(self.parser, string)
        output = transformation(input1=input1, input2=input2)
        self.assertEqual(output, [2, 2, 5])

        # div
        input1 = [4, 6, 8]
        input2 = [2, 3, 4]
        string = '$input1 / $input2'
        _, transformation = make_transformation_from_string(self.parser, string)
        output = transformation(input1=input1, input2=input2)
        self.assertEqual(output, [2, 2, 2])

        # Expresion Numeric operation
        # add
        input1 = [0, 1, 2]
        input2 = 2
        string = '$input1 + #input2'
        _, transformation = make_transformation_from_string(self.parser, string)
        output = transformation(input1=input1, input2=input2)
        self.assertEqual(output, [2, 3, 4])

        # prod
        string = '$input1 * #input2'
        _, transformation = make_transformation_from_string(self.parser, string)
        output = transformation(input1=input1, input2=input2)
        self.assertEqual(output, [0, 2, 4])

        # mod
        input1 = [4, 6, 8]
        input2 =  5
        string = '$input1 % #input2'
        _, transformation = make_transformation_from_string(self.parser, string)
        output = transformation(input1=input1, input2=input2)
        self.assertEqual(output, [4, 1, 3])

        # sub
        input1 = [4, 6, 8]
        input2 =  2
        string = '$input1 - #input2'
        _, transformation = make_transformation_from_string(self.parser, string)
        output = transformation(input1=input1, input2=input2)
        self.assertEqual(output, [2, 4, 6])

        # div
        input1 = [4, 6, 8]
        input2 = 2
        string = '$input1 / #input2'
        _, transformation = make_transformation_from_string(self.parser, string)
        output = transformation(input1=input1, input2=input2)
        self.assertEqual(output, [2, 3, 4])


        # Numeric Numeric operation
        # add
        input1 = 2
        input2 = 2
        string = '#input1 + #input2'
        _, transformation = make_transformation_from_string(self.parser, string)
        output = transformation(input1=input1, input2=input2)
        self.assertEqual(output, 4)

        # prod
        string = '#input1 * #input2'
        _, transformation = make_transformation_from_string(self.parser, string)
        output = transformation(input1=input1, input2=input2)
        self.assertEqual(output, 4)

        # mod
        input1 = 5
        input2 = 4
        string = '#input1 % #input2'
        _, transformation = make_transformation_from_string(self.parser, string)
        output = transformation(input1=input1, input2=input2)
        self.assertEqual(output, 1)

        # sub
        input1 = 7
        input2 = 2
        string = '#input1 - #input2'
        _, transformation = make_transformation_from_string(self.parser, string)
        output = transformation(input1=input1, input2=input2)
        self.assertEqual(output, 5)

        # div
        input1 = 5
        input2 = 2
        string = '#input1 / #input2'
        _, transformation = make_transformation_from_string(self.parser, string)
        output = transformation(input1=input1, input2=input2)
        self.assertEqual(output, 2.5)

        # Expresion func
        # floor
        input = [1, 1.5, 2]
        string = 'floor($input)'
        _, transformation = make_transformation_from_string(self.parser, string)
        output = transformation(input=input)
        self.assertEqual(output, [1, 1, 2])

        # ceil
        input = [1, 1.5, 2]
        string = 'ceil($input)'
        _, transformation = make_transformation_from_string(self.parser, string)
        output = transformation(input=input)
        self.assertEqual(output, [1, 2, 2])

        # prod
        input = [2, 3, 4]
        string = 'prod($input)'
        _, transformation = make_transformation_from_string(self.parser, string)
        output = transformation(input=input)
        self.assertEqual(output, 24)

        # sum
        input = [2, 3, 4]
        string = 'sum($input)'
        _, transformation = make_transformation_from_string(self.parser, string)
        output = transformation(input=input)
        self.assertEqual(output, 9)

        # Numeric func
        # floor
        input = 1.5
        string = 'floor(#input)'
        _, transformation = make_transformation_from_string(self.parser, string)
        output = transformation(input=input)
        self.assertEqual(output, 1)

        # ceil
        input = 1.5
        string = 'ceil(#input)'
        _, transformation = make_transformation_from_string(self.parser, string)
        output = transformation(input=input)
        self.assertEqual(output, 2)

        # List
        string = '[1,2,3]'
        _, transformation = make_transformation_from_string(self.parser, string)
        output = transformation()
        self.assertEqual(output, [1, 2, 3])

        # Expresion list
        input = [0,1,2,3,4,5,6]
        string = '$input[1, 3, 4]'
        _, transformation = make_transformation_from_string(self.parser, string)
        output = transformation(input=input)
        self.assertEqual(output, [1, 3, 4])

        # Slices
        # Slice from expresion
        input = [0, 1, 2, 3, 4]
        permutation = [2, 1, 4, 3, 0]
        string = '$input[$permutation]'
        _, transformation = make_transformation_from_string(self.parser, string)
        output = transformation(input=input, permutation=permutation)
        self.assertEqual(output, [2, 1, 4, 3, 0])

        # Normal slice
        input = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        string = '$input[3:6]'
        _, transformation = make_transformation_from_string(self.parser, string)
        output = transformation(input=input)
        self.assertEqual(output, [3, 4, 5])

        # Start slice
        string = '$input[3:]'
        _, transformation = make_transformation_from_string(self.parser, string)
        output = transformation(input=input)
        self.assertEqual(output, [3, 4, 5, 6, 7, 8])

        # End slice
        string = '$input[:5]'
        _, transformation = make_transformation_from_string(self.parser, string)
        output = transformation(input=input)
        self.assertEqual(output, [0, 1, 2, 3, 4])

        # Full strided slice
        string = '$input[2:8:2]'
        _, transformation = make_transformation_from_string(self.parser, string)
        output = transformation(input=input)
        self.assertEqual(output, [2, 4, 6])

        # End strided slice
        string = '$input[:5:2]'
        _, transformation = make_transformation_from_string(self.parser, string)
        output = transformation(input=input)
        self.assertEqual(output, [0, 2, 4])

        # Start strided slice
        string = '$input[5::2]'
        _, transformation = make_transformation_from_string(self.parser, string)
        output = transformation(input=input)
        self.assertEqual(output, [5, 7])

        # Strided slice
        string = '$input[::3]'
        _, transformation = make_transformation_from_string(self.parser, string)
        output = transformation(input=input)
        self.assertEqual(output, [0, 3, 6])

        # Strided slice reverse
        string = '$input[::-1]'
        _, transformation = make_transformation_from_string(self.parser, string)
        output = transformation(input=input)
        self.assertEqual(output, [8, 7, 6, 5, 4, 3, 2, 1, 0])

        # Expresion get
        string = '$input[-1]'
        _, transformation = make_transformation_from_string(self.parser, string)
        output = transformation(input=input)
        self.assertEqual(output, 8)

        string = '$input[4]'
        _, transformation = make_transformation_from_string(self.parser, string)
        output = transformation(input=input)
        self.assertEqual(output, 4)

        # Literal match
        string = '$input == true'
        _, transformation = make_transformation_from_string(self.parser, string)
        output1 = transformation(input='nottrue')
        self.assertFalse(output1)
        output2 = transformation(input='true')
        self.assertTrue(output2)

