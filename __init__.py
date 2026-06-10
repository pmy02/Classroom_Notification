"""Run timetable EDA: print top slots and save the demand heatmap.

Usage:
    python scripts/run_eda.py [--in DAY_PERIOD.xlsx] [--fig docs/heatmap.png]
"""

from __future__ import annotations

import argparse

import pandas as pd

from eodi_classroom import config as C
from eodi_classroom.eda import busiest_slots, plot_heatmap


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--in", dest="inp", default=str(C.TIMETABLE_DAY_PERIOD_XLSX),
                        help="Day/period-level timetable .xlsx.")
    parser.add_argument("--fig", default=str(C.DOCS_DIR / "heatmap.png"),
                        help="Where to save the day x period heatmap.")
    parser.add_argument("--top", type=int, default=10, help="Number of busiest slots to print.")
    args = parser.parse_args()

    df = pd.read_excel(args.inp)

    print(f"Top {args.top} busiest (day, period) slots:")
    print(busiest_slots(df, top_n=args.top).to_string(index=False))

    import matplotlib
    matplotlib.use("Agg")

    ax = plot_heatmap(df)
    ax.figure.tight_layout()
    ax.figure.savefig(args.fig, dpi=150)
    print(f"Saved heatmap to {args.fig}")


if __name__ == "__main__":
    main()
