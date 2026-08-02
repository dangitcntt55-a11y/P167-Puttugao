# CLAUDE.md — Hướng dẫn cho AI Assistant khi làm việc với repo này

> **Đọc file này TRƯỚC** khi bắt đầu bất kỳ task code/research nào trong dự án.
> Repo này thuộc đồ án nhóm 4 người: **Đăng, Lý, Khôi, Hải**.
> Đề tài: **GEO AI Agent cho E-commerce Việt Nam** — xem `GEO_AI_Agent_Ecommerce_VN.md` để hiểu toàn bộ scope.

---

## 1. Bối cảnh dự án (context bắt buộc)

- **Mục tiêu cuối**: AI Agent theo dõi AI visibility (GEO) cho shop/brand E-commerce VN trên 4 nguồn AI: **ChatGPT + Gemini + Claude + Tavily**.
- **3 trụ cột** (không được quên):
  1. **Stability-aware Monitoring** — chạy prompt N lần (N=3 demo, 7–8 production), tính Stability Score ≥ 0.7 mới đưa vào diagnosis.
  2. **Evidence-grounded Diagnosis** — mỗi gap có citation URL + quote + cross-check giá/ship/uy tín với Tavily.
  3. **Closed-loop Re-measurement** — sau khi task done → re-scan + bootstrap 95% CI → phân loại `Improved signal` / `No clear evidence` / `Regressed`.
- **Phạm vi demo 5 tuần**: 2 brand E-commerce (1 sàn + 1 D2C) + 2–3 đối thủ/brand + ~100 prompt tiếng Việt chia 5 nhóm (uy tín, giá, so sánh, review, ship).
- **Căn cứ học thuật**: Schulte et al. arXiv 2604.07585 + arXiv 2603.08924 + Tian et al. arXiv 2603.09296.

Đọc kỹ `GEO_AI_Agent_Ecommerce_VN.md` (file gốc 1137 dòng) trước khi code. Đặc biệt:
- **PART 1 (WHY)** — tại sao đề tài này hợp lý.
- **PART 2 (WHAT)** — 2 core features + 1 advanced feature.
- **PART 3 (HOW)** — kiến trúc, schema, tech stack, roadmap 5 tuần.
- **PHỤ LỤC B** — nguồn tham khảo.

---

## 2. Cấu trúc repo

```
.
├── CLAUDE.md                       ← file này
├── README.md                       ← giới thiệu + quick start
├── tasks.md                        ← phân công & kế hoạch 5 tuần
├── GEO_AI_Agent_Ecommerce_VN.md    ← tài liệu gốc (đọc trước)
├── backend/                        ← Đăng (Tech Lead)
├── agent/                          ← Lý (Agent Engineer)
├── data/                           ← Khôi (Data/NLP)
├── frontend/                       ← Hải (Frontend/Infra)
├── shared/                         ← tài nguyên chung (schema, prompts, config)
└── docs/                           ← weekly reports, meeting notes, demo scripts
```

---

## 3. Quy tắc cứng khi code (MUST)

### 3.1. Về ngôn ngữ & prompt
- **Tiếng Việt** là ngôn ngữ chính cho prompt library, brand name, mô tả.
- Xử lý được **3 biến thể tên**: có dấu / không dấu / viết tắt (vd: `Minh Long`, `Minh Long Book`, `MLB`).
- Logging internal (biến, comment) dùng tiếng Anh. UI label tiếng Việt.

### 3.2. Về AI calls
- **Mỗi prompt chạy N lần** (N=3 demo), không bao giờ chạy 1 lần — vi phạm nguyên tắc Stability-aware.
- **Stability Score ≥ 0.7** mới đưa gap vào diagnosis. Nếu < 0.7 thì đánh dấu `observation_only`.
- **FN (bỏ sót) nguy hiểm hơn FP** (đếm nhầm) — thiết kế parser thiên về recall.
- **Hallucination về giá/ship/uy tín tolerance rất thấp** — luôn cần HITL verify.

### 3.3. Về closed-loop
- Mọi kết luận "improved" PHẢI có **bootstrap 95% CI** vượt **noise floor 5–7 điểm %** (theo arXiv 2603.08924).
- Không ép kết luận — nếu CI overlap với 0 thì ghi `No clear evidence`.

