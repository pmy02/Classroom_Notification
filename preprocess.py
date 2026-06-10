"""Generate the synthetic device-touch dataset (reproducible via --seed).

The output is synthetic and exists only to exercise the forecasting pipeline.

Usage:
    python scripts/generate_synthetic.py [--out device_touches.xlsx] [--rows N] [--seed S]
"""

from __future__ import annotations

import argparse

from eodi_classroom import config as C
from eodi_classroom.synthetic import generate_touches


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=str(C.DEVICE_TOUCHES_XLSX),
                        help="Output .xlsx path.")
    parser.add_argument("--rows", type=int, default=40_000, help="Number of rows to generate.")
    parser.add_argument("--seed", type=int, default=42, help="RNG seed.")
    args = parser.parse_args()

    df = generate_touches(n_rows=args.rows, seed=args.seed)
    df.to_excel(args.out, index=False)
    print(f"Wrote {len(df):,} synthetic rows to {args.out} (seed={args.seed})")


if __name__ == "__main__":
    main()
