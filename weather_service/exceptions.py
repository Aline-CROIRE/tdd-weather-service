
"""Define custom exceptions for the weather service."""


class CityNotFoundError(Exception):
    """Raise when a requested city is not supported."""
