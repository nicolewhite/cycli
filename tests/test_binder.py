from unittest import TestCase, main
from mock import MagicMock, call
from cycli.binder import curly_left, curly_right, paren_left, paren_right, bracket_left, bracket_right, apostrophe, quote


class TestBinder(TestCase):
  def test_curly_left(self):
    mock_event = MagicMock()
    curly_left(mock_event)
    mock_event.cli.current_buffer.insert_text.assert_has_calls([call("{"), call("}", move_cursor=False)])

  def test_curly_right_curly_current(self):
    mock_event = MagicMock()
    mock_event.cli.current_buffer.document.current_char = "}"
    curly_right(mock_event)
    mock_event.cli.current_buffer.cursor_right.assert_called_once_with()

  def test_curly_right_not_curly_current(self):
    mock_event = MagicMock()
    mock_event.cli.current_buffer.document.current_char = "n"
    curly_right(mock_event)
    mock_event.cli.current_buffer.insert_text.assert_has_calls([call("}")])

  def test_paren_left(self):
    mock_event = MagicMock()
    paren_left(mock_event)
    mock_event.cli.current_buffer.insert_text.assert_has_calls([call("("), call(")", move_cursor=False)])

  def test_paren_right_paren_current(self):
    mock_event = MagicMock()
    mock_event.cli.current_buffer.document.current_char = ")"
    paren_right(mock_event)
    mock_event.cli.current_buffer.cursor_right.assert_called_once_with()

  def test_paren_right_not_paren_current(self):
    mock_event = MagicMock()
    mock_event.cli.current_buffer.document.current_char = "n"
    paren_right(mock_event)
    mock_event.cli.current_buffer.insert_text.assert_has_calls([call(")")])

  def test_bracket_left(self):
    mock_event = MagicMock()
    bracket_left(mock_event)
    mock_event.cli.current_buffer.insert_text.assert_has_calls([call("["), call("]", move_cursor=False)])

  def test_bracket_right_bracket_current(self):
    mock_event = MagicMock()
    mock_event.cli.current_buffer.document.current_char = "]"
    bracket_right(mock_event)
    mock_event.cli.current_buffer.cursor_right.assert_called_once_with()

  def test_bracket_right_not_bracket_current(self):
    mock_event = MagicMock()
    mock_event.cli.current_buffer.document.current_char = "n"
    bracket_right(mock_event)
    mock_event.cli.current_buffer.insert_text.assert_has_calls([call("]")])

  def test_apostrophe_current(self):
    mock_event = MagicMock()
    mock_event.cli.current_buffer.document.current_char = "'"
    apostrophe(mock_event)
    mock_event.cli.current_buffer.cursor_right.assert_called_once_with()

  def test_apostrophe_not_current(self):
    mock_event = MagicMock()
    mock_event.cli.current_buffer.document.current_char = "n"
    apostrophe(mock_event)
    mock_event.cli.current_buffer.insert_text.assert_has_calls([call("'"), call("'", move_cursor=False)])

  def test_quote_current(self):
    mock_event = MagicMock()
    mock_event.cli.current_buffer.document.current_char = "\""
    quote(mock_event)
    mock_event.cli.current_buffer.cursor_right.assert_called_once_with()

  def test_quote_not_current(self):
    mock_event = MagicMock()
    mock_event.cli.current_buffer.document.current_char = "n"
    quote(mock_event)
    mock_event.cli.current_buffer.insert_text.assert_has_calls([call("\""), call("\"", move_cursor=False)])


if __name__ == "__main__":
  main()