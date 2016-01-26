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
        # data and free_text are optional, so they will be prepended with \n
        # only if present later on
        '%(level_color)s%(levelname)s%(reset)s %(message)s%(data)s%(free_text)s'
    )

    def __init__(self, style='friendly', fmt=None, datefmt=None, pprint=True):
        fmt = fmt or self.DEFAULT_FORMAT
        require_msg = (
            "Provide '%%(level_color)s' and '%%(reset)s in format', e.g: %s"
            % self._get_demo()
        )
        assert '%(level_color)s' in fmt and '%(reset)s' in fmt, require_msg
        self.pprint = pprint
        self.free_text_formatter = Terminal256Formatter(style='monokai')
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
        # beware, same record might be passed twice (many handlers)!
        # so we need to save the state of our actions on the records
        # I have no idea why setting state as ___fdone did not work
        color = self.default_level_colors[record.levelname]
        record.level_color = console.codes[color]
        record.reset = console.codes['reset']
        if hasattr(record, 'data'):
            if not hasattr(record, 'ddone'):
                data = record.data
                data = pformat(data) if self.pprint else unicode(data)
                record.data = highlight(data, self.lexer, self.formatter)
                if self.pprint:
                    record.data = '\n' + record.data
        else:
            record.data = ''
        record.ddone = True
        if hasattr(record, 'free_text'):
            if not hasattr(record, '_fdone'):
                data = record.free_text
                record.free_text = highlight(data, self.lexer, self.free_text_formatter)
                if self.pprint:
                    record.free_text = '\n' + record.free_text
        else:
            record.free_text = ''
        record._fdone = True
        return super(PygmentsFormatter, self).format(record)
