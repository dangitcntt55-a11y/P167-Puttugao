# 📋 tasks.md — Phân công & Kế hoạch 5 tuần

> **Cập nhật mỗi tuần** (cuối ngày sync). Tick `[x]` khi xong, ghi `[~]` khi đang làm, `[ ]` khi chưa bắt đầu.
> **Lead tuần xoay vòng**: Tuần 1 = Đăng, Tuần 2 = Lý, Tuần 3 = Khôi, Tuần 4 = Hải, Tuần 5 = Đăng (chốt + demo).

---

## 👥 Phân công vai trò (cố định suốt 5 tuần)

| Member | Role | Folder | Phụ trách |
|--------|------|--------|-----------|
| **Đăng** | Tech Lead | `backend/` | FastAPI, PostgreSQL schema, scheduler, Closed-loop re-scan engine, bootstrap CI, deployment |
| **Lý** | Agent Engineer | `agent/` | LiteLLM routing, Prompt runner (4 AI), Tavily tools, Parser LLM, Diagnosis agent, HITL UI logic |
| **Khôi** | Data/NLP | `data/` | Prompt library ~100 prompts / 5 nhóm, Gold dataset 50–100 mẫu, Stability analysis, Evaluation reports |
| **Hải** | Frontend/Infra | `frontend/` | Next.js dashboard, Chart viz, HITL approval UI, Docker Compose, Monitoring |

---

## 📅 Tuần 0 — Chuẩn bị (1 tuần trước khi chạy chính)

> **Mục tiêu**: có API key + 2 brand được chọn + prompt library + gold dataset.

### Đăng (Tech Lead)
- [ ] Đăng ký & nhận API key: OpenAI, Anthropic, Google AI Studio, **Tavily**
- [ ] Setup repo: Git init, branch protection, PR template, `.gitignore`
- [ ] Tạo `docker-compose.yml` (PostgreSQL + Redis + Qdrant)
- [ ] Tạo `backend/app/db/schema.sql` (copy từ `GEO_AI_Agent_Ecommerce_VN.md` §19.3)
- [ ] Setup Alembic migration cho schema

### Lý (Agent Engineer)
- [ ] Verify **Tavily API** cho tiếng Việt + Shopee/Lazada (test 20 query)
- [ ] Verify OpenAI, Anthropic, Gemini API: response time, cost/1k token
- [ ] Nghiên cứu LiteLLM syntax cho multi-model routing
- [ ] Draft kiến trúc `agent/` (folder structure)

### Khôi (Data/NLP)
- [ ] Chọn **2 brand E-commerce demo** (1 sàn + 1 D2C) + 2–3 đối thủ/brand
- [ ] Thu thập Brand Knowledge Base: URL Shopee/Lazada/web, bảng giá, FAQ, ship policy, rating
- [ ] Khởi tạo Gold dataset (20 mẫu pilot) — gán nhãn thủ công
- [ ] Liệt kê draft **~100 prompt tiếng Việt** chia 5 nhóm

### Hải (Frontend/Infra)
- [ ] Setup Next.js 14 + Tailwind + Recharts
- [ ] Wireframe dashboard E-commerce (low-fi Figma hoặc vẽ tay)
- [ ] Setup Vercel project (chưa deploy, chỉ config)
- [ ] Setup Prometheus + Grafana local

### Deliverable Tuần 0
- [ ] 4 API key live + test OK
- [ ] 2 brand + 4–6 đối thủ đã chọn + KB thu thập xong
- [ ] DB schema đã migrate lên PostgreSQL local
- [ ] Prompt library draft ~100 prompts
- [ ] Gold dataset 20 mẫu pilot

---

## 📅 Tuần 1 — Foundation + Stability-aware Baseline

> **Mục tiêu**: chạy được baseline scan cho 2 brand + dashboard cơ bản + Stability Score.

### Đăng
- [ ] FastAPI skeleton: `app/main.py`, router, lifespan
- [ ] Model SQLAlchemy cho `responses`, `mentions`, `stability_scores`, `diagnoses`, `tasks`
- [ ] Endpoint `POST /api/v1/scan/` (manual trigger)
- [ ] Endpoint `GET /api/v1/visibility/{brand_id}` (trả về Visibility Rate, SOV)
- [ ] Cấu hình Celery + Redis (scheduler chạy 3 lần/ngày)
- [ ] Setup logging (JSON format, có `trace_id`)

