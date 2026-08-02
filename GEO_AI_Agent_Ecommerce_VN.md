# GEO AI Agent cho E-commerce Việt Nam

> **File nội bộ cho AI assistant** — dùng làm context khi code/research trong repo này.
> Đối tượng đọc: Cursor / Claude. Không phải tài liệu pitch.
> Repo: dự án nhóm 4 người (Đăng, Lý, Khôi, Hải) — Đồ án.

---

## 1. Pain points cần giải quyết

| # | Pain point | Lý do cần giải |
|---|------------|---------------|
| 1 | Kết quả từ nhiều AI bị phân tán (ChatGPT, Gemini, Claude, Tavily chạy rời rạc) | Marketer không có dashboard gộp, phải mở 4 tab mỗi lần check |
| 2 | Các mô hình AI đưa ra đề xuất khác nhau cho cùng 1 prompt | Không biết đề xuất nào đáng tin, không có cơ chế đo độ ổn định |
| 3 | Đề xuất AI thiếu bối cảnh doanh nghiệp (ngành hàng, đối thủ, prompt đặc thù VN) | Tool quốc tế (Semrush, Ahrefs) dùng prompt pattern US/EU, không cover câu hỏi tiếng Việt |
| 4 | Nhiều đề xuất nhưng không biết làm gì trước | Không có priority ranking, không gắn với citation/bằng chứng |
| 5 | Khó đánh giá độ tin cậy của đề xuất AI | Không có stability score, không có evidence-grounded, không có closed-loop để verify |

---

## 2. Hướng đi: 2 Core Features + 1 Advanced

> Nguyên tắc thiết kế: **Stability-aware** (mỗi prompt chạy N lần, N=3 demo) + **Evidence-grounded** (mỗi gap có citation URL + quote) + **Closed-loop** (re-measure sau action).

### 2.1. AI Visibility Monitor (Core #1)

**Giá trị:** Theo dõi thương hiệu xuất hiện trong câu trả lời AI một cách ổn định theo thời gian.

**Capabilities bên trong:**

| Capability | Mô tả ngắn |
|------------|------------|
| **Query Generation** | Sinh prompt tiếng Việt theo 5 nhóm (uy tín, giá, so sánh, review, ship) — tổng ~100 prompt/brand |
| **Multi-AI Search** | Gửi prompt đến 4 nguồn: ChatGPT, Gemini, Claude, Tavily (Tavily = web-grounded cho citation) |
| **Visibility Metrics** | Tính visibility_rate (0–1), mention_position (1/2/3), SOV (share of voice vs đối thủ) |
| **Stability Analysis** | Mỗi prompt chạy N=3 lần, tính Stability Score ≥ 0.7 mới đưa vào diagnosis. < 0.7 → đánh `observation_only` |
| **Trend Dashboard** | Biểu đồ visibility theo ngày/tuần, theo AI engine, theo nhóm prompt |

**Anti-patterns (KHÔNG LÀM):**
- Chạy prompt 1 lần → vi phạm stability-aware.
- Đếm nhầm mention (FP) vẫn ok, bỏ sót mention (FN) thì nguy hiểm — parser thiên về recall.

---

### 2.2. GEO Recommendation Agent (Core #2)

**Giá trị:** Phân tích nguyên nhân thương hiệu chưa được AI ưu tiên và đề xuất hành động cải thiện có bằng chứng.

**Capabilities bên trong:**

| Capability | Mô tả ngắn |
|------------|------------|
| **Citation Analysis** | Phân tích URL nguồn mà AI tham chiếu → biết AI đang "học" từ đâu, brand mình có mặt ở nguồn đó không |
| **Content Gap Analysis** | So câu trả lời AI với nội dung brand đang có → tìm topic brand chưa cover |
| **Schema Audit** | Check structured data (Product, FAQ, Organization, Review) trên site brand — AI ưu tiên nguồn có schema đầy đủ |
| **Claim Verification** | Cross-check mọi claim về giá/ship/uy tín với Tavily (search web grounded) → phát hiện hallucination |
| **Action Plan Generation** | Output danh sách task ưu tiên, mỗi task gắn với evidence (citation URL + quote) |

