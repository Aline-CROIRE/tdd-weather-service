
import pytest

from weather_service.exceptions import CityNotFoundError, InvalidAPIKeyError
from weather_service.service import WeatherService


def test_get_forecast_returns_kigali_forecast():
    service = WeatherService()

    forecast = service.get_forecast("Kigali")

    assert forecast.city == "Kigali"


def test_get_forecast_returns_weather_details():
    service = WeatherService()

    forecast = service.get_forecast("Kigali")

    assert forecast.condition == "Sunny"
    assert forecast.temperature_celsius == 25


def test_get_forecast_returns_nairobi_forecast():
    service = WeatherService()

    forecast = service.get_forecast("Nairobi")

    assert forecast.city == "Nairobi"
    assert forecast.condition == "Cloudy"
    assert forecast.temperature_celsius == 20


def test_get_forecast_raises_error_for_unknown_city():
    service = WeatherService()

    with pytest.raises(CityNotFoundError):
        service.get_forecast("UnknownCity")




def test_invalid_api_key_error_is_an_exception():
    error = InvalidAPIKeyError("Invalid API key")

    assert str(error) == "Invalid API key"