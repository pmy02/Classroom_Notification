[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fpmy02&Classroom_Notification&count_bg=%2372F2F3&title_bg=%234B7CFF&icon=github.svg&icon_color=%23E7E7E7&title=VISIT&edge_flat=false)](https://github.com/pmy02/Classroom_Notification)

# Classroom_Notification
- 프로젝트명: 어디강의실 - 강의실 정보 알림이
- 프로젝트 기간: 2021.11.25 ~ 2021.11.30

# 프로젝트 설명
경상국립대학교의 넓은 면적으로 신입생 분들이 강의실을 찾는 데 어려움을 겪고 있습니다. 각 수업의 건물과 강의실의 위치를 알려주는 기기인 “강의실 알림이"를 학생의 출입이 잦은 장소에 설치한다면 현재 재학생뿐만 아니라 외부인에게도 많은 도움이 될 것이라는 생각이 들어 “어디강의실"을 계획하게 되었습니다.

본 프로젝트는 알림이 기기 설치가 필요한 장소를 파악하고, 설치 이후에 수업 시간대별로 기기 사용량의 변화를 분석하고, 이를 바탕으로 기기 사용량을 예측하는 프로젝트입니다. 또한, 이를 바탕으로 학생들의 학습 환경 개선을 위한 방안을 도출합니다.

# 데이터 분석
- 사용한 데이터: 2018 ~ 2021 수업시간표, 가상의 기기 사용량 데이터
- 데이터 전처리: 수업시간표에서 불필요한 정보를 제거하고, 결측치를 처리합니다.
- 분석 도구: Python의 pandas, numpy, matplotlib, seaborn, prophet 라이브러리를 사용합니다.
- 시각화: matplotlib, seaborn 라이브러리를 사용하여 기기 사용량의 변화를 시각화합니다.
- 자세한 내용은 Classroom_EDA와 Device_Usage 폴더를 확인해주세요.

# 결과
- 분석 결과, 교양학관에 기기를 설치하는 것으로 결정하였습니다. 또한, prophet을 사용한 시계열 예측 결과, 특정 시기에 기기 사용량이 증가하는 것을 확인할 수 있었습니다.
- 시각화 결과: 강의를 요일별, 교시별로 시각화한 히트맵과 학생들의 기기 사용량을 예측 결과를 제공합니다.

# 결론
- 결론 및 인사이트: 학생들은 수업 시간대에 따라 기기 사용량이 크게 차이납니다. 또한, 기기 사용량이 급격히 증가하는 시기를 미리 파악하여 학생들의 학습 환경을 개선하는 방안을 마련할 필요가 있습니다.
- 한계점: 본 프로젝트에서는 가상의 기기 사용량을 분석하였으므로 정확하지 않습니다. 또한, 데이터 양이 적어 정확한 예측을 할 수 없는 한계가 있습니다.

# 참고 문헌
- 참고 문헌: Facebook Prophet Documentation (https://facebook.github.io/prophet/docs/)
