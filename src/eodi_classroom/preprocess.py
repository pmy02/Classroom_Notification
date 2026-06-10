"""Timetable preprocessing.

Turns the raw, PDF-derived timetable export into analysis-ready tables. The
logic mirrors the original ``PDF_to_Excel`` and ``Classroom_Day_Time_EDA``
notebooks, refactored into pure functions that take and return DataFrames so
they can be tested and reused outside a notebook.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from . import config as C


def merge_timetable_sheets(xlsx_path) -> pd.DataFrame:
    """Merge every sheet of a multi-sheet timetable export into one table.

    Keeps only the course, professor, and combined time/room columns.

    Args:
        xlsx_path: Path to an .xlsx file whose sheets share the raw schema.

    Returns:
        Concatenated DataFrame with columns [course, professor, time/room].
    """
    sheets = pd.read_excel(xlsx_path, sheet_name=None)
    combined = pd.concat(sheets.values(), ignore_index=True)
    return combined[[C.COL_COURSE, C.COL_PROFESSOR, C.COL_TIME_ROOM]]


def clean_timetable(df: pd.DataFrame) -> pd.DataFrame:
    """Drop unusable rows and split the combined time/room field.

    Removes rows with missing values or an undetermined instructor, strips the
    department suffix from professor names, and separates the bracketed room
    code from the lecture-time string (raw form: ``"월1, 2 [024-0158]"``).

    Args:
        df: Output of :func:`merge_timetable_sheets`.

    Returns:
        DataFrame with columns [course, professor, time, room], no missing rows.
    """
    df = df.dropna().copy()

    # Drop rows whose instructor is marked as undetermined.
    undetermined = df[C.COL_PROFESSOR].str.contains("강사미정|교수미정", regex=True)
    df = df[~undetermined]

    # Strip the parenthesised department from the professor field.
    df[C.COL_PROFESSOR] = df[C.COL_PROFESSOR].str.replace(r"\(.*?\)", "", regex=True)

    # Separate the bracketed room code from the lecture-time string.
    df[C.COL_ROOM] = df[C.COL_TIME_ROOM].str.extract(r"\[(.*)\]")[0]
    df[C.COL_TIME] = df[C.COL_TIME_ROOM].str.replace(r"\[.*?\]", "", regex=True).str.strip()

    # Blank cells become NaN so they can be dropped uniformly.
    df[[C.COL_TIME, C.COL_ROOM]] = df[[C.COL_TIME, C.COL_ROOM]].replace("", np.nan)
    df = df.dropna(subset=[C.COL_TIME, C.COL_ROOM])

    return df[[C.COL_COURSE, C.COL_PROFESSOR, C.COL_TIME, C.COL_ROOM]].reset_index(drop=True)


def split_day_period(df: pd.DataFrame) -> pd.DataFrame:
    """Expand the lecture-time string into one row per day-tagged token.

    A time string such as ``"월1, 화3"`` becomes two rows: (월, 1) and (화, 3).

    Note: this faithfully reproduces the original project's behaviour, in which
    only tokens that carry their own weekday letter are kept. A string like
    ``"월1, 2"`` (Monday periods 1 and 2) yields only (월, 1); the trailing
    ``2`` has no weekday letter and is dropped. Forward-filling the day onto
    bare period tokens would recover those rows and is a documented limitation
    rather than a bug fix, so the output stays identical to the shipped table.

    Args:
        df: DataFrame containing the lecture-time column.

    Returns:
        DataFrame with columns [course, professor, room, day, period].
    """
    df = df.copy()
    df[C.COL_TIME] = df[C.COL_TIME].astype(str).str.split(",")
    df = df.explode(C.COL_TIME).reset_index(drop=True)
    df[C.COL_TIME] = df[C.COL_TIME].str.strip()

    df[C.COL_DAY] = df[C.COL_TIME].str.extract(r"(\D+)")[0].str.strip()
    df[C.COL_PERIOD] = df[C.COL_TIME].str.extract(r"(\d+)")[0]

    df = df[df[C.COL_PERIOD].notna() & df[C.COL_DAY].notna()].copy()
    df[C.COL_PERIOD] = df[C.COL_PERIOD].astype(int)

    cols = [C.COL_COURSE, C.COL_PROFESSOR, C.COL_ROOM, C.COL_DAY, C.COL_PERIOD]
    return df[cols].reset_index(drop=True)


def build_timetable(xlsx_path) -> pd.DataFrame:
    """Run the timetable pipeline end to end, accepting either input stage.

    The repository ships the already-merged timetable (room and time already
    separated), while the original raw export is a multi-sheet file with the
    combined ``강의시간/강의실`` field. This function detects which it was given:

    * raw export (has the combined time/room column) → merge + clean + split;
    * pre-cleaned table (has separate time and room columns) → split only.

    Either way the result is the day/period-level table.

    Args:
        xlsx_path: Path to a raw or pre-cleaned timetable .xlsx.

    Returns:
        Day/period-level timetable DataFrame.
    """
    sheets = pd.read_excel(xlsx_path, sheet_name=None)
    df = pd.concat(sheets.values(), ignore_index=True)

    if C.COL_TIME_ROOM in df.columns:
        df = clean_timetable(df[[C.COL_COURSE, C.COL_PROFESSOR, C.COL_TIME_ROOM]])

    return split_day_period(df)
