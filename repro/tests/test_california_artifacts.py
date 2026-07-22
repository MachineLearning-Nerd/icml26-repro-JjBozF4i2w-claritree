from repro.src.verify_california_artifacts import summarize


def test_california_release_contains_exactly_five_selected_folds_per_method():
    assert len(summarize("claritree")["selected_folds"]) == 5
    assert len(summarize("streed")["selected_folds"]) == 5


def test_california_claritree_beats_streed_after_validation_only_selection():
    assert summarize("claritree")["mean_test_r2"] > summarize("streed")["mean_test_r2"]
