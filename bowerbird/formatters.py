import logging
from functools import partial
from pprint import pformat

import sqlparse
from pygments import console, highlight
from pygments.formatters.terminal256 import Terminal256Formatter
from pygments.lexers import get_lexer_by_name

lexers = {
    'python': get_lexer_by_name('python', ensurenl=False),
    'sql': get_lexer_by_name('sql', ensurenl=False),
}
sql_parse = partial(sqlparse.format, reindent=True, keyword_case='upper')


class PygmentsFormatter(logging.Formatter):
    level_colors = {
        'DEBUG': 'white',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'turquoise',
    }
    DEFAULT_FORMAT = (
        # data, free and sql are "parts", optional, will get prefixed with \n
        '%(level_color)s%(levelname)s%(reset)s '
        '%(message)s%(data)s%(free)s%(sql)s'
    )

    def __init__(self, styles=None, fmt=None, datefmt=None):
        styles = styles or {
            'data': 'default',
            'free': 'default',
            'sql': 'default',
        }
        self.formatters = {
            part_name: Terminal256Formatter(style=style)
            for part_name, style in styles.items()
        }
        self.record = None
        fmt = fmt or self.DEFAULT_FORMAT
        super(PygmentsFormatter, self).__init__(fmt=fmt, datefmt=datefmt)

    def format(self, record):
        self.record = record
        level_color = self.level_colors[record.levelname]
        self.record.level_color = console.codes[level_color]
        self.record.reset = console.codes['reset']
        self.format_part('data', 'python', pformat)
        self.format_part('free', 'python')
        self.format_part('sql', 'sql', sql_parse)
        return super(PygmentsFormatter, self).format(record)

    def format_part(self, part_name, lexer, function=None):
        """
        Same record might be passed twice (many handlers).
        So we need to save the state of our actions on the record
        """
        done_marker = part_name + '_done'
        if hasattr(self.record, part_name):
            if not hasattr(self.record, done_marker):
                data = getattr(self.record, part_name)
                data = function(data) if function else data
                formatter = self.formatters[part_name]
                setattr(
                    self.record,
                    part_name,
                    '\n' + highlight(data, lexers[lexer], formatter)
                )
        else:
            # format might require this part, and extra might not
            # provide it, add it in that case
            setattr(self.record, part_name, '')
        setattr(self.record, done_marker, True)
