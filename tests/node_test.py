import unittest
import compgraph as cg

class NodeTests(unittest.TestCase):
    def test_name_has_info(self):
        graph_name = 'custom'
        node_name = 'node1'

        node_shape = [20, 10, 5]
        shape_representation = str(node_shape)

        graph = cg.Graph(name=graph_name)
        with graph.as_default():
            node = cg.Node(name=node_name, shape=node_shape)

        representation = str(node)
        self.assertTrue(node_name in representation)
        self.assertTrue(graph_name in representation)
        self.assertTrue(shape_representation in representation)

    def test_device_setting(self):
        node = cg.Node()

        device = '/CPU:0'
        node.set_device(device)

        self.assertEqual(node.device, device)

    def test_shape_fixing(self):
        node = cg.Node()

        shape = [10, 20, 30]
        node.shape = shape

        self.assertEqual(node.shape, shape)

        node.toggle_fix_shape()

        shape = [20, 20]
        def change_shape():
            node.shape = shape

        self.assertRaises(
            cg.Node.FixedShapeError,
            change_shape)

        node.toggle_fix_shape()
        node.shape = shape
        self.assertEqual(node.shape, shape)

        shape = [20, 10]
        node.fix_shape()
        def change_shape():
            node.shape = shape

        self.assertRaises(
            cg.Node.FixedShapeError,
            change_shape)


