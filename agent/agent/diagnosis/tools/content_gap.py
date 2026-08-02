"""Tool: detect_content_gap — kiểm tra trang web shop có đủ thông tin không."""


async def detect_content_gap(brand_id: int, topic: str) -> dict:
    """Kiểm tra content gap trên web shop.

    Args:
        brand_id: ID brand
        topic: chủ đề cần check (vd: 'chính sách ship', 'bảng giá', 'FAQ')

    Returns:
        {
            "has_topic": bool,
            "url": str | None,
            "missing_info": list[str]
        }
    """
    # TODO: integrate với Tavily search để check trên web shop
    return {
        "has_topic": False,
        "url": None,
        "missing_info": [topic],
        "message": "TODO: integrate with Tavily + brand KB",
    }
