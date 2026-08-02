"""Tool: compare_with_brand_source — so sánh claim giá/ship/uy tín với brand KB.

Quan trọng trong E-commerce: hallucination giá/ship tolerance rất thấp.
"""


async def compare_with_brand_source(claim: str, claim_type: str, brand_id: int) -> dict:
    """Tool so sánh claim với brand knowledge base.

    Args:
        claim: claim từ AI (vd: "Minh Long bán nồi chiên 300.000 VND")
        claim_type: 'price' | 'ship' | 'review' | 'general'
        brand_id: ID brand

    Returns:
        {
            "match": bool,
            "confidence": float,
            "brand_actual_value": str | None,
            "claim_value": str | None,
            "explanation": str
        }
    """
    # TODO:
    # 1. Lấy brand.knowledge_base từ backend
    # 2. So sánh claim với brand_actual (giá/ship policy)
    # 3. Nếu mismatch → flag hallucination
    return {
        "match": True,
        "confidence": 0.0,
        "brand_actual_value": None,
        "claim_value": None,
        "explanation": "TODO: implement comparison logic",
    }
