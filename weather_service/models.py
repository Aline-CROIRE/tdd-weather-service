"""Define weather data models."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Forecast:
    """Represent a weather forecast."""

    city: str
    condition: str
    temperature_celsius: int