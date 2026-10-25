"""전체 흐름.

사설 읽기 → 벡터화 → 중앙지 군집화 → 지역지 매칭 → 분기 점수 → 비교 초안 → 저장
"""
from dataclasses import dataclass, field

from . import clustering, config, divergence, exporter, loader, matching, report, vectorize
from .utils.logging_utils import Timer, get_logger

log = get_logger(__name__)


@dataclass
class Result:
    n_central: int = 0
    n_local: int = 0
    n_matched: int = 0
    k: int = 0
    flags: list = field(default_factory=list)
    drafts: list = field(default_factory=list)
    files: dict = field(default_factory=dict)

    def summary(self) -> dict:
        return {
            "central": self.n_central, "local": self.n_local, "matched": self.n_matched, "k": self.k,
            "flagged": sum(f.flagged for f in self.flags), "drafts": len(self.drafts),
            "files": {k: str(v) for k, v in self.files.items()},
        }


def run(path=None, end=None, out_dir=None, max_reports: int | None = None) -> Result:
    with Timer(log, "데이터 읽기"):
        central, local = loader.load(path, end)
    res = Result(n_central=len(central), n_local=len(local))

    with Timer(log, "벡터화·군집화"):
        Xc = vectorize.to_vectors(central)
        km = clustering.cluster(Xc)
        central = central.assign(cluster=km.labels_)
        res.k = km.n_clusters

    matched = matching.match(central, local)
    res.n_matched = len(matched)
    table = matching.match_table(central, matched)

    res.flags = divergence.score_all(central, matched)
    picked = [f for f in res.flags if f.flagged][: max_reports or config.MAX_REPORTS]
    res.drafts = [report.make_draft(f, central, matched) for f in picked]

    res.files = exporter.save(out_dir or config.OUTPUT_DIR, res.drafts, res.flags, table)
    log.info("완료: %s", res.summary())
    return res
