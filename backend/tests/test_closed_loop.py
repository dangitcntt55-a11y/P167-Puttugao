"""Test cho Closed-loop engine."""
from app.services.closed_loop import bootstrap_diff_ci, classify_closed_loop


class TestBootstrapCI:
    def test_returns_tuple(self):
        pre = [0.1, 0.12, 0.11]
        post = [0.2, 0.22, 0.21]
        ci = bootstrap_diff_ci(pre, post, n_iter=200)
        assert isinstance(ci, tuple)
        assert len(ci) == 2

    def test_post_greater_than_pre_has_positive_ci(self):
        pre = [0.1, 0.11, 0.12, 0.13]
        post = [0.2, 0.21, 0.22, 0.23]
        ci_lower, ci_upper = bootstrap_diff_ci(pre, post, n_iter=500)
        assert ci_lower > 0
        assert ci_upper > ci_lower

    def test_empty_input_returns_zero(self):
        assert bootstrap_diff_ci([], []) == (0.0, 0.0)


class TestClassifyClosedLoop:
    def test_improved_when_ci_lower_above_noise_floor(self):
        # pre=0.1, post=0.2, ci_lower=0.08 > noise_floor (0.06)
        assert classify_closed_loop(0.1, 0.2, 0.08, 0.12) == "improved"

    def test_regressed_when_ci_upper_below_negative_noise_floor(self):
        # pre=0.3, post=0.2, ci_upper=-0.08 < -noise_floor (-0.06)
        assert classify_closed_loop(0.3, 0.2, -0.12, -0.08) == "regressed"

    def test_no_evidence_when_ci_overlaps_zero(self):
        # ci bao quanh 0 → no_evidence
        assert classify_closed_loop(0.1, 0.12, -0.02, 0.04) == "no_evidence"