### Lý
- [ ] **Prompt runner** gửi prompt đến 4 nguồn AI (ChatGPT, Gemini, Claude, Tavily)
- [ ] LiteLLM config: mapping `ai_engine` → model
- [ ] Retry + exponential backoff cho mỗi API call
- [ ] Lưu raw response vào DB bảng `responses` (kèm `run_index`, `model_version`)
- [ ] Smoke test: 5 prompt × 3 lần × 4 AI = 60 responses

### Khôi
- [ ] Hoàn thiện **Prompt library ~100 prompt** chia 5 nhóm (uy tín, giá, so sánh, review, ship)
- [ ] Hoàn thiện Gold dataset (50–100 mẫu) — có nhãn `is_target_brand`, `sentiment`, `claim_type`
- [ ] Chạy baseline scan thật cho 2 brand + 4–6 đối thủ
- [ ] Tính **Stability Score** = 1 - normalized variance (từ 3 lần chạy)
- [ ] Phân tích: bao nhiêu % gap đạt Stability ≥ 0.7?

### Hải
- [ ] Dashboard page: danh sách 2 brand + 4–6 đối thủ
- [ ] Biểu đồ visibility rate theo ngành hàng (Recharts)
- [ ] Biểu đồ SOV per brand theo AI engine
- [ ] Bảng chi tiết: prompt × AI engine × visibility + stability score
- [ ] Filter: theo brand, theo prompt group, theo AI engine

### Deliverable Tuần 1
- [ ] Baseline scan report cho 2 brand + 4–6 đối thủ với Stability Score
- [ ] Dashboard chạy được, hiển thị số liệu thật
- [ ] ≥ 600 raw responses trong DB (50 prompt × 3 lần × 4 AI = 600)
- [ ] Phân tích Stability: phải có ≥ 50% gap đạt ≥ 0.7 (nếu thấp hơn → cần tăng N lần chạy)

---

## 📅 Tuần 2 — Diagnosis & Evidence Agent

> **Mục tiêu**: parse mention từ raw response + diagnosis với evidence + Tavily cross-check.

### Đăng
- [ ] Endpoint `GET /api/v1/diagnoses/` (liệt kê gap qua Stability filter)
- [ ] Endpoint `POST /api/v1/diagnoses/{id}/approve` (HITL approve)
- [ ] Endpoint `POST /api/v1/diagnoses/{id}/reject` (HITL reject)
- [ ] DB indexes tối ưu cho query theo `brand_id`, `stability_score`, `created_at`
- [ ] API contract cho frontend (OpenAPI schema)

### Lý
- [ ] **Parser LLM** (GPT-4o-mini): extract mention, position, sentiment, context quote, claim_type
- [ ] **Diagnosis tools** (function calling cho LLM):
  - `fetch_citations(response_id)` — lấy URL từ citations JSONB
  - `compare_with_brand_source(claim, brand_id)` — so sánh giá/ship/uy tín với Shopee/Lazada/web
  - `detect_content_gap(brand_id, topic)` — kiểm tra trang web shop có đủ thông tin không
  - `schema_check(url)` — kiểm tra schema.org Product/Offer/Review
- [ ] **Tavily cross-check workflow**: lấy claim → Tavily search → verify → output evidence package
- [ ] Output: `evidence_package` = `{url, quote_span, claim_type, confidence, verified_at}`
- [ ] Test với 5 gap thực tế từ baseline scan

### Khôi
- [ ] Đánh giá **Mention extraction F1** trên Gold dataset (target ≥ 0.85)
- [ ] Confusion matrix: FP vs FN (xem có thiên về recall không?)
- [ ] Hỗ trợ Lý review parser output (HITL batch: 20 diagnoses)
- [ ] Phân tích sentiment cho 50 responses (manual label, check parser accuracy)
- [ ] Document pattern: brand name có dấu / không dấu / viết tắt

### Hải
- [ ] Diagnosis detail page: hiển thị gap + evidence package
- [ ] UI: hiển thị citation URL (clickable) + quote span (highlighted)
- [ ] UI: hiển thị Tavily cross-check result (giá/ship match hay không)
- [ ] UI: nút Approve / Reject cho marketer
- [ ] Show Stability Score + 3 lần responses khác nhau (nếu variance cao)

