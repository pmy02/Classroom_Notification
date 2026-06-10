"""Exploratory analysis of the cleaned timetable.

These functions answer the project's core placement question — where and when
is teaching concentrated — by counting lectures per classroom, professor, day,
and period, and by building the day x period demand heatmap. Plotting is kept
separate from computation so the tables can be tested without a display.
"""

from __future__ import annotations

import pandas as pd

from . import config as C


def count_by(df: pd.DataFrame, column: str) -> pd.Series:
    """Return value counts for a single column, descending.

    Args:
        df: Any timetable DataFrame.
        column: Column to tally.

    Returns:
        Series indexed by category value, sorted by frequency.
    """
    return df[column].value_counts()


def day_period_crosstab(df: pd.DataFrame) -> pd.DataFrame:
    """Build the day x period lecture-count matrix.

    Rows follow weekday order and columns follow period order, both restricted
    to values actually present in the data.

    Args:
        df: Day/period-level timetable (see ``preprocess.build_timetable``).

    Returns:
        Crosstab DataFrame of lecture counts.
    """
    table = pd.crosstab(df[C.COL_DAY], df[C.COL_PERIOD])
    day_order = [d for d in C.DAYS if d in table.index]
    period_order = [p for p in C.PERIODS if p in table.columns]
    return table.reindex(index=day_order, columns=period_order).fillna(0).astype(int)


def busiest_slots(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Return the busiest (day, period) slots by lecture count.

    Args:
        df: Day/period-level timetable.
        top_n: Number of slots to return.

    Returns:
        DataFrame with columns [day, period, count], highest first.
    """
    stacked = (
        day_period_crosstab(df)
        .stack()
        .reset_index(name="count")
        .rename(columns={C.COL_DAY: "day", C.COL_PERIOD: "period"})
    )
    return stacked.nlargest(top_n, "count").reset_index(drop=True)


def plot_heatmap(df: pd.DataFrame, ax=None):
    """Render the day x period demand heatmap.

    Args:
        df: Day/period-level timetable.
        ax: Optional matplotlib Axes; created if omitted.

    Returns:
        The matplotlib Axes containing the heatmap.
    """
    import matplotlib.pyplot as plt
    import seaborn as sns

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 4))
    sns.heatmap(day_period_crosstab(df), cmap="Blues", annot=True, fmt="d", ax=ax)
    ax.set_title("Lectures by day and period")
    ax.set_xlabel("Period")
    ax.set_ylabel("Day")
    return ax
