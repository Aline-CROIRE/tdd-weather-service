"""Define the weather provider interface."""

from abc import ABC, abstractmethod

from weather_service.models import Forecast


class WeatherProvider(ABC):
    """Define the contract for weather data providers."""

    @abstractmethod
    def get_forecast(self, city: str) -> Forecast:
        """Return a forecast for a city."""
        raise NotImplementedError
