# 📄 PRD — Product Requirements Document
## GEO AI Agent cho E-commerce Việt Nam

> **Gate 1 Deliverable** · Ngày 02/08/2026
> **Nhóm:** Đăng, Lý, Khôi, Hải
> **Trạng thái:** Draft — chờ review Gate 1

---

## MỤC LỤC

1. [Tổng quan sản phẩm](#1-tổng-quan-sản-phẩm)
2. [Mục tiêu & Chỉ số thành công](#2-mục-tiêu--chỉ-số-thành-công)
3. [Đối tượng người dùng](#3-đối-tượng-người-dùng)
4. [User Stories](#4-user-stories)
5. [Yêu cầu chức năng (Functional Requirements)](#5-yêu-cầu-chức-năng)
6. [Yêu cầu phi chức năng (Non-functional Requirements)](#6-yêu-cầu-phi-chức-năng)
7. [Kiến trúc hệ thống](#7-kiến-trúc-hệ-thống)
8. [Data Model & Schema](#8-data-model--schema)
9. [API Specification](#9-api-specification)
10. [Prompt Library Design](#10-prompt-library-design)
11. [Phương pháp luận](#11-phương-pháp-luận)
12. [HITL Boundary](#12-hitl-boundary)
13. [Milestones & Timeline](#13-milestones--timeline)
14. [Dependencies & Risks](#14-dependencies--risks)
15. [Out of Scope](#15-out-of-scope)

---

## 1. Tổng quan sản phẩm

### 1.1. Product Vision

Xây dựng một **AI Agent Platform** giúp SME E-commerce Việt Nam **theo dõi, phân tích, và tối ưu hoá AI Visibility** của shop/brand trên 4 nền tảng AI (ChatGPT, Gemini, Claude, Tavily), với phương pháp luận có căn cứ học thuật và đo lường khép kín.

### 1.2. Product Name

**VN-ECOM-GEO Agent** (tên tạm, nhóm có thể đổi)

### 1.3. Vấn đề cần giải quyết

SME E-commerce Việt Nam đang phải đối mặt với 5 pain points chưa có công cụ giải quyết:

| # | Pain Point | Lý do cần giải |
|---|------------|---------------|
| 1 | Kết quả từ nhiều AI bị phân tán (ChatGPT, Gemini, Claude, Tavily chạy rời rạc) | Marketer không có dashboard gộp, phải mở 4 tab mỗi lần check |
| 2 | Các mô hình AI đưa ra đề xuất khác nhau cho cùng 1 prompt | Không biết đề xuất nào đáng tin, không có cơ chế đo độ ổn định |
| 3 | Đề xuất AI thiếu bối cảnh doanh nghiệp (ngành hàng, đối thủ, prompt đặc thù VN) | Tool quốc tế (Semrush, Ahrefs) dùng prompt pattern US/EU, không cover câu hỏi tiếng Việt |
| 4 | Nhiều đề xuất nhưng không biết làm gì trước | Không có priority ranking, không gắn với citation/bằng chứng |
| 5 | Khó đánh giá độ tin cậy của đề xuất AI | Không có stability score, không có evidence-grounded, không có closed-loop để verify |

Hệ quả: Marketing Manager dành **~80 giờ/tháng** thủ công theo dõi AI visibility cho 2 brand, với tỷ lệ sót mention 10-20% và sót hallucination giá/ship 20-30%. Không có công cụ nào chuyên biệt cho E-commerce VN ở mức giá phù hợp.

### 1.4. Giải pháp

AI Agent tự động hoá 90% pipeline, với:
- **Prompt runner** gửi 100 prompt × 3 lần × 4 AI
- **Parser LLM** trích xuất mention, sentiment, claim
- **Tavily cross-check** verify giá/ship/uy tín
- **Stability filter** chỉ đưa gap ổn định vào diagnosis
- **Action recommender** đề xuất hành động có bằng chứng
- **Closed-loop engine** đo lại hiệu quả với bootstrap CI
- **HITL UI** cho marketer duyệt/sửa/từ chối

---

## 2. Mục tiêu & Chỉ số thành công

### 2.1. Mục tiêu kinh doanh

| Mục tiêu | Đo lường |
|----------|---------|
| Giảm 90% thời gian monitoring | 80h → <8h/tháng |
| Tăng 10× prompt coverage | 50 → 500+ prompts/tháng |
| Phát hiện ≥ 80% hallucination trong 24h | Manual review 20 cases |
| Đo hiệu quả action với bootstrap CI | ≥ 75% phân loại đúng |

### 2.2. Chỉ số kỹ thuật (KPI)

| Metric | Target | Cách đo |
|--------|--------|---------|
| Mention extraction F1 | ≥ 0.85 | Gold dataset E-commerce 50-100 mẫu |
| Stability Score (gate) | ≥ 0.7 mỗi gap | Tính từ 3 lần chạy/prompt |
| Stability filter precision | False alert giảm ≥ 30% | So sánh với chạy 1 lần |
| Hallucination detection recall | ≥ 80% trong 24h | Manual review 20 cases |
| Diagnosis evidence support rate | ≥ 70% hypothesis có URL + quote | Manual review 20 diagnoses |
| Action acceptance rate | ≥ 60% | Đếm trên 10 actions/brand |
| Re-scan classification accuracy | ≥ 75% | Manual review 6 reports |
| Cost per scan | ≤ $0.30 | API usage log |

---

## 3. Đối tượng người dùng

### 3.1. Primary Persona: Marketing Manager E-commerce

| Thuộc tính | Giá trị |
|-----------|---------|
| **Vai trò** | Marketing Manager / CMO / Chủ shop |
| **Quy mô DN** | 5-100 nhân viên |
| **Doanh thu** | 1-20 tỷ VND/năm |
| **Platform** | Shopee, Lazada, Tiki hoặc D2C website |
| **Nhu cầu** | Biết AI nói gì về shop, đứng ở đâu so đối thủ, làm gì để tối ưu |
| **Đau đớn** | 80h/tháng thủ công, sót hallucination, không có closed-loop |

### 3.2. Secondary Persona: Shop Admin / Content Team

- Nhận task từ Marketing Manager
- Thực hiện action (sửa listing, viết content, đẩy review)
- Cần xem evidence package để hiểu bối cảnh

---

## 4. User Stories

### 4.1. Epic 1: Visibility Monitoring

| ID | User Story | Priority | Sprint |
|----|-----------|----------|--------|
| US-01 | Là Marketing Manager, tôi muốn xem **Visibility Rate** của shop mình trên 4 AI, để biết AI có nhắc đến shop không | P0 | Tuần 1 |
| US-02 | Là Marketing Manager, tôi muốn xem **SOV** (Share of Voice) so với đối thủ trong ngành hàng | P0 | Tuần 1 |
| US-03 | Là Marketing Manager, tôi muốn xem **Stability Score** của mỗi gap, để biết kết quả có đáng tin không | P0 | Tuần 1 |
| US-04 | Là Marketing Manager, tôi muốn **lọc theo brand, prompt group, AI engine** | P1 | Tuần 1 |
| US-05 | Là Marketing Manager, tôi muốn xem **trend visibility** theo thời gian | P1 | Tuần 1 |
| US-06 | Là Marketing Manager, tôi muốn **trigger scan thủ công** khi cần | P1 | Tuần 1 |

### 4.2. Epic 2: Diagnosis & Evidence

| ID | User Story | Priority | Sprint |
|----|-----------|----------|--------|
| US-07 | Là Marketing Manager, tôi muốn xem **danh sách gap** (prompt mà shop không được nhắc hoặc bị nói sai) đã qua Stability filter | P0 | Tuần 2 |
| US-08 | Là Marketing Manager, tôi muốn xem **evidence package**: citation URL + quote + Tavily cross-check | P0 | Tuần 2 |
| US-09 | Là Marketing Manager, tôi muốn biết **AI nói sai giá/ship** của sản phẩm (hallucination detection) | P0 | Tuần 2 |
| US-10 | Là Marketing Manager, tôi muốn **duyệt (approve) hoặc từ chối (reject)** diagnosis | P0 | Tuần 2 |
| US-11 | Là Marketing Manager, tôi muốn xem **3 câu trả lời khác nhau** (từ 3 lần chạy) cho cùng 1 prompt | P1 | Tuần 2 |

### 4.3. Epic 3: Action Plan & HITL

| ID | User Story | Priority | Sprint |
|----|-----------|----------|--------|
| US-12 | Là Marketing Manager, tôi muốn xem **đề xuất 1-3 action** cho mỗi gap (listing_update, content_add, schema_add, outreach, content_pr) | P0 | Tuần 3 |
| US-13 | Là Marketing Manager, tôi muốn **duyệt / sửa / từ chối** action | P0 | Tuần 3 |
| US-14 | Là Marketing Manager, tôi muốn xem **task board** (To do / In progress / Done) | P0 | Tuần 3 |
| US-15 | Là Marketing Manager, tôi muốn nhận **alert** khi phát hiện hallucination giá/ship nghiêm trọng | P1 | Tuần 3 |

### 4.4. Epic 4: Closed-loop Re-measurement

| ID | User Story | Priority | Sprint |
|----|-----------|----------|--------|
| US-16 | Là Marketing Manager, tôi muốn hệ thống **tự re-scan** sau khi tôi đánh dấu task "done" | P0 | Tuần 4 |
| US-17 | Là Marketing Manager, tôi muốn xem **evaluation report**: pre/post chart + bootstrap CI | P0 | Tuần 4 |
| US-18 | Là Marketing Manager, tôi muốn biết action nào **"Improved signal"**, **"No clear evidence"**, hoặc **"Regressed"** | P0 | Tuần 4 |
| US-19 | Là Marketing Manager, tôi muốn **so sánh 2 brand** để biết brand nào cải thiện nhiều hơn | P1 | Tuần 4 |
| US-20 | Là Marketing Manager, tôi muốn **export PDF report** để gửi CMO/chủ shop | P1 | Tuần 4 |

---

## 5. Yêu cầu chức năng (Functional Requirements)

### FR-01: Prompt Runner Engine

| ID | Requirement | Priority |
|----|------------|----------|
| FR-01.1 | Gửi prompt đến 4 AI engines (ChatGPT, Gemini, Claude, Tavily) | P0 |
| FR-01.2 | Mỗi prompt chạy lặp N lần (N=3 cho demo) | P0 |
| FR-01.3 | Lưu raw response + metadata (ai_engine, model_version, run_index, timestamp) | P0 |
| FR-01.4 | Retry + exponential backoff cho mỗi API call | P0 |
| FR-01.5 | LiteLLM routing: mapping ai_engine → model endpoint | P0 |
| FR-01.6 | Budget cap: ≤ $0.30/scan (30 prompt × 3 lần × 4 AI) | P1 |

### FR-02: Parser & Mention Extraction

| ID | Requirement | Priority |
|----|------------|----------|
| FR-02.1 | Trích xuất brand mention từ raw response (GPT-4o-mini) | P0 |
| FR-02.2 | Xác định: brand_name, position (1,2,3), sentiment (-1 to +1), context_quote, claim_type | P0 |
| FR-02.3 | Xử lý 3 biến thể tên: có dấu / không dấu / viết tắt ("Điện Máy Xanh" / "Dien May Xanh" / "DMX") | P0 |
| FR-02.4 | Thiên về recall (FN nguy hiểm hơn FP) | P0 |

### FR-03: Stability Score Computation

| ID | Requirement | Priority |
|----|------------|----------|
| FR-03.1 | Tính Stability Score = 1 - normalized variance (từ N lần chạy) | P0 |
| FR-03.2 | Gate: chỉ gap có Stability Score ≥ 0.7 mới vào diagnosis | P0 |
| FR-03.3 | Gap có Stability < 0.7 đánh dấu `observation_only` | P0 |
| FR-03.4 | Tính Visibility Rate (FLOAT 0-1) cho mỗi brand/prompt | P0 |

### FR-04: Diagnosis & Evidence

| ID | Requirement | Priority |
|----|------------|----------|
| FR-04.1 | `fetch_citations(response_id)` — lấy URL từ citations JSONB | P0 |
| FR-04.2 | `compare_with_brand_source(claim, brand_id)` — so sánh giá/ship/uy tín | P0 |
| FR-04.3 | `detect_content_gap(brand_id, topic)` — kiểm tra trang web có đủ info | P1 |
| FR-04.4 | `schema_check(url)` — kiểm tra schema.org Product/Offer/Review | P1 |
| FR-04.5 | Tavily cross-check workflow: claim → Tavily search → verify → evidence package | P0 |
| FR-04.6 | Evidence package output: `{url, quote_span, claim_type, confidence, verified_at}` | P0 |

### FR-05: Action Recommender

| ID | Requirement | Priority |
|----|------------|----------|
| FR-05.1 | Từ evidence package → đề xuất 1-3 action cụ thể | P0 |
| FR-05.2 | 5 loại action: `listing_update`, `content_add`, `schema_add`, `outreach`, `content_pr` | P0 |
| FR-05.3 | Mỗi action kèm: action_type, target_url, suggested_change, evidence_url, confidence | P0 |

### FR-06: HITL Approval Workflow

| ID | Requirement | Priority |
|----|------------|----------|
| FR-06.1 | Marketer có thể Approve / Reject diagnosis | P0 |
| FR-06.2 | Marketer có thể Approve / Edit / Reject action | P0 |
| FR-06.3 | Task board: Todo → In Progress → Done | P0 |
| FR-06.4 | Khi task → status=done → trigger re-scan (Celery queue) | P0 |

### FR-07: Closed-loop Re-measurement

| ID | Requirement | Priority |
|----|------------|----------|
| FR-07.1 | Khi task.status = done → re-scan prompt liên quan (3 lần × 4 AI) | P0 |
| FR-07.2 | Tính pre/post difference | P0 |
| FR-07.3 | Bootstrap 95% CI engine | P0 |
| FR-07.4 | Phân loại: `improved` (vượt noise floor 5-7%) / `no_evidence` / `regressed` | P0 |
| FR-07.5 | Evaluation report per task | P0 |

### FR-08: Dashboard & Visualization

| ID | Requirement | Priority |
|----|------------|----------|
| FR-08.1 | Danh sách brand + đối thủ | P0 |
| FR-08.2 | Biểu đồ visibility rate theo ngành hàng (Recharts) | P0 |
| FR-08.3 | Biểu đồ SOV per brand theo AI engine | P0 |
| FR-08.4 | Bảng chi tiết: prompt × AI engine × visibility + stability | P0 |
| FR-08.5 | Filter: theo brand, prompt group, AI engine | P1 |
| FR-08.6 | Diagnosis detail page: gap + evidence package | P0 |
| FR-08.7 | Evaluation report UI: pre/post chart + CI bar | P0 |
| FR-08.8 | Verdict display: Improved (xanh) / No evidence (vàng) / Regressed (đỏ) | P0 |
| FR-08.9 | Export PDF report | P1 |

---

## 6. Yêu cầu phi chức năng (Non-functional Requirements)

### NFR-01: Performance

| ID | Requirement |
|----|------------|
| NFR-01.1 | Dashboard load time < 3 giây |
| NFR-01.2 | Full scan (100 prompt × 3 lần × 4 AI) hoàn thành < 30 phút |
| NFR-01.3 | API response time < 500ms cho endpoint đọc |

### NFR-02: Cost

| ID | Requirement |
|----|------------|
| NFR-02.1 | Cost per scan ≤ $0.30 (30 prompt × 3 lần × 4 AI) |
| NFR-02.2 | Ưu tiên GPT-4o-mini / Claude Haiku cho parse & NER |
| NFR-02.3 | GPT-4o / Claude Sonnet chỉ cho sentiment & hallucination verify |
| NFR-02.4 | Tavily chỉ cho cross-check giá/ship, KHÔNG dùng để parse mention |

### NFR-03: Security

| ID | Requirement |
|----|------------|
| NFR-03.1 | Không commit .env chứa API key thật |
| NFR-03.2 | Mỗi folder có .env.example riêng |
| NFR-03.3 | API key lưu trong environment variables |

### NFR-04: Reliability

| ID | Requirement |
|----|------------|
| NFR-04.1 | Retry + exponential backoff cho API calls |
| NFR-04.2 | Graceful degradation khi 1 AI engine down |
| NFR-04.3 | Logging JSON format với trace_id |

### NFR-05: Scalability

| ID | Requirement |
|----|------------|
| NFR-05.1 | MVP: SQLite có thể dùng thay PostgreSQL |
| NFR-05.2 | Cấu trúc sẵn sàng scale lên nhiều brand |
| NFR-05.3 | Docker Compose cho deployment |

---

## 7. Kiến trúc hệ thống

### 7.1. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (Next.js 14)                    │
│  ┌──────────┐ ┌───────────┐ ┌──────────┐ ┌──────────────────┐  │
│  │Dashboard │ │Diagnosis  │ │Task Board│ │Evaluation Report │  │
│  │(Charts)  │ │Detail     │ │(HITL)    │ │(CI Bar)          │  │
│  └──────────┘ └───────────┘ └──────────┘ └──────────────────┘  │
└─────────────────────────┬───────────────────────────────────────┘
                          │ REST API
┌─────────────────────────┴───────────────────────────────────────┐
│                      BACKEND (FastAPI)                           │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────────┐   │
│  │API Router│ │Services  │ │Workers   │ │Celery Scheduler  │   │
│  │(REST)    │ │(Business)│ │(Async)   │ │(3×/ngày)         │   │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────────┘   │
└─────────────────────────┬───────────────────────────────────────┘
                          │
┌─────────────────────────┴───────────────────────────────────────┐
│                       AGENT LAYER                                │
│  ┌──────────────┐ ┌──────────────┐ ┌────────────────────────┐   │
│  │Prompt Runner │ │Parser LLM    │ │Diagnosis Agent         │   │
│  │(4 AI × N lần)│ │(GPT-4o-mini) │ │(Evidence + Tavily)     │   │
│  └──────────────┘ └──────────────┘ └────────────────────────┘   │
│  ┌──────────────┐ ┌──────────────┐ ┌────────────────────────┐   │
│  │Action Recom. │ │Tavily Tools  │ │Closed-loop Engine      │   │
│  │(LLM)         │ │(Cross-check) │ │(Re-scan + Bootstrap CI)│   │
│  └──────────────┘ └──────────────┘ └────────────────────────┘   │
└─────────────────────────┬───────────────────────────────────────┘
                          │
┌─────────────────────────┴───────────────────────────────────────┐
│                      DATA LAYER                                  │
│  ┌──────────────┐ ┌──────────────┐ ┌────────────────────────┐   │
│  │PostgreSQL 16 │ │Redis (cache) │ │Prompt Library (JSON)   │   │
│  │(5 bảng chính)│ │              │ │Gold Dataset            │   │
│  └──────────────┘ └──────────────┘ └────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────┴───────────────────────────────────────┐
│                    EXTERNAL AI APIs                              │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐                   │
│  │ChatGPT │ │Gemini  │ │Claude  │ │Tavily  │                   │
│  │(OpenAI)│ │(Google)│ │(Anthro)│ │(Web)   │                   │
│  └────────┘ └────────┘ └────────┘ └────────┘                   │
└─────────────────────────────────────────────────────────────────┘
```

### 7.2. Data Flow

```
Prompt Library → Prompt Runner → 4 AI APIs → Raw Responses (DB)
                                                    │
                                             Parser LLM
                                                    │
                                            Mentions (DB)
                                                    │
                                        Stability Score (DB)
                                                    │
                                    ┌───────────────┴───────────┐
                                    │ Stability ≥ 0.7?          │
                                    │  YES → Diagnosis          │
                                    │  NO  → observation_only   │
                                    └───────────┬───────────────┘
                                                │
                                        Tavily Cross-check
                                                │
                                        Evidence Package
                                                │
                                        Action Recommender
                                                │
                                        HITL Approval (UI)
                                                │
                                        Task Board (DB)
                                                │
                                    ┌───────────┴───────────┐
                                    │ Task status = done?    │
                                    │  YES → Re-scan         │
                                    │  NO  → wait            │
                                    └───────────┬────────────┘
                                                │
                                        Bootstrap 95% CI
                                                │
                                    Improved / No evidence / Regressed
```

---

## 8. Data Model & Schema

### 8.1. Database Schema (PostgreSQL)

#### Bảng `responses` — Raw AI response

| Cột | Type | Mô tả |
|-----|------|-------|
| id | SERIAL PK | Auto-increment |
| scan_id | INT | FK scan session |
| prompt_id | INT | FK prompt |
| brand_id | INT | FK brand |
| ai_engine | TEXT | `chatgpt` / `gemini` / `claude` / `tavily` |
| raw_text | TEXT | Toàn bộ câu trả lời AI |
| citations | JSONB | `[{url, title, snippet}]` |
| model_version | TEXT | Vd: `gpt-4o-mini-2024-07-18` |
| run_index | INT | 1, 2, 3 (cho Stability) |
| created_at | TIMESTAMP | Thời điểm response |

#### Bảng `mentions` — Extracted mention

| Cột | Type | Mô tả |
|-----|------|-------|
| id | SERIAL PK | Auto-increment |
| response_id | INT FK | FK → responses |
| brand_name | TEXT | Tên brand được nhắc |
| is_target_brand | BOOLEAN | Có phải brand mục tiêu |
| position | INT | Vị trí mention (1, 2, 3...) |
| sentiment | FLOAT | -1 to +1 |
| context_quote | TEXT | Đoạn trích dẫn |
| claim_type | TEXT | `price` / `ship` / `review` / `general` |

#### Bảng `stability_scores` — Stability per prompt

| Cột | Type | Mô tả |
|-----|------|-------|
| id | SERIAL PK | Auto-increment |
| brand_id | INT | FK brand |
| prompt_id | INT | FK prompt |
| stability_score | FLOAT | 1 - normalized variance |
| visibility_rate | FLOAT | 0-1 |
| is_stable | BOOLEAN | TRUE if score ≥ 0.7 |
| computed_at | TIMESTAMP | Thời điểm tính |

#### Bảng `diagnoses` — Diagnosis output

| Cột | Type | Mô tả |
|-----|------|-------|
| id | SERIAL PK | Auto-increment |
| brand_id | INT | FK brand |
| prompt_id | INT | FK prompt |
| is_stable | BOOLEAN | Stability check |
| stability_score | FLOAT | Score tham chiếu |
| hypotheses | JSONB | `[{hypothesis, confidence, evidence_urls}]` |
| recommended_actions | JSONB | Action list |
| status | TEXT | `pending_review` / `approved` / `rejected` |
| reviewed_by | TEXT | Người duyệt |
| reviewed_at | TIMESTAMP | Thời điểm duyệt |

#### Bảng `tasks` — Task tracking

| Cột | Type | Mô tả |
|-----|------|-------|
| id | SERIAL PK | Auto-increment |
| brand_id | INT | FK brand |
| diagnosis_id | INT FK | FK → diagnoses |
| action_type | TEXT | `listing_update` / `schema_add` / `outreach` / `content_pr` / `content_add` |
| owner_team | TEXT | Team phụ trách |
| status | TEXT | `todo` / `in_progress` / `done` |
| pre_scan_id | INT | Baseline scan reference |
| post_scan_id | INT | Re-scan reference |
| result | TEXT | `improved` / `no_evidence` / `regressed` |
| ci_lower | FLOAT | Bootstrap CI lower bound |
| ci_upper | FLOAT | Bootstrap CI upper bound |

### 8.2. Quy ước tên biến

| Biến | Type | Range | Mô tả |
|------|------|-------|-------|
| `visibility_rate` | FLOAT | 0-1 | Tỷ lệ prompt mà brand được nhắc |
| `stability_score` | FLOAT | 0-1 | 1 - normalized variance, gate ≥ 0.7 |
| `mention_position` | INT | 1, 2, 3... | Vị trí mention trong câu trả lời |
| `sentiment` | FLOAT | -1 to +1 | Cảm xúc |
| `claim_type` | ENUM | `price`, `ship`, `review`, `general` | Loại claim |
| `ai_engine` | ENUM | `chatgpt`, `gemini`, `claude`, `tavily` | Nguồn AI |
| `task_result` | ENUM | `improved`, `no_evidence`, `regressed` | Kết quả re-measurement |

---

## 9. API Specification

### 9.1. Scan APIs

| Method | Endpoint | Mô tả | Sprint |
|--------|----------|-------|--------|
| POST | `/api/v1/scan/` | Trigger manual scan | Tuần 1 |
| GET | `/api/v1/visibility/{brand_id}` | Trả về Visibility Rate, SOV | Tuần 1 |

### 9.2. Diagnosis APIs

| Method | Endpoint | Mô tả | Sprint |
|--------|----------|-------|--------|
| GET | `/api/v1/diagnoses/` | Liệt kê gap qua Stability filter | Tuần 2 |
| POST | `/api/v1/diagnoses/{id}/approve` | HITL approve | Tuần 2 |
| POST | `/api/v1/diagnoses/{id}/reject` | HITL reject | Tuần 2 |

### 9.3. Task APIs

| Method | Endpoint | Mô tả | Sprint |
|--------|----------|-------|--------|
| POST | `/api/v1/tasks/` | Tạo task từ diagnosis | Tuần 3 |
| PATCH | `/api/v1/tasks/{id}` | Update status | Tuần 3 |
| GET | `/api/v1/tasks/` | List tasks (filter brand_id, status) | Tuần 3 |

### 9.4. Evaluation APIs

| Method | Endpoint | Mô tả | Sprint |
|--------|----------|-------|--------|
| GET | `/api/v1/evaluation/{task_id}` | Evaluation report (pre/post + CI) | Tuần 4 |

---

## 10. Prompt Library Design

### 10.1. Cấu trúc

~100 prompt tiếng Việt, chia 5 nhóm:

| Nhóm | Số lượng | Ví dụ |
|------|----------|-------|
| **Uy tín** | 20 prompt | "shop điện máy nào uy tín TPHCM?" |
| **Giá** | 20 prompt | "TV Samsung giá bao nhiêu?" |
| **So sánh** | 20 prompt | "so sánh Điện Máy Xanh vs FPT Shop?" |
| **Review** | 20 prompt | "review Samsung Galaxy có tốt không?" |
| **Ship/Dịch vụ** | 20 prompt | "Điện Máy Xanh ship có nhanh không?" |

### 10.2. Format (JSON)

```json
{
  "id": "uy_tin_001",
  "text": "Mua tivi ở đâu chính hãng, uy tín?",
  "group": "uy_tin",
  "language": "vi",
  "tags": ["tivi", "chính hãng", "uy_tín"],
  "difficulty": "easy",
  "expected_mentions": ["Điện Máy Xanh", "Samsung", "Nguyễn Kim"],
  "applies_to_brands": [1, 2]
}
```

### 10.3. Biến thể tên brand

Mỗi brand phải xử lý 3+ biến thể (theo `data/brands/*.json`):
- **Điện Máy Xanh**: `"Điện Máy Xanh"`, `"Dien May Xanh"`, `"DMX"`, `"ĐMX"`, `"dienmayxanh"`
- **Samsung Vietnam**: `"Samsung"`, `"Samsung Vietnam"`, `"Samsung VN"`, `"samsungvietnam"`, `"SAMSUNG"`

---

## 11. Phương pháp luận

### 11.1. Stability-aware Monitoring

**Căn cứ:** Schulte et al. [arXiv 2604.07585](https://arxiv.org/abs/2604.07585)

- GEO là **stochastic, partially observable pipeline**
- Cùng prompt, cùng model → kết quả khác nhau giữa các lần chạy
- Cần ≥ 7-8 lần chạy/prompt/ngày cho standard error < 0.10
- **MVP:** N=3 lần chạy, Stability Score = 1 - normalized variance
- **Gate:** Score ≥ 0.7 mới đưa vào diagnosis

### 11.2. Evidence-grounded Diagnosis

**Căn cứ:** Tian et al. [arXiv 2603.09296](https://arxiv.org/abs/2603.09296)

- Diagnose-and-repair system (AgentGEO) cải thiện >40% citation rate với chỉ 5% sửa nội dung
- Mỗi gap cần evidence package: URL + quote_span + claim_type + confidence + verified_at
- Tavily cross-check giá/ship với source thực (Shopee, Lazada, web shop)

### 11.3. Closed-loop Re-measurement

**Căn cứ:** [arXiv 2603.08924](https://arxiv.org/abs/2603.08924)

- Citation share có noise floor 5-7 điểm %
- Bootstrap 95% CI bắt buộc khi báo cáo hiệu quả action
- **Phân loại:**
  - `Improved signal`: difference vượt noise floor 5-7%
  - `No clear evidence`: CI overlap với 0
  - `Regressed`: giảm có ý nghĩa thống kê

---

## 12. HITL Boundary

| Tác vụ | Tự động | HITL | Lý do |
|--------|---------|------|-------|
| Gửi prompt | ✅ | | Không rủi ro |
| Parse câu trả lời | ✅ | | Có thể re-run |
| Đếm mention | ✅ | | Có thể sửa |
| Cross-check giá/ship (Tavily) | ✅ | | Có thể verify |
| Phân tích sentiment | | ✅ | Sarcasm E-commerce |
| Verify hallucination giá/ship | | ✅ | Tolerance rất thấp |
| Duyệt diagnosis | | ✅ | Quyết định kinh doanh |
| Duyệt action plan | | ✅ | Marketer quyết cuối |
| Đánh dấu task done | | ✅ | Cần xác nhận con người |
| Re-scan | ✅ | | Tự động trigger |
| Bootstrap CI computation | ✅ | | Thuần toán |

---

## 13. Milestones & Timeline

| Milestone | Tuần | Deliverable | Acceptance Criteria |
|-----------|------|------------|---------------------|
| **M0: Setup** | 0 | API keys, brand profile, prompt library, gold dataset | 4 API live, 100 prompts, 50 gold samples |
| **M1: Baseline** | 1 | Dashboard + Stability Score | ≥600 responses, dashboard chạy, Stability tính được |
| **M2: Diagnosis** | 2 | 5 evidence packages | F1 ≥ 0.85, Tavily cross-check work |
| **M3: Action** | 3 | Action backlog + HITL UI | ≥10 actions duyệt, acceptance ≥ 60% |
| **M4: Closed-loop** | 4 | 6 evaluation reports | Classification accuracy ≥ 75% |
| **M5: Demo** | 5 | Video + báo cáo doanh nghiệp | End-to-end demo 5-10 phút |

---

## 14. Dependencies & Risks

### 14.1. External Dependencies

| Dependency | Risk | Mitigation |
|-----------|------|-----------|
| OpenAI API | Quota, latency | Backup: GPT-4o-mini |
| Anthropic API | Quota | Backup: Claude Haiku |
| Google AI Studio | Quota | Free tier |
| Tavily API | Cache cũ, tiếng Việt | Playwright fallback |
| Shopee/Lazada data | Anti-scrape | Public API + Tavily |

### 14.2. Internal Dependencies

| Dependency | From → To | Sprint |
|-----------|-----------|--------|
| DB Schema ready | Backend → All | Tuần 0 |
| Prompt Library ready | Data → Agent | Tuần 0 |
| Prompt Runner ready | Agent → Backend | Tuần 1 |
| API Endpoints ready | Backend → Frontend | Tuần 1 |
| Parser output → Stability | Agent → Data | Tuần 1 |
| Stability → Diagnosis | Data → Agent | Tuần 2 |
| Diagnosis → Action | Agent → Backend | Tuần 3 |
| Task done → Re-scan | Backend → Agent | Tuần 4 |

---

## 15. Out of Scope (MVP 5 tuần)

| Feature | Lý do out of scope |
|---------|-------------------|
| Hỗ trợ > 2 brand | Giới hạn thời gian + budget |
| Multi-language (Anh, Hàn, Nhật) | Focus tiếng Việt |
| Real-time monitoring (cron < 1 ngày) | Cost optimization |
| Mobile app | Web dashboard đủ cho MVP |
| SSO / team management | Single-user cho demo |
| Vector DB (Qdrant) search | Nâng cao, chưa cần cho MVP |
| LangGraph complex orchestration | LiteLLM đủ cho MVP |
| A/B testing actions | Cần > 5 tuần data |
| Perplexity / Copilot engines | 4 engines đủ cho demo |
| Auto-execute actions | HITL bắt buộc |

---

> 📌 **Ghi chú:** PRD này là living document, sẽ được cập nhật theo tiến độ mỗi tuần. Mọi thay đổi schema phải có ADR trong `docs/decisions/`.
