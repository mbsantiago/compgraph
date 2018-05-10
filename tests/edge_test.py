from __future__ import print_function

import glob
import os
import unittest
import compgraph as cg

from compgraph.core.edge import load_edges_from_directory
from compgraph.core.edge import build_class_from_description


class EdgeTests(unittest.TestCase):
    # def setUp(self):
    #     self.graph = cg.Graph(name='edge_tests_graph')
    #     with self.graph.as_default():
    #         yield

    def test_load_edges_from_directory(self):
        directory = os.path.join(cg.PKG_DIR, 'edges')
        descriptions = load_edges_from_directory(directory)
        num_descriptions = len(descriptions)

        num_edge_files = len(glob.glob(os.path.join(directory, '*.json')))

        self.assertEqual(num_edge_files, num_descriptions)

    def test_make_edge_classes_from_directory(self):
        directory = os.path.join(cg.PKG_DIR, 'edges')
        descriptions = load_edges_from_directory(directory)

        for description in descriptions:
            build_class_from_description(description)

        help(cg.Identity)
        self.assertEqual(1, 2)
