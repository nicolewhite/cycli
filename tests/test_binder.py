from __future__ import unicode_literals

from mock import call, MagicMock
import pytest

from cycli.binder import *


@pytest.fixture
def binder():
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


def test_backtick_current(binder):
  binder.cli.current_buffer.document.current_char = "`"
  backtick(binder)
  binder.cli.current_buffer.cursor_right.assert_called_once_with()


def test_backtick_not_current(binder):
  binder.cli.current_buffer.document.current_char = "n"
  backtick(binder)
  binder.cli.current_buffer.insert_text.assert_has_calls([call("`"), call("`", move_cursor=False)])


def test_backspace_no_pattern(binder):
  binder.cli.current_buffer.document.current_char = "n"
  backspace(binder)
  binder.cli.current_buffer.delete_before_cursor.assert_called_once_with()


@pytest.mark.parametrize(("char_before_cursor", "current_char"), [
  ("(", ")"),
  ("[", "]"),
  ("{", "}"),
  ("'", "'"),
  ('"', '"'),
  ("`", "`")
])
def test_backspace_with_pattern(char_before_cursor, current_char):
  binder = MagicMock()

  binder.cli.current_buffer.document.char_before_cursor = char_before_cursor
  binder.cli.current_buffer.document.current_char = current_char

  backspace(binder)

  binder.cli.current_buffer.cursor_right.assert_called_once_with()
  binder.cli.current_buffer.delete_before_cursor.assert_called_once_with(2)
