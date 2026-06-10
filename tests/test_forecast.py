"""Optional smoke test for the Prophet forecast path.

Prophet is a heavy dependency, so this test skips itself when it is not
installed. When present, it verifies that a forecast runs end to end and
returns the expected columns on a small synthetic series.
"""

import pytest

from eodi_classroom.forecast import aggregate_daily, fit_forecast
from eodi_classroom.synthetic import generate_touches

prophet = pytest.importorskip("prophet")


def test_fit_forecast_returns_future_predictions():
    df = generate_touches(n_rows=3000, seed=5)
    device = df["device_location"].iloc[0]
    daily = aggregate_daily(df, device_location=device)

    _, forecast = fit_forecast(daily, periods=14)

    for col in ("ds", "yhat", "yhat_lower", "yhat_upper", "yhat_touches"):
        assert col in forecast.columns
    # Forecast horizon extends past the observed window.
    assert len(forecast) == len(daily) + 14
