"""중앙지 사설 군집과 지역지 매칭 결과만 출력한다 (초안 생성 없음).

python scripts/inspect_clusters.py data/articles.csv
"""
import sys

from localcritique import clustering, loader, matching, vectorize


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else None
    central, local = loader.load(path)
    Xc = vectorize.to_vectors(central)
    km = clustering.cluster(Xc)
    central = central.assign(cluster=km.labels_)
    print(clustering.summarize(central, km.labels_))
    matched = matching.match(central, local)
    print(matching.match_table(central, matched))


if __name__ == "__main__":
    main()
