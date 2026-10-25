"""가상 사설 데이터 CSV를 만든다.

python scripts/make_sample.py --days 3 --out sample/articles.csv
"""
import argparse

from localcritique.sample_data import write


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=2)
    ap.add_argument("--out", default="sample/articles.csv")
    args = ap.parse_args()
    print(write(args.out, n_days=args.days))


if __name__ == "__main__":
    main()
