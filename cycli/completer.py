from __future__ import unicode_literals
from prompt_toolkit.completion import Completer, Completion
from neo4j import reltypes, labels, props
from cypher import cypher_words


class CypherCompleter(Completer):

    def get_completions(self, document, complete_event):
        chars_before_cursor = document.get_word_before_cursor(WORD=True)

        if not chars_before_cursor:
            return

        word = self.find_last_word(chars_before_cursor)

        if self.most_recent_non_alpha(chars_before_cursor) == ":":
            if self.looking_for_label(chars_before_cursor):
                choices = labels
            else:
                choices = reltypes
        elif self.most_recent_non_alpha(chars_before_cursor) == ".":
            choices = props
        elif self.all_alpha(chars_before_cursor):
            choices = cypher_words
        else:
            return

        choices = self.find_matches(word, choices)

        for completion in choices:
            yield Completion(completion, -len(word))

    def find_matches(self, word, choices):
        word = word.lower()
        lower_choices = [x.lower() for x in choices]

        completions = []

        for i, choice in enumerate(lower_choices):
            if choice.startswith(word):
                completions.append(choices[i])

        return completions

    def looking_for_label(self, word_before_cursor):
        paren = word_before_cursor.rfind("(")
        bracket = word_before_cursor.rfind("[")

        if paren > bracket:
            return True

        return False

    def find_last_word(self, chars):
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

    def most_recent_non_alpha(self, chars):
        chars = list(chars)
        chars.reverse()

        for c in chars:
            if not c.isalpha():
                return c

        return ""

    def all_alpha(self, chars):
        return all([x.isalpha() or x.isspace() for x in chars])