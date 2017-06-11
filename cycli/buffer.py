from prompt_toolkit.buffer import Buffer
from prompt_toolkit.filters import Condition


class UserWantsOut(Exception):
  pass


class CypherBuffer(Buffer):
  def __init__(self, *args, **kwargs):
    @Condition
    def is_multiline():
      return not self.user_wants_out(self.document.text)

    super(self.__class__, self).__init__(*args, is_multiline=is_multiline, **kwargs)

  def user_wants_out(self, text):
    return any([
      text.endswith(";"),
      text.endswith("\n"),
      text == "quit",
      text == "exit",
      text == "help",
      text == "refresh",
      text == "schema",
      text == "schema-constraints",
      text == "schema-indexes",
      text == "schema-labels",
      text == "schema-rels",
      text.startswith("env"),
      text.startswith("export ")
    ])
