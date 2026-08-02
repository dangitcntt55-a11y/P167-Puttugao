"""Mention parser — extract mentions từ raw response dùng LLM.

Dùng GPT-4o-mini (cheap) cho NER/mention extraction.
Schema output:
    {
        "mentions": [
            {
                "brand_name": str,
                "is_target_brand": bool,
                "position": int,
                "context_quote": str,
                "claim_type": 'price' | 'ship' | 'review' | 'general',
                "claim_value": str | None
            }
        ],
        "sentiment": float (-1 to +1),
        "requires_hitl": bool
    }
"""
import json
import httpx
from openai import AsyncOpenAI

from agent.config import settings


class MentionParser:
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def parse(self, response_text: str, brand_name: str, brand_name_variants: list[str]) -> dict:
        """Parse response text, extract mentions và metadata.

        Args:
            response_text: raw response từ AI
            brand_name: tên target brand (vd: 'Minh Long')
            brand_name_variants: list biến thể (vd: ['Minh Long Book', 'MLB'])

        Returns:
            Dict với mentions list + sentiment + requires_hitl
        """
        prompt = f"""Phân tích câu trả lời AI sau về thương mại điện tử Việt Nam.

TARGET BRAND: "{brand_name}"
Các biến thể tên: {brand_name_variants}

CÂU TRẢ LỜI CỦA AI:
\"\"\"
{response_text}
\"\"\"

Hãy trả về JSON với format:
{{
    "mentions": [
        {{
            "brand_name": "<tên brand được nhắc đến>",
            "is_target_brand": true/false,
            "position": <1, 2, 3... theo thứ tự xuất hiện>,
            "context_quote": "<đoạn text chứa mention, khoảng 20-50 từ>",
            "claim_type": "price" | "ship" | "review" | "general",
            "claim_value": "<nếu có claim về giá/ship, vd: '300.000 VND', 'freeship TPHCM'> hoặc null"
        }}
    ],
    "sentiment": <-1 đến +1, -1 rất tiêu cực, +1 rất tích cực>,
    "requires_hitl": <true nếu có sarcasm, mơ hồ, hoặc claim quan trọng về giá/ship/uy tín cần verify>
}}

Lưu ý:
- Tiếng Việt, có thể có dấu hoặc không dấu
- Position 1 = nhắc đầu tiên
- Claim_type 'price' = nói về giá, 'ship' = vận chuyển, 'review' = đánh giá, 'general' = chung chung
- Nếu không nhắc target brand, vẫn list các brand khác (để tính SOV)
"""
        completion = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Bạn là chuyên gia NER cho thương mại điện tử Việt Nam. Trả về JSON hợp lệ."},
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.0,
        )
        result = json.loads(completion.choices[0].message.content)
        return result


async def parse_response(response_id: int) -> dict:
    """Parse 1 response từ backend API."""
    # TODO: gọi backend API để lấy response + brand info
    # TODO: gọi MentionParser.parse()
    # TODO: lưu mentions vào DB
    return {"status": "ok", "response_id": response_id, "mentions": []}
