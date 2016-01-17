import logging
from logging.config import dictConfig

import pytest

LOGGING = {
    'version': 1,
    'loggers': {
        'test': {'handlers': ['stream']},
    },
    'handlers': {
        'stream': {
            'class': 'logging.StreamHandler',
            'formatter': 'pygments_formatter',
        },
    },
    'formatters': {
        'pygments_formatter': {'()': 'bowerbird.formatters.PygmentsFormatter'}
    },
}


@pytest.fixture
def pygments_logger():
    dictConfig(LOGGING)
    logger = logging.getLogger('test')
    return logger
