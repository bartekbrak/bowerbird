"""
I had troubles capturing stdout from capsys in test_colours_the_log

These tests get ridiculous to fix after default colours change. Yuck
"""
import logging

from bowerbird.formatters import PygmentsFormatter

fmt = (
    '%(level_color)s%(levelname)s%(reset)s:'
    '%(name)s:%(message)s:%(data)s%(free)s'
)
styles = {
    'data': 'default',
    'sql': 'default',
    'free': 'default',
}


def test_colours_the_log(caplog):
    logger = logging.getLogger('test_logger')

    caplog.handler.formatter = PygmentsFormatter(styles=styles, fmt=fmt)
    logger.debug('test', extra={'data': 'string'})
    expected = (
        "\x1b[01mDEBUG\x1b[39;49;00m:test_logger:test:\n"
        "\x1b[38;5;124m'\x1b[39m\x1b[38;5;124m"
        "string\x1b[39m\x1b[38;5;124m'\x1b[39m\n"
    )
    assert caplog.text == expected


def test_what_if_there_is_no_data(caplog):
    logger = logging.getLogger('test_logger')
    caplog.handler.formatter = PygmentsFormatter(fmt=fmt)
    logger.debug('test')
    expected = '\x1b[01mDEBUG\x1b[39;49;00m:test_logger:test:\n'
    assert caplog.text == expected
