"""Sentiment analyzer — với HITL flag cho sarcasm E-commerce.

Dùng GPT-4o hoặc Claude Sonnet (heavy) để hiểu nuance:
- Sarcasm: "Shop này ship nhanh lắm, 3 ngày mới tới" (nhanh = châm chọc)
- Negation: "Không tệ" = tích cực nhẹ
- Comparison: "Rẻ hơn Shopee" = ưu đãi
"""
import json
from openai import AsyncOpenAI

from agent.config import settings


class SentimentAnalyzer:
    """Phân tích sentiment với HITL flag."""

    def __init__(self, model: str = "gpt-4o"):
        self.model = model
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def analyze(self, text: str, context_quote: str, brand_name: str) -> dict:
        """Sentiment + flag cần HITL.

        Returns:
            {
                "sentiment": float (-1 to +1),
                "confidence": float (0 to 1),
                "requires_hitl": bool,
                "reason": str (nếu requires_hitl)
            }
        """
        prompt = f"""Phân tích sentiment về "{brand_name}" trong câu trả lời sau.

CONTEXT: "{context_quote}"
FULL TEXT: "{text}"

Trả về JSON:
{{
    "sentiment": <-1 đến +1>,
    "confidence": <0 đến 1, bao nhiêu % chắc chắn>,
    "requires_hitl": true/false,
    "reason": "<nếu requires_hitl=true, giải thích: sarcasm, mơ hồ, claim quan trọng, v.v.>"
}}

Lưu ý đặc biệt cho E-commerce VN:
- Sarcasm phổ biến: "ship nhanh lắm" (nghĩa là chậm)
- Negation Việt: "không tệ", "cũng được"
- So sánh: "rẻ hơn X"
- Claim giá/ship/uу tín: LUÔN requires_hitl=true
"""
        if not settings.enable_hitl_sentiment:
            # Nếu tắt HITL, parse thẳng
            completion = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.0,
            )
            return json.loads(completion.choices[0].message.content)

        # TODO: implement queue HITL nếu cần
        completion = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.0,
        )
        return json.loads(completion.choices[0].message.content)
