"""Tool: schema_check — kiểm tra schema.org Product/Offer/Review trên URL."""
import httpx


async def schema_check(url: str) -> dict:
    """Check schema.org markup trên URL.

    Args:
        url: URL cần check

    Returns:
        {
            "has_product_schema": bool,
            "has_offer_schema": bool,
            "has_review_schema": bool,
            "has_faq_schema": bool,
            "missing": list[str]
        }
    """
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(url)
            html = r.text.lower()
        return {
            "has_product_schema": '"@type":"product"' in html or 'itemtype="http://schema.org/product"' in html,
            "has_offer_schema": '"@type":"offer"' in html or 'itemtype="http://schema.org/offer"' in html,
            "has_review_schema": '"@type":"review"' in html or 'itemtype="http://schema.org/review"' in html,
            "has_faq_schema": '"@type":"faqpage"' in html or 'itemtype="http://schema.org/faqpage"' in html,
            "missing": [],
        }
    except Exception as e:
        return {"error": str(e), "missing": ["url_unreachable"]}
