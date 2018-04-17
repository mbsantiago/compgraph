from __future__ import print_function

import glob
import os
import unittest
import compgraph as cg


class EdgeTests(unittest.TestCase):
    # def setUp(self):
    #     self.graph = cg.Graph(name='edge_tests_graph')
    #     with self.graph.as_default():
    #         yield

    def test_load_edges_from_directory(self):
        from compgraph.core.edge import load_edges_from_directory

        directory = os.path.join(cg.PKG_DIR, 'edges')
        descriptions = load_edges_from_directory(directory)
        num_descriptions = len(descriptions)

        num_edge_files = len(glob.glob(os.path.join(directory, '*.json')))

        self.assertEqual(num_edge_files, num_descriptions)


