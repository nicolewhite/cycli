from __future__ import unicode_literals
from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.keys import Keys

CypherBinder = KeyBindingManager()

@CypherBinder.registry.add_binding("{")
def curly_left(event):
    b = event.cli.current_buffer
    b.insert_text("{")
    b.insert_text("}", move_cursor=False)

@CypherBinder.registry.add_binding("}")
def curly_right(event):
    b = event.cli.current_buffer
    char = b.document.current_char

    if char == "}":
        b.cursor_right()
    else:
        b.insert_text("}")

@CypherBinder.registry.add_binding("(")
def paren_left(event):
    b = event.cli.current_buffer
    b.insert_text("(")
    b.insert_text(")", move_cursor=False)

@CypherBinder.registry.add_binding(")")
def paren_right(event):
    b = event.cli.current_buffer
    char = b.document.current_char

    if char == ")":
        b.cursor_right()
    else:
        b.insert_text(")")

@CypherBinder.registry.add_binding("[")
def bracket_left(event):
    b = event.cli.current_buffer
    b.insert_text("[")
    b.insert_text("]", move_cursor=False)

@CypherBinder.registry.add_binding("]")
def bracket_right(event):
    b = event.cli.current_buffer
    char = b.document.current_char

    if char == "]":
        b.cursor_right()
    else:
        b.insert_text("]")

@CypherBinder.registry.add_binding("'")
def apostrophe(event):
    b = event.cli.current_buffer
    char = b.document.current_char

    if char == "'":
        b.cursor_right()
    else:
        b.insert_text("'")
        b.insert_text("'", move_cursor=False)

@CypherBinder.registry.add_binding("\"")
def quote(event):
    b = event.cli.current_buffer
    char = b.document.current_char

    if char == "\"":
        b.cursor_right()
    else:
        b.insert_text("\"")
        b.insert_text("\"", move_cursor=False)

@CypherBinder.registry.add_binding("`")
def backtick(event):
    b = event.cli.current_buffer
    char = b.document.current_char

    if char == "`":
        b.cursor_right()
    else:
        b.insert_text("`")
        b.insert_text("`", move_cursor=False)

@CypherBinder.registry.add_binding(Keys.Backspace)
def backspace(event):
    b = event.cli.current_buffer
    current_char = b.document.current_char
    before_char = b.document.char_before_cursor

    patterns = [("(", ")"), ("[", "]"), ("{", "}"), ("'", "'"), ('"', '"'), ("`", "`")]

    for pattern in patterns:
        if before_char == pattern[0] and current_char == pattern[1]:
            b.cursor_right()
            b.delete_before_cursor(2)
            return

    b.delete_before_cursor()