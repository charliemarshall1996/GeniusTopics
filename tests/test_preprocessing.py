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


class TestStripTextWSqBrackets(unittest.TestCase):

    def test_strip_text_w_sq_brackets(self):
        txt = "[test strip square brackets]"
        expected = ""
        actual = strip_text_w_sq_brackets(txt)
        self.assertEqual(actual, expected)

    def test_strip_text_w_sq_brackets_in_str(self):
        txt = "[test strip square brackets]test strip square brackets"
        expected = "test strip square brackets"
        actual = strip_text_w_sq_brackets(txt)
        self.assertEqual(actual, expected)


class TestStripTextWSqBracketsEdge(unittest.TestCase):

    def test_strip_text_w_sq_brackets_empty_str(self):
        txt = ""
        expected = ""
        actual = strip_text_w_sq_brackets(txt)
        self.assertEqual(actual, expected)

    def test_strip_text_w_sq_brackets_empty_brackets(self):
        txt = "[]"
        expected = ""
        actual = strip_text_w_sq_brackets(txt)
        self.assertEqual(actual, expected)

    def test_strip_text_w_sq_brackets_long_string(self):
        txt = "test strip square brackets[test strip square brackets] test strip square brackets test strip square brackets test strip square brackets"
        expected = "test strip square brackets test strip square brackets test strip square brackets test strip square brackets"
        actual = strip_text_w_sq_brackets(txt)
        self.assertEqual(actual, expected)

    def test_strip_text_w_sq_brackets_long_string_inside(self):
        txt = '[test strip square brackets test strip square brackets test strip square brackets test strip square brackets test strip square brackets test strip square brackets]'
        expected = ""
        actual = strip_text_w_sq_brackets(txt)
        self.assertEqual(actual, expected)

    def test_strip_text_w_sq_brackets_nested(self):
        txt = '[test strip square brackets [test strip square brackets] test strip square brackets test strip square brackets]'
        expected = ""
        actual = strip_text_w_sq_brackets(txt)
        self.assertEqual(actual, expected)


class TestStripTextWSqBracketsNegative(unittest.TestCase):

    def test_strip_text_w_sq_brackets_none(self):
        txt = None
        actual = strip_text_w_sq_brackets(txt)
        self.assertEqual(actual, "")

    def test_strip_text_w_sq_brackets_int(self):
        txt = 1
        actual = strip_text_w_sq_brackets(txt)
        self.assertEqual(actual, "")

    def test_strip_text_w_sq_brackets_bool(self):
        txt = False
        actual = strip_text_w_sq_brackets(txt)
        self.assertEqual(actual, "")

    def test_strip_text_w_sq_brackets_list(self):
        txt = ["test strip square brackets"]
        actual = strip_text_w_sq_brackets(txt)
        self.assertEqual(actual, "")


class TestStripPunctuation(unittest.TestCase):
    def test_strip_punctuation_full_stop(self):
        txt = "test strip punctuation."
        expected = "test strip punctuation"
        actual = strip_punctuation(txt)
        self.assertEqual(actual, expected)

    def test_strip_punctuation_apos(self):
        txt = "test strip punctuation'"
        expected = "test strip punctuation"
        actual = strip_punctuation(txt)
        self.assertEqual(actual, expected)

    def test_strip_punctuation_comma(self):
        txt = "test strip punctuation,"
        expected = "test strip punctuation"
        actual = strip_punctuation(txt)
        self.assertEqual(actual, expected)

    def test_strip_punctuation_excl(self):
        txt = "test strip punctuation!"
        expected = "test strip punctuation"
        actual = strip_punctuation(txt)
        self.assertEqual(actual, expected)

    def test_strip_punctuation_amp(self):
        txt = "test strip punctuation&"
        expected = "test strip punctuation"
        actual = strip_punctuation(txt)
        self.assertEqual(actual, expected)


