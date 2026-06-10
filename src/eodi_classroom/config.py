"""Shared paths, column names, and domain constants.

Centralising these removes the hard-coded, per-notebook file names that the
original project scattered across cells, and makes the column references
robust to the Korean headers used in the source spreadsheets.
"""

from __future__ import annotations

from pathlib import Path

# --- Paths -----------------------------------------------------------------
# Repository root, resolved relative to this file (src/eodi_classroom/config.py).
ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "Data"
DOCS_DIR = ROOT / "docs"

# Canonical input/intermediate artifacts shipped in the repo.
TIMETABLE_XLSX = DATA_DIR / "2020 ~ 2021 수업시간표.xlsx"
TIMETABLE_DAY_PERIOD_XLSX = DATA_DIR / "2020 ~ 2021 수업시간표 - 요일,교시 분리.xlsx"
DEVICE_TOUCHES_XLSX = DATA_DIR / "device_touches.xlsx"

# --- Timetable columns (Korean source headers) -----------------------------
COL_COURSE = "교과목명"       # course name
COL_PROFESSOR = "교수명"      # professor
COL_TIME_ROOM = "강의시간/강의실"  # combined "time [room]" field in the raw export
COL_TIME = "강의시간"         # lecture time, e.g. "월1, 2"
COL_ROOM = "강의실"           # classroom code, e.g. "024-0158"
COL_DAY = "요일"             # day of week
COL_PERIOD = "교시"          # class period (1..11)

# --- Device-touch columns --------------------------------------------------
COL_BUILDING = "building"
COL_DEVICE = "device_location"
COL_DATETIME = "datetime"
COL_TOUCHES = "touches"

# --- Domain constants ------------------------------------------------------
# Korean weekday tokens in timetable order (Mon..Sun).
DAYS = ["월", "화", "수", "목", "금", "토", "일"]
# Class periods used on campus.
PERIODS = list(range(1, 12))

# Buildings considered for notifier-device placement, and the per-floor device
# locations present in the (synthetic) usage dataset.
BUILDINGS = ["교양학관", "자연과학관", "공학관", "인문사회과학관"]
DEVICE_LOCATIONS = [
    "교양학관-1층", "교양학관-2층",
    "자연과학관-1층", "자연과학관-2층", "자연과학관-3층", "자연과학관-4층",
    "공학관-1층", "공학관-2층", "공학관-3층", "공학관-4층", "공학관-5층",
    "인문사회과학관-1층", "인문사회과학관-2층", "인문사회과학관-3층",
    "인문사회과학관-4층", "인문사회과학관-5층",
]
