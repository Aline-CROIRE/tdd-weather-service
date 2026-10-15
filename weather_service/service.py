
"""Provide weather forecast services."""

from dataclasses import dataclass

from weather_service.exceptions import CityNotFoundError


@dataclass(frozen=True)
class Forecast:
    """Represent a weather forecast.

    Attributes:
        city: Name of the city.
        condition: Description of the weather.
        temperature_celsius: Temperature in degrees Celsius.
    """

    city: str
    condition: str
    temperature_celsius: int


class WeatherService:
    """Provide predefined weather forecasts."""

    FORECASTS = {
        "Kigali": Forecast(
            city="Kigali",
            condition="Sunny",
            temperature_celsius=25,
        ),
        "Nairobi": Forecast(
            city="Nairobi",
            condition="Cloudy",
            temperature_celsius=20,
        ),
    }

    def get_forecast(self, city: str) -> Forecast:
        """Return a forecast for a supported city.

        Args:
            city: Name of the requested city.

        Returns:
            The predefined forecast for the requested city.

        Raises:
            CityNotFoundError: If the city is not supported.
        """
        if city not in self.FORECASTS:
            raise CityNotFoundError(f"City '{city}' was not found.")

        return self.FORECASTS[city]
