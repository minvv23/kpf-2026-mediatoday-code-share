# 데이터 형식

## 1. 입력 기사 (CSV, UTF-8)

| 열 | 설명 |
|---|---|
| title | 기사 제목. 사설은 제목에 `사설`이 들어간다고 가정 (`EDITORIAL_KEYWORD`로 변경) |
| content | 본문 |
| provider | 매체명. `providers.py` 목록으로 중앙지/지역지를 구분 |
| date | 발행 시각 (`YYYY-MM-DD HH:MM:SS`) |

## 2. 이슈 표시 (`flags.json`)

```json
[
  {"cluster": 0, "n_central": 4, "n_local": 3, "score": 0.62,
   "central_words": ["..."], "local_words": ["..."], "flagged": true}
]
```

## 3. 비교 초안 (`drafts.csv`, `draft_<cluster>.txt`)

| 열 | 설명 |
|---|---|
| cluster | 군집 번호 |
| title | 초안 제목 |
| body | 이슈 개요, 중앙지, 지역 신문, 주요 단어 순서의 본문 |

`prompt_<cluster>.txt`는 `prompt.py`의 프롬프트에 초안 본문을 넣은 텍스트로, 각사 LLM에 그대로 입력한다.

## 4. 군집별 기사 수 (`match_table.csv`)

| 열 | 설명 |
|---|---|
| cluster | 군집 번호 |
| central | 중앙지 사설 수 |
| local | 매칭된 지역지 사설 수 |

## 5. 뷰어 API 응답 (예시)

```json
{"date": "20260101", "items": [{"title": "...", "body": "..."}]}
```
