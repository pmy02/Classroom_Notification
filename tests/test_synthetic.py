"""Tests for the synthetic generator and daily aggregation.

No Prophet here: model fitting is slow and is covered by the (optional)
forecast smoke test. These checks are fast and deterministic.
"""

from eodi_classroom import config as C
from eodi_classroom.forecast import aggregate_daily
from eodi_classroom.synthetic import generate_touches


def test_generate_is_reproducible_with_seed():
    a = generate_touches(n_rows=500, seed=7)
    b = generate_touches(n_rows=500, seed=7)
    assert a.equals(b)


def test_generate_schema_and_building_consistency():
    df = generate_touches(n_rows=500, seed=1)
    assert list(df.columns) == [C.COL_BUILDING, C.COL_DEVICE, C.COL_DATETIME, C.COL_TOUCHES]
    assert len(df) == 500
    # The building prefix must match its device location.
    for building, device in zip(df[C.COL_BUILDING], df[C.COL_DEVICE]):
        assert device.startswith(building)
    assert df[C.COL_TOUCHES].min() >= 0


def test_aggregate_daily_sums_within_device_and_day():
    df = generate_touches(n_rows=2000, seed=3)
    daily = aggregate_daily(df)
    # Aggregated total must equal the raw total.
    assert daily[C.COL_TOUCHES].sum() == df[C.COL_TOUCHES].sum()
    # One row per (device, day) pair.
    assert not daily.duplicated(subset=[C.COL_DEVICE, "date"]).any()
