# kpf-2026-mediatoday-code-share

2026년 한국언론진흥재단 디지털 미디어 서비스 개발 지원 사업으로 개발한
**AI를 활용한 <아침 신문 솎아보기>의 "지역 이슈 비평" 기능 추가**(미디어오늘)의 공개 소스코드입니다.

중앙 일간지와 지역 신문의 사설을 같은 시간 창에서 모아, 중앙지 사설을 이슈별로 군집화하고 지역지 사설을 같은 이슈에 붙인 뒤,
두 묶음의 차이가 큰 이슈를 골라 비교 초안을 만드는 흐름을 담고 있습니다.
다른 언론사가 자사 데이터와 편집 기준에 맞춰 바꿔 쓸 수 있도록 기본형(reference implementation)으로 정리했습니다.

## 구성

```
localcritique/
  config.py           설정 로더 (환경변수 > config/settings.yaml > 기본값)
  providers.py        중앙지·지역지 목록과 권역 (예시)
  loader.py           기사 읽기, 정리, 사설 추출, 시간 창
  vectorize.py        단어 빈도(TF-IDF) 벡터
  clustering.py       중앙지 사설 군집화 (KMeans, 실루엣 점수로 k 선택)
  matching.py         지역지 사설을 제목 단어가 겹치는 군집에 배정
  divergence.py       군집별 중앙지·지역지 단어 차이 점수
  report.py           비교 초안 (템플릿)
  prompt.py           기사 생성용 프롬프트 (예시, LLM 호출 없음)
  exporter.py         결과 저장
  pipeline.py         전체 흐름
  run.py              명령행 진입점
  sample_data.py      동작 확인용 가상 데이터
  utils/              로깅, 예외, 텍스트, 날짜, 입출력, 입력 검사
scripts/
  make_sample.py      가상 데이터 CSV 만들기
  provider_stats.py   매체 유형·권역별 사설 수
  inspect_clusters.py 군집·매칭 결과만 보기
tests/                단위 테스트 (pytest)
config/
  settings.example.yaml
web/
  index.html          결과 뷰어 기본 틀
docs/
  architecture.md     처리 흐름
  data_format.md      입력·출력 데이터 형식
```

## 설치

Python 3.11 이상을 권장합니다.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env                                  # 선택
cp config/settings.example.yaml config/settings.yaml  # 선택
```

## 환경 설정

| 변수 | 설명 |
|---|---|
| `INPUT_PATH` | 기사 CSV 경로 |
| `OUTPUT_DIR` | 결과 저장 폴더 |
| `WINDOW_HOURS` | 분석할 시간 창(시간) |
| `MIN_SHARED_WORDS` | 지역지 사설 제목과 군집 대표 제목이 겹쳐야 하는 최소 단어 수 |
| `DIVERGENCE_MIN` | 비교 대상으로 표시할 최소 차이 점수 |
| `MIN_LOCAL_PER_ISSUE` | 이슈당 필요한 최소 지역지 사설 수 |
| `MAX_REPORTS` | 한 번에 만들 초안 수 상한 |

기본값은 가상 데이터 확인용입니다. 실제 값은 각사 데이터로 검증해 정하세요.
기사 수집 경로, 계정, 서버 주소, API 키는 저장소에 포함하지 않았습니다.

## 실행

```bash
# 가상 데이터로 흐름 확인
python -m localcritique.run --sample

# 실제 데이터
python -m localcritique.run --input data/articles.csv --end "2026-01-02 07:00"

# 보조 스크립트
python scripts/make_sample.py --days 3
python scripts/provider_stats.py data/articles.csv
python scripts/inspect_clusters.py data/articles.csv
```

테스트:

```bash
pytest -q
```

## 웹 화면

`web/index.html`은 날짜 이동과 결과 카드 목록만 담은 뷰어 기본 틀입니다. 각사 환경의 결과 조회 API와 연결해 사용합니다.

## 이용 시 유의사항

- 이 도구는 비교 후보와 초안까지만 만듭니다. 기사로 내보내기 전에 기자가 원문과 맥락을 확인해야 합니다.
- 사설 원문 이용은 각 매체의 이용 조건과 저작권법을 따르세요.

## 라이선스

MIT License. `LICENSE` 파일을 참고하세요.
