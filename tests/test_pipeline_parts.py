from localcritique import clustering, divergence, matching, vectorize


def test_split(split):
    central, local = split
    assert len(central) > 0 and len(local) > 0


def test_cluster_and_match(split):
    central, local = split
    km = clustering.cluster(vectorize.to_vectors(central), k=3)
    central = central.assign(cluster=km.labels_)
    matched = matching.match(central, local, min_shared=0)
    assert len(matched) == len(local)


def test_shared_words():
    assert matching.shared_words("지역 경제 위기", {"지역", "경제"}) == 2


def test_word_divergence():
    assert divergence.word_divergence(["a", "b"], ["a", "b"]) == 0.0
    assert divergence.word_divergence(["a"], ["b"]) == 1.0
