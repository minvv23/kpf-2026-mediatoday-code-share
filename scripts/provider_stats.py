"""입력 데이터의 매체 유형·권역별 사설 수를 출력한다.

python scripts/provider_stats.py data/articles.csv
"""
import sys

from localcritique import loader


def main():
    if len(sys.argv) < 2:
        print("사용법: python scripts/provider_stats.py <CSV 경로>")
        return
    df = loader.editorials(loader.clean(loader.read_articles(sys.argv[1])))
    print(df.groupby(["media_type", "region"]).agg(articles=("title", "size"), providers=("provider", "nunique")))


if __name__ == "__main__":
    main()
