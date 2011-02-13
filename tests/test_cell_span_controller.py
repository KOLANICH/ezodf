#!/usr/bin/env python
#coding:utf-8
# Author:  mozman -- <mozman@gmx.at>
# Purpose: test cell spanning controller
# Created: 13.02.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

import sys
import unittest

# trusted objects
from ezodf.xmlns import etree, CN, wrap
from ezodf.tablerowcontroller import TableRowController
from ezodf.tableutils import iter_cell_range

# object to test
from ezodf.cellspancontroller import CellSpanController


class TestCellSpanController(unittest.TestCase):
    def setUp(self):
        self.table = etree.Element(CN('table:table'))
        self.table_row_controller = TableRowController(self.table)
        self.table_row_controller.reset(size=(10, 10))
        self.span_controller = CellSpanController(self.table_row_controller)

    def get_cell(self, pos):
        return wrap(self.table_row_controller.get_cell(pos))

    def set_span(self, pos, size):
        cell = self.get_cell(pos)
        cell._set_span(size)

    def is_covered(self, pos):
        return self.get_cell(pos).covered

    def test_cell_is_not_spanning(self):
        self.assertFalse(self.span_controller.is_cell_spanning((0, 0)))

    def test_cell_is_spanning(self):
        self.set_span(pos=(0, 0), size=(2, 2))
        self.assertTrue(self.span_controller.is_cell_spanning((0, 0)))

    def test_span_cell(self):
        pos = (0, 0)
        size = (3, 3)
        self.span_controller.set_span(pos, size)
        for cell_index in (x for x in iter_cell_range(pos, size) if x != pos):
            self.assertTrue(self.is_covered(cell_index), "cell %s is not covered." % str(cell_index))

    def test_error_on_row_spanning_over_table_limits(self):
        with self.assertRaises(ValueError):
            self.span_controller.set_span((0,0), (11, 1))

    def test_error_on_column_spanning_over_table_limits(self):
        with self.assertRaises(ValueError):
            self.span_controller.set_span((0,0), (1, 11))

    def test_do_not_span_already_spanned_cells(self):
        self.span_controller.set_span(pos=(2, 2), size=(2, 2))
        with self.assertRaises(ValueError):
            self.span_controller.set_span(pos=(2, 2), size=(2, 2))

    def test_do_not_span_over_already_spanned_cells(self):
        self.span_controller.set_span(pos=(2, 2), size=(2, 2))
        with self.assertRaises(ValueError):
            self.span_controller.set_span(pos=(0, 0), size=(3, 3))

    def test_remove_span(self):
        pos = (0, 0)
        size = (3, 3)
        self.span_controller.set_span(pos, size)
        self.span_controller.remove_span(pos)
        self.assertEqual((1, 1), self.get_cell(pos).span, "cell at %s is spanned." % str(pos))
        for cell_index in (x for x in iter_cell_range(pos, size) if x != pos):
            self.assertFalse(self.is_covered(cell_index), "cell %s is covered." % str(cell_index))

if __name__=='__main__':
    unittest.main()