from prompt_toolkit.key_binding.manager import KeyBindingManager

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