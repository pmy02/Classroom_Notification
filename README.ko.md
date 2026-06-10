"""Daily usage aggregation and Prophet time-series forecasting.

Refactors the ``Device_Usage_Analytics`` notebook into reusable functions.
The forecast is fit on a log-transformed daily touch total, matching the
original analysis; predictions are returned on both the log and original
scales so callers do not have to remember the transform.

Because the input is synthetic (see :mod:`eodi_classroom.synthetic`), the
forecast demonstrates the pipeline rather than any real campus usage trend.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from . import config as C


def aggregate_daily(df: pd.DataFrame, device_location: str | None = None) -> pd.DataFrame:
    """Aggregate touch logs into a daily total per device.

    Args:
        df: Device-touch log with datetime and touch columns.
        device_location: If given, restrict to a single device location.

    Returns:
        DataFrame with columns [device_location, date, touches], one row per
        device per day.
    """
    df = df.copy()
    df[C.COL_DATETIME] = pd.to_datetime(df[C.COL_DATETIME])
    df["date"] = df[C.COL_DATETIME].dt.normalize()

    if device_location is not None:
        df = df[df[C.COL_DEVICE] == device_location]

    daily = (
        df.groupby([C.COL_DEVICE, "date"], as_index=False)[C.COL_TOUCHES]
        .sum()
    )
    return daily


def to_prophet_frame(daily: pd.DataFrame, log_transform: bool = True) -> pd.DataFrame:
    """Reshape a daily series into Prophet's ``ds``/``y`` schema.

    Args:
        daily: Output of :func:`aggregate_daily` for a single device.
        log_transform: If True, model ``log(touches)`` (clipped at 1) to keep
            the series positive and stabilise variance.

    Returns:
        DataFrame with columns [ds, y].
    """
    frame = daily.rename(columns={"date": "ds", C.COL_TOUCHES: "y"})[["ds", "y"]].copy()
    if log_transform:
        frame["y"] = np.log(frame["y"].clip(lower=1))
    return frame


def fit_forecast(daily: pd.DataFrame, periods: int = 30, log_transform: bool = True):
    """Fit Prophet on one device's daily series and forecast forward.

    Args:
        daily: Output of :func:`aggregate_daily` for a single device.
        periods: Number of future days to forecast.
        log_transform: Whether the series was log-transformed (see
            :func:`to_prophet_frame`). If True, an extra ``yhat_touches``
            column is added with the inverse-transformed prediction.

    Returns:
        Tuple ``(model, forecast)`` where ``forecast`` is Prophet's output
        DataFrame, optionally with the original-scale prediction appended.
    """
    from prophet import Prophet

    frame = to_prophet_frame(daily, log_transform=log_transform)

    model = Prophet()
    model.fit(frame)

    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)

    if log_transform:
        forecast["yhat_touches"] = np.exp(forecast["yhat"])

    return model, forecast
