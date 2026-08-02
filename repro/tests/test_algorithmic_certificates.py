from fractions import Fraction

from repro.src.verify_algorithmic_certificates import (
    arbitrary_gap_certificate,
    rank_update_work_certificate,
    runtime_space_certificate,
)


def test_full_refactor_control_loses_quadratic_rank_update_property():
    payload = rank_update_work_certificate()
    assert payload["polynomial_degree_in_p"] == 2
    assert payload["condition_relaxing_control"]["polynomial_degree_in_p"] == 3


def test_space_bound_control_fails_outside_the_theorem_regime():
    payload = runtime_space_certificate()
    assert payload["space_bound_z3_verified"]
    assert payload["condition_relaxing_control"]["bound_fails_outside_regime"]


def test_gap_controls_break_the_relaxed_assumptions():
    controls = arbitrary_gap_certificate()["condition_relaxing_controls"]
    assert Fraction(controls["epsilon"]["ratio_margin_over_1/(4*epsilon)"]) < 0
    assert controls["nuisance_pairs"]["unresolved_pairs_after_d_splits"] == 0
