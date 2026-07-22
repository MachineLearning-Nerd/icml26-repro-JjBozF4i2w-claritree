from repro.src.verify_completion_artifacts import summarize


def test_completion_readback_uses_released_plot_selection():
    payload = summarize()
    assert payload["selection"] == {
        "outer": "mean",
        "depth": 4,
        "n_thresholds": 20,
        "time_limit_s": 590.0,
    }
    assert payload["claritree"]["records"] == 880
    assert payload["streed"]["records"] == 1760


def test_completion_artifacts_support_direction_without_rewriting_paper_rounding():
    payload = summarize()
    assert payload["source_backed_direction_verified"]
    assert payload["claritree"]["completion_rate_percent"] == 100.0
    assert payload["streed"]["completion_rate_percent"] == 70.0
    assert not payload["paper_rounded_endpoint_exactly_reproduced"]
