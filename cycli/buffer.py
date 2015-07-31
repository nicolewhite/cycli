from prompt_toolkit.buffer import Buffer
from prompt_toolkit.filters import Condition

class CypherBuffer(Buffer):

    def __init__(self, *args, **kwargs):

        @Condition
        def is_multiline():
            text = self.document.text

            return not text.endswith(";")

        super(self.__class__, self).__init__(*args, is_multiline=is_multiline, **kwargs)