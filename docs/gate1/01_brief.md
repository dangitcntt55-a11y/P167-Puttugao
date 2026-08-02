# 📋 BRIEF — GEO AI Agent cho E-commerce Việt Nam

> **Gate 1 Deliverable** · Phiên bản 1.0 · Ngày 02/08/2026
> **Nhóm:** Đăng (Tech Lead), Lý (Agent Engineer), Khôi (Data/NLP), Hải (Frontend/Infra)
> **Mã dự án:** P167-Puttugao

---

## 1. Tên dự án

**VN-ECOM-GEO Agent** — Công cụ AI Agent theo dõi AI Visibility cho Shop/Brand E-commerce Việt Nam

---

## 2. Bối cảnh & Vấn đề

### 2.1. Bối cảnh thị trường

- **78% người dùng internet Việt Nam** đã sử dụng ít nhất 1 nền tảng AI trong 3 tháng gần nhất (Decision Lab, 2025).
- **36% người dùng khám phá brand mới qua ChatGPT**, 30% tin tưởng khuyến nghị từ AI.
- **21,5 triệu lượt AI referral traffic** tại Việt Nam (SimilarWeb, 07/2025), tăng **740% YoY**.
- Ngành **TMĐT Việt Nam đạt ~22 tỷ USD** năm 2025, tăng trưởng 20%+ YoY. SME E-commerce chiếm ~70% gian hàng trên Shopee, Lazada, Tiki.

### 2.2. Vấn đề cốt lõi

> **SME E-commerce Việt Nam hoàn toàn "mù" trước kênh AI**: không biết AI đang nói gì về shop/brand mình, không biết đứng ở đâu so với đối thủ, và không biết phải làm gì để được AI "chọn" trong các câu trả lời về mua sắm.

**5 pain points cụ thể:**

| # | Pain Point | Tác động |
|---|-----------|----------|
| 1 | Kết quả từ nhiều AI bị phân tán (ChatGPT, Gemini, Claude, Tavily chạy rời rạc) | Marketer không có dashboard gộp, phải mở 4 tab mỗi lần check |
| 2 | Các mô hình AI đưa ra đề xuất khác nhau cho cùng 1 prompt | Không biết đề xuất nào đáng tin, không có cơ chế đo độ ổn định |
| 3 | Đề xuất AI thiếu bối cảnh doanh nghiệp (ngành hàng, đối thủ, prompt đặc thù VN) | Tool quốc tế (Semrush, Ahrefs) dùng prompt pattern US/EU, không cover câu hỏi tiếng Việt |
| 4 | Nhiều đề xuất nhưng không biết làm gì trước | Không có priority ranking, không gắn với citation/bằng chứng |
| 5 | Khó đánh giá độ tin cậy của đề xuất AI | Không có stability score, không có evidence-grounded, không có closed-loop để verify |

### 2.3. Quy trình hiện tại (thủ công)

Marketing Manager phải thực hiện 7 bước thủ công, tốn **~80 giờ/tháng** chỉ để theo dõi AI visibility cho 2 brand E-commerce:

1. Liệt kê prompts → 2. Gửi đến 4 AI (mở 4 tab rời rạc) → 3. Đọc câu trả lời + check claim → 4. So sánh đối thủ → 5. Tổng hợp vào Excel → 6. Viết báo cáo + check hallucination thủ công → 7. Đề xuất action không có bằng chứng

**Chi phí ước lượng: ~30-35 triệu VND/tháng** (nhân sự + công cụ + chi phí cơ hội).

---

## 3. Giải pháp đề xuất

### 3.1. Tổng quan

Xây dựng **AI Agent** tự động hóa toàn bộ pipeline theo dõi AI Visibility cho shop/brand E-commerce VN, với **3 trụ cột phương pháp luận** có căn cứ học thuật:

