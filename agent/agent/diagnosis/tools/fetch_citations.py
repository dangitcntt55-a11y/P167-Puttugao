"""Tool: fetch_citations — lấy danh sách URL từ citation AI/Tavily."""


async def fetch_citations(response_id: int) -> list[dict]:
    """Tool cho LLM function calling.

    Args:
        response_id: ID của response trong DB

    Returns:
        List[dict]: [{"url": str, "title": str, "snippet": str}]
    """
    # TODO: gọi backend API để lấy citations JSONB
    return []
