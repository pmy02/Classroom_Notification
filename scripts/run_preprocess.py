"""Build the cleaned, day/period-level timetable from the raw export.

Usage:
    python scripts/run_preprocess.py [--in RAW.xlsx] [--out OUT.xlsx]
"""

from __future__ import annotations

import argparse

from eodi_classroom import config as C
from eodi_classroom.preprocess import build_timetable


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--in", dest="inp", default=str(C.TIMETABLE_XLSX),
                        help="Raw timetable .xlsx (multi-sheet export).")
    parser.add_argument("--out", default=str(C.TIMETABLE_DAY_PERIOD_XLSX),
                        help="Output path for the day/period table.")
    args = parser.parse_args()

    df = build_timetable(args.inp)
    df.to_excel(args.out, index=False)
    print(f"Wrote {len(df):,} day/period rows to {args.out}")


if __name__ == "__main__":
    main()
