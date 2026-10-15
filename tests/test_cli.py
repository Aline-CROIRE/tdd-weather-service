"""Test the interactive weather service CLI."""

from _pytest.capture import CaptureFixture
from _pytest.monkeypatch import MonkeyPatch

from weather_service.cli import main


def test_cli_displays_forecast_for_valid_input(
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    """Display a forecast when the user enters valid input."""
    inputs = iter(["test-api-key", "Kigali"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    main()

    output = capsys.readouterr().out
    assert "Kigali" in output
    assert "Sunny" in output
    assert "25" in output


def test_cli_displays_error_for_invalid_api_key(
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    """Display an error when the API key is invalid."""
    inputs = iter(["wrong-key", "Kigali"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    main()

    output = capsys.readouterr().out
    assert "Invalid API key" in output


def test_cli_displays_error_for_unknown_city(
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    """Display an error when the city is unsupported."""
    inputs = iter(["test-api-key", "London"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    main()

    output = capsys.readouterr().out
    assert "not found" in output
