# TDD Weather Service

A Python weather forecasting service built to practise Test-Driven Development (TDD), object-oriented programming, dependency injection, mocking, automated testing, logging, and code-quality automation.

The project uses a mock weather provider with predefined forecasts. It does not make requests to a real external weather API.

## Features

- **Weather forecasts:** Retrieve predefined forecasts for supported cities.
- **Dependency injection:** Supply a custom weather provider to `WeatherService`.
- **Abstract provider interface:** Define a consistent contract for weather providers using `WeatherProvider`.
- **API-key validation:** Simulate authorization using a configurable test API key.
- **Custom exceptions:** Handle invalid API keys and unsupported cities.
- **Structured logging:** Record successful requests and rejected requests.
- **Automated testing:** Use pytest fixtures, parametrized tests, mocks, and log assertions.
- **Code quality:** Apply Black, Ruff, and strict Mypy checks.
- **Automated checks:** Run configured pre-commit hooks.

## Project Structure

```text
tdd-weather-service/
├── tests/
│   ├── __init__.py
│   └── test_weather_service.py
├── weather_service/
│   ├── __init__.py
│   ├── exceptions.py
│   ├── mock_provider.py
│   ├── models.py
│   ├── provider.py
│   └── service.py
├── .gitignore
├── .pre-commit-config.yaml
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.10 or newer
- Git
- PowerShell or another terminal

The project was developed and tested with Python 3.14.

## Installation

### 1. Clone the repository

```powershell
git clone https://github.com/Aline-CROIRE/tdd-weather-service.git
cd tdd-weather-service
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

### 3. Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use an appropriate execution-policy setting for your environment or activate the environment through another supported method.

### 4. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

## Usage

The service provides predefined forecasts for Kigali and Nairobi.

Example:

```python
from weather_service.service import WeatherService

service = WeatherService(api_key="test-api-key")
forecast = service.get_forecast("Kigali")

print(forecast)
```

Example output:

```text
Forecast(city='Kigali', condition='Sunny', temperature_celsius=25)
```

### Using a custom provider

The service accepts a provider that implements the `WeatherProvider` interface. This allows the forecasting logic to work with different providers without depending on a particular implementation.

```python
from weather_service.mock_provider import MockWeatherProvider
from weather_service.service import WeatherService

provider = MockWeatherProvider()
service = WeatherService(provider=provider)

forecast = service.get_forecast("Nairobi")
print(forecast)
```

## API-Key Validation and Exceptions

The service currently uses a simulated API key for learning purposes:

```python
"test-api-key"
```

An invalid key raises `InvalidAPIKeyError`. Requesting an unsupported city raises `CityNotFoundError`.

Example:

```python
from weather_service.exceptions import (
    CityNotFoundError,
    InvalidAPIKeyError,
)
from weather_service.service import WeatherService

service = WeatherService(api_key="wrong-key")

try:
    service.get_forecast("Kigali")
except InvalidAPIKeyError as error:
    print(error)
```

**Security note:** The test key is not a production authentication mechanism. A real application should use secure credential management and an appropriate authentication design.

## Running the Tests

Run the complete test suite:

```powershell
python -m pytest
```

Run tests with coverage:

```powershell
python -m pytest --cov=weather_service --cov-report=term-missing
```

Generate an HTML coverage report:

```powershell
python -m pytest --cov=weather_service --cov-report=html
```

Open the report in your browser:

```powershell
Start-Process htmlcov/index.html
```

The latest recorded test run passed all 10 tests and reported 99% overall coverage. The abstract method in `provider.py` accounts for the remaining uncovered line.

## Code Quality

Run the individual checks:

```powershell
python -m black --check .
python -m ruff check .
python -m mypy --strict weather_service tests
```

Run all configured pre-commit hooks:

```powershell
python -m pre_commit run --all-files
```

These tools help maintain consistent formatting, identify potential errors, and enforce static type checking.

## Development Workflow

This project uses short-lived feature branches and pull requests rather than direct commits to `main`.

1. Update your local `main` branch.
2. Create a branch for one focused feature or improvement.
3. Write a failing test before implementing the feature.
4. Implement the smallest change that makes the test pass.
5. Refactor while keeping the tests green.
6. Run the tests and quality checks.
7. Commit and push the feature branch.
8. Open a pull request, review the changes, and merge after approval.

Example:

```powershell
git switch main
git pull origin main
git switch -c feature/example-change
```

After implementing and testing the change:

```powershell
git add .
git commit -m "feat: describe the change"
git push -u origin feature/example-change
```

Open a pull request on GitHub to merge the feature into `main`.

## Learning Objectives

This project demonstrates practical experience with:

- Test-Driven Development: red, green, and refactor.
- Python dataclasses, type hints, and abstract base classes.
- Dependency injection and separation of responsibilities.
- Custom exceptions and logging.
- Pytest fixtures, parametrization, mocking, and coverage.
- Formatting, linting, static type checking, and pre-commit hooks.
- Git branching, commits, pull requests, and collaborative workflows.

## Author

Aline NIYONIZERA

GitHub: [Aline-CROIRE](https://github.com/Aline-CROIRE)