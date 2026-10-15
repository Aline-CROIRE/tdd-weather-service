"""Define custom exceptions for the weather service."""


class CityNotFoundError(Exception):
    """Raise when a requested city is not supported."""


class InvalidAPIKeyError(Exception):
    """Raise when the API key is invalid."""
