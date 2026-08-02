"""Tavily client wrapper — chuyên cho cross-check price/ship/uy tín."""
from tavily import AsyncTavilyClient

from agent.config import settings


class TavilyCrossCheck:
    """Wrapper cho Tavily search với logic E-commerce."""

    def __init__(self):
        self.client = AsyncTavilyClient(api_key=settings.tavily_api_key)

    async def check_price_claim(self, brand_name: str, product_name: str, claimed_price: str) -> dict:
        """Verify claim giá sản phẩm.

        Args:
            brand_name: tên brand
            product_name: tên sản phẩm
            claimed_price: giá AI claim (vd: '300.000 VND')

        Returns:
            {
                "match": bool,
                "verified_price": str | None,
                "source_url": str | None,
                "confidence": float
            }
        """
        query = f'giá {product_name} {brand_name} site:shopee.vn OR site:lazada.vn'
        response = await self.client.search(
            query=query,
            search_depth="advanced",
            max_results=5,
            include_answer=True,
        )
        # TODO: parse answer + extract actual price
        return {
            "match": False,
            "verified_price": None,
            "source_url": response.get("results", [{}])[0].get("url") if response.get("results") else None,
            "confidence": 0.0,
            "raw_results": response.get("results", []),
        }

    async def check_ship_policy(self, brand_name: str, claimed_ship: str) -> dict:
        """Verify claim ship policy."""
        query = f'chính sách giao hàng {brand_name} site:shopee.vn OR phí ship'
        response = await self.client.search(query=query, search_depth="advanced", max_results=5)
        return {
            "match": False,
            "verified_ship": None,
            "source_url": response.get("results", [{}])[0].get("url") if response.get("results") else None,
            "confidence": 0.0,
        }

    async def check_brand_reputation(self, brand_name: str) -> dict:
        """Check brand reputation/uy tín."""
        query = f"{brand_name} review uy tín đánh giá"
        response = await self.client.search(query=query, search_depth="advanced", max_results=5)
        return {
            "source_url": response.get("results", [{}])[0].get("url") if response.get("results") else None,
            "snippets": [r.get("content") for r in response.get("results", [])[:3]],
        }
