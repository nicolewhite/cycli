from __future__ import unicode_literals
from prompt_toolkit.completion import Completer, Completion
from cycli.cypher import Cypher


cypher = Cypher()


class CypherCompleter(Completer):

    def __init__(self, labels, relationship_types, properties):
        super(CypherCompleter, self).__init__()

        self.labels = labels
        self.relationship_types = relationship_types
        self.properties = properties

    def get_completions(self, document, complete_event):
        chars_before_cursor = document.get_word_before_cursor(WORD=True)

        all_text = document.text_before_cursor

        if not chars_before_cursor or self.unclosed_strings(all_text):
            return

        word = self.find_last_word(chars_before_cursor)

        if self.most_recent_non_alpha(chars_before_cursor) == ":":
            if self.looking_for(chars_before_cursor) == "label":
                choices = self.labels
            elif self.looking_for(chars_before_cursor) == "relationship":
                choices = self.relationship_types
            else:
                return
        elif self.most_recent_non_alpha(chars_before_cursor) == ".":
            loc = chars_before_cursor.find(".")

            if loc:
                prev_char = chars_before_cursor[loc - 1]

                if prev_char.isalpha():
                    choices = self.properties

                else:
                    return
        elif word:
            last_cypher_word = self.most_recent_cypher_word(all_text)
            choices = cypher.most_probable_next_keyword(last_cypher_word)
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

    def looking_for(self, chars_before_cursor):
        paren = chars_before_cursor.rfind("(")
        bracket = chars_before_cursor.rfind("[")
        curly = chars_before_cursor.rfind("{")

        d = dict(label=paren, relationship=bracket, curly=curly)
        return max(d, key=d.get)

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

    def most_recent_cypher_word(self, all_text):
        text = " " + all_text
        keyword_indices = [(word, text.rfind(" " + word + " ")) for word in cypher.KEYWORDS]
        function_indices = [(word, text.rfind(" " + word + "(")) for word in cypher.FUNCTIONS]

        indices = keyword_indices + function_indices

        # If no keywords were found, we want to be in the "" state in the Markov model.
        if not any([i[1] > -1 for i in indices]):
            return ""

        most_recent = max(indices, key=lambda i:i[1])[0]
        return most_recent

    def most_recent_non_alpha(self, chars):
        chars = list(chars)
        chars.reverse()

        for c in chars:
            if not c.isalpha():
                return c

        return ""

    def unclosed_strings(self, chars):
        return chars.count("\"") % 2 != 0 or chars.count("'") % 2 != 0