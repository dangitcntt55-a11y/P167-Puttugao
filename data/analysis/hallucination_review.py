"""Hallucination review template — manual review cho 20 cases."""
# Format: response_id, ai_engine, claim_type, claim_value, brand_actual, is_hallucination, severity

CASES_TO_REVIEW = [
    # claim giá
    {"response_id": 1, "ai_engine": "chatgpt", "claim_type": "price", "claim_value": "300.000 VND", "brand_actual": "?", "is_hallucination": "?", "severity": "?"},
    # claim ship
    {"response_id": 2, "ai_engine": "claude", "claim_type": "ship", "claim_value": "freeship toàn quốc", "brand_actual": "?", "is_hallucination": "?", "severity": "?"},
    # claim review
    {"response_id": 3, "ai_engine": "gemini", "claim_type": "review", "claim_value": "uy tín, 5 sao", "brand_actual": "?", "is_hallucination": "?", "severity": "?"},
]
