"""Provide an interactive command-line weather demonstration."""

from weather_service.exceptions import (
    CityNotFoundError,
    InvalidAPIKeyError,
)
from weather_service.service import WeatherService


def main() -> None:
    """Prompt for credentials and a city, then display its forecast."""
    print("=== TDD Weather Service ===")

    api_key = input("Enter API key: ").strip()
    city = input("Enter city (Kigali/Nairobi): ").strip()

    service = WeatherService(api_key=api_key)

    try:
        forecast = service.get_forecast(city)
    except InvalidAPIKeyError as error:
        print(f"Error: {error}")
        return
    except CityNotFoundError as error:
        print(f"Error: {error}")
        return

    print("\nWeather Forecast")
    print(f"City: {forecast.city}")
    print(f"Condition: {forecast.condition}")
    print(f"Temperature: {forecast.temperature_celsius}°C")
    print("\nThank you for using the Weather Service!")


if __name__ == "__main__":
    main()
