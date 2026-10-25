from localcritique import pipeline, sample_data


def test_run(tmp_path):
    path = sample_data.write(tmp_path / "a.csv", n_days=1)
    res = pipeline.run(path, out_dir=tmp_path / "out", max_reports=2)
    assert res.n_central > 0
    assert "drafts" in res.files
