import logging
from contextlib import contextmanager

LOG_WIDTH = 120


class NamedLoggerAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        return f'[{self.extra["name"]}] {msg}', kwargs


@contextmanager
def log_block(logger: logging.Logger, name: str):
    half_width = (LOG_WIDTH - len(name) - 2) // 2
    logger.info(f'{"-" * half_width} {name} {"-" * half_width}')
    try:
        yield
    finally:
        logger.info('-' * LOG_WIDTH)
        logger.info('')
