"""Tests for the timetable preprocessing logic.

These run on small inline DataFrames, so they need no data files and no
network, and exercise the parsing rules that are easy to break.
"""

import pandas as pd

from eodi_classroom import config as C
from eodi_classroom.preprocess import clean_timetable, split_day_period


def _raw_row(course, prof, time_room):
    return {C.COL_COURSE: course, C.COL_PROFESSOR: prof, C.COL_TIME_ROOM: time_room}


def test_clean_splits_room_and_drops_undetermined():
    raw = pd.DataFrame([
        _raw_row("논어이야기", "문정우(철학과)", "목1, 2 [024-0158]"),
        _raw_row("미정과목", "강사미정", "월3 [024-0100]"),
    ])
    cleaned = clean_timetable(raw)

    # The undetermined-instructor row is dropped.
    assert len(cleaned) == 1
    row = cleaned.iloc[0]
    # Department suffix is stripped, room is separated from time.
    assert row[C.COL_PROFESSOR] == "문정우"
    assert row[C.COL_ROOM] == "024-0158"
    assert row[C.COL_TIME] == "목1, 2"


def test_split_day_period_explodes_day_tagged_tokens():
    cleaned = pd.DataFrame({
        C.COL_COURSE: ["논어이야기"],
        C.COL_PROFESSOR: ["문정우"],
        C.COL_TIME: ["월1, 화3"],
        C.COL_ROOM: ["024-0158"],
    })
    out = split_day_period(cleaned)

    # Each day-tagged token becomes its own row.
    assert len(out) == 2
    assert sorted(zip(out[C.COL_DAY], out[C.COL_PERIOD])) == [("월", 1), ("화", 3)]
    assert out[C.COL_PERIOD].dtype.kind == "i"


def test_split_day_period_drops_bare_period_tokens():
    # Faithful to the original project: a trailing period with no weekday
    # letter ("월1, 2" -> Monday periods 1 and 2) keeps only the tagged token.
    cleaned = pd.DataFrame({
        C.COL_COURSE: ["행복심리학"],
        C.COL_PROFESSOR: ["양난미"],
        C.COL_TIME: ["월1, 2"],
        C.COL_ROOM: ["024-0175"],
    })
    out = split_day_period(cleaned)
    assert list(zip(out[C.COL_DAY], out[C.COL_PERIOD])) == [("월", 1)]
