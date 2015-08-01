from pygments.style import Style
from pygments.token import Token

class CypherStyle(Style):
    styles = {
        Token.Keyword: '#3498DB',
        Token.String: '#E67E22',
        Token.Name: '#1ABC9C',
        Token.Pattern: '#E74C3C',

        Token.Line: 'bg:#000000 #ffffff',

        Token.LineNumber:  'bg:#ffffaa #000000',
        Token.Menu.Completions.Completion.Current: 'bg:#00aaaa #000000',
        Token.Menu.Completions.Completion:         'bg:#008888 #ffffff',
        Token.Menu.Completions.ProgressButton:     'bg:#003333',
        Token.Menu.Completions.ProgressBar:        'bg:#00aaaa',

        Token.Toolbar.Completions:  'bg:#888800 #000000',
        Token.Toolbar.Completions.Arrow: 'bg:#888800 #000000',
        Token.Toolbar.Completions.Completion:  'bg:#aaaa00 #000000',
        Token.Toolbar.Completions.Completion.Current:  'bg:#ffffaa #000000 bold',

        Token.AfterInput: 'bg:#ff44ff #000000',
    }