### Deliverable Tuần 2
- [ ] Diagnosis output cho **5 gap thực tế** của 2 brand (có evidence package)
- [ ] Mention extraction F1 ≥ 0.85 trên Gold dataset
- [ ] Tavily cross-check chạy được cho giá/ship
- [ ] HITL approval UI work

---

## 📅 Tuần 3 — Action Plan + HITL UI

> **Mục tiêu**: đề xuất action có bằng chứng + marketer duyệt + task board.

### Đăng
- [ ] Bảng `tasks` (đã có schema, thêm endpoints)
- [ ] Endpoint `POST /api/v1/tasks/` (tạo task từ diagnosis)
- [ ] Endpoint `PATCH /api/v1/tasks/{id}` (update status: todo → in_progress → done)
- [ ] Endpoint `GET /api/v1/tasks/?brand_id=&status=`
- [ ] Logic: khi task → status=done → trigger re-scan (queue Celery)

### Lý
- [ ] **Action recommender** (LLM): từ evidence package → đề xuất 1–3 action cụ thể:
  - `listing_update` — cập nhật listing Shopee/Lazada (schema Product, SEO)
  - `content_add` — thêm nội dung web shop (FAQ, bảng giá)
  - `schema_add` — thêm schema FAQ cho trang
  - `outreach` — outreach cập nhật citation (Tinhte, Voz)
  - `content_pr` — viết bài PR chất lượng cao
- [ ] Mỗi action kèm: `action_type`, `target_url`, `suggested_change`, `evidence_url`, `confidence`
- [ ] Test action recommender trên 5 diagnosis → output 10–15 action

### Khôi
- [ ] Tạo **Action acceptance rate** metric (manual count)
- [ ] Document: 5 loại action là gì, khi nào dùng, template content cho mỗi loại
- [ ] Hỗ trợ Lý review action output (HITL: 10 actions)
- [ ] Phân tích: action nào được marketer duyệt nhiều nhất? Vì sao?

### Hải
- [ ] Action backlog UI: list task theo brand, theo status
- [ ] Action detail modal: hiển thị action + suggested change + evidence
- [ ] Nút Approve / Edit / Reject
- [ ] Task board (kanban đơn giản): To do / In progress / Done
- [ ] Alert khi có hallucination giá/ship severity cao

### Deliverable Tuần 3
- [ ] Action backlog có cấu trúc + workflow duyệt
- [ ] **≥ 10 actions** được marketer duyệt (chia đều 2 brand)
- [ ] Action acceptance rate ≥ 60%

---

## 📅 Tuần 4 — Closed-loop Re-measurement

> **Mục tiêu**: re-scan sau action + bootstrap CI + phân loại Improved/No evidence/Regressed.

### Đăng
- [ ] **Re-scan engine**: trigger từ Celery khi task.status = done
- [ ] Re-scan logic: lấy các prompt E-commerce liên quan → chạy 3 lần × 4 AI
- [ ] Lưu kết quả vào `post_scan_id` (FK từ tasks)
- [ ] **Bootstrap CI engine**: tính 95% CI cho pre/post difference
- [ ] Phân loại: `improved` (vượt noise floor 5–7%) / `no_evidence` / `regressed`
- [ ] Endpoint `GET /api/v1/evaluation/{task_id}` (trả về report)

### Lý
- [ ] Lưu pre-scan baseline cho task (tại thời điểm tạo task)
- [ ] Lưu post-scan sau re-scan
- [ ] Logic integrated: closed-loop workflow từ re-scan → CI → report
- [ ] Test với **3 task đã mock-complete** (từ Tuần 3)
- [ ] Giải thích logic cho Khôi (để viết report)

### Khôi
- [ ] **Bootstrap 95% CI implementation** (Python, dùng numpy hoặc scipy)
- [ ] Noise floor check: ≥ 5 điểm % mới tính là improved
- [ ] Eval reports cho 6 task (3 task × 2 brand)
- [ ] Phân tích: bao nhiêu % task phân loại đúng? (manual review)
- [ ] Document: phương pháp bootstrap + cách interpret CI

