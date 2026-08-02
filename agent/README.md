# agent/ — Agent Engineer (Lý)

> **Phụ trách**: Lý (Agent Engineer)
> **Stack**: LiteLLM (multi-model routing), Tavily API, LangChain/LangGraph (advanced), httpx, tenacity (retry)

## 🎯 Trách nhiệm

1. **Prompt Runner**: gửi prompt đến **4 nguồn AI** (ChatGPT + Gemini + Claude + Tavily).
2. **LiteLLM routing**: ánh xạ `ai_engine` → model provider.
3. **Parser LLM**: extract mention, sentiment, claim, citation từ raw response.
4. **Diagnosis Agent**: gọi tools (fetch_citations, compare_with_brand_source, schema_check, detect_content_gap).
5. **Tavily cross-check**: verify claim giá/ship với web public.
6. **Action Recommender**: đề xuất 1–3 action có bằng chứng.
7. **HITL logic**: trigger yêu cầu verify cho sentiment + hallucination.

## 📁 Cấu trúc folder

```
agent/
├── README.md
├── requirements.txt
├── .env.example
├── agent/
│   ├── __init__.py
│   ├── config.py                       ← Settings (LiteLLM, Tavily)
│   ├── cli.py                          ← CLI entry: `python -m agent.cli runner --once`
│   ├── engines/
│   │   ├── __init__.py
│   │   ├── base.py                     ← BaseEngine abstract
│   │   ├── chatgpt.py                  ← GPT-4o-mini / GPT-4o
│   │   ├── gemini.py                   ← Gemini 1.5 Flash/Pro
│   │   ├── claude.py                   ← Claude Haiku/Sonnet
│   │   └── tavily.py                   ← Tavily search
│   ├── runner/
│   │   ├── __init__.py
│   │   ├── prompt_runner.py            ← Runner chính (gọi 4 engines)
│   │   └── orchestrator.py             ← Orchestrate N lần × 4 AI
│   ├── parser/
│   │   ├── __init__.py
│   │   ├── mention_parser.py           ← LLM-based extractor
│   │   ├── sentiment.py                ← Sentiment với HITL flag
│   │   └── claim_extractor.py          ← Detect price/ship/review claim
│   ├── diagnosis/
│   │   ├── __init__.py
│   │   ├── agent.py                    ← Diagnosis Agent (function calling)
│   │   ├── tools/
│   │   │   ├── __init__.py
│   │   │   ├── fetch_citations.py      ← lấy URL từ citations
│   │   │   ├── compare_with_brand.py   ← so sánh claim giá/ship
│   │   │   ├── schema_check.py         ← schema.org check
│   │   │   └── content_gap.py          ← detect content gap
│   │   └── evidence.py                 ← Build evidence package
│   ├── tavily/
│   │   ├── __init__.py
│   │   ├── client.py                   ← Tavily client wrapper
│   │   └── cross_check.py              ← Verify giá/ship với web
│   ├── actions/
│   │   ├── __init__.py
│   │   ├── recommender.py              ← Đề xuất action từ evidence
│   │   └── templates.py                ← Template content cho mỗi action
│   └── hitl/
│       ├── __init__.py
│       └── reviewer.py                 ← Logic yêu cần HITL verify
├── scripts/
│   ├── run_baseline.py
│   └── verify_tavily.py
└── tests/
    ├── __init__.py
    ├── test_runner.py
    ├── test_parser.py
    └── test_tavily.py
```

## 🚀 Quick start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# → điền OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_AI_API_KEY, TAVILY_API_KEY

# Smoke test
python scripts/verify_tavily.py

# Run 1 scan (3 lần × 4 AI)
python -m agent.cli runner --brand-id 1 --n-runs 3

# Run parser
python -m agent.cli parse --response-id 100
```

## 🔧 Luồng chính

```
PromptRunner.orchestrate(brand_id, prompt_ids, ai_engines, n_runs=3)
    │
    ├─→ for each prompt in prompt_ids:
    │     for each ai_engine in ai_engines:
    │       for run_index in range(n_runs):
    │           engine = get_engine(ai_engine)
    │           response = engine.query(prompt_text)
    │           save_to_backend_api(response)
    │
    ├─→ for each saved response:
    │     parser = MentionParser()
    │     mentions = parser.extract(response)
    │     save_mentions(mentions)
    │
    └─→ for each (brand, prompt) with stability >= 0.7:
          diagnosis_agent.run(brand, prompt)
          ├─→ fetch_citations(...)
          ├─→ compare_with_brand_source(...)
          ├─→ schema_check(...)
          └─→ build_evidence_package()
          save_diagnosis(evidence)
```

## 📡 Engines interface

Mỗi engine implement `BaseEngine`:

```python
class BaseEngine(Protocol):
    def query(self, prompt: str, **kwargs) -> EngineResponse:
        ...

@dataclass
class EngineResponse:
    text: str
    citations: list[dict]
    model_version: str
    latency_ms: int
    cost_usd: float
    raw: dict
```

## 🔗 Dependency với folder khác

- **`backend/`** (Đăng): gọi API để lưu response + đọc task.
- **`data/`** (Khôi): đọc prompt library + brand knowledge base.
- **`shared/`**: schema prompt, brand KB.
- **`frontend/`** (Hải): không gọi trực tiếp — qua backend API.

## ⚠️ Lưu ý quan trọng

1. **Mỗi prompt chạy N=3 lần** (production: 7-8). KHÔNG BAO GIỜ chạy 1 lần.
2. **Tavily dùng cho cross-check giá/ship**, không dùng để parse mention.
3. **GPT-4o-mini / Claude Haiku** cho parse, NER. **GPT-4o / Sonnet** cho sentiment & hallucination verify.
4. **HITL bắt buộc** cho: sentiment (sarcasm E-commerce), hallucination về giá/ship/uy tín.
5. **Retry + exponential backoff** cho mỗi API call (3 lần retry, backoff 1s/2s/4s).
6. **Lưu raw response** vào `responses` table (kèm `run_index`, `model_version`).

## 📋 Checklist riêng cho Lý

Xem `../tasks.md` chi tiết. Tóm tắt:

- **Tuần 0**: Verify Tavily (tiếng Việt + Shopee/Lazada), nghiên cứu LiteLLM
- **Tuần 1**: Prompt runner 4 AI, retry/backoff, lưu raw response
- **Tuần 2**: Parser LLM, Diagnosis tools, Tavily cross-check
- **Tuần 3**: Action recommender, HITL logic
- **Tuần 4**: Closed-loop integration (re-scan + classify)
- **Tuần 5**: Polish parser, edge cases, Tavily freshness
