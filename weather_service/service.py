"""Provide weather forecast services."""

import logging

from weather_service.exceptions import (
    CityNotFoundError,
    InvalidAPIKeyError,
)
from weather_service.mock_provider import MockWeatherProvider
from weather_service.models import Forecast
from weather_service.provider import WeatherProvider

logger = logging.getLogger(__name__)


class WeatherService:
    """Provide forecasts using an injected weather provider."""

    VALID_API_KEY = "test-api-key"

    def __init__(
        self,
        provider: WeatherProvider | None = None,
        api_key: str = "test-api-key",
    ) -> None:
        """Initialize the service with a provider and API key.

        Args:
            provider: Provider used to retrieve forecasts. Defaults to
                MockWeatherProvider when no provider is supplied.
            api_key: API key used to authorize forecast requests.
        """
        self.provider = provider if provider is not None else MockWeatherProvider()
        self.api_key = api_key

    def get_forecast(self, city: str) -> Forecast:
        """Return a forecast for the requested city.

        Args:
            city: Name of the requested city.

        Returns:
            The forecast returned by the configured provider.

        Raises:
            InvalidAPIKeyError: If the API key is invalid.
            CityNotFoundError: If the requested city is unsupported.
        """
        if self.api_key != self.VALID_API_KEY:
            logger.warning("Forecast request rejected: invalid API key")
            raise InvalidAPIKeyError("Invalid API key")

        logger.info("Fetching forecast for city: %s", city)

        try:
            forecast = self.provider.get_forecast(city)
        except CityNotFoundError:
            logger.warning(
                "Forecast requested for unsupported city: %s",
                city,
            )
            raise

        logger.info("Forecast retrieved successfully for city: %s", city)
        return forecast
