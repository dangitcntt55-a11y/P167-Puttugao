"""Diagnosis Agent — OpenAI function calling thật để build evidence package.

Flow:
    1. Lấy responses + brand info từ backend API.
    2. Setup OpenAI function calling với 4 tools.
    3. Run agent loop tối đa 6 turns (đủ cho 4 tools).
    4. Tổng hợp evidence package.
    5. Trả về JSON: {hypotheses, evidence_package, recommended_actions, severity}.

Severity rule:
    - critical: claim sai về giá/ship/uy tín (E-commerce tolerance thấp).
    - high: brand không được nhắc + stability >= 0.7.
    - medium: brand được nhắc nhưng ở position thấp hoặc sentiment tiêu cực.
    - low: gap nhỏ (vd: brand nhắc cuối cùng trong list).
"""
import json
import re

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
- compare_with_brand_source(claim, brand_id, claim_type): so sánh claim giá/ship với brand KB
- schema_check(url): kiểm tra schema.org Product/Offer/Review/FAQPage
- detect_content_gap(brand_id, topic): kiểm tra nội dung web shop theo topic

Quy trình:
1. Đọc responses + brand KB được cung cấp trong user message.
2. Gọi fetch_citations cho từng response để biết AI tham chiếu nguồn nào.
3. Gọi compare_with_brand_source cho MỖI claim nhạy cảm (giá/ship/uy tín) để verify hallucination.
4. Gọi schema_check cho URL brand để đánh giá GEO markup.
5. Gọi detect_content_gap cho các topic AI hỏi mà brand có thể thiếu.
6. Cuối cùng trả lời bằng JSON thuần (không markdown) theo schema bên dưới.

