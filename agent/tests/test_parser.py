"""Test claim extractor."""
from agent.parser.claim_extractor import extract_claim_type, extract_claim_value, requires_hallucination_check


class TestClaimType:
    def test_price(self):
        text = "Minh Long bán nồi chiên giá 300.000 VND"
        assert extract_claim_type(text) == "price"

    def test_ship(self):
        text = "Shop này có freeship TPHCM"
        assert extract_claim_type(text) == "ship"

    def test_review(self):
        text = "Đánh giá 5 sao, chất lượng tốt"
        assert extract_claim_type(text) == "review"

    def test_general(self):
        text = "Shop bán đồ gia dụng uy tín"
        assert extract_claim_type(text) == "general"


class TestRequiresHallucinationCheck:
    def test_price_requires_check(self):
        assert requires_hallucination_check("price") is True

    def test_ship_requires_check(self):
        assert requires_hallucination_check("ship") is True

    def test_review_requires_check(self):
        assert requires_hallucination_check("review") is True

    def test_general_no_check(self):
        assert requires_hallucination_check("general") is False
