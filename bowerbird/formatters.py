import logging
import textwrap
from pprint import pformat

from pygments import console, highlight
from pygments.formatters.terminal256 import Terminal256Formatter
from pygments.lexers import get_lexer_by_name


class BaseColorFormatter(logging.Formatter):
    def __init__(self, style, lexer, fmt=None, datefmt=None):
        self.lexer = get_lexer_by_name(lexer)
        self.formatter = Terminal256Formatter(style=style)
        super(BaseColorFormatter, self).__init__(fmt, datefmt)


class PygmentsFormatter(BaseColorFormatter):
    default_level_colors = {
        'DEBUG': 'white',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        # not sure, but no other available
        'CRITICAL': 'turquoise',
    }
    DEFAULT_FORMAT = (
        '%(level_color)s%(levelname)s%(reset)s:%(name)s:%(message)s:\n%(data)s'
    )

    def __init__(self, style='friendly', fmt=None, datefmt=None, pprint=True):
        fmt = fmt or self.DEFAULT_FORMAT
        require_msg = (
            "Provide '%%(level_color)s' and '%%(reset)s in format', e.g: %s"
            % self._get_demo()
        )
        assert '%(level_color)s' in fmt and '%(reset)s' in fmt, require_msg
        self.pprint = pprint
        super(PygmentsFormatter, self).__init__(style, 'python', fmt, datefmt)

    @classmethod
    def _get_demo(cls):
        # This may be used in some library demo, that is not ready yet
        demo = """
            LOGGING = {
                'formatters': {
                    'pygments_formatter': {
                        '()': %r.%r,
                        'format': %r,
                },
            }
        """ % (cls.__module__, cls.__name__, cls.DEFAULT_FORMAT)
        return textwrap.dedent(demo)

    def format(self, record):
        color = self.default_level_colors[record.levelname]
        record.level_color = console.codes[color]
        record.reset = console.codes['reset']
        if hasattr(record, 'data'):
            data = record.data
            data = pformat(data) if self.pprint else unicode(data)
            record.data = highlight(data, self.lexer, self.formatter)
        return super(PygmentsFormatter, self).format(record)
