# encoding: utf-8
# pylint: disable=invalid-name,wrong-import-position

import logging

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)
# logging.getLogger('app').setLevel(logging.DEBUG)

try:
    import colorlog
except ImportError:
    pass
else:
    formatter = colorlog.ColoredFormatter(
        (
            '%(asctime)s '
            '[%(log_color)s%(levelname)s%(reset)s] '
            '[%(cyan)s%(name)s%(reset)s] '
            '%(message_log_color)s%(message)s'
        ),
        reset=True,
        log_colors={
            'DEBUG': 'bold_cyan',
            'INFO': 'bold_green',
            'WARNING': 'bold_yellow',
            'ERROR': 'bold_red',
            'CRITICAL': 'bold_red,bg_white',
        },
        secondary_log_colors={
            'message': {
                'DEBUG': 'white',
                'INFO': 'bold_white',
                'WARNING': 'bold_yellow',
                'ERROR': 'bold_red',
                'CRITICAL': 'bold_red',
            },
        },
        style='%'
    )

    for handler in logger.handlers:
        if isinstance(handler, logging.StreamHandler):
            break
    else:
        handler = logging.StreamHandler()
        logger.addHandler(handler)
    handler.setFormatter(formatter)
