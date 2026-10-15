
import pytest

from weather_service.exceptions import CityNotFoundError
from weather_service.service import WeatherService


def test_get_forecast_returns_kigali_forecast():
    service = WeatherService()

    forecast = service.get_forecast("Kigali")

    assert forecast.city == "Kigali"


def test_get_forecast_raises_error_for_unknown_city():
    service = WeatherService()

    with pytest.raises(CityNotFoundError):
        service.get_forecast("UnknownCity")
