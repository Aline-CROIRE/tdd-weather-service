"""Provide weather forecast services."""

import logging

from weather_service.exceptions import CityNotFoundError
from weather_service.mock_provider import MockWeatherProvider
from weather_service.models import Forecast
from weather_service.provider import WeatherProvider

logger = logging.getLogger(__name__)


class WeatherService:
    """Provide forecasts using an injected weather provider."""

    def __init__(self, provider: WeatherProvider | None = None) -> None:
        """Initialize the service with a weather provider.

        Args:
            provider: Provider used to retrieve forecasts. Defaults to
                MockWeatherProvider when no provider is supplied.
        """
        self.provider = (
            provider if provider is not None else MockWeatherProvider()
        )

    def get_forecast(self, city: str) -> Forecast:
        """Return a forecast for the requested city.

        Args:
            city: Name of the requested city.

        Returns:
            The forecast returned by the configured provider.

        Raises:
            CityNotFoundError: If the requested city is unsupported.
        """
        logger.info("Fetching forecast for city: %s", city)

        try:
            forecast = self.provider.get_forecast(city)
        except CityNotFoundError:
            logger.warning(
                "Forecast requested for unsupported city: %s",
                city,
            )
            raise

        logger.info(
            "Forecast retrieved successfully for city: %s",
            city,
        )
        return forecast
