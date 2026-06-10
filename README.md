**English** | [한국어](README.ko.md)

# 어디강의실 (Eodi-Ganguisil) — Classroom-Notifier Placement & Usage Analysis

A data-analysis project that decides **where to install classroom-finder notifier devices** on a large university campus, and forecasts **how heavily each device would be used** over time. It combines exploratory analysis of two years of course-timetable data with a Prophet time-series model fit on a synthetic device-usage dataset.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![pandas](https://img.shields.io/badge/pandas-2.x-150458)
![Prophet](https://img.shields.io/badge/forecasting-Prophet-1f77b4)
![License: MIT](https://img.shields.io/badge/License-MIT-green)
<!-- TODO: after pushing, enable the CI badge:
![CI](https://github.com/pmy02/Classroom_Notification/actions/workflows/ci.yml/badge.svg) -->

> Originally a one-week team project (Nov 2021) at Gyeongsang National University (GNU). This repository has since been refactored from standalone notebooks into a reproducible, tested Python pipeline; the analysis and conclusions are unchanged.

## Overview

GNU's campus is large, and incoming students often struggle to locate the right building and classroom for a given course. The proposal is a set of **"어디강의실" notifier devices** — kiosks placed at high-traffic spots that show the building and room for each class. This project answers two practical questions for that proposal:

1. **Placement** — which buildings and time slots concentrate the most teaching, and therefore the most foot traffic? This is answered from real 2020–2021 timetable data.
2. **Usage forecasting** — once devices are installed, how would per-device usage trend, so operations can be planned ahead? Because no device was ever deployed, this is demonstrated on a **synthetic** usage dataset.

The placement analysis pointed to the General Education building (교양학관), where general-education courses — the bulk of the timetable — are concentrated.

## Key Features

- **Timetable preprocessing** that merges a multi-sheet, PDF-derived export, cleans missing and undetermined-instructor rows, and splits a combined `time [room]` field into separate room, day, and period columns.
- **Exploratory analysis** of lecture counts by classroom, professor, day, and period, plus a **day × period demand heatmap** that surfaces the busiest slots.
- **A seeded synthetic-usage generator** so the device-touch dataset is fully reproducible.
- **Prophet time-series forecasting** of daily per-device usage, with results returned on both the log and original scales.
- Refactored into an **importable package with entry-point scripts, unit tests, and CI**.

## Method / Approach

The pipeline runs in four stages:

1. **Preprocess** (`preprocess.py`) — merge timetable sheets → clean → split into one row per day-tagged class period.
2. **EDA** (`eda.py`) — frequency counts and the day × period crosstab/heatmap to identify demand concentration.
3. **Synthesize** (`synthetic.py`) — generate a reproducible device-touch log over a date window (the devices were never physically deployed).
4. **Forecast** (`forecast.py`) — aggregate to a daily series per device, log-transform, fit Prophet, and project usage forward.

<!-- TODO: add a pipeline diagram at docs/architecture.png and reference it here:
![Architecture](docs/architecture.png) -->

## Demo / Results

The placement decision is driven by the timetable EDA; the forecast demonstrates the operational pipeline on synthetic data.

**Project concept**

![어디강의실 main](https://user-images.githubusercontent.com/62882579/227795105-3e892fcf-2791-4ecc-9023-7dee8396efa3.png)

**Timetable preprocessing** — the source timetable arrived as PDF, was converted to Excel, cleaned, and split into structured columns.

![preprocessing](https://user-images.githubusercontent.com/62882579/230105045-fa615d4e-606e-4e05-8206-0e9412b7bad8.png)

**Day × period demand heatmap** — general-education courses dominate, which motivated placing a device in the General Education building; the heatmap also highlights the peak-traffic time slots.

![day-period heatmap](https://user-images.githubusercontent.com/62882579/230106069-8bd7b413-f24c-4f75-ad7d-cd5e422e7f34.png)

**Usage forecast (synthetic data)** — Prophet projection of daily device touches.

![forecast](https://user-images.githubusercontent.com/62882579/230107016-9f67acf1-dbfa-4d91-89ac-2e6412629de7.png)

> The forecast above is fit on synthetic usage data and illustrates the pipeline, not a measured campus trend.

## Installation

```bash
git clone https://github.com/pmy02/Classroom_Notification.git
cd Classroom_Notification

python -m venv .venv && source .venv/bin/activate   # optional
pip install -e ".[dev]"          # installs the package + pytest/ruff
```

Prophet pulls in a C++/Stan toolchain via `cmdstanpy`; see the [Prophet install guide](https://facebook.github.io/prophet/docs/installation.html) if the build step fails on your platform.

## Usage

After installing in editable mode, run the pipeline on the data shipped in `Data/`:

```bash
# 1. Build the cleaned day/period timetable
python scripts/run_preprocess.py

# 2. Print the busiest slots and save the demand heatmap to docs/
python scripts/run_eda.py

# 3. (Re)generate the synthetic device-usage dataset, reproducibly
python scripts/generate_synthetic.py --seed 42

# 4. Forecast usage for one device and save the plot
python scripts/run_forecast.py --device "교양학관-1층" --periods 30
```

Or use the package directly:

```python
from eodi_classroom.preprocess import build_timetable
from eodi_classroom.eda import busiest_slots

df = build_timetable("Data/2020 ~ 2021 수업시간표.xlsx")
print(busiest_slots(df, top_n=10))
```

`make pipeline` runs steps 1, 2, and 4 in sequence; `make test` and `make lint` run the checks.

## Project Structure

```
.
├── src/eodi_classroom/     # importable package
│   ├── config.py           # paths, column names, domain constants
│   ├── preprocess.py       # timetable cleaning + day/period split
│   ├── eda.py              # counts and the day × period heatmap
│   ├── synthetic.py        # seeded device-touch generator
│   └── forecast.py         # daily aggregation + Prophet forecasting
├── scripts/                # CLI entry points (run_preprocess, run_eda, ...)
├── tests/                  # unit + smoke tests (pytest)
├── Data/                   # timetable + synthetic usage spreadsheets
├── Classroom_EDA/          # original EDA notebooks
├── Device_Usage/           # original usage/forecasting notebooks
├── docs/                   # generated and manual figures
├── .github/workflows/ci.yml
├── requirements.txt
└── pyproject.toml
```

## Reproducibility

- **Python**: 3.9+ (CI runs 3.10).
- **Dependencies**: see `requirements.txt` / `pyproject.toml`. Pin exact versions for a byte-stable environment.
- **Data**: the timetable spreadsheets and a generated synthetic usage file are committed under `Data/`. Regenerate the synthetic file with `python scripts/generate_synthetic.py --seed 42`.
- **Determinism**: the synthetic generator is fully seeded. The preprocessing refactor reproduces the original project's day/period table exactly (1,154 rows).
- **Hardware**: CPU only; the full pipeline runs in well under a minute on a laptop (Prophet fitting dominates).

## Limitations

- **Synthetic usage data.** No notifier device was physically deployed, so the forecasting results are illustrative, not empirical.
- **Small forecasting sample.** The synthetic series spans roughly one month per device, which is short for stable seasonal estimates.
- **Faithful parsing quirk.** Timetable entries like `"월1, 2"` (Monday periods 1 and 2) keep only the day-tagged token, matching the original analysis; forward-filling the weekday onto bare period tokens is a known, deliberate-to-preserve limitation (see `preprocess.split_day_period`).

## Roadmap

- Forward-fill weekdays onto bare period tokens and quantify the effect on the heatmap.
- Per-building/-floor forecasts with shared seasonality.
- A small dashboard (e.g. Streamlit) over the EDA and forecast outputs.

## License

Released under the MIT License. See [LICENSE](LICENSE).

## Acknowledgments

- [Facebook Prophet](https://facebook.github.io/prophet/docs/) for time-series forecasting.
- Course-timetable data from Gyeongsang National University (2020–2021).

## Contact

<!-- TODO: confirm/replace with your preferred contact details -->
- GitHub: [@pmy02](https://github.com/pmy02)
- Email: <!-- TODO: add academic email -->
