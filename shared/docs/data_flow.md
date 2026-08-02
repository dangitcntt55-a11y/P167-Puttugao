# Data Flow — GEO AI Agent

## Tổng quan

```
┌─────────────────────────────────────────────────────────────────┐
│                         DATA FLOW                                │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│ Prompt       │      │ 4 AI Engines │      │ Tavily       │
│ Library      │      │ ChatGPT      │      │ (Web-grounded)│
│ (100 prompts)│      │ Gemini       │      │              │
│              │      │ Claude       │      │              │
└──────┬───────┘      └──────┬───────┘      └──────┬───────┘
       │                     │                     │
       └─────────────────────┼─────────────────────┘
                             │
                             ▼
                    ┌────────────────┐
                    │ Prompt Runner  │
                    │ (3 lần × 4 AI) │
                    └────────┬───────┘
                             │
                             ▼
                    ┌────────────────┐
                    │ PostgreSQL     │
                    │ responses      │
                    │ (raw + meta)   │
                    └────────┬───────┘
                             │
                             ▼
                    ┌────────────────┐
                    │ Parser LLM     │
                    │ (GPT-4o-mini)  │
                    └────────┬───────┘
                             │
                             ▼
                    ┌────────────────┐
                    │ PostgreSQL     │
                    │ mentions       │
                    │ (NER + sent.)  │
                    └────────┬───────┘
                             │
                             ▼
                    ┌────────────────┐
                    │ Stability      │
                    │ Engine         │
                    │ threshold=0.7  │
                    └────────┬───────┘
                             │
                  ┌──────────┴──────────┐
                  │                     │
            <0.7 (noise)         ≥0.7 (stable)
                  │                     │
                  ▼                     ▼
            [Observation]      ┌────────────────┐
                                │ Diagnosis      │
                                │ Agent          │
                                │ (LLM + tools)  │
                                └────────┬───────┘
                                         │
                                         ▼
                                ┌────────────────┐
                                │ Tavily         │
                                │ Cross-check    │
                                │ giá/ship       │
                                └────────┬───────┘
                                         │
                                         ▼
                                ┌────────────────┐
                                │ Evidence       │
                                │ Package        │
                                └────────┬───────┘
                                         │
                                         ▼
                                ┌────────────────┐
                                │ Action         │
                                │ Recommender    │
                                │ (1-3 actions)  │
                                └────────┬───────┘
                                         │
                                         ▼
                                ┌────────────────┐
                                │ HITL UI        │
                                │ Approve/Reject │
                                └────────┬───────┘
                                         │
                                  Approve (HITL)
                                         │
                                         ▼
                                ┌────────────────┐
                                │ Task DB        │
                                │ (todo)         │
                                └────────┬───────┘
                                         │
                                  Marketer làm xong
                                         │
                                         ▼
                                ┌────────────────┐
                                │ Task → done    │
                                │ → trigger      │
                                │ re-scan (Celery)│
                                └────────┬───────┘
                                         │
                                         ▼
                                ┌────────────────┐
                                │ Re-scan 3×4    │
                                │ post_responses │
                                └────────┬───────┘
                                         │
                                         ▼
                                ┌────────────────┐
                                │ Bootstrap CI   │
                                │ 95% CI         │
                                └────────┬───────┘
                                         │
                                         ▼
                                ┌────────────────┐
                                │ Classification │
                                │ improved /     │
                                │ no_evidence /  │
                                │ regressed      │
                                └────────┬───────┘
                                         │
                                         ▼
                                ┌────────────────┐
                                │ Evaluation     │
                                │ Report UI      │
                                └────────────────┘
```

## Luồng chính

### 1. Scan (Tuần 1)
1. Celery scheduler trigger scan mỗi ngày
2. Prompt runner gửi 100 prompts × 4 AI × 3 lần = 1200 responses
3. Raw responses lưu vào DB

### 2. Parse + Stability (Tuần 1-2)
1. Parser LLM extract mentions (NER + sentiment + claim_type)
2. Stability Engine tính điểm ổn định từ 3 lần chạy
3. Gap có Stability ≥ 0.7 → vào diagnosis

### 3. Diagnosis (Tuần 2)
1. Diagnosis Agent dùng tools:
   - `fetch_citations` → lấy URL citation
   - `compare_with_brand_source` → verify giá/ship
   - `schema_check` → check schema.org
   - `detect_content_gap` → kiểm tra nội dung
2. Build evidence package
3. Action recommender đề xuất 1-3 actions

### 4. HITL (Tuần 2-3)
1. Marketer review diagnoses trên UI
2. Approve / Reject / Edit
3. Approved → tạo task

### 5. Task execution (Tuần 3)
1. Marketer / content team làm task
2. Mark task done → trigger re-scan

### 6. Closed-loop (Tuần 4)
1. Re-scan 3 lần × 4 AI (post-action)
2. Bootstrap 95% CI cho (post - pre)
3. Phân loại: improved / no_evidence / regressed
4. Report UI

## Frequency

| Bước | Tần suất |
|------|----------|
| Scan | 1 lần/ngày |
| Parse + Stability | Real-time (sau scan) |
| Diagnosis | On-demand (khi có stable gap mới) |
| Re-scan | Khi task done |
| Evaluation report | Sau re-scan |
