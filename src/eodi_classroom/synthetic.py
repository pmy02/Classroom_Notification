"""Seeded generator for the synthetic device-touch dataset.

The notifier devices were never physically deployed, so usage data does not
exist. This module produces a *synthetic* stand-in used only to exercise the
forecasting pipeline. Unlike the original notebook, generation is seeded and
parameterised, so the dataset is reproducible.

The output is not real measurement data and must not be interpreted as such.
"""

from __future__ import annotations

import datetime as dt

import numpy as np
import pandas as pd

from . import config as C


def generate_touches(
    device_locations=None,
    start: dt.date = dt.date(2022, 1, 1),
    end: dt.date = dt.date(2022, 1, 31),
    n_rows: int = 40_000,
    max_touches: int = 100,
    seed: int = 42,
) -> pd.DataFrame:
    """Generate a reproducible synthetic device-touch log.

    Each row is one logged interaction: a building, a per-floor device
    location, a timestamp drawn uniformly from ``[start, end)``, and a touch
    count drawn uniformly from ``[0, max_touches]``.

    Args:
        device_locations: Device locations to sample from. Defaults to the
            project's full set (``config.DEVICE_LOCATIONS``).
        start: Inclusive start date of the timestamp window.
        end: Exclusive end date of the timestamp window.
        n_rows: Number of rows to generate.
        max_touches: Maximum touch count per row.
        seed: RNG seed for reproducibility.

    Returns:
        DataFrame with columns [building, device_location, datetime, touches],
        sorted by device location then timestamp.
    """
    rng = np.random.default_rng(seed)
    locations = list(device_locations or C.DEVICE_LOCATIONS)

    chosen = rng.choice(locations, size=n_rows)
    buildings = np.array([loc.split("-")[0] for loc in chosen])

    span_seconds = int((end - start).total_seconds())
    offsets = rng.integers(0, span_seconds, size=n_rows)
    base = dt.datetime.combine(start, dt.time())
    timestamps = [base + dt.timedelta(seconds=int(s)) for s in offsets]

    touches = rng.integers(0, max_touches + 1, size=n_rows)

    df = pd.DataFrame(
        {
            C.COL_BUILDING: buildings,
            C.COL_DEVICE: chosen,
            C.COL_DATETIME: timestamps,
            C.COL_TOUCHES: touches,
        }
    )
    return df.sort_values([C.COL_DEVICE, C.COL_DATETIME]).reset_index(drop=True)
