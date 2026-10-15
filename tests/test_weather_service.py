"""Test the weather service and its mock provider."""

import logging

import pytest
from pytest import LogCaptureFixture
from pytest_mock import MockerFixture

from weather_service.exceptions import (
    CityNotFoundError,
    InvalidAPIKeyError,
)
from weather_service.mock_provider import MockWeatherProvider
from weather_service.models import Forecast
from weather_service.provider import WeatherProvider
from weather_service.service import WeatherService


class FakeProvider(WeatherProvider):
    """Provide predictable forecasts for service tests."""

    def get_forecast(self, city: str) -> Forecast:
        """Return a fake forecast for a supported city.

        Args:
            city: Name of the requested city.

        Returns:
            A predictable forecast.

        Raises:
            CityNotFoundError: If the city is unsupported.
        """
        if city not in ("Kigali", "Nairobi"):
            raise CityNotFoundError(f"City '{city}' was not found.")

        return Forecast(
            city=city,
            condition="Rainy",
            temperature_celsius=18,
        )


@pytest.fixture
def provider() -> FakeProvider:
    """Create a fake weather provider."""
    return FakeProvider()


@pytest.fixture
def service(provider: FakeProvider) -> WeatherService:
    """Create a weather service with a fake provider."""
    return WeatherService(provider=provider)


@pytest.mark.parametrize(
    ("city", "expected_condition", "expected_temperature"),
    [
        ("Kigali", "Rainy", 18),
        ("Nairobi", "Rainy", 18),
    ],
)
def test_get_forecast_with_provider(
    service: WeatherService,
    city: str,
    expected_condition: str,
    expected_temperature: int,
) -> None:
    """Return the expected forecast for a supported city."""
    forecast = service.get_forecast(city)

    assert forecast.city == city
    assert forecast.condition == expected_condition
    assert forecast.temperature_celsius == expected_temperature


def test_get_forecast_raises_for_unknown_city(
    service: WeatherService,
) -> None:
    """Raise an exception for an unsupported city."""
    with pytest.raises(CityNotFoundError, match="was not found"):
        service.get_forecast("London")


def test_service_uses_injected_provider(
    provider: FakeProvider,
    mocker: MockerFixture,
) -> None:
    """Use the provider supplied to the service."""
    spy = mocker.spy(provider, "get_forecast")
    service = WeatherService(provider=provider)

    forecast = service.get_forecast("Kigali")

    spy.assert_called_once_with("Kigali")
    assert forecast.city == "Kigali"


def test_valid_api_key_allows_forecast(
    provider: FakeProvider,
) -> None:
    """Allow requests when the API key is valid."""
    service = WeatherService(
        provider=provider,
        api_key="test-api-key",
    )

    forecast = service.get_forecast("Kigali")

    assert forecast.city == "Kigali"


def test_invalid_api_key_raises_error(
    provider: FakeProvider,
) -> None:
    """Reject requests when the API key is invalid."""
    service = WeatherService(
        provider=provider,
        api_key="wrong-key",
    )

    with pytest.raises(InvalidAPIKeyError, match="Invalid API key"):
        service.get_forecast("Kigali")


def test_mock_provider_rejects_unknown_city() -> None:
    """Raise an exception for an unsupported mock-provider city."""
    provider = MockWeatherProvider()

    with pytest.raises(CityNotFoundError, match="was not found"):
        provider.get_forecast("London")


def test_mock_provider_returns_kigali_forecast() -> None:
    """Return the predefined forecast for Kigali."""
    provider = MockWeatherProvider()

    forecast = provider.get_forecast("Kigali")

    assert forecast == Forecast(
        city="Kigali",
        condition="Sunny",
        temperature_celsius=25,
    )


def test_successful_forecast_is_logged(
    caplog: LogCaptureFixture,
    provider: FakeProvider,
) -> None:
    """Log a successful forecast request."""
    service = WeatherService(provider=provider)

    with caplog.at_level(logging.INFO):
        service.get_forecast("Kigali")

    assert "Fetching forecast for city: Kigali" in caplog.text
    assert "Forecast retrieved successfully for city: Kigali" in caplog.text


def test_unknown_city_warning_is_logged(
    caplog: LogCaptureFixture,
    provider: FakeProvider,
) -> None:
    """Log a warning when a city is unsupported."""
    service = WeatherService(provider=provider)

    with caplog.at_level(logging.WARNING):
        with pytest.raises(CityNotFoundError):
            service.get_forecast("London")

    assert "Forecast requested for unsupported city: London" in caplog.text


def test_invalid_api_key_warning_is_logged(
    caplog: LogCaptureFixture,
    provider: FakeProvider,
) -> None:
    """Log a warning when an invalid API key is supplied."""
    service = WeatherService(
        provider=provider,
        api_key="wrong-key",
    )

    with caplog.at_level(logging.WARNING):
        with pytest.raises(InvalidAPIKeyError):
            service.get_forecast("Kigali")

    assert "Forecast request rejected: invalid API key" in caplog.text
