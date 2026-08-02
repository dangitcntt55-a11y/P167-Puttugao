"""Diagnosis Agent — gọi tools để build evidence package.

Workflow:
    1. fetch_citations(responses) → list URLs
    2. compare_with_brand_source(claim, brand_id) → verify giá/ship
    3. schema_check(brand_url) → check schema.org
    4. detect_content_gap(brand_id, topic) → kiểm tra nội dung
    5. → build evidence_package = {url, quote, claim_type, confidence, verified_at}
"""
import json
from openai import AsyncOpenAI

from agent.config import settings
from agent.diagnosis.tools.fetch_citations import fetch_citations
from agent.diagnosis.tools.compare_with_brand import compare_with_brand_source
from agent.diagnosis.tools.schema_check import schema_check
from agent.diagnosis.tools.content_gap import detect_content_gap


DIAGNOSIS_SYSTEM_PROMPT = """Bạn là GEO Diagnosis Agent cho E-commerce Việt Nam.

Nhiệm vụ: phân tích MỘT gap (brand không được nhắc đến hoặc bị nhắc sai) trong AI responses,
GỌI CÁC TOOLS để thu thập evidence, rồi tổng hợp thành evidence package.

Tools available:
- fetch_citations(response_id): lấy URL citation
- compare_with_brand_source(claim, brand_id): so sánh claim giá/ship với brand KB
- schema_check(brand_url): kiểm tra schema.org Product/Offer/Review
- detect_content_gap(brand_id, topic): kiểm tra trang web shop

Output: JSON evidence_package:
{
    "hypotheses": [
        {
            "hypothesis": "<lý do brand không được nhắc>",
            "confidence": <0-1>,
            "evidence_urls": [url]
        }
    ],
    "recommended_actions": [
        {
            "action_type": "listing_update" | "schema_add" | "outreach" | "content_pr" | "content_add",
            "target_url": "<url cần sửa>",
            "suggested_change": "<mô tả thay đổi cụ thể>",
            "evidence_url": "<url chứng minh>"
        }
    ],
    "severity": "low" | "medium" | "high" | "critical",
    "requires_hitl": bool
}

Quy tắc:
- Severity 'critical' nếu liên quan giá/ship sai (E-commerce tolerance thấp)
- Mỗi hypothesis PHẢI có evidence_url (không được suy đoán)
- Recommended action phải cụ thể, có thể thực hiện được
"""


async def diagnose(brand_id: int, prompt_id: int) -> dict:
    """Main diagnosis entry.

    Args:
        brand_id: ID của brand
        prompt_id: ID của prompt

    Returns:
        Dict evidence_package
    """
    # TODO: thực tế cần:
    # 1. Lấy responses + brand info từ backend
    # 2. Setup LLM with tools (function calling)
    # 3. Run agent loop với tools
    # 4. Save diagnosis via backend API
    return {
        "status": "ok",
        "brand_id": brand_id,
        "prompt_id": prompt_id,
        "evidence_package": {},
        "message": "TODO: integrate with backend + LLM function calling",
    }
