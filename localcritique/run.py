"""명령행 진입점.

python -m localcritique.run --sample
python -m localcritique.run --input data/articles.csv --end "2026-01-02 07:00"
"""
import argparse
import json
import sys

from . import config, pipeline, sample_data
from .utils.exceptions import LocalCritiqueError
from .utils.logging_utils import get_logger, setup_logging


def parse_args(argv=None):
    ap = argparse.ArgumentParser(description="중앙지·지역지 사설 비교")
    ap.add_argument("--input", help="기사 CSV 경로 (title, content, provider, date)")
    ap.add_argument("--sample", action="store_true", help="가상 데이터를 만들어 실행")
    ap.add_argument("--end", default=None, help="분석 시간 창의 끝 시각 (기본: 데이터의 마지막 시각)")
    ap.add_argument("--out", default=None, help="출력 폴더")
    ap.add_argument("--max-reports", type=int, default=None, help="만들 초안 수 상한")
    return ap.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    setup_logging(config.LOG_LEVEL)
    log = get_logger("localcritique")
    log.info("설정: %s", config.summary())
    path = sample_data.write() if args.sample else args.input
    try:
        res = pipeline.run(path, args.end, args.out, args.max_reports)
    except LocalCritiqueError as e:
        log.error("%s", e)
        return 1
    print(json.dumps(res.summary(), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
