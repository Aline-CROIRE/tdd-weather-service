
"""Provide weather forecast services."""

from dataclasses import dataclass

from weather_service.exceptions import CityNotFoundError


@dataclass
class Forecast:
    """Represent a weather forecast."""

    city: str


class WeatherService:
    """Provide predefined weather forecasts."""

    SUPPORTED_CITIES = {"Kigali"}

    def get_forecast(self, city: str) -> Forecast:
        """Return a forecast for a supported city.

        Args:
            city: Name of the requested city.

        Returns:
            The forecast for the requested city.

        Raises:
            CityNotFoundError: If the city is not supported.
        """
        if city not in self.SUPPORTED_CITIES:
            raise CityNotFoundError(f"City '{city}' was not found.")

        return Forecast(city=city)
