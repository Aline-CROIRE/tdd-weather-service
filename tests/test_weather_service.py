"""Test weather service behavior."""

import pytest

from weather_service.exceptions import CityNotFoundError, InvalidAPIKeyError
from weather_service.models import Forecast
from weather_service.service import WeatherService


class FakeProvider:
    """Provide predictable forecasts for tests."""

    def get_forecast(self, city: str) -> Forecast:
        """Return a forecast for the requested city."""
        if city not in {"Kigali", "Nairobi"}:
            raise CityNotFoundError(f"City '{city}' was not found.")
        return Forecast(city, "Rainy", 18)


@pytest.fixture
def provider():
    """Create a fake weather provider."""
    return FakeProvider()


@pytest.fixture
def service(provider):
    """Create a service with an injected fake provider."""
    return WeatherService(provider=provider)


@pytest.mark.parametrize(
    ("city", "expected_condition", "expected_temperature"),
    [
        ("Kigali", "Rainy", 18),
        ("Nairobi", "Rainy", 18),
    ],
)
def test_get_forecast_with_provider(
    service, city, expected_condition, expected_temperature
):
    """Test forecasts for multiple supported cities."""
    forecast = service.get_forecast(city)

    assert forecast.city == city
    assert forecast.condition == expected_condition
    assert forecast.temperature_celsius == expected_temperature


def test_get_forecast_raises_for_unknown_city(service):
    """Test that unsupported cities raise an exception."""
    with pytest.raises(CityNotFoundError):
        service.get_forecast("UnknownCity")


def test_service_uses_injected_provider(mocker):
    """Test dependency injection with a mocked provider."""
    mock_provider = mocker.Mock()
    expected = Forecast("Kigali", "Cloudy", 21)
    mock_provider.get_forecast.return_value = expected

    service = WeatherService(provider=mock_provider)
    result = service.get_forecast("Kigali")

    assert result == expected
    mock_provider.get_forecast.assert_called_once_with("Kigali")


def test_invalid_api_key_error_is_an_exception():
    """Test the custom API key exception."""
    error = InvalidAPIKeyError("Invalid API key")

    assert str(error) == "Invalid API key"


def test_mock_provider_rejects_unknown_city():
    """Test that the mock provider rejects unsupported cities."""
    from weather_service.mock_provider import MockWeatherProvider

    provider = MockWeatherProvider()

    with pytest.raises(CityNotFoundError):
        provider.get_forecast("UnknownCity")


def test_mock_provider_returns_kigali_forecast():
    """Test the mock provider returns its predefined Kigali forecast."""
    from weather_service.mock_provider import MockWeatherProvider

    provider = MockWeatherProvider()

    forecast = provider.get_forecast("Kigali")

    assert forecast.city == "Kigali"
    assert forecast.condition == "Sunny"
