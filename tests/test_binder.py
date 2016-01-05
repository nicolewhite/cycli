from cycli.binder import curly_left, curly_right, paren_left, paren_right, bracket_left, bracket_right, apostrophe, \
    quote
from mock import call

import pytest


@pytest.fixture
def binder():
    from mock import MagicMock
    return MagicMock()


def test_curly_left(binder):
    curly_left(binder)
    binder.cli.current_buffer.insert_text.assert_has_calls([call("{"), call("}", move_cursor=False)])


def test_curly_right_curly_current(binder):
    binder.cli.current_buffer.document.current_char = "}"
    curly_right(binder)
    binder.cli.current_buffer.cursor_right.assert_called_once_with()


def test_curly_right_not_curly_current(binder):
    binder.cli.current_buffer.document.current_char = "n"
    curly_right(binder)
    binder.cli.current_buffer.insert_text.assert_has_calls([call("}")])


def test_paren_left(binder):
    paren_left(binder)
    binder.cli.current_buffer.insert_text.assert_has_calls([call("("), call(")", move_cursor=False)])


def test_paren_right_paren_current(binder):
    binder.cli.current_buffer.document.current_char = ")"
    paren_right(binder)
    binder.cli.current_buffer.cursor_right.assert_called_once_with()


def test_paren_right_not_paren_current(binder):
    binder.cli.current_buffer.document.current_char = "n"
    paren_right(binder)
    binder.cli.current_buffer.insert_text.assert_has_calls([call(")")])


def test_bracket_left(binder):
    bracket_left(binder)
    binder.cli.current_buffer.insert_text.assert_has_calls([call("["), call("]", move_cursor=False)])


def test_bracket_right_bracket_current(binder):
    binder.cli.current_buffer.document.current_char = "]"
    bracket_right(binder)
    binder.cli.current_buffer.cursor_right.assert_called_once_with()


def test_bracket_right_not_bracket_current(binder):
    binder.cli.current_buffer.document.current_char = "n"
    bracket_right(binder)
    binder.cli.current_buffer.insert_text.assert_has_calls([call("]")])


def test_apostrophe_current(binder):
    binder.cli.current_buffer.document.current_char = "'"
    apostrophe(binder)
    binder.cli.current_buffer.cursor_right.assert_called_once_with()


def test_apostrophe_not_current(binder):
    binder.cli.current_buffer.document.current_char = "n"
    apostrophe(binder)
    binder.cli.current_buffer.insert_text.assert_has_calls([call("'"), call("'", move_cursor=False)])


def test_quote_current(binder):
    binder.cli.current_buffer.document.current_char = "\""
    quote(binder)
    binder.cli.current_buffer.cursor_right.assert_called_once_with()


def test_quote_not_current(binder):
    binder.cli.current_buffer.document.current_char = "n"
    quote(binder)
    binder.cli.current_buffer.insert_text.assert_has_calls([call("\""), call("\"", move_cursor=False)])
