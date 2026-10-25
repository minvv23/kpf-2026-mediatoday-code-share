# 처리 흐름

```
기사 CSV (title, content, provider, date)
   │
   ▼
loader        정리, 사설만 추출, 시간 창 적용, 매체 유형(중앙지/지역지)·권역 부여
   │
   ▼
vectorize     단어 빈도(TF-IDF) 벡터
   │
   ▼
clustering    중앙지 사설 KMeans 군집화 (실루엣 점수로 k 선택)
   │
   ▼
matching      지역지 사설 제목과 군집 대표 제목의 겹치는 단어 수로 배정
   │
   ▼
divergence    군집별 중앙지·지역지 주요 단어 차이 점수, 기준 이상이면 표시
   │
   ▼
report        표시된 이슈의 비교 초안 (템플릿: 이슈 개요, 중앙지, 지역 신문, 주요 단어)
   │
   ▼
exporter      drafts.csv, flags.json, match_table.csv, draft_*.txt, prompt_*.txt
```

## 모듈별 역할

| 모듈 | 역할 |
|---|---|
| `config.py` | 환경변수와 설정 파일 읽기 |
| `providers.py` | 중앙지·지역지 목록과 권역 (예시) |
| `loader.py` | 기사 읽기, 정리, 사설 추출, 시간 창 |
| `vectorize.py` | 단어 빈도 벡터 |
| `clustering.py` | 군집 수 선택, 군집화, 군집 요약 |
| `matching.py` | 지역지 사설 군집 배정, 군집별 기사 수 |
| `divergence.py` | 단어 차이 점수, 이슈 표시 |
| `report.py` | 비교 초안 |
| `prompt.py` | 기사 생성용 프롬프트 (각사 LLM에 입력) |
| `exporter.py` | 결과 저장 |
| `pipeline.py` | 위 단계를 차례로 실행 |
| `run.py` | 명령행 진입점 |

## 사람의 역할

이 도구는 비교할 만한 이슈를 고르고 기사를 나란히 놓은 초안까지만 만든다.
실제 기사로 쓸지, 어떤 논지를 어떻게 소개할지는 기자가 원문을 확인해 정한다.