Output: JSON evidence_package:
{
    "hypotheses": [
        {
            "hypothesis": "<lý do brand không được nhắc hoặc bị nhắc sai>",
            "confidence": <0-1>,
            "evidence_urls": [url],
            "quote_span": "<trích đoạn từ response, optional>",
            "claim_type": "price" | "ship" | "review" | "general"
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
- Severity 'critical' nếu liên quan giá/ship sai (E-commerce tolerance thấp).
- Mỗi hypothesis PHẢI có evidence_url (không được suy đoán).
- Recommended action phải cụ thể, có thể thực hiện được.
- Trả lời JSON thuần, KHÔNG bọc trong markdown code fence.
"""

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "fetch_citations",
            "description": (
                "Lấy URL citations từ response_id. "
                "Trả về list URLs AI đã tham chiếu cùng title/snippet."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "response_id": {
                        "type": "integer",
                        "description": "ID của response trong DB",
                    },
                },
                "required": ["response_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "compare_with_brand_source",
            "description": (
                "So sánh claim giá/ship/uy tín với brand KB để verify hallucination. "
                "Trả về match boolean + brand_actual_value + explanation."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "claim": {
                        "type": "string",
                        "description": "Claim cần verify, vd: 'Samsung Galaxy S24 giá 15 triệu'",
                    },
                    "brand_id": {
                        "type": "integer",
                        "description": "ID brand",
                    },
                    "claim_type": {
                        "type": "string",
                        "enum": ["price", "ship", "review", "general"],
                        "description": "Loại claim để chọn nguồn KB phù hợp.",
                    },
                },
                "required": ["claim", "brand_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "schema_check",
            "description": (
                "Kiểm tra schema.org markup (Product/Offer/Review/FAQPage) trên URL."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL trang cần check",
                    },
                },
                "required": ["url"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "detect_content_gap",
            "description": (
                "So sánh topic AI hỏi với nội dung brand có trên web → phát hiện content gap."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "brand_id": {
                        "type": "integer",
                        "description": "ID brand",
                    },
                    "topic": {
                        "type": "string",
                        "description": "Topic cần check, vd: 'chính sách bảo hành Samsung'",
                    },
                },
                "required": ["brand_id", "topic"],
            },
        },
    },
]


async def _call_tool(fn_name: str, fn_args: dict) -> dict | list:
    """Dispatch tool call tới hàm async tương ứng, trả về output đã chuẩn hoá."""
    if fn_name == "fetch_citations":
        return await fetch_citations(int(fn_args["response_id"]))
    if fn_name == "compare_with_brand_source":
        return await compare_with_brand_source(
            str(fn_args["claim"]),
            str(fn_args.get("claim_type", "general")),
            int(fn_args["brand_id"]),
        )
    if fn_name == "schema_check":
        return await schema_check(str(fn_args["url"]))
    if fn_name == "detect_content_gap":
        return await detect_content_gap(int(fn_args["brand_id"]), str(fn_args["topic"]))
    return {"error": f"Unknown tool: {fn_name}"}


def compute_severity(evidence: dict, stability: float) -> str:
    """Tính severity dựa trên evidence collected.

    Returns: 'critical' | 'high' | 'medium' | 'low'.

    Quy tắc (theo CLAUDE.md §3.2 — E-commerce tolerance thấp về giá/ship/uy tín):
        - critical: có bất kỳ hallucination nào về giá / ship / review.
        - high: có hypothesis + stability >= 0.7.
        - medium: có hypothesis nhưng stability < 0.7.
        - low: không có hypothesis nào.
    """
    hallucinations = evidence.get("tavily_mismatches", []) or []
    for h in hallucinations:
        if h.get("claim_type") in ("price", "ship", "review"):
            return "critical"

    hypotheses = evidence.get("hypotheses", []) or []
    if hypotheses and stability >= settings.stability_threshold:
        return "high"
    if hypotheses:
        return "medium"
    return "low"


def _extract_json(text: str) -> dict:
    """Extract JSON object từ text (handle ```json fences)."""
    if not text:
        raise ValueError("Empty text")

    cleaned = text.strip()

    # 1) Parse trực tiếp
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # 2) Tìm trong markdown fences ```json ... ```
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", cleaned, re.DOTALL)
    if m:
        return json.loads(m.group(1))

    # 3) Fallback: tìm { đầu tiên đến } cuối cùng
    m = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if m:
        return json.loads(m.group(0))

    raise ValueError("No JSON object found in text")


async def diagnose(
    brand_id: int,
    prompt_id: int,
    responses: list[dict],
    brand_kb: dict,
    prompt_text: str,
    stability: float,
) -> dict:
    """Main diagnosis entry — thật, dùng OpenAI function calling.

    Args:
        brand_id: ID brand trong DB.
        prompt_id: ID prompt.
        responses: list raw responses từ DB. Mỗi phần tử có shape
            ``{"id" | "response_id": int, "llm_engine": str,
            "search_engine": str, "response_text": str, ...}``.
        brand_kb: brand knowledge base từ ``brands`` table — vd:
            ``{"price_table": [...], "ship_policy": "...", "website": "...", ...}``.
        prompt_text: text gốc của prompt.
        stability: stability score (0-1) đã được tính từ trước.

    Returns:
        Dict với evidence package::

            {
                "status": "ok" | "error",
                "brand_id": int,
                "prompt_id": int,
                "hypotheses": [...],
                "evidence_package": {
                    "citations": [...],
                    "tavily_cross_check": {...},
                    "schema_audit": {...},
                    "content_gap": {...},
                },
                "recommended_actions": [...],
                "severity": "critical" | "high" | "medium" | "low",
                "raw_tool_calls": [{tool_name, args, output}],
                "iterations": int,
                # khi status == "error" có thêm "error" / "raw_text" / "evidence_so_far"
            }
    """
    if not settings.openai_api_key:
        return {
            "status": "error",
            "brand_id": brand_id,
            "prompt_id": prompt_id,
            "error": "OPENAI_API_KEY missing",
        }

    client = AsyncOpenAI(api_key=settings.openai_api_key)

    response_ids = [
        r.get("id") or r.get("response_id") for r in responses
    ]

    responses_snippet = json.dumps(
        [
            {
                "engine": r.get("llm_engine") or r.get("search_engine"),
                "response_id": r.get("id") or r.get("response_id"),
                "text": (r.get("response_text") or r.get("text") or "")[:1000],
            }
            for r in responses
        ],
        ensure_ascii=False,
        indent=2,
    )

    user_msg = (
        f"Brand ID: {brand_id}\n"
        f"Prompt ID: {prompt_id}\n"
        f"Prompt: {prompt_text}\n"
        f"Stability score: {stability:.3f}\n"
        f"Response IDs: {response_ids}\n\n"
        f"Brand knowledge base (snippet, JSON):\n"
        f"{json.dumps(brand_kb, ensure_ascii=False)[:2000]}\n\n"
        f"Responses từ {len(responses)} AI engine "
        f"(đã truncate còn ~1000 ký tự mỗi cái):\n"
        f"{responses_snippet}\n\n"
        f"Hãy phân tích TẠI SAO brand không được nhắc / bị nhắc sai, "
        f"gọi tools để thu thập evidence, rồi output JSON theo schema quy định."
    )

    messages: list[dict] = [
        {"role": "system", "content": DIAGNOSIS_SYSTEM_PROMPT},
        {"role": "user", "content": user_msg},
    ]

    raw_tool_calls: list[dict] = []
    evidence: dict = {
        "citations": [],
        "tavily_cross_check": {},
        "schema_audit": {},
        "content_gap": {},
        "tavily_mismatches": [],
    }

    max_iterations = 6
    for iteration in range(max_iterations):
        try:
            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=TOOL_DEFINITIONS,
                tool_choice="auto",
                max_tokens=2048,
                temperature=0.3,
            )
        except Exception as e:
            return {
                "status": "error",
                "brand_id": brand_id,
                "prompt_id": prompt_id,
                "error": f"OpenAI call failed: {e}",
                "iterations": iteration,
                "raw_tool_calls": raw_tool_calls,
            }

        message = response.choices[0].message

        # Nếu model gọi tools
        if message.tool_calls:
            messages.append(message)
            for tool_call in message.tool_calls:
                fn_name = tool_call.function.name
                try:
                    fn_args = json.loads(tool_call.function.arguments or "{}")
                except json.JSONDecodeError:
                    fn_args = {}

                try:
                    output = await _call_tool(fn_name, fn_args)
                except Exception as e:
                    output = {"error": str(e)}

                raw_tool_calls.append(
                    {"tool_name": fn_name, "args": fn_args, "output": output}
                )

                # Ghi nhận evidence
                if fn_name == "fetch_citations":
                    if isinstance(output, list):
                        for item in output:
                            if isinstance(item, dict) and item.get("url"):
                                evidence["citations"].append(item)
                elif fn_name == "compare_with_brand_source":
                    evidence["tavily_cross_check"] = output
                    if isinstance(output, dict) and output.get("match") is False:
                        evidence["tavily_mismatches"].append(
                            {
                                "claim": fn_args.get("claim"),
                                "claim_type": fn_args.get("claim_type", "general"),
                                "ai_value": output.get("claim_value"),
                                "actual_value": output.get("brand_actual_value"),
                                "explanation": output.get("explanation"),
                            }
                        )
                elif fn_name == "schema_check":
                    evidence["schema_audit"][fn_args.get("url", "")] = output
                elif fn_name == "detect_content_gap":
                    evidence["content_gap"][fn_args.get("topic", "")] = output

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(output, ensure_ascii=False, default=str),
                    }
                )
            continue

        # Model trả lời text (không gọi tool) → parse JSON
        final_text = message.content or ""
        messages.append(message)
        try:
            parsed = _extract_json(final_text)
        except Exception as e:
            return {
                "status": "error",
                "brand_id": brand_id,
                "prompt_id": prompt_id,
                "error": f"JSON parse failed: {e}",
                "raw_text": final_text,
                "iterations": iteration + 1,
                "raw_tool_calls": raw_tool_calls,
                "evidence_so_far": evidence,
            }

        hypotheses = parsed.get("hypotheses", []) or []
        recommended_actions = parsed.get("recommended_actions", []) or []
        model_severity = parsed.get("severity")

        severity_input = {
            "tavily_mismatches": evidence["tavily_mismatches"],
            "hypotheses": hypotheses,
        }
        severity = compute_severity(severity_input, stability)
        # Nếu model tự đánh critical về giá/ship thì ưu tiên giữ nó,
        # ngược lại dùng severity do rule engine tính.
        if model_severity == "critical" and severity != "critical":
            if any(
                h.get("claim_type") in ("price", "ship", "review")
                for h in hypotheses
            ):
                severity = "critical"

        requires_hitl = bool(parsed.get("requires_hitl", False)) or severity in (
            "critical",
            "high",
        )

        return {
            "status": "ok",
            "brand_id": brand_id,
            "prompt_id": prompt_id,
            "hypotheses": hypotheses,
            "evidence_package": {
                "citations": evidence["citations"],
                "tavily_cross_check": evidence["tavily_cross_check"],
                "schema_audit": evidence["schema_audit"],
                "content_gap": evidence["content_gap"],
                "tavily_mismatches": evidence["tavily_mismatches"],
            },
            "recommended_actions": recommended_actions,
            "severity": severity,
            "requires_hitl": requires_hitl,
            "raw_tool_calls": raw_tool_calls,
            "iterations": iteration + 1,
        }

    # Hết iteration mà model vẫn chưa return JSON
    return {
        "status": "error",
        "brand_id": brand_id,
        "prompt_id": prompt_id,
        "error": f"Max iterations ({max_iterations}) reached without JSON output",
        "evidence_so_far": evidence,
        "raw_tool_calls": raw_tool_calls,
    }
