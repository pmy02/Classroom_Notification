"""eodi_classroom — analysis pipeline for the "어디강의실" classroom-notifier project.

The package turns raw university timetable spreadsheets into clean,
analysis-ready tables, runs exploratory analysis to decide where notifier
devices should be installed, and forecasts per-device usage with Prophet.

Submodules:
    config      Shared paths, column names, and domain constants.
    preprocess  Timetable cleaning: sheet merge, room/time split, day/period split.
    eda         Frequency counts and the day x period demand heatmap.
    synthetic   Seeded generator for the (synthetic) device-touch dataset.
    forecast    Daily aggregation and Prophet time-series forecasting.
"""

__version__ = "0.2.0"

__all__ = ["config", "preprocess", "eda", "synthetic", "forecast"]
