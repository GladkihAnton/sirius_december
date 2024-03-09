import logging
from contextvars import ContextVar

import yaml

with open('conf/logging.conf.yml', 'r') as f:
    LOGGING_CONFIG = yaml.full_load(f)


class ConsoleFormatter(logging.Formatter):

    def format(self, record: logging.LogRecord) -> str:
        try:
            correlation_id = correlation_id_ctx.get()
            return '[%s] %s' % (correlation_id, super().format(record))
        except LookupError:
            return super().format(record)


correlation_id_ctx = ContextVar('correlation_id_ctx')
logger = logging.getLogger('tinder_bot')