### Hải
- [ ] Evaluation report UI: pre/post chart + CI bar
- [ ] Hiển thị verdict: `Improved signal` (xanh) / `No clear evidence` (vàng) / `Regressed` (đỏ)
- [ ] Export PDF report (cho demo)
- [ ] Compare 2 brand: brand nào cải thiện nhiều hơn?

### Deliverable Tuần 4
- [ ] Evaluation report cho **6 task** (3 task × 2 brand)
- [ ] Closed-loop classification accuracy ≥ 75% (manual review)
- [ ] UI report work + export PDF

---

## 📅 Tuần 5 — Polish + Demo + Gửi doanh nghiệp

> **Mục tiêu**: demo mượt + báo cáo doanh nghiệp + slide pitch.

### Đăng
- [ ] Load test: 100 prompt × 3 lần × 4 AI = 1200 responses (xem cost + time)
- [ ] Cost optimization: chọn model phù hợp, cache Tavily responses
- [ ] Giám sát Prometheus + Grafana (latency, error rate, cost)
- [ ] Production deployment (Docker Compose trên VPS, hoặc Vercel + Railway)
- [ ] Tổng kết: `docs/final-report-backend.md`

### Lý
- [ ] Tinh chỉnh parser (edge cases: sarcasm E-commerce, brand name có dấu)
- [ ] Action recommender polish (template content chất lượng cao)
- [ ] Verify Tavily freshness cho critical claim (giá/ship thay đổi hàng giờ)
- [ ] Tổng kết: `docs/final-report-agent.md`

### Khôi
- [ ] Final eval: precision/recall, F1, false alert rate, cost per scan
- [ ] Stability Score trung bình: phải ≥ 0.7
- [ ] Closed-loop classification accuracy: ≥ 75%
- [ ] Tổng kết: `docs/final-report-data.md`
- [ ] Slides phần data + eval

### Hải
- [ ] Demo video 5–10 phút (case 2 brand E-commerce)
- [ ] Slides pitch 10–15 slide
- [ ] HUD của dashboard polish (màu sắc, typography)
- [ ] Tổng kết: `docs/final-report-frontend.md`

### Deliverable Tuần 5
- [ ] **Demo video** 5–10 phút (chạy được end-to-end)
- [ ] **Báo cáo đề xuất giải pháp** gửi 2 doanh nghiệp E-commerce
- [ ] **Slide pitch** 10–15 slide
- [ ] Final metrics: precision ≥ 85%, F1 ≥ 0.85, Stability avg ≥ 0.7, Closed-loop ≥ 75%, cost ≤ $0.30/scan

---

## 🎯 KPI tổng kết (5 tuần)

| Metric | Target | Đo ở đâu |
|--------|--------|----------|
| Mention extraction F1 | ≥ 0.85 | Gold dataset |
| Stability Score trung bình | ≥ 0.7 | Tất cả gap |
| Hallucination recall (giá/ship) | ≥ 80% trong 24h | Manual review 20 cases |
| Diagnosis evidence support rate | ≥ 70% | Manual review 20 diagnoses |
| Action acceptance rate | ≥ 60% | Đếm trên 10 actions/brand |
| Closed-loop classification accuracy | ≥ 75% | Manual review 6 reports |
| Cost per scan | ≤ $0.30 | API usage log |
| SOV top 3 (2 brand demo) | Đạt | Demo |

---

## 📝 Quy tắc update task

1. **Mỗi member tự update** task của mình trong file này (không cần đợi).
2. **Cuối ngày** (chủ nhật) — review tổng, note blocker trong `docs/weekly/week-N.md`.
3. **Format tick**: `[x]` xong, `[~]` đang làm, `[ ]` chưa, `[!]` bị blocker.
4. **Task mới phát sinh** → thêm vào cuối tuần tương ứng, ghi rõ owner.

---

## 🔗 Liên kết nhanh

- [x] Tuần 0 — Chuẩn bị (Đã xong?)
- [ ] Tuần 1 — Foundation
- [ ] Tuần 2 — Diagnosis & Evidence
- [ ] Tuần 3 — Action Plan
- [ ] Tuần 4 — Closed-loop
- [ ] Tuần 5 — Demo + Báo cáo
