Bowerbird - A collection of stdlib logging.Formatter classes using Pygments
===========================================================================

A `bowerbird <https://en.wikipedia.org/wiki/Satin_bowerbird>`__ is known
to like colours in its courtship behaviours. I do to, in my logging.

Install
=======

pip install bowerbird

Use
===

dictConfig:
-----------

::

    LOGGING = {
        ...
        'formatters': {
            'bowerbird_formatter': {
                '()': bowerbird.formatters.PygmentsFormatter,
        },
        ...
    }

Then, in code, use with optional extra params:

- ``data``: any python object, can be nested, will be pygentized and pretty printed
- ``free``: Any text, will also by pygmentized
- ``sql``: SQL string, will be formatted and pygmentized

::

    free = "db_counts:\nauth_user from 0 to 10"
    logger.debug(
        'I got this data',
        extra={'data': some_obj.__dict__, 'free': free}
    )


TODO / Research
===============

-  Add DjangoColorSQLFormatter - ready, but not tested
-  Add SQLAlchemyColorSQLFormatter - ready but not tested
-  Have a look at pip.utils.logging.ColorizedStreamHandler, does it
   overlap?
-  Add Python3 support
-  Add more examples to configuration

License
=======

MIT