| Trụ cột | Mô tả | Căn cứ |
|---------|-------|--------|
| **Stability-aware Monitoring** | Mỗi prompt chạy N lần (N=3 demo), tính Stability Score ≥ 0.7 mới đưa vào diagnosis | Schulte et al. arXiv 2604.07585 |
| **Evidence-grounded Diagnosis** | Mỗi gap có citation URL + quote + cross-check giá/ship/uy tín với Tavily | Tian et al. arXiv 2603.09296 |
| **Closed-loop Re-measurement** | Sau task done → re-scan + bootstrap 95% CI → phân loại Improved / No evidence / Regressed | arXiv 2603.08924 |

### 3.2. Tính năng chính

**2 Tính năng cốt lõi:**
1. **Stability-aware Visibility Monitoring**: Gửi prompt đến 4 AI (ChatGPT, Gemini, Claude, Tavily), chạy lặp 3 lần, tính Visibility Rate, SOV, Sentiment, Stability Score.
2. **Evidence-grounded Diagnosis & Action Plan**: Thu thập evidence (citation URL, Tavily cross-check giá/ship), đề xuất action có bằng chứng cho marketer E-commerce.

**1 Tính năng nâng cao:**
3. **Closed-loop Re-measurement**: Tự động re-scan sau khi task hoàn thành, so sánh pre/post với bootstrap 95% CI.

---

## 4. Đối tượng sử dụng

### 4.1. Primary User

**Marketing Manager / CMO / Chủ shop** của SME E-commerce Việt Nam.

### 4.2. Persona

> *"Shop mình bán đồ gia dụng trên Shopee 3 năm, doanh thu 5 tỷ/năm. Mở ChatGPT hỏi thử 'shop bán đồ gia dụng uy tín TPHCM' — không thấy shop mình, nhưng thấy 4 đối thủ. Mình sợ mỗi tháng đang mất 20-30% traffic pre-purchase mà không biết."*

### 4.3. Quy mô doanh nghiệp

- 5-100 nhân viên
- Doanh thu ~1-20 tỷ VND/năm
- Đã có mặt trên Shopee/Lazada/Tiki hoặc D2C

### 4.4. Phân khúc mục tiêu

| Phân khúc | Mô tả |
|-----------|-------|
| **Sàn TMĐT** | Shop bán đa ngành hàng trên Shopee/Lazada/Tiki |
| **D2C Brand** | Brand có website riêng, content-driven |
| **Retailer chuyển đổi số** | Chuỗi cửa hàng truyền thống đẩy online |

---

## 5. Phạm vi MVP (5 tuần)

| Yếu tố | Phạm vi |
|---------|---------|
| **Brand demo** | 2 brand E-commerce (1 sàn + 1 D2C) + 2-3 đối thủ/brand |
| **AI engines** | 4 nguồn: ChatGPT + Gemini + Claude + Tavily |
| **Prompt set** | ~100 prompt tiếng Việt, chia 5 nhóm (uy tín, giá, so sánh, review, ship) |
| **Lặp/prompt** | 3 lần/ngày (demo), 7-8 lần (production) |
| **Ngôn ngữ** | Tiếng Việt (chính) |
| **Tần suất scan** | 1 lần/ngày trong 4 tuần demo |
| **Stakeholder** | Gửi 2 SME E-commerce VN duyệt demo |

### Brand demo đã chọn

| Brand | Loại | Ngành hàng | Đối thủ |
|-------|------|-----------|---------|
| **Minh Long** | D2C (target) | Đồ gia dụng | Sunhouse, Kangaroo, Philips, Tefal |
| **Lock&Lock** | D2C (benchmark) | Đồ gia dụng | (cùng nhóm đối thủ) |

---

## 6. KPI & Chỉ số thành công

| Metric | Baseline | Target MVP |
|--------|----------|------------|
| **Thời gian GEO monitoring** | 80h/tháng | <8h/tháng (giảm 90%) |
| **Prompt coverage** | 50/tháng | 100 × N lần × 2 brand |
| **Mention extraction F1** | — | ≥ 0.85 |
| **Stability Score (gate)** | Không đo | ≥ 0.7 |
| **Hallucination recall (giá/ship)** | Không đo | ≥ 80% trong 24h |
| **Action acceptance rate** | — | ≥ 60% |
| **Closed-loop classification** | — | ≥ 75% phân loại đúng |
| **Cost per scan** | — | ≤ $0.30 |

