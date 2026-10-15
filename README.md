# TDD Weather Service

A Python-based mock weather forecasting service developed to demonstrate **Test-Driven Development (TDD)**, clean code, object-oriented design, dependency injection, automated testing, logging, and Git collaboration workflows.

The application returns predefined weather forecasts for supported cities and handles invalid API keys and unsupported cities using custom exceptions. It includes an interactive command-line interface (CLI) for testing the service.

**This project uses a mock weather provider. It does not connect to a real external weather API.**

## Table of Contents

- [Project Objectives](#project-objectives)
- [Features](#features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Error Handling](#error-handling)
- [Testing](#testing)
- [Code Quality](#code-quality)
- [Test-Driven Development Workflow](#test-driven-development-workflow)
- [Git Collaboration Workflow](#git-collaboration-workflow)
- [Limitations and Future Improvements](#limitations-and-future-improvements)
- [Author](#author)

## Project Objectives

This project was developed to practise the following skills:

- Applying the Red-Green-Refactor cycle of Test-Driven Development.
- Writing automated tests with pytest.
- Using pytest fixtures, parametrization, mocking, and log assertions.
- Applying object-oriented programming and SOLID design principles.
- Using dataclasses, type hints, and abstract base classes.
- Implementing dependency injection to reduce coupling.
- Handling errors with custom exceptions.
- Recording application events with Python logging.
- Measuring test coverage using Coverage.py.
- Enforcing code quality using Black, Ruff, Mypy, and pre-commit.
- Managing changes through feature branches and pull requests.

## Features

- **Predefined forecasts:** Returns mock weather forecasts for Kigali and Nairobi.
- **Weather provider abstraction:** Defines a common interface for weather data providers.
- **Dependency injection:** Allows a provider to be supplied to `WeatherService`.
- **API-key validation:** Simulates authorization using a demonstration API key.
- **Custom exceptions:** Distinguishes invalid credentials from unsupported cities.
- **Logging:** Records successful requests and relevant error conditions.
- **Interactive CLI:** Accepts user input and displays forecasts or friendly error messages.
- **Automated tests:** Covers service behavior, errors, provider injection, logging, and CLI output.
- **Type safety:** Uses type hints and strict Mypy checking.
- **Automated quality checks:** Uses Black, Ruff, and pre-commit hooks.

## Architecture

The application separates weather data, provider behavior, service logic, errors, and user interaction into individual modules.

### Components

| Component | Responsibility |
|---|---|
| `models.py` | Defines the `Forecast` dataclass used to represent forecast data. |
| `provider.py` | Defines the abstract `WeatherProvider` interface. |
| `mock_provider.py` | Supplies predefined forecasts and rejects unsupported cities. |
| `service.py` | Implements `WeatherService`, validates the demonstration API key, delegates forecast retrieval, and logs events. |
| `exceptions.py` | Defines `InvalidAPIKeyError` and `CityNotFoundError`. |
| `cli.py` | Provides the interactive command-line interface. |

### Design principles

**Single Responsibility Principle (SRP)**

Each module has a focused responsibility. For example, the mock provider supplies forecast data, while the CLI handles user interaction.

**Dependency Inversion Principle (DIP)**

`WeatherService` depends on the abstract `WeatherProvider` contract rather than requiring a specific provider implementation.

**Dependency Injection**

A provider can be passed to `WeatherService`, allowing alternative implementations to be used without rewriting the service's core logic.

**Abstraction**

The abstract provider defines the expected `get_forecast(city)` method, providing a consistent contract for provider implementations.

**Dataclasses and type hints**

The `Forecast` dataclass represents forecast information, while type hints communicate the expected inputs and outputs of methods.

### Forecast data

The mock provider supplies predefined forecasts for the supported cities. The example below illustrates the response model:

```python
Forecast(
    city="Kigali",
    condition="Sunny",
    temperature_celsius=25,
)
```

The actual forecast returned is determined by the predefined data in `mock_provider.py`.

## Project Structure

```text
tdd-weather-service/
├── tests/
│   ├── __init__.py
│   ├── test_cli.py
│   └── test_weather_service.py
├── weather_service/
│   ├── __init__.py
│   ├── cli.py
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

Coverage.py also generates a `.coverage` data file and an `htmlcov/` report directory when the corresponding commands are run. These are generated artifacts rather than application source files.

## Requirements

- Python 3.11 or newer, as specified by the lab.
- Git.
- PowerShell or another terminal.
- A code editor such as Visual Studio Code.

The project was developed and tested using Python 3.14.8.

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

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell prevents activation, follow the execution-policy guidance appropriate for your environment or use another supported virtual-environment activation method.

### 4. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

## Usage

### Using the service directly

The service can be imported and used from Python code.

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

The output above illustrates the predefined Kigali forecast in the mock provider.

### Using a custom provider

`WeatherService` accepts an injected provider that implements the `WeatherProvider` interface.

```python
from weather_service.mock_provider import MockWeatherProvider
from weather_service.service import WeatherService

provider = MockWeatherProvider()
service = WeatherService(provider=provider)

forecast = service.get_forecast("Nairobi")
print(forecast)
```

This design separates the service's behavior from the source of forecast data.

### Running the interactive CLI

Start the application from the project root:

```powershell
python -m weather_service.cli
```

The application prompts for an API key and a city.

For a successful request, enter:

```text
API key: test-api-key
City: Kigali
```

The CLI displays the forecast details and a completion message.

You can also try the following scenarios:

- Enter an incorrect API key to observe the authentication error.
- Enter an unsupported city, such as `London`, with the correct demonstration key to observe the city-not-found error.

The CLI is an interactive demonstration, not a live weather API client.

## Error Handling

The service uses custom exceptions to make failure cases explicit.

### `InvalidAPIKeyError`

Raised when a request uses an invalid demonstration API key.

### `CityNotFoundError`

Raised when the requested city is not supported by the mock provider.

Example:

```python
from weather_service.exceptions import InvalidAPIKeyError
from weather_service.service import WeatherService

service = WeatherService(api_key="wrong-key")

try:
    service.get_forecast("Kigali")
except InvalidAPIKeyError as error:
    print(f"Request failed: {error}")
```

The CLI catches the expected service exceptions and displays friendly error messages instead of exposing a traceback to the user.

### Security note

The key `test-api-key` is for demonstration and testing only. It is not a production authentication mechanism. A production service would require an appropriate authentication design and secure credential management.

## Testing

The project uses pytest to validate the expected behavior of the service and CLI.

### Run all tests

```powershell
python -m pytest -v
```

### Measure test coverage

Run the test suite through Coverage.py:

```powershell
python -m coverage run -m pytest
python -m coverage report -m
```

The report displays the number of statements, missed statements, coverage percentage, and uncovered line numbers for each measured file.

### Generate an HTML coverage report

```powershell
python -m coverage html
Start-Process htmlcov/index.html
```

The HTML report makes it easier to identify statements that the tests did not execute.

### Testing techniques

The test suite demonstrates:

- **Fixtures:** Set up reusable test dependencies and capture log records.
- **Parametrization:** Check multiple supported-city scenarios using one parametrized test.
- **Mocking and spying:** Verify that the service uses an injected provider.
- **Exception assertions:** Check behavior for invalid API keys and unsupported cities.
- **Log assertions:** Verify that successful requests and errors produce the expected log records.
- **CLI tests:** Simulate user input and inspect displayed output.

### Latest recorded test results

The latest verified run for this version of the project reported:

- **14 tests passed.**
- **99% overall coverage** across the files included in the report.
- Strict Mypy checks passed.
- Black formatting checks passed.
- Ruff lint checks passed.
- All configured pre-commit hooks passed.

These results describe the recorded run; rerun the checks after making changes to verify the current state.

## Code Quality

The project uses automated tools to improve consistency and detect potential problems.

### Black

Check formatting without changing files:

```powershell
python -m black --check .
```

### Ruff

Run lint checks:

```powershell
python -m ruff check .
```

### Mypy

Run strict type checking on the application and tests:

```powershell
python -m mypy --strict weather_service tests
```

### Pre-commit

Run all configured hooks against the repository:

```powershell
python -m pre_commit run --all-files
```

The repository configuration defines hooks for Black, Ruff, and Mypy.

## Test-Driven Development Workflow

The project follows the **Red-Green-Refactor** cycle.

### 1. Red — Write a failing test

Write a test that describes the behavior required from the service. Run it and verify that it fails for the expected reason.

### 2. Green — Implement the minimum solution

Write only enough production code to satisfy the failing test. Run the test again and verify that it passes.

### 3. Refactor — Improve the design

Improve the code's organization, naming, typing, or structure without changing its intended behavior. Run the relevant tests and quality checks again.

### Repeat

Apply this cycle as new behavior is introduced, including predefined forecasts, error handling, logging, provider injection, and CLI interactions.

The Git history provides evidence of the development process. Individual commits should be reviewed to identify the specific test and implementation changes that demonstrate the cycle.

## Git Collaboration Workflow

The project uses short-lived feature branches and pull requests rather than direct commits to `main`.

### 1. Update the main branch

```powershell
git switch main
git pull origin main
```

### 2. Create a feature branch

```powershell
git switch -c feature/example-change
```

Choose a branch name that describes the feature or improvement.

### 3. Implement the change using TDD

Write a failing test, implement the minimum behavior, and refactor while keeping tests passing.

### 4. Run validation

```powershell
python -m pytest -v
python -m mypy --strict weather_service tests
python -m black --check .
python -m ruff check .
python -m pre_commit run --all-files
```

### 5. Commit and push

```powershell
git add .
git commit -m "feat: describe the change"
git push -u origin feature/example-change
```

### 6. Open a pull request

Create a pull request on GitHub, review the changes, address feedback, and merge according to the repository's review process.

Keep feature branches focused and avoid committing directly to `main`.

## Limitations and Future Improvements

This project is intentionally a mock service designed for learning and assessment.

Possible future improvements include:

- Implementing a real provider that retrieves data from a weather API.
- Adding provider-specific integration tests using mocked external responses.
- Expanding supported cities and forecast scenarios.
- Introducing richer forecast models and input validation.
- Adding automated coverage thresholds to the quality-check workflow.
- Testing additional CLI execution paths and provider edge cases.

These are possible extensions, not features currently claimed as implemented.

## Author

**Aline NIYONIZERA**

GitHub: [Aline-CROIRE](https://github.com/Aline-CROIRE)

Project repository: [TDD Weather Service](https://github.com/Aline-CROIRE/tdd-weather-service)