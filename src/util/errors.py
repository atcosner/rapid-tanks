from  typing import NamedTuple


class MissingData(Exception):
    pass


class CalculationError(Exception):
    pass


class DataEntryResult(NamedTuple):
    valid: bool
    errors: list
