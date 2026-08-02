from repro.src.verify_completion_artifacts import summarize


def test_completion_readback_uses_released_plot_selection():
    payload = summarize()
    assert payload["selection"] == {
        "outer": "mean",
        "depth": 4,
        "n_thresholds": 20,
        "author_operational_time_limit_s": 590.0,
        "displayed_budget_s": 600.0,
    }
    assert payload["claritree"]["records"] == 880
    assert payload["streed"]["records"] == 1760


def test_completion_artifacts_execute_author_script_and_apply_locked_rule():
    payload = summarize()
    assert payload["source_backed_direction_verified"]
    assert payload["claritree"]["completion_rate_percent"] == 100.0
    assert payload["streed"]["completion_rate_percent"] == 70.0
    assert payload["author_vs_independent_exact_crosscheck"]
    assert payload["locked_tolerance_percentage_points"] == 5.0
    assert payload["within_locked_tolerance"] == {
        "claritree": True,
        "streed": False,
    }
    assert payload["numeric_claim_assessment"] == "falsified under released author artifacts"
    assert payload["author_timeout_contract"]["contract_verified"]


def test_literal_600_second_control_exposes_timeout_misclassification():
    control = summarize()["condition_relaxing_control"]
    assert control["literal_display_cutoff"]["streed"]["completion_rate_percent"] == 100.0
    assert control["author_timeout_rows_misclassified_as_completed"] == {
        "claritree": 0,
        "streed": 528,
    }
    assert control["control_changes_streed_endpoint_from_70_to_100_percent"]
