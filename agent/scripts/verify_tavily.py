"""Verify Tavily API for Vietnamese + Shopee/Lazada."""
import asyncio
from tavily import AsyncTavilyClient

from agent.config import settings


async def main():
    print(f"Testing Tavily với tiếng Việt + Shopee/Lazada...")
    client = AsyncTavilyClient(api_key=settings.tavily_api_key)

    test_queries = [
        "nồi chiên không dầu loại nào tốt",
        "shop bán đồ gia dụng uy tín TPHCM",
        "Minh Long nồi chiên giá bao nhiêu",
        "shop đồ gia dụng Hà Nội review",
        "so sánh giá shopee lazada nồi chiên",
    ]

    for q in test_queries:
        print(f"\n--- Query: {q}")
        try:
            response = await client.search(query=q, search_depth="advanced", max_results=3, include_answer=True)
            answer = response.get("answer", "")
            results = response.get("results", [])
            print(f"Answer: {answer[:200] if answer else 'N/A'}...")
            print(f"Top results: {len(results)}")
            for r in results[:2]:
                print(f"  - {r.get('url')}: {r.get('title')[:50]}")
        except Exception as e:
            print(f"ERROR: {e}")


if __name__ == "__main__":
    asyncio.run(main())
