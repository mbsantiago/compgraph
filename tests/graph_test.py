import unittest
import compgraph as cg

class GraphTests(unittest.TestCase):
    def tearDown(self):
        cg.Graph.clear_default()

    def test_use_different_graph(self):
        new_graph = cg.Graph()

        with new_graph.as_default():
            node = cg.Node(name='nodo1')

        self.assertEqual(len(new_graph.nodes), 1)
        self.assertEqual(len(cg.Graph.get_default().nodes), 0)

    def test_no_name_collision_for_many_nodes(self):
        N = 10000
        for _ in range(N):
            cg.Node()
        self.assertEqual(len(cg.Graph.get_default().nodes), N)

    def test_name_collision(self):
        def make_two_nodes_with_same_name():
            node1 = cg.Node(name='node')
            node2 = cg.Node(name='node')

        self.assertRaises(
            cg.Graph.NameCollisionError,
            make_two_nodes_with_same_name)

if __name__ == "__main__":
    unittest.main()
