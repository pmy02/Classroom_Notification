[English](README.md) | **한국어**

# 어디강의실 — 강의실 알림이 설치 위치 및 사용량 분석

넓은 대학 캠퍼스에서 **강의실 안내 알림이 기기를 어디에 설치할지** 정하고, 설치 이후 **각 기기의 사용량이 어떻게 변할지** 예측하는 데이터 분석 프로젝트입니다. 2년치 수업시간표 데이터의 탐색적 분석(EDA)과, 가상 기기 사용량 데이터에 적합시킨 Prophet 시계열 모델을 함께 사용합니다.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![pandas](https://img.shields.io/badge/pandas-2.x-150458)
![Prophet](https://img.shields.io/badge/forecasting-Prophet-1f77b4)
![License: MIT](https://img.shields.io/badge/License-MIT-green)
<!-- TODO: 푸시 후 CI 배지 활성화:
![CI](https://github.com/pmy02/Classroom_Notification/actions/workflows/ci.yml/badge.svg) -->

> 본래 경상국립대학교(GNU)에서 진행한 1주일 팀 프로젝트(2021년 11월)입니다. 이후 개별 노트북을 재현 가능하고 테스트가 포함된 Python 파이프라인으로 리팩터링했으며, 분석 내용과 결론은 그대로입니다.

## 개요

경상국립대학교는 캠퍼스가 넓어 신입생이 강의가 열리는 건물과 강의실을 찾기 어렵습니다. 이를 해결하기 위해, 학생 통행이 잦은 곳에 강의별 건물·강의실을 안내하는 **"어디강의실" 알림이 기기**를 설치하자는 제안에서 출발했습니다. 본 프로젝트는 이 제안에 필요한 두 가지 실무적 질문에 답합니다.

1. **설치 위치** — 어느 건물과 시간대에 강의가 가장 몰려 통행량이 많은가? 실제 2020–2021 수업시간표 데이터로 분석합니다.
2. **사용량 예측** — 설치 이후 기기별 사용량이 어떻게 변할지 미리 파악해 운영 계획에 반영할 수 있는가? 기기가 실제로 설치된 적은 없으므로 **가상 사용량 데이터**로 시연합니다.

설치 위치 분석 결과, 시간표의 대부분을 차지하는 교양 수업이 집중된 **교양학관**이 우선 설치 후보로 도출되었습니다.

## 주요 기능

- **수업시간표 전처리**: 여러 시트로 나뉜 PDF 변환 시간표를 통합하고, 결측·강사미정 행을 제거하며, `강의시간 [강의실]` 형태의 결합 필드를 강의실·요일·교시 열로 분리합니다.
- **탐색적 분석(EDA)**: 강의실·교수·요일·교시별 강의 수 집계와, 가장 붐비는 시간대를 드러내는 **요일 × 교시 히트맵**.
- **시드 기반 가상 사용량 생성기**: 기기 사용량 데이터를 완전히 재현 가능하게 생성합니다.
- **Prophet 시계열 예측**: 기기별 일간 사용량을 예측하며, 로그/원래 스케일 결과를 모두 반환합니다.
- **임포트 가능한 패키지 + 실행 스크립트 + 단위 테스트 + CI**로 재구성.

## 방법

파이프라인은 4단계로 동작합니다.

1. **전처리** (`preprocess.py`) — 시트 통합 → 정제 → 요일이 표기된 교시 단위로 분리.
2. **EDA** (`eda.py`) — 빈도 집계와 요일 × 교시 교차표/히트맵으로 수요 집중 구간 파악.
3. **가상 데이터 생성** (`synthetic.py`) — 지정한 기간에 대해 재현 가능한 기기 사용 로그 생성(기기는 실제 설치된 적 없음).
4. **예측** (`forecast.py`) — 기기별 일간 시계열로 집계 → 로그 변환 → Prophet 적합 → 사용량 예측.

<!-- TODO: docs/architecture.png 에 파이프라인 다이어그램 추가 후 참조:
![아키텍처](docs/architecture.png) -->

## 데모·결과

설치 위치 결정은 시간표 EDA에 기반하며, 예측은 가상 데이터로 운영 파이프라인을 시연합니다.

**프로젝트 개념**

![어디강의실 메인](https://user-images.githubusercontent.com/62882579/227795105-3e892fcf-2791-4ecc-9023-7dee8396efa3.png)

**시간표 전처리** — PDF로 제공된 시간표를 엑셀로 변환하고, 정제한 뒤 구조화된 열로 분리했습니다.

![전처리](https://user-images.githubusercontent.com/62882579/230105045-fa615d4e-606e-4e05-8206-0e9412b7bad8.png)

**요일 × 교시 수요 히트맵** — 교양 수업이 큰 비중을 차지해 교양학관 설치 근거가 되었고, 통행이 몰리는 시간대도 함께 확인됩니다.

![요일-교시 히트맵](https://user-images.githubusercontent.com/62882579/230106069-8bd7b413-f24c-4f75-ad7d-cd5e422e7f34.png)

**사용량 예측 (가상 데이터)** — Prophet으로 예측한 일간 기기 터치 수.

![예측](https://user-images.githubusercontent.com/62882579/230107016-9f67acf1-dbfa-4d91-89ac-2e6412629de7.png)

> 위 예측은 가상 사용량 데이터로 적합한 것으로, 실제 측정된 캠퍼스 추세가 아니라 파이프라인을 보여 주기 위한 것입니다.

## 설치

```bash
git clone https://github.com/pmy02/Classroom_Notification.git
cd Classroom_Notification

python -m venv .venv && source .venv/bin/activate   # 선택
pip install -e ".[dev]"          # 패키지 + pytest/ruff 설치
```

Prophet은 `cmdstanpy`를 통해 C++/Stan 빌드 도구를 필요로 합니다. 빌드 단계에서 오류가 나면 [Prophet 설치 가이드](https://facebook.github.io/prophet/docs/installation.html)를 참고하세요.

## 사용법

editable 모드로 설치한 뒤, `Data/`에 포함된 데이터로 파이프라인을 실행합니다.

```bash
# 1. 정제된 요일/교시 시간표 생성
python scripts/run_preprocess.py

# 2. 가장 붐비는 시간대 출력 + 히트맵을 docs/ 에 저장
python scripts/run_eda.py

# 3. 가상 기기 사용량 데이터 재현 가능하게 (재)생성
python scripts/generate_synthetic.py --seed 42

# 4. 특정 기기 사용량 예측 + 그래프 저장
python scripts/run_forecast.py --device "교양학관-1층" --periods 30
```

패키지를 직접 사용할 수도 있습니다.

```python
from eodi_classroom.preprocess import build_timetable
from eodi_classroom.eda import busiest_slots

df = build_timetable("Data/2020 ~ 2021 수업시간표.xlsx")
print(busiest_slots(df, top_n=10))
```

`make pipeline`은 1·2·4단계를 순서대로 실행하고, `make test`·`make lint`로 검사를 돌립니다.

## 프로젝트 구조

```
.
├── src/eodi_classroom/     # 임포트 가능한 패키지
│   ├── config.py           # 경로, 열 이름, 도메인 상수
│   ├── preprocess.py       # 시간표 정제 + 요일/교시 분리
│   ├── eda.py              # 집계 및 요일 × 교시 히트맵
│   ├── synthetic.py        # 시드 기반 기기 사용량 생성기
│   └── forecast.py         # 일간 집계 + Prophet 예측
├── scripts/                # CLI 진입점 (run_preprocess, run_eda, ...)
├── tests/                  # 단위·스모크 테스트 (pytest)
├── Data/                   # 시간표 + 가상 사용량 스프레드시트
├── Classroom_EDA/          # 원본 EDA 노트북
├── Device_Usage/           # 원본 사용량/예측 노트북
├── docs/                   # 생성 및 수동 추가 그림
├── .github/workflows/ci.yml
├── requirements.txt
└── pyproject.toml
```

## 재현

- **Python**: 3.9 이상 (CI는 3.10).
- **의존성**: `requirements.txt` / `pyproject.toml` 참고. 완전히 동일한 환경이 필요하면 버전을 고정하세요.
- **데이터**: 시간표 스프레드시트와 생성된 가상 사용량 파일을 `Data/`에 포함. `python scripts/generate_synthetic.py --seed 42`로 재생성 가능.
- **결정성**: 가상 데이터 생성기는 시드로 완전히 고정됩니다. 전처리 리팩터링은 원본 프로젝트의 요일/교시 표(1,154행)를 정확히 재현합니다.
- **하드웨어**: CPU만으로 충분하며, 전체 파이프라인은 노트북에서 1분 이내(주로 Prophet 적합)에 실행됩니다.

## 한계

- **가상 사용량 데이터.** 알림이 기기가 실제로 설치된 적이 없어 예측 결과는 시연용이며 실측이 아닙니다.
- **예측 표본이 작음.** 가상 시계열이 기기당 약 1개월로, 안정적인 계절성 추정에는 짧습니다.
- **전처리의 의도된 한계.** `"월1, 2"`(월요일 1·2교시) 같은 항목은 요일이 표기된 토큰만 남기며, 이는 원본 분석과 동일합니다. 빈 교시 토큰에 요일을 채워 넣는 것은 의도적으로 보존한 알려진 한계입니다(`preprocess.split_day_period` 참고).

## 로드맵

- 빈 교시 토큰에 요일을 채워 넣고 히트맵에 미치는 영향 정량화.
- 건물·층별 예측 및 공유 계절성 모델링.
- EDA·예측 결과를 보여 주는 소형 대시보드(예: Streamlit).

## 라이선스

MIT 라이선스로 배포됩니다. [LICENSE](LICENSE) 참고.

## 감사의 글

- 시계열 예측에 사용한 [Facebook Prophet](https://facebook.github.io/prophet/docs/).
- 경상국립대학교 수업시간표 데이터(2020–2021).

## 연락처

<!-- TODO: 선호하는 연락처로 확인/교체 -->
- GitHub: [@pmy02](https://github.com/pmy02)
- 이메일: <!-- TODO: 학교 이메일 추가 -->