### 3.4. Về cost
- Ưu tiên **GPT-4o-mini / Claude Haiku** cho parse & NER.
- **GPT-4o / Claude Sonnet** chỉ dùng cho sentiment & hallucination verify.
- **Tavily** cho cross-check giá/ship — KHÔNG dùng để parse mention.
- Budget MVP: **≤ $0.30/scan** (30 prompt × 3 lần × 4 AI).

### 3.5. Về schema DB
- Đã chốt schema ở `GEO_AI_Agent_Ecommerce_VN.md` §19.3. **Không tự ý thêm cột** mà không update cả team.
- Bảng `responses` lưu raw text + JSONB citations + `ai_engine` ∈ {`chatgpt`, `gemini`, `claude`, `tavily`}.
- Luôn có `run_index` (1, 2, 3) để tính Stability.

### 3.6. Về bảo mật
- **KHÔNG commit** file `.env` chứa API key thật. Dùng `.env.example` cho template.
- Mỗi folder có `.env.example` riêng; root có `.env` dùng chung (chỉ local).

---

## 4. Quy tắc làm việc nhóm

### 4.1. Workflow mỗi tuần
1. **Thứ 2** — Sync 30 phút: review tuần trước + chốt task tuần này (update `tasks.md`).
2. **Thứ 4** — Pair session 2 giờ (Đăng–Lý, Khôi–Hải tùy task).
3. **Thứ 6** — Demo nội bộ 30 phút, ghi vào `docs/weekly/week-N.md`.
4. **Chủ nhật** — Mỗi người push code + update tiến độ.

### 4.2. Quy tắc commit
- Format: `<scope>: <mô tả ngắn>` — vd: `backend: add stability score endpoint`.
- Mỗi PR ≤ 300 dòng diff. PR > 500 dòng phải split.
- **Mỗi member tự review PR của mình** trước khi merge.
- Lead tuần (xoay vòng) review cross-PR.

### 4.3. Quy tắc giao tiếp
- Issue trong `tasks.md` (markdown checklist) — không dùng tool ngoài.
- Daily standup 15 phút trên group chat (cập nhật 3 câu: hôm qua / hôm nay / blocker).
- Decision quan trọng phải ghi vào `docs/decisions/ADR-NNN-*.md`.

### 4.4. Code ownership
| Member | Folder | Touch chính |
|--------|--------|-------------|
| **Đăng** (Tech Lead) | `backend/` | FastAPI, PostgreSQL, scheduler, closed-loop re-scan, eval |
| **Lý** (Agent Engineer) | `agent/` | LiteLLM, Tavily tools, prompt runner, parser, diagnosis agent |
| **Khôi** (Data/NLP) | `data/` | Prompt library, gold dataset, stability analysis, bootstrap CI |
| **Hải** (Frontend/Infra) | `frontend/` | Next.js dashboard, HITL UI, chart, Docker, deployment |

