from repro.src.verify_source_structure import summarize
from repro.src.verify_theorem_consequences import summarize as theorem_summary


def test_pinned_source_contains_c1_algorithmic_components():
    assert summarize()["source_structure_verified"]


def test_c2_expression_and_c3_displayed_gap_consequence_are_consistent():
    payload = theorem_summary()
    assert payload["runtime_expression_verified"]
    assert payload["c3_gap_inequality_verified"]
