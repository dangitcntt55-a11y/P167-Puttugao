"""Test cho Stability Score."""
from app.services.stability import compute_stability_score


class TestStabilityScore:
    def test_all_mentions_returns_max(self):
        """3 lần đều có mention → stability = 1.0."""
        assert compute_stability_score([1, 1, 1]) == 1.0

    def test_no_mentions_returns_max(self):
        """3 lần đều không có mention → stability = 1.0 (vẫn ổn định)."""
        assert compute_stability_score([0, 0, 0]) == 1.0

    def test_mixed_returns_partial(self):
        """2/3 lần có mention → stability thấp hơn 1.0."""
        score = compute_stability_score([1, 1, 0])
        assert 0.0 < score < 1.0

    def test_empty_returns_zero(self):
        assert compute_stability_score([]) == 0.0

    def test_high_variance_below_threshold(self):
        """Mỗi lần khác nhau hoàn toàn → stability rất thấp."""
        score = compute_stability_score([1, 0, 1, 0])
        assert score < 0.7
