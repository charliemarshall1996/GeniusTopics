import unittest
import pandas as pd
from geniustopics.preprocessing import *


class TestRemoveNewLine(unittest.TestCase):

    def test_remove_new_line(self):
        txt = "test new line\n"
        expected = "test new line"
        actual = remove_new_line(txt)
        self.assertEqual(actual, expected)

    def test_remove_new_line_multi(self):
        txt = "test new line\n test new line\n test new line\n"
        expected = "test new line test new line test new line"
        actual = remove_new_line(txt)
        self.assertEqual(actual, expected)

    def test_remove_new_line_multi_line(self):
        txt = """test new line\n
 test new line\n
 test new line\n"""
        expected = """test new line test new line test new line"""
        actual = remove_new_line(txt)
        self.assertEqual(actual, expected)


class TestRemoveNewLineEdge(unittest.TestCase):

    def test_remove_new_line_no_escape(self):
        txt = "test new line"
        expected = "test new line"
        actual = remove_new_line(txt)
        self.assertEqual(actual, expected)

    def test_remove_new_line_all_escape(self):
        txt = "\n\n\n\n\n\n"
        expected = ""
        actual = remove_new_line(txt)
        self.assertEqual(actual, expected)

    def test_remove_new_line_long_string(self):
        txt = "test new line\n test new line\n test new line\n test new line\n test new line\n test new line\n test new line\n test new line\n test new line\n test new line\n test new line\n"
        expected = "test new line test new line test new line test new line test new line test new line test new line test new line test new line test new line test new line"
        actual = remove_new_line(txt)
        self.assertEqual(actual, expected)

    def test_remove_new_line_empty_string(self):
        txt = ""
        expected = ""
        actual = remove_new_line(txt)
        self.assertEqual(actual, expected)


class TestRemoveNewLineNegative(unittest.TestCase):

    def test_remove_new_line_none(self):
        txt = None
        actual = remove_new_line(txt)
        self.assertEqual(actual, "")

    def test_remove_new_line_int(self):
        txt = 1
        actual = remove_new_line(txt)
        self.assertEqual(actual, "")

    def test_remove_new_line_bool(self):
        txt = False
        actual = remove_new_line(txt)
        self.assertEqual(actual, "")

    def test_remove_new_line_list(self):
        txt = ["test new line \n"]
        actual = remove_new_line(txt)
        self.assertEqual(actual, "")


if __name__ == "__main__":
    unittest.main()
