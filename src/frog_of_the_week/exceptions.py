"""
Different custom errors for various cases. They mostly inherit the errors that are thrown
"""


class FrogDataError(Exception):
    """
    Super class Errors of the data service.
    """


class MissingApiKeyError(KeyError, FrogDataError):
    """
    Error for missing API keys.
    """


class InvalidApiKeyError(KeyError, FrogDataError):
    """
    Error for missing API keys.
    """