**Hallucination tolerance rất thấp** — Mọi claim về giá/ship/uy tín PHẢI qua cross-check Tavily + HITL verify.

---

### 2.3. Closed-loop Re-measurement (Advanced Feature)

**Giá trị:** Sau khi marketer làm task tối ưu → re-scan → đo xem visibility có cải thiện thật không (không phải ngẫu nhiên).

**Flow:**
1. Marketer đánh dấu task trong Action Plan là `done`.
2. Agent tự động re-scan các prompt trong task đó (cùng N=3 lần).
3. Tính bootstrap 95% CI cho delta visibility.
4. Phân loại:
   - `improved_signal` — CI vượt noise floor 5–7 điểm %.
   - `no_clear_evidence` — CI overlap với 0.
   - `regressed` — CI giảm có ý nghĩa.

**Không ép kết quả** — nếu CI overlap 0 thì ghi `no_clear_evidence`, không tự ý phân loại `improved`.

---

## 3. Scope

| Trường | Giá trị |
|--------|---------|
| **Đối tượng** | Marketing Manager / CMO của **SME E-commerce Việt Nam** |
| **Phạm vi thời gian** | **5 tuần** |
| **Phạm vi kỹ thuật** | 4 nguồn AI: **ChatGPT + Gemini + Claude + Tavily** × **E-commerce** × **10 brands mẫu** (2 brand demo chính + 2–3 đối thủ/brand → tổng ~10 brand) |
| **Phạm vi ngôn ngữ** | **Tiếng Việt** |
| **Prompt library** | ~100 prompt/brand chia 5 nhóm: uy tín, giá, so sánh, review, ship |
| **Mục tiêu cuối** | Giảm **90%** thời gian GEO monitoring, tăng **10×** prompt coverage, phát hiện **≥ 80%** hallucination trong 24h `[Ước lượng]` |

**Lưu ý về 10 brands:**
- 2 brand demo chính: 1 sàn (nhiều SKU, đối thủ nhiều) + 1 D2C (entity riêng, content-driven).
- Mỗi brand chính kèm 2–3 đối thủ trực tiếp cùng ngành hàng.
- Tổng cộng ~10 brand để so sánh SOV.

---

## 4. Tech Stack & Quy tắc cứng

### 4.1. Tech stack (đã chốt)

| Layer | Công nghệ |
|-------|-----------|
| Frontend | Next.js 14, Tailwind CSS, Recharts |
| Backend | FastAPI (Python 3.11), Celery (scheduler) |
| Database | PostgreSQL 16, Redis (cache), Qdrant (vector DB) |
| LLM orchestration | LiteLLM (multi-model), LangGraph (advanced) |
| AI APIs | OpenAI, Anthropic, Google AI Studio, **Tavily** |
| Scraper | Playwright (fallback Shopee/Lazada) |
| Monitoring | Prometheus + Grafana |
| Deployment | Docker Compose, Vercel (frontend) |

**Demo có thể đơn giản hóa:** SQLite thay PostgreSQL, JSON file thay Redis — **nhưng PHẢI giữ 4 nguồn AI + Tavily**.

### 4.2. Quy tắc AI calls

- **Mỗi prompt chạy N=3 lần** (demo), N=7–8 (production). Không bao giờ 1 lần.
- **Stability Score ≥ 0.7** mới đưa gap vào diagnosis. < 0.7 → `observation_only`.
- **FN nguy hiểm hơn FP** — parser thiên về recall.
- **Hallucination về giá/ship/uy tín** → tolerance rất thấp, luôn cần HITL verify.

### 4.3. Quy tắc cost

| Task | Model khuyến nghị |
|------|-------------------|
| Parse mention, NER | **GPT-4o-mini / Claude Haiku** |
| Sentiment, hallucination verify | **GPT-4o / Claude Sonnet** |
| Citation web-grounded | **Tavily** (KHÔNG dùng Tavily để parse mention) |

**Budget MVP:** ≤ $0.30/scan (30 prompt × 3 lần × 4 AI).

### 4.4. Quy tắc schema DB

- Schema đã chốt ở §19.3 của bản gốc — **không tự ý thêm cột** mà không update cả team + ADR.
- Bảng `responses` lưu raw text + JSONB citations + `ai_engine` ∈ {`chatgpt`, `gemini`, `claude`, `tavily`}.
- Luôn có `run_index` (1, 2, 3) để tính Stability.