class TestStripPunctuationEdge(unittest.TestCase):
    def test_strip_punctuation_empty_str(self):
        txt = ""
        expected = ""
        actual = strip_punctuation(txt)
        self.assertEqual(actual, expected)

    def test_strip_punctuation_all_punc(self):
        txt = "!.&,'"
        expected = ""
        actual = strip_punctuation(txt)
        self.assertEqual(actual, expected)

    def test_strip_punctuation_long_text(self):
        txt = "Hello, today I am looking to strip punctuation! After the string has been placed through the punctuation stripper function & has had the punctuation removed, there will be no more punctuation's left."
        expected = "Hello today I am looking to strip punctuation After the string has been placed through the punctuation stripper function  has had the punctuation removed there will be no more punctuations left"
        actual = strip_punctuation(txt)
        self.assertEqual(actual, expected)


class TestStripPunctuationNegative(unittest.TestCase):
    def test_strip_punctuation_none(self):
        txt = None
        actual = strip_punctuation(txt)
        self.assertEqual(actual, "")

    def test_strip_punctuation_int(self):
        txt = 1
        actual = strip_punctuation(txt)
        self.assertEqual(actual, "")

    def test_strip_punctuation_bool(self):
        txt = False
        actual = strip_punctuation(txt)
        self.assertEqual(actual, "")

    def test_strip_punctuation_list(self):
        txt = ["test strip punctuation."]
        actual = strip_punctuation(txt)
        self.assertEqual(actual, "")


class TestStripWhiteSpace(unittest.TestCase):

    def test_strip_white_space_dbl_space(self):
        txt = "test  strip  white  space"
        expected = "test strip white space"
        actual = strip_white_space(txt)
        self.assertEqual(actual, expected)

    def test_strip_white_space_tab(self):
        txt = "test  strip  white   space"
        expected = "test strip white space"
        actual = strip_white_space(txt)
        self.assertEqual(actual, expected)

    def test_strip_white_space_return(self):
        txt = """test
        strip
        white
        space"""
        expcted = "test strip white space"
        actual = strip_white_space(txt)
        self.assertEqual(actual, expcted)

    def test_strip_white_space_before(self):
        txt = " test strip white space"
        expected = "test strip white space"
        actual = strip_white_space(txt)
        self.assertEqual(actual, expected)

    def test_strip_white_space_after(self):
        txt = "test strip white space "
        expected = "test strip white space"
        actual = strip_white_space(txt)
        self.assertEqual(actual, expected)


class TestStripWhiteSpaceEdge(unittest.TestCase):

    def test_strip_white_space_empty_string(self):
        txt = ""
        expected = ""
        actual = strip_white_space(txt)
        self.assertEqual(actual, expected)

    def test_strip_white_space_all_white_space(self):
        txt = """
                     """
        expected = ""
        actual = strip_white_space(txt)
        self.assertEqual(actual, expected)

    def test_strip_white_space_long_string(self):
        txt = "test strip white space   test strip white space  test strip white space  "
        expected = "test strip white space test strip white space test strip white space"
        actual = strip_white_space(txt)
        self.assertEqual(actual, expected)

    def test_strip_white_space_long_before(self):
        txt = "                         test strip white space"
        expected = "test strip white space"
        actual = strip_white_space(txt)
        self.assertEqual(actual, expected)

    def test_strip_white_space_long_after(self):
        txt = "test strip white space                         "
        expected = "test strip white space"
        actual = strip_white_space(txt)
        self.assertEqual(actual, expected)


class TestStripWhiteSpaceNegative(unittest.TestCase):

    def test_strip_white_space_none(self):
        txt = None
        expected = ""
        actual = strip_white_space(txt)
        self.assertEqual(actual, expected)

    def test_strip_white_space_int(self):
        txt = 1
        expected = ""
        actual = strip_white_space(txt)
        self.assertEqual(actual, expected)

    def test_strip_white_space_bool(self):
        txt = False
        expected = ""
        actual = strip_white_space(txt)
        self.assertEqual(actual, expected)

    def test_strip_white_space_list(self):
        txt = ["test strip white space."]
        expected = ""
        actual = strip_white_space(txt)
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
