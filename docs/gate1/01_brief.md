# 📋 BRIEF — GEO AI Agent cho E-commerce Việt Nam

> **Gate 1 Deliverable** · Ngày 02/08/2026
> **Nhóm:** Đăng (Tech Lead), Lý (Agent Engineer), Khôi (Data/NLP), Hải (Frontend/Infra)
> **Mã dự án:** P167-Puttugao

---

## 1. Tên dự án

**GEO AI Agent cho E-commerce Việt Nam** (tên kỹ thuật tạm: `VN-ECOM-GEO Agent`)

---

## 2. Bối cảnh & Vấn đề

### 2.1. Bối cảnh thị trường

- **78% người dùng internet Việt Nam đã tương tác với ít nhất 1 nền tảng AI, 1/3 dùng hàng ngày** ([Decision Lab, "Vietnam Consumer AI market 2025"](https://www.decisionlab.co/blog/vietnam-consumer-ai-market-2025-78-of-online-population-have-engaged-with-ai-one-third-turn-it-into-a-daily-habit)).
- Ngành TMĐT Việt Nam: doanh số bán lẻ trực tuyến đạt **~22 tỷ USD (2025)**; quy mô tổng thị trường TMĐT (theo VECOM) ước tính **~27–32 tỷ USD**, tăng trưởng **~20–27%/năm** ([Vietnam-Briefing, E-Commerce 2025](https://www.vietnam-briefing.com/news/vietnam-e-commerce-growth-key-findings-from-the-2025-e-business-index.html/)).
- Ngành điện máy/điện tử (ngành nhóm chọn demo — xem §5): giá thay đổi liên tục, cạnh tranh giá khốc liệt giữa sàn và D2C, khiến AI dễ trả lời sai giá/chính sách bảo hành hơn các ngành ổn định giá — hallucination risk cao và dễ đo lường tác động.

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

1. Liệt kê prompts → 2. Gửi đến 4 AI (mở 4 tab rời rạc) → 3. Đọc câu trả lời + check claim → 4. So sánh đối thủ → 5. Tổng hợp vào Excel → 6. Viết báo cáo + check hallucination thủ công → 7. Đề xuất action không có bằng chứng.

**Chi phí ước lượng: ~30–35 triệu VND/tháng** (nhân sự + công cụ + chi phí cơ hội mất traffic pre-purchase).

---

## 3. Giải pháp đề xuất

### 3.1. Tổng quan

Xây dựng **AI Agent** tự động hóa toàn bộ pipeline theo dõi AI Visibility cho shop/brand E-commerce VN, với **3 trụ cột phương pháp luận** có căn cứ học thuật:

| Trụ cột | Mô tả | Căn cứ |
|---------|-------|--------|
| **Stability-aware Monitoring** | Mỗi prompt chạy N lần (N=3 demo), tính Stability Score ≥ 0.7 mới đưa vào diagnosis | Schulte et al. [arXiv 2604.07585](https://arxiv.org/abs/2604.07585) |
| **Evidence-grounded Diagnosis** | Mỗi gap có citation URL + quote + cross-check giá/ship/uy tín với Tavily | Tian et al. [arXiv 2603.09296](https://arxiv.org/abs/2603.09296) |
| **Closed-loop Re-measurement** | Sau task done → re-scan + bootstrap 95% CI → phân loại Improved / No evidence / Regressed | [arXiv 2603.08924](https://arxiv.org/abs/2603.08924) |

### 3.2. Tính năng chính

**2 tính năng cốt lõi:**
1. **Stability-aware Visibility Monitoring** — Gửi prompt đến 4 AI (ChatGPT, Gemini, Claude, Tavily), chạy lặp 3 lần, tính Visibility Rate, mention position, SOV, Sentiment, Stability Score.
2. **Evidence-grounded Diagnosis & Action Plan** — Thu thập evidence (citation URL, Tavily cross-check giá/ship/uy tín với Shopee/Lazada), đề xuất 1-3 action có bằng chứng cho marketer.

**1 tính năng nâng cao:**
3. **Closed-loop Re-measurement** — Tự động re-scan sau khi task hoàn thành, so sánh pre/post với bootstrap 95% CI, phân loại `Improved signal` / `No clear evidence` / `Regressed`.

---

## 4. Đối tượng sử dụng

### 4.1. Primary User

**Marketing Manager / CMO / chủ shop** của SME E-commerce Việt Nam.

### 4.2. Persona

> *"Shop mình bán đồ điện máy trên Shopee được 3 năm. Mình thử hỏi ChatGPT: 'shop điện máy nào uy tín TPHCM' — không thấy shop mình, chỉ thấy đối thủ. Hỏi tiếp 'TV Samsung giá bao nhiêu' — AI trả lời sai giá. Mình không biết đây là do 1 lần hỏi ngẫu nhiên hay xảy ra hàng ngày, và không biết phải làm gì để AI bắt đầu nhắc đến shop mình. Mình sợ mỗi tháng đang mất traffic pre-purchase mà không hề hay biết."*

### 4.3. Quy mô doanh nghiệp

- 5–100 nhân viên.
- Doanh thu ~1–20 tỷ VND/năm.
- Đã có mặt trên Shopee/Lazada/Tiki hoặc D2C.

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
| **Brand demo** | 2 brand E-commerce (1 sàn + 1 D2C) + 6 đối thủ (3/brand) |
| **AI engines** | 4 nguồn: ChatGPT + Gemini + Claude + Tavily |
| **Prompt set** | ~100 prompt tiếng Việt, chia 5 nhóm (uy tín, giá, so sánh, review, ship) |
| **Lặp/prompt** | 3 lần/ngày (demo), 7-8 lần (production) |
| **Ngôn ngữ** | Tiếng Việt (chính) |
| **Tần suất scan** | 1 lần/ngày trong 4 tuần demo |
| **Stakeholder** | Gửi 2 SME E-commerce VN duyệt demo |

### Brand demo đã chọn

| Brand | Loại | Ngành hàng | Đối thủ trực tiếp |
|-------|------|-----------|---------|
| **Điện Máy Xanh** | Sàn (target) | Điện máy / điện tử gia dụng | Nguyễn Kim, PICO, FPT Shop |
| **Samsung Vietnam** | D2C (target) | Điện tử (điện thoại, TV, gia dụng) | CellphoneS, Apple Vietnam, Xiaomi Vietnam |

**Lý do chọn ngành điện tử:** GEO gap rõ giữa thực tế thị trường và AI visibility (Samsung VN được nhắc nhiều nhưng AI hay nói sai giá/policy VN); hallucination risk cao về giá/ship do giá điện tử biến động liên tục — lý tưởng để demo Core Feature #2 (Evidence-grounded Diagnosis); schema markup tốt trên các trang này → dễ demo Schema Audit; đủ 6 đối thủ cùng ngành → tính SOV có ý nghĩa thống kê.

---

## 6. KPI & Chỉ số thành công

| Metric | Baseline | Target MVP |
|--------|----------|------------|
| **Thời gian GEO monitoring** | 80h/tháng | <8h/tháng (giảm 90%) |
| **Prompt coverage** | 50/tháng | 100 × N lần × 2 brand |
| **Mention extraction F1** | — | ≥ 0.85 |
| **Stability Score (gate)** | Không đo | ≥ 0.7 |
| **Hallucination recall (giá/ship)** | Không đo | ≥ 80% trong 24h |
| **Diagnosis evidence support rate** | — | ≥ 70% |
| **Action acceptance rate** | — | ≥ 60% |
| **Closed-loop classification accuracy** | — | ≥ 75% phân loại đúng |
| **Cost per scan** | — | ≤ $0.30 |
| **SOV ngành hàng chính** | — | Top 3 cho 2 brand demo |

---

## 7. Đội ngũ & Phân công

| Member | Role | Phụ trách chính |
|--------|------|----------------|
| **Đăng** | Tech Lead (Backend) | FastAPI, PostgreSQL, scheduler, Closed-loop re-scan engine, eval |
| **Lý** | Agent Engineer | LiteLLM, Tavily tools, prompt runner, parser, diagnosis agent |
| **Khôi** | Data/NLP | Prompt library, gold dataset, stability analysis, bootstrap CI |
| **Hải** | Frontend/Infra | Next.js dashboard, HITL UI, chart, Docker, deployment |

---

## 8. Timeline tổng quan

| Tuần | Output chính |
|------|-------------|
| **Tuần 0** | API keys, brand profile (Điện Máy Xanh + Samsung + 6 đối thủ), prompt library ~100, gold dataset pilot |
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
| API key hết quota (4 AI) | Trung bình | Đăng ký sớm Tuần 0; fallback Playwright scrape |
| AI response không ổn định → nhiễu | Cao | Stability filter ≥ 0.7, chạy lặp ≥ 3 lần |
| Tavily cache cũ → cross-check sai giá | Trung bình | Scrape trực tiếp Shopee/Lazada cho claim critical |
| Hallucination giá/ship tolerance thấp | Trung bình | HITL chặt, alert trong 24h |
| Không tìm được SME duyệt demo | Trung bình | Liên hệ sớm Tuần 0; demo brand thật + disclaimer |
| Đối thủ quốc tế (Perplexity, Copilot) vào thị trường VN | Thấp | Focus tiếng Việt + giá rẻ + chuyên biệt E-commerce điện tử |

---

## 11. Định vị & Điểm khác biệt

> **Định vị một câu:** Công cụ theo dõi AI visibility cho shop/brand E-commerce Việt Nam trên ChatGPT, Gemini, Claude và Tavily — tập trung vào đo lặp có kiểm soát (Stability-aware), evidence-grounded diagnosis, và closed-loop re-measurement.

| Sản phẩm | Giá | Điểm mạnh | Khoảng trống |
|---|---|---|---|
| [Profound](https://www.tryprofound.com) (US) | $499/tháng | 10+ AI engine, SOC2, source-level citation intelligence | Đắt, không phù hợp SME |
| [Peec AI](https://peec.ai/) | €89–199/tháng | Depth-to-price tốt cho mid-market, self-serve analytics | Chưa đủ rẻ cho SME VN |
| [Otterly.AI](https://otterly.ai/) | $29/tháng | Rẻ nhất thị trường, GEO Audit chi tiết | Engine giới hạn ở gói thấp |
| Semrush/Ahrefs AI add-on | $139–199/tháng | Tận dụng SEO stack có sẵn | GEO chỉ là add-on, không sâu |
| [Kompa GEO](https://kompa.ai/giai-phap/kompa-geo) (VN) | Báo giá riêng | 4 AI, prompt discovery, đã có khách DN | Chưa công khai agent tự tạo task + closed-loop |

**3 điểm khác biệt:**
1. **Đo lặp + Stability Score** — Đối thủ chạy 1 lần; nhóm chạy N lần/prompt, tính Stability Score.
2. **Evidence-grounded Diagnosis** — Đối thủ chỉ "diagnose"; nhóm có citation URL + Tavily cross-check trực tiếp với Shopee/Lazada.
3. **Closed-loop Evaluation** — Chưa công cụ nào (kể cả Kompa) công khai re-scan + bootstrap CI sau action.

Giá mục tiêu **~$20–50/tháng** — rẻ hơn Semrush/Ahrefs 3–7×, phù hợp SME Việt Nam.

---

## 12. Budget dự kiến (5 tuần demo)

| Hạng mục | Chi phí |
|----------|---------|
| API calls (4 AI × 100 prompt × 3 lần × 30 ngày) | < 500.000 VND |
| Infrastructure (Docker, Vercel free tier) | 0 VND |
| **Tổng (demo 5 tuần)** | **< 500.000 VND** |

**Production scale:** < 4 triệu VND/tháng cho 2 brand × 4 AI.

---

## Phụ lục A — Câu pitch đề xuất

**Pitch 30 giây (mentor/thầy):**
> *"Chúng em xây dựng GEO AI Agent cho E-commerce Việt Nam — theo dõi AI visibility cho shop/brand trên ChatGPT, Gemini, Claude và Tavily (web-grounded). Tập trung vào đo lặp có kiểm soát (Stability-aware Monitoring, theo Schulte et al.), evidence-grounded diagnosis (Tavily cross-check giá/ship/uy tín + citation URL), và closed-loop evaluation (đo lại sau hành động bằng bootstrap CI). Phạm vi 5 tuần: 2 brand E-commerce demo (Điện Máy Xanh + Samsung Vietnam) + 6 đối thủ + ~100 prompt tiếng Việt chia 5 nhóm."*

**Pitch 1–2 phút (doanh nghiệp E-commerce):**
> *"Hiện nay nhiều công cụ GEO đã có mặt — Profound, Peec, Otterly ở nước ngoài, Kompa GEO ở Việt Nam. Nhưng các công cụ này thường gặp 3 hạn chế: (1) chạy prompt 1 lần rồi vẽ dashboard, trong khi nghiên cứu học thuật cho thấy AI không ổn định — cần đo lặp nhiều lần; (2) đề xuất hành động chung chung, thiếu bằng chứng; (3) không đo lại hiệu quả sau khi team thực hiện. Chúng tôi xây dựng công cụ tập trung vào đúng 3 điểm này: đo lặp có kiểm soát, evidence-grounded diagnosis với Tavily cross-check giá/ship/uy tín trực tiếp với Shopee/Lazada, và closed-loop evaluation với bootstrap CI. Trong 5 tuần, chúng tôi demo với 2 brand E-commerce: chạy ~100 prompt tiếng Việt trên 4 nguồn AI, tìm gap có bằng chứng, đề xuất action cụ thể, và đo lại hiệu quả sau khi thực hiện."*

## Phụ lục B — Kiểm tra trùng đề tài

Rà soát 360 đề tài AI20K theo từ khóa "GEO", "AI visibility", "AI mention", "E-commerce GEO", "Tavily" — không tìm thấy đề tài nào trực tiếp trùng lặp. Đề tài gần nhất chỉ liên quan gián tiếp (brand sentiment trên social media, web scraping tổng quát, recommendation E-commerce).

## Phụ lục C — Nguồn tham khảo

- Schulte, Bleeker & Kaufmann (2026), "Don't Measure Once: Measuring Visibility in AI Search (GEO)" — [arXiv 2604.07585](https://arxiv.org/abs/2604.07585)
- Sielinski (2026), "Quantifying Uncertainty in AI Visibility: A Statistical Framework for Generative Search Measurement" — [arXiv 2603.08924](https://arxiv.org/abs/2603.08924)
- Tian et al. (2026), "Diagnosing and Repairing Citation Failures in Generative Engine Optimization" — [arXiv 2603.09296](https://arxiv.org/abs/2603.09296)
- [Decision Lab — "Vietnam Consumer AI market 2025"](https://www.decisionlab.co/blog/vietnam-consumer-ai-market-2025-78-of-online-population-have-engaged-with-ai-one-third-turn-it-into-a-daily-habit)
- [Vietnam-Briefing — E-Commerce 2025 Highlights](https://www.vietnam-briefing.com/news/vietnam-e-commerce-growth-key-findings-from-the-2025-e-business-index.html/)
- Đối thủ tham khảo: [Profound](https://www.tryprofound.com), [Peec AI](https://peec.ai/), [Otterly.AI](https://otterly.ai/), [Kompa GEO](https://kompa.ai/giai-phap/kompa-geo)

---