### 4.5. Bảo mật

- **KHÔNG commit** file `.env` chứa API key thật. Dùng `.env.example`.
- Mỗi folder có `.env.example` riêng; root có `.env` dùng chung (chỉ local).

---

## 5. Phân công nhóm & Folder ownership

| Member | Vai trò | Folder | Touch chính |
|--------|---------|--------|-------------|
| **Đăng** | Tech Lead | `backend/` | FastAPI, PostgreSQL, scheduler, closed-loop re-scan, eval |
| **Lý** | Agent Engineer | `agent/` | LiteLLM, Tavily tools, prompt runner, parser, diagnosis agent |
| **Khôi** | Data/NLP | `data/` | Prompt library, gold dataset, stability analysis, bootstrap CI |
| **Hải** | Frontend/Infra | `frontend/` | Next.js dashboard, HITL UI, chart, Docker, deployment |

`shared/` (schema, prompts, config) và `docs/` là chung — PR phải có 1 reviewer.

---

## 6. Convention code

### 6.1. Python (backend/agent)
- **Black** (line length 100), **Ruff** lint.
- Type hint bắt buộc cho function public.
- Docstring: **Google style** module, **NumPy style** function.

### 6.2. TypeScript (frontend)
- ESLint + Prettier (Next.js default).
- Component prop type rõ ràng, không `any`.

### 6.3. SQL
- Alembic migration (backend) hoặc raw SQL file version.
- Bảng số ít, snake_case (`responses`, `mentions`, `stability_scores`).
- Index cho FK + cột query thường xuyên.

### 6.4. Tên biến chuẩn

| Biến | Type | Domain |
|------|------|--------|
| `visibility_rate` | FLOAT 0–1 | Tỷ lệ prompt brand được nhắc |
| `stability_score` | FLOAT 0–1, ≥ 0.7 | Độ ổn định qua N lần chạy |
| `mention_position` | INT 1, 2, 3 | Vị trí nhắc trong answer |
| `sentiment` | FLOAT -1 to +1 | Sentiment về brand |
| `claim_type` | enum | `price`, `ship`, `review`, `general` |
| `ai_engine` | enum | `chatgpt`, `gemini`, `claude`, `tavily` |
| `task_result` | enum | `improved`, `no_evidence`, `regressed` |

---

## 7. Definition of Done (mỗi task)

- [ ] Code push lên branch + PR.
- [ ] README/screenshot nếu là UI.
- [ ] Test pass (unit test logic, smoke test API).
- [ ] Update `tasks.md` (tick checkbox).
- [ ] Đổi schema → update `shared/schema.sql` + ADR.
- [ ] Đổi prompt → update `shared/prompts/`.

---

## 8. Lệnh nhanh

```bash
# Dev (mỗi member mở terminal riêng)
cd backend && uvicorn app.main:app --reload
cd agent && python -m agent.cli runner --once
cd frontend && npm run dev

# Database
docker-compose up -d postgres redis
psql -h localhost -U geo -d geo_ecom_dev

# Test
cd backend && pytest
cd agent && pytest
cd frontend && npm test

# Lint
cd backend && ruff check . && black . --check
cd frontend && npm run lint
```

---

## 9. Liên hệ nhanh khi cần hỏi

- **Schema / API contract / deployment** → @Đăng (Tech Lead).
- **LLM / Tavily / prompt runner / diagnosis** → @Lý.
- **Prompt library / gold dataset / eval / bootstrap CI** → @Khôi.
- **UI / dashboard / chart / Docker** → @Hải.

**Hỏi member phụ trách folder trước** — AI chỉ hỗ trợ accelerate, không thay thế domain knowledge.

---

## 10. Căn cứ học thuật (reference khi đề xuất giải pháp)

- **Schulte et al.** arXiv 2604.07585 — Stability-aware Monitoring (Don't Measure Once).
- **arXiv 2603.08924** — Closed-loop re-measurement + noise floor 5–7 điểm %.
- **Tian et al.** arXiv 2603.09296 — Evidence-grounded Diagnosis (citation URL + claim quote).
