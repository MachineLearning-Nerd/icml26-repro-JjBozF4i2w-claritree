from repro.src.verify_core_claims import check_dominance, check_threshold_pool


def test_quantile_threshold_pool_matches_independent_numpy():
    assert check_threshold_pool()["all_match"]


def test_claritree_never_loses_to_greedy_on_seeded_suite():
    assert min(record["slack"] for record in check_dominance()) >= -1e-10


def test_claritree_is_strictly_better_on_at_least_one_seeded_case():
    assert any(record["slack"] > 1e-10 for record in check_dominance())
