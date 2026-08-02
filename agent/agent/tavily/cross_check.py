"""Cross-check claim với web public (Shopee, Lazada, web shop)."""
from agent.tavily.client import TavilyCrossCheck


async def cross_check_claim(claim: str, claim_type: str, brand_name: str) -> dict:
    """Cross-check 1 claim với web public.

    Args:
        claim: claim text từ AI
        claim_type: 'price' | 'ship' | 'review' | 'general'
        brand_name: tên brand

    Returns:
        Dict verification result
    """
    checker = TavilyCrossCheck()
    if claim_type == "price":
        # Extract product name from claim (rough)
        return await checker.check_price_claim(brand_name, "<product>", claim)
    if claim_type == "ship":
        return await checker.check_ship_policy(brand_name, claim)
    if claim_type == "review":
        return await checker.check_brand_reputation(brand_name)
    return {"match": None, "reason": "general claim, no cross-check needed"}
