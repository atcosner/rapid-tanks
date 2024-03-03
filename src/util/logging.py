import logging
import sys
from contextlib import contextmanager
from types import TracebackType
from typing import Type

logger = logging.getLogger(__name__)

LOG_WIDTH = 120


class NamedLoggerAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        return f'[{self.extra["name"]}] {msg}', kwargs


@contextmanager
def log_block(log: logging.Logger, name: str):
    half_width = (LOG_WIDTH - len(name) - 2) // 2
    log.info(f'{"-" * half_width} {name} {"-" * half_width}')
    try:
        yield
    finally:
        log.info('-' * LOG_WIDTH)
        log.info('')


def configure_root_logger() -> None:
    logging.basicConfig(
        format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
        level=logging.DEBUG,
    )


def log_uncaught_exception(exc_type, exc_value: Type[Exception], exc_traceback: TracebackType) -> None:
    # Log the exception
    logger.critical('Uncaught exception', exc_info=(exc_type, exc_value, exc_traceback))

    # Pass the exception to the default handler
    sys.__excepthook__(exc_type, exc_value, exc_traceback)