Folder **shared/** và **docs/** là chung — ai cũng có thể sửa, nhưng PR phải có 1 reviewer.

---

## 5. Quy tắc khi tương tác AI Assistant (Cursor/Claude)

### 5.1. Trước khi hỏi AI
- Đã đọc `GEO_AI_Agent_Ecommerce_VN.md` phần liên quan chưa?
- Đã check `tasks.md` để biết task đang làm thuộc tuần nào chưa?
- Đã copy schema/db structure vào context chưa (nếu cần)?

### 5.2. Cách hỏi hiệu quả
- **Cung cấp context**: "Tôi đang code phần X cho tuần Y, schema bảng Z là..., cần viết function A."
- **Specify file đường dẫn tuyệt đối**: `d:\AI_THUCCHIEN\BTNHOM\backend\app\...`
- **Reference tài liệu**: "theo §19.3 schema" hoặc "theo hằng số Stability ≥ 0.7".

### 5.3. AI KHÔNG ĐƯỢC
- ❌ Tự ý thêm cột DB / đổi schema mà không hỏi.
- ❌ Hardcode API key vào code.
- ❌ Bỏ qua Stability Score (chạy 1 lần).
- ❌ Tự ý chọn model đắt khi có model rẻ tương đương.
- ❌ Viết code không có test cho phần reward function / stability / bootstrap CI.

### 5.4. AI NÊN
- ✅ Gợi ý chia nhỏ task nếu thấy quá lớn.
- ✅ Cảnh báo khi phát hiện anti-pattern (xem §5 của `GEO_AI_Agent_Ecommerce_VN.md`).
- ✅ Reference paper arXiv khi đề xuất giải pháp.
- ✅ Kiểm tra cost ước lượng mỗi khi thêm API call.

---

## 6. Tech stack đã chốt (từ §19.2)

| Layer | Công nghệ |
|-------|-----------|
| Frontend | Next.js 14, Tailwind CSS, Recharts |
| Backend | FastAPI (Python 3.11), Celery (scheduler) |
| Database | PostgreSQL 16, Redis (cache), Qdrant (vector DB) |
| LLM orchestration | LiteLLM (multi-model), LangGraph (nâng cao) |
| AI APIs | OpenAI, Anthropic, Google AI Studio, **Tavily** |
| Scraper | Playwright (fallback Shopee/Lazada) |
| Monitoring | Prometheus + Grafana |
| Deployment | Docker Compose, Vercel (frontend) |

**Lưu ý**: Stack có thể đơn giản hóa cho demo (vd: SQLite thay PostgreSQL, JSON file thay Redis) — nhưng **PHẢI** giữ 4 nguồn AI + Tavily.

---

## 7. Convention code

### 7.1. Python (backend/agent)
- Format: **Black** (line length 100), **Ruff** cho lint.
- Type hint bắt buộc cho function public.
- Docstring: **Google style** cho module, **NumPy style** cho function.
- Mỗi module có `__init__.py` rỗng nếu cần.

### 7.2. TypeScript (frontend)
- ESLint + Prettier (config mặc định Next.js).
- Component có prop type rõ ràng, không dùng `any`.
- Folder: `app/` (Next.js App Router), `components/`, `lib/`, `hooks/`.

### 7.3. SQL
- Migration dùng Alembic (backend) hoặc raw SQL file đánh version.
- Tên bảng: số ít, snake_case (`responses`, `mentions`, `stability_scores`).
- Index cho cột FK + cột query thường xuyên (`brand_id`, `prompt_id`, `created_at`).

### 7.4. Tên biến
- `visibility_rate` (FLOAT 0–1)
- `stability_score` (FLOAT 0–1, ≥ 0.7)
- `mention_position` (INT 1, 2, 3)
- `sentiment` (FLOAT -1 to +1)
- `claim_type` ∈ {`price`, `ship`, `review`, `general`}
- `ai_engine` ∈ {`chatgpt`, `gemini`, `claude`, `tavily`}
- `task_result` ∈ {`improved`, `no_evidence`, `regressed`}

---

## 8. Definition of Done (mỗi task)

Một task được coi là xong khi:
- [ ] Code đã push lên branch + PR.
- [ ] Có README/screenshot nếu là UI.
- [ ] Test pass (unit test cho logic, smoke test cho API).
- [ ] Update `tasks.md` (tick checkbox).
- [ ] Nếu thay đổi schema → update `shared/schema.sql` + ADR.
- [ ] Nếu thay đổi prompt → update `shared/prompts/`.

---

## 9. Liên hệ nhanh

- **Đăng (Tech Lead)**: Backend & DB → mọi câu hỏi về schema, API contract, deployment.
- **Lý (Agent)**: Mọi câu hỏi về LLM, Tavily, diagnosis agent, prompt runner.
- **Khôi (Data)**: Mọi câu hỏi về prompt library, gold dataset, eval, bootstrap CI.
- **Hải (Frontend)**: Mọi câu hỏi về UI, dashboard, chart, deployment.

**Trước khi hỏi AI Assistant, hỏi member phụ trách folder trước** — AI chỉ hỗ trợ accelerate, không thay thế domain knowledge của member.

---

## 10. Lệnh nhanh

```bash
# Chạy dev (mỗi member mở terminal riêng)
cd backend && uvicorn app.main:app --reload        # Đăng
cd agent && python -m agent.cli runner --once      # Lý
cd frontend && npm run dev                          # Hải

# Database
docker-compose up -d postgres redis                 # Postgres + Redis
psql -h localhost -U geo -d geo_ecom_dev            # Connect

# Test
cd backend && pytest                                # Backend test
cd agent && pytest                                  # Agent test
cd frontend && npm test                             # Frontend test

# Lint
cd backend && ruff check . && black . --check       # Python
cd frontend && npm run lint                         # TypeScript
```

---

> 📌 **Mọi thay đổi kiến trúc quan trọng đều phải update file này + GHI ADR vào `docs/decisions/`.**