---

## 7. Đội ngũ & Phân công

| Member | Role | Phụ trách chính |
|--------|------|----------------|
| **Đăng** | Tech Lead (Backend) | FastAPI, PostgreSQL, scheduler, Closed-loop engine |
| **Lý** | Agent Engineer | LiteLLM, Tavily tools, prompt runner, parser, diagnosis agent |
| **Khôi** | Data/NLP | Prompt library, gold dataset, stability analysis, bootstrap CI |
| **Hải** | Frontend/Infra | Next.js dashboard, HITL UI, chart, Docker, deployment |

---

## 8. Timeline tổng quan

| Tuần | Output chính |
|------|-------------|
| **Tuần 0** | API keys, brand profile, prompt library ~100, gold dataset 50-100 mẫu |
| **Tuần 1** | Baseline scan + dashboard + Stability Score |
| **Tuần 2** | Diagnosis output cho 5 gap (evidence package) |
| **Tuần 3** | Action backlog + HITL UI |
| **Tuần 4** | Closed-loop evaluation report (6 reports) |
| **Tuần 5** | Demo video + báo cáo cho 2 doanh nghiệp |

---

## 9. Tech Stack

| Layer | Công nghệ |
|-------|-----------|
| Frontend | Next.js 14, Tailwind CSS, Recharts |
| Backend | FastAPI (Python 3.11), Celery |
| Database | PostgreSQL 16, Redis, Qdrant |
| LLM Orchestration | LiteLLM, LangGraph |
| AI APIs | OpenAI, Anthropic, Google AI Studio, Tavily |
| Deployment | Docker Compose, Vercel |

---

## 10. Rủi ro chính & Giảm thiểu

| Rủi ro | Xác suất | Giảm thiểu |
|--------|----------|------------|
| API key hết quota | Trung bình | Đăng ký sớm Tuần 0; fallback Playwright |
| AI response không ổn định | Cao | Stability filter ≥ 0.7 |
| Tavily cache cũ → sai giá | Trung bình | Scrape trực tiếp Shopee/Lazada |
| Hallucination giá/ship | Trung bình | HITL chặt, alert 24h |
| Không tìm được SME duyệt | Trung bình | Liên hệ sớm Tuần 0 |

---

## 11. Định vị & Điểm khác biệt

> **Định vị một câu:** Công cụ theo dõi AI visibility cho shop/brand E-commerce Việt Nam trên ChatGPT, Gemini, Claude và Tavily — tập trung vào đo lặp có kiểm soát (Stability-aware), evidence-grounded diagnosis, và closed-loop re-measurement.

**3 điểm khác biệt so với đối thủ (Profound, Peec, Otterly, Kompa):**

1. **Đo lặp + Stability Score** — Đối thủ chạy 1 lần; nhóm chạy N lần/prompt, tính Stability Score.
2. **Evidence-grounded Diagnosis** — Đối thủ chỉ "diagnose"; nhóm có citation URL + Tavily cross-check.
3. **Closed-loop Evaluation** — Chưa công cụ nào re-scan + bootstrap CI sau action.

---

## 12. Budget dự kiến (5 tuần demo)

| Hạng mục | Chi phí |
|----------|---------|
| API calls (4 AI × 100 prompt × 3 lần × 30 ngày) | < 500.000 VND |
| Infrastructure (Docker, Vercel free tier) | 0 VND |
| **Tổng** | **< 500.000 VND** |

**Production scale:** < 4 triệu VND/tháng cho 2 brand × 4 AI.

---

> 📌 **Phê duyệt Brief**: Tài liệu này cần được toàn bộ nhóm review và đồng ý trước khi chuyển sang phase tiếp theo.
