"""결과 저장."""
from pathlib import Path

from .prompt import build_prompt
from .report import Draft
from .utils.date_utils import yyyymmdd
from .utils.io_utils import ensure_dir, write_csv, write_json, write_text


def save(out_dir, drafts: list[Draft], flags: list, match_table) -> dict:
    out = ensure_dir(Path(out_dir) / yyyymmdd())
    rows = [{"cluster": d.cluster, "title": d.title, "body": d.body} for d in drafts]
    files = {
        "drafts": write_csv(out / "drafts.csv", rows, ["cluster", "title", "body"]),
        "flags": write_json(out / "flags.json", [f.__dict__ | {"flagged": f.flagged} for f in flags]),
        "matches": write_text(out / "match_table.csv", match_table.to_csv()),
    }
    for d in drafts:
        write_text(out / f"draft_{d.cluster}.txt", f"{d.title}\n\n{d.body}\n")
        write_text(out / f"prompt_{d.cluster}.txt", build_prompt(d))
    return files
