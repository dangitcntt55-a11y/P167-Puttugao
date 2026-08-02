"""HITL reviewer — quyết định khi nào cần human verify.

Trigger HITL khi:
1. Sarcasm E-commerce (vd: "ship nhanh lắm" = châm chọc)
2. Hallucination giá/ship/uy tín (tolerance rất thấp)
3. Claim ambiguous (mơ hồ, không rõ ràng)
4. Severity = 'critical'
"""
from agent.config import settings


def should_require_hitl_sentiment(
    sentiment: float, confidence: float, context_quote: str, claim_type: str
) -> bool:
    """Cần HITL cho sentiment?

    Args:
        sentiment: -1 to +1
        confidence: 0 to 1
        context_quote: đoạn text chứa mention
        claim_type: 'price' | 'ship' | 'review' | 'general'

    Returns:
        bool
    """
    if not settings.enable_hitl_sentiment:
        return False

    # Low confidence → HITL
    if confidence < 0.7:
        return True

    # Sarcasm indicators (Tiếng Việt)
    sarcasm_markers = ["nhanh lắm", "lắm", "cũng được", "tạm ổn", "chất lượng cao (ironic)"]
    if any(marker in context_quote.lower() for marker in sarcasm_markers):
        return True

    # Claim about price/ship/review → HITL
    if claim_type in {"price", "ship", "review"}:
        return True

    return False


def should_require_hitl_hallucination(claim_type: str, severity: str) -> bool:
    """Cần HITL verify hallucination?

    Args:
        claim_type: 'price' | 'ship' | 'review' | 'general'
        severity: 'low' | 'medium' | 'high' | 'critical'

    Returns:
        bool
    """
    if not settings.enable_hitl_hallucination:
        return False

    # E-commerce: giá/ship/uy tín tolerance rất thấp
    if claim_type in {"price", "ship", "review"}:
        return True

    if severity == "critical":
        return True

    return False
