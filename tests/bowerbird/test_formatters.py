"""
I had troubles capturing stdout from capsys in test_colours_the_log
"""
import logging

from pygments.console import codes

from bowerbird.formatters import PygmentsFormatter


def test_requires_data_set(pygments_logger, capsys):
    pygments_logger.debug('')
    _, err = capsys.readouterr()
    # this does not raise due to logging.Handler.handleError default behaviour
    assert "AssertionError: Provide extra={'data': 'something'}" in err


def test_colours_the_log(caplog):
    logger = logging.getLogger('test_logger')
    caplog.handler.formatter = PygmentsFormatter()
    logger.debug('test', extra={'data': 'string'})
    expected = (
        "{white}DEBUG{reset}:test_logger:test:\n"
        "{violet}'{reset2}{violet}string{reset2}{violet}'{reset2}\n\n"
    ).format(violet='\x1b[38;5;61m', reset2='\x1b[39m', **codes)
    assert caplog.text == expected
