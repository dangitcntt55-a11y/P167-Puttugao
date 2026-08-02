"""Pytest fixtures."""
import pytest
from app.services.stability import compute_stability_score
from app.services.closed_loop import bootstrap_diff_ci, classify_closed_loop


def test_compute_stability_score_all_mentions():
    assert compute_stability_score([1, 1, 1]) == 1.0


def test_compute_stability_score_no_mentions():
    assert compute_stability_score([0, 0, 0]) == 1.0


def test_compute_stability_score_mixed():
    score = compute_stability_score([1, 1, 0])
    assert 0.0 < score < 1.0


def test_bootstrap_diff_ci():
    pre = [0.1, 0.12, 0.11, 0.13]
    post = [0.2, 0.22, 0.21, 0.23]
    ci_lower, ci_upper = bootstrap_diff_ci(pre, post, n_iter=500)
    assert ci_lower > 0  # CI phải dương vì post > pre


def test_classify_closed_loop_improved():
    assert classify_closed_loop(0.1, 0.2, 0.08, 0.12) == "improved"


def test_classify_closed_loop_no_evidence():
    assert classify_closed_loop(0.1, 0.12, -0.02, 0.04) == "no_evidence"


def test_classify_closed_loop_regressed():
    assert classify_closed_loop(0.3, 0.2, -0.12, -0.08) == "regressed"
