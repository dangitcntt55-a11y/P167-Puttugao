"""Claim extractor — detect price/ship/review claim.

Trong E-commerce, claim về giá/ship/uy tín tolerance rất thấp → cần verify.
"""
import re
from typing import Literal

ClaimType = Literal["price", "ship", "review", "general"]


# Regex patterns cho tiếng Việt
PRICE_PATTERNS = [
    r"(\d{1,3}(?:[.,]\d{3})*(?:\s*[kK]|\s*nghìn|\s*triệu|\s*tr|\s*VND|\s*đ))",
    r"giá\s*(?:khoảng|là)?\s*\d+",
    r"\d+[\.,]?\d*\s*đồng",
]
SHIP_PATTERNS = [
    r"(?:miễn\s*phí\s*ship|freeship|free\s*ship)",
    r"ship\s*(?:nhanh|chậm|chỉ|tốn)?",
    r"giao\s*hàng\s*(?:nhanh|chậm)?",
    r"\d+\s*ngày",
]
REVIEW_PATTERNS = [
    r"(?:đánh giá|review|rating)",
    r"\d+\s*sao",
    r"(?:uy tín|chất lượng|dở|tệ|hay|tốt|xịn)",
]


def extract_claim_type(text: str) -> ClaimType:
    """Classify claim type từ text snippet."""
    text_lower = text.lower()
    for pattern in PRICE_PATTERNS:
        if re.search(pattern, text_lower):
            return "price"
    for pattern in SHIP_PATTERNS:
        if re.search(pattern, text_lower):
            return "ship"
    for pattern in REVIEW_PATTERNS:
        if re.search(pattern, text_lower):
            return "review"
    return "general"


def extract_claim_value(text: str, claim_type: ClaimType) -> str | None:
    """Extract giá trị claim (vd: '300.000 VND', 'freeship TPHCM')."""
    if claim_type == "price":
        match = re.search(PRICE_PATTERNS[0], text, re.IGNORECASE)
        return match.group(0) if match else None
    if claim_type == "ship":
        match = re.search(SHIP_PATTERNS[0], text, re.IGNORECASE)
        return match.group(0) if match else None
    return None


def requires_hallucination_check(claim_type: ClaimType) -> bool:
    """Claim nào cần verify hallucination (giá/ship/uy tín)."""
    return claim_type in {"price", "ship", "review"}
