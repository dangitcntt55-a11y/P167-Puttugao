"""Action recommender — đề xuất 1-3 action từ evidence package.

Loại action:
- listing_update: cập nhật listing Shopee/Lazada (schema Product, SEO)
- content_add: thêm nội dung web shop (FAQ, bảng giá)
- schema_add: thêm schema FAQ cho trang
- outreach: outreach cập nhật citation (Tinhte, Voz)
- content_pr: viết bài PR chất lượng cao
"""
import json
from openai import AsyncOpenAI

from agent.config import settings


ACTION_TYPES = [
    "listing_update",
    "content_add",
    "schema_add",
    "outreach",
    "content_pr",
]


async def recommend_actions(evidence_package: dict) -> list[dict]:
    """Đề xuất 1-3 action cụ thể từ evidence package.

    Args:
        evidence_package: dict từ Diagnosis Agent

    Returns:
        list[dict]: mỗi action có {action_type, target_url, suggested_change, evidence_url}
    """
    client = AsyncOpenAI(api_key=settings.openai_api_key)
    prompt = f"""Từ evidence package sau, đề xuất 1-3 action cụ thể để tối ưu AI visibility.

EVIDENCE PACKAGE:
{json.dumps(evidence_package, ensure_ascii=False, indent=2)}

CÁC LOẠI ACTION ĐƯỢC PHÉP: {ACTION_TYPES}

Trả về JSON list:
[
    {{
        "action_type": "<1 trong 5 loại trên>",
        "target_url": "<url cần sửa — cụ thể, có thể là listing, trang FAQ, v.v.>",
        "suggested_change": "<mô tả thay đổi cụ thể, vd: 'Thêm schema Product với price=300000, availability=InStock'>",
        "evidence_url": "<url chứng minh từ evidence>",
        "estimated_impact": "low" | "medium" | "high",
        "effort": "low" | "medium" | "high"
    }}
]

Quy tắc:
- Mỗi action PHẢI có evidence_url (không suy đoán)
- Ưu tiên action có impact high + effort low
- 1-3 actions, không hơn
"""
    completion = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.3,
    )
    result = json.loads(completion.choices[0].message.content)
    actions = result.get("actions", []) if isinstance(result, dict) else result
    return actions[:3]  # cap at 3
