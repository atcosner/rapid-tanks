import logging


class NamedLoggerAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        return f'[{self.extra["name"]}] {msg}', kwargs
