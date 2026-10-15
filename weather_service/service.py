"""Provide weather forecast services."""

from weather_service.mock_provider import MockWeatherProvider
from weather_service.models import Forecast
from weather_service.provider import WeatherProvider


class WeatherService:
    """Provide forecasts using an injected weather provider."""

    def __init__(self, provider: WeatherProvider | None = None) -> None:
        """Initialize the service with a provider."""
        self.provider = provider or MockWeatherProvider()

    def get_forecast(self, city: str) -> Forecast:
        """Return a forecast using the configured provider."""
        return self.provider.get_forecast(city)
