"""Forecast daily touches for one device with Prophet and save the plot.

Usage:
    python scripts/run_forecast.py [--in device_touches.xlsx] \
        [--device "교양학관-1층"] [--periods 30] [--fig docs/forecast.png]
"""

from __future__ import annotations

import argparse

import pandas as pd

from eodi_classroom import config as C
from eodi_classroom.forecast import aggregate_daily, fit_forecast


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--in", dest="inp", default=str(C.DEVICE_TOUCHES_XLSX),
                        help="Device-touch log .xlsx.")
    parser.add_argument("--device", default=C.DEVICE_LOCATIONS[0],
                        help="Device location to forecast.")
    parser.add_argument("--periods", type=int, default=30, help="Days to forecast ahead.")
    parser.add_argument("--fig", default=str(C.DOCS_DIR / "forecast.png"),
                        help="Where to save the forecast plot.")
    args = parser.parse_args()

    df = pd.read_excel(args.inp)
    daily = aggregate_daily(df, device_location=args.device)
    if daily.empty:
        raise SystemExit(f"No rows for device '{args.device}'. "
                         f"Known devices: {C.DEVICE_LOCATIONS}")

    model, forecast = fit_forecast(daily, periods=args.periods)
    tail = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail()
    print(f"Forecast tail for {args.device} (log scale):")
    print(tail.to_string(index=False))

    import matplotlib
    matplotlib.use("Agg")

    fig = model.plot(forecast, xlabel="Date", ylabel="log(touch count)")
    fig.gca().set_title(f"Device touch forecast — {args.device} (synthetic data)")
    fig.tight_layout()
    fig.savefig(args.fig, dpi=150)
    print(f"Saved forecast plot to {args.fig}")


if __name__ == "__main__":
    main()
