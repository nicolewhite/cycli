from __future__ import unicode_literals
from prompt_toolkit.completion import Completer, Completion
from cycli.cypher import Cypher


class CypherCompleter(Completer):
  def __init__(self, labels, relationship_types, properties):
    super(CypherCompleter, self).__init__()

    self.labels = labels
    self.relationship_types = relationship_types
    self.properties = properties
    self.cypher = Cypher()

  def get_completions(self, document, complete_event):
    text_before_cursor = document.text_before_cursor

    if currently_inside_quotes(text_before_cursor):
      return
    elif typing_label(text_before_cursor):
      choices = self.labels
      lookup = everything_after_last(":", text_before_cursor)
    elif typing_relationship(text_before_cursor):
      choices = self.relationship_types
      lookup = everything_after_last(":", text_before_cursor)
    elif typing_property(text_before_cursor):
      period_loc = text_before_cursor.rfind(".")
      variable_start_loc = max(text_before_cursor.rfind("(", 0, period_loc), text_before_cursor.rfind(" ", 0, period_loc))
      variable = text_before_cursor[variable_start_loc + 1:period_loc]

      if variable.isalnum() and any(c.isalpha() for c in variable):
        choices = self.properties
        lookup = everything_after_last(".", text_before_cursor)
      else:
        return
    elif text_before_cursor and text_before_cursor[-1].isalpha():
      last_cypher_word = self.most_recent_cypher_word(text_before_cursor)
      choices = self.cypher.most_probable_next_keyword(last_cypher_word)
      lookup = last_alphabetic_chunk(text_before_cursor)
    else:
      return

    completions = find_matches(lookup, choices)

    for completion in completions:
      yield Completion(completion, -len(lookup))

  def most_recent_cypher_word(self, chars):
    text = " " + chars
    keyword_indices = [(word, text.rfind(" " + word + " ")) for word in self.cypher.KEYWORDS]
    function_indices = [(word, text.rfind(" " + word + "(")) for word in self.cypher.FUNCTIONS]

    indices = keyword_indices + function_indices

    # If no keywords were found, we want to be in the "" state in the Markov model.
    if not any([i[1] > -1 for i in indices]):
      return ""

    most_recent = max(indices, key=lambda i:i[1])[0]
    return most_recent


def find_matches(word, choices):
  word = word.lower()
  lower_choices = [x.lower() for x in choices]

  completions = []

  for i, choice in enumerate(lower_choices):
    if choice.startswith(word):
      completions.append(choices[i])

  return completions


def last_alphabetic_chunk(chars):
  chars = list(chars)
  chars.reverse()

  keep = []

  for c in chars:
    if c.isalpha():
      keep.append(c)
    else:
      break

  keep.reverse()
  return "".join(keep)


def everything_after_last(char, chars):
  chars = chars.replace("`", "")
  loc = chars.rfind(char)
  return chars[loc + 1:]


def exists_unclosed_char(char, chars):
  return chars.count(char) % 2 != 0


def exists_unclosed_pattern(open_char, close_char, chars):
  return chars.count(open_char) != chars.count(close_char)


def currently_inside_quotes(chars):
  return exists_unclosed_char("'", chars) or exists_unclosed_char('"', chars)


def colon_inside_unclosed_pattern(open_char, close_char, chars):
  return exists_unclosed_pattern(open_char, close_char, chars) and chars.rfind(":") > chars.rfind(open_char)


def typing_relationship(chars):
  return colon_inside_unclosed_pattern("[", "]", chars) and chars.rfind("[") > chars.rfind("(")


def typing_label(chars):
  return colon_inside_unclosed_pattern("(", ")", chars) and chars.rfind("(") > chars.rfind("[")


def typing_property(chars):
  chars = list(chars)
  chars.reverse()

  skip = ["_", "`"]

  # Skip spaces if we're inside backticks.
  if exists_unclosed_char("`", chars):
    skip.append(" ")

  for c in chars:
    if not c.isalnum() and c not in skip:
      return c == "."

  return False
