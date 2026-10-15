"""Provide predefined weather forecasts for testing."""

from weather_service.exceptions import CityNotFoundError
from weather_service.models import Forecast
from weather_service.provider import WeatherProvider


class MockWeatherProvider(WeatherProvider):
    """Return predefined forecasts without making network requests."""

    FORECASTS = {
        "Kigali": Forecast("Kigali", "Sunny", 25),
        "Nairobi": Forecast("Nairobi", "Cloudy", 20),
    }

    def get_forecast(self, city: str) -> Forecast:
        """Return a forecast for a supported city.

        Args:
            city: Requested city.

        Raises:
            CityNotFoundError: If the city is unsupported.
        """
        if city not in self.FORECASTS:
            raise CityNotFoundError(f"City '{city}' was not found.")
        return self.FORECASTS[city]
