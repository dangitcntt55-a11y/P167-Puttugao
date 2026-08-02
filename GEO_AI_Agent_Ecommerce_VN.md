# 🛒 GEO AI AGENT CHO E-COMMERCE VIỆT NAM
## Stability-aware Visibility Monitoring + Evidence-grounded Diagnosis + Closed-loop Re-measurement

> **Phiên bản:** 1.0 — Ngày 02/08/2026
> **Nhóm:** Đăng, Lý, Khôi, Hải
> **Trạng thái:** Đã chốt scope với mentor + thầy, sẵn sàng thực hiện 5 tuần
> **Đối tượng sử dụng tài liệu:** Nhóm nội bộ (tham chiếu hàng ngày trong 5 tuần phát triển)

---

## 📖 HƯỚNG DẪN SỬ DỤNG FILE

Tài liệu này là sự **gộp** của 2 file trước đó:
- `DeXuat_GEO_AI_Agent.md` (985 dòng) — phần "tại sao" + justification
- `BaoCao_HuongDi_GEO_VN_5Tuan.md` (776 dòng) — phần "làm gì" + "làm như thế nào"

**File được chia thành 3 PART logic:**

| PART | Mục đích | Nguồn chính | Khi nào đọc |
|------|---------|-------------|-------------|
| **PART 1 — WHY** | Tại sao đề tài này hợp lý? Căn cứ stakeholder, anti-patterns | DeXuat | Member mới onboard, khi cần defend trước câu hỏi "tại sao?" |
| **PART 2 — WHAT** | Làm gì? Scope, tính năng, học thuật, thị trường | Gộp cả 2 | Khi cần biết "feature X là gì, tại sao cần" |
| **PART 3 — HOW** | Làm như thế nào? Kiến trúc, timeline, KPI, rủi ro | Baocao | Khi code, khi planning sprint, khi demo |

**Quy ước đánh dấu:**
- `[Ước lượng]` = con số cần verify thêm
- `[Nguồn: X]` = nguồn dữ liệu công khai
- `🟢` = đã thống nhất với nhóm
- `🟡` = cần verify thêm
- `🔴` = rủi ro cao, cần HITL

---

## MỤC LỤC TỔNG

### PART 1 — TẠI SAO (WHY)
1. [Bối cảnh & lý do đề xuất](#1-bối-cảnh--lý-do-đề-xuất)
   - 1.1. Đặt vấn đề bằng dữ liệu
   - 1.2. Vấn đề của SME E-commerce VN
   - 1.3. Tại sao là "GEO Agent cho E-commerce"
2. [Lộ trình 5 bước chọn giải pháp AI](#2-lộ-trình-5-bước-chọn-giải-pháp-ai)
3. [Tìm bài toán AI ở đâu (4 lăng kính)](#3-tìm-bài-toán-ai-ở-đâu-4-lăng-kính)
4. [5 câu hỏi stakeholder](#4-5-câu-hỏi-stakeholder)
5. [Anti-patterns cần tránh](#5-anti-patterns-cần-tránh)
6. [Quick Problem Card](#6-quick-problem-card)

### PART 2 — LÀM GÌ (WHAT)
7. [Thị trường GEO 2026](#7-thị-trường-geo-2026)
   - 7.1. Phân khúc sản phẩm quốc tế
   - 7.2. Phân khúc Việt Nam
   - 7.3. Khoảng trống nhóm nhắm
8. [Căn cứ học thuật](#8-căn-cứ-học-thuật)
9. [Đề xuất hướng đi](#9-đề-xuất-hướng-đi)
   - 9.1. 2 tính năng cốt lõi
   - 9.2. 1 tính năng nâng cao (Closed-loop)
   - 9.3. Phạm vi MVP 5 tuần
   - 9.4. Đối tượng sử dụng E-commerce
10. [Khai thác bài toán chi tiết](#10-khai-thác-bài-toán-chi-tiết)
11. [Định lượng hóa bài toán](#11-định-lượng-hóa-bài-toán)
12. [Thiết lập chỉ số Output vs Input](#12-thiết-lập-chỉ-số-output-vs-input)
13. [Ba bước quyết định AI theo PAIR](#13-ba-bước-quyết-định-ai-theo-pair)
14. [Khi nào AI có/không có lợi thế](#14-khi-nào-ai-cókhông-có-lợi-thế)
15. [Thang câu hỏi lựa chọn cấp độ giải pháp](#15-thang-câu-hỏi-lựa-chọn-cấp-độ-giải-pháp)
16. [Reward function](#16-reward-function)
17. [So sánh với 360 đề tài trong ngân hàng](#17-so-sánh-với-360-đề-tài-trong-ngân-hàng)

### PART 3 — LÀM NHƯ THẾ NÀO (HOW)
18. [Hệ thống AI = Model + Context + Planning + Tools](#18-hệ-thống-ai--model--context--planning--tools)
19. [Kiến trúc giải pháp Agent](#19-kiến-trúc-giải-pháp-agent)
   - 19.1. Sơ đồ tổng quan
   - 19.2. Tech stack đề xuất
   - 19.3. Cấu trúc dữ liệu (SQL schema)
20. [Roadmap 5 tuần](#20-roadmap-5-tuần)
   - 20.1. Tuần 0 (chuẩn bị)
   - 20.2. Tuần 1–5
   - 20.3. Tổng kết timeline + KPI
21. [Phân công nhóm 4 người](#21-phân-công-nhóm-4-người)
22. [Đo lường thành công & demo flow](#22-đo-lường-thành-công--demo-flow)
   - 22.1. Metrics kỹ thuật
   - 22.2. Demo flow 5–10 phút
   - 22.3. Cách demo tính năng nâng cao
23. [Rủi ro & hành động giảm thiểu](#23-rủi-ro--hành-động-giảm-thiểu)
24. [Câu pitch đề xuất](#24-câu-pitch-đề-xuất)
   - 24.1. Pitch 30 giây (mentor/thầy)
   - 24.2. Pitch 1–2 phút (doanh nghiệp)
   - 24.3. Pitch tính năng nâng cao
25. [Cam kết & giới hạn](#25-cam-kết--giới-hạn)

### PHỤ LỤC
- [A. Tóm tắt quyết định](#a-tóm-tắt-quyết-định)
- [B. Nguồn tham khảo tổng hợp](#b-nguồn-tham-khảo-tổng-hợp)

---

# 🟢 PART 1 — TẠI SAO LÀM ĐỀ TÀI NÀY (WHY)

> **Mục đích PART 1:** Chứng minh đề tài **hợp lý thực sự** (không gượng ép) thông qua lộ trình nhận diện bài toán → đo lường hiện trạng → đánh giá lợi thế AI → đề xuất giải pháp. **Nguyên tắc:** AI chỉ là một phương án. Tài liệu ưu tiên *khai thác bài toán* trước, *định lượng tổn thất* hiện tại, *đánh giá anti-patterns* và chỉ đề xuất Agent khi đã qua đủ ngưỡng chứng minh.

## Scope đã chốt với nhóm

- **Đối tượng:** Marketing Manager / CMO của **SME E-commerce Việt Nam** (sàn TMĐT, D2C brand, retailer chuyển đổi số).
- **Phạm vi thời gian:** **5 tuần** (theo mentor + thầy duyệt, gửi doanh nghiệp lấy feedback).
- **Phạm vi kỹ thuật:** **4 nguồn AI** — ChatGPT, Gemini, Claude, và **Tavily** (dùng cho web-grounded citation & claim verification). Tập trung 100% vào **lĩnh vực Thương mại điện tử** với **2 brand demo** (mỗi brand kèm 2–3 đối thủ trực tiếp).
- **Phạm vi ngôn ngữ:** Tiếng Việt.
- **Phương pháp luận:** Stability-aware Monitoring (Don't Measure Once — Schulte et al. arXiv 2604.07585, 2026) + Evidence-grounded Diagnosis + **Closed-loop Re-measurement** (tính năng nâng cao nổi bật theo yêu cầu của thầy).
- **Mục tiêu cuối:** Giảm 90% thời gian GEO monitoring, tăng 10× prompt coverage, phát hiện ≥ 80% hallucination trong 24h, đo lại hiệu quả action với bootstrap CI.

> **Lưu ý trung thực:** Mọi số liệu dùng trong tài liệu là **nguồn công khai** (Decision Lab, SimilarWeb, Semrush, Ahrefs, AppLabX, Kompa.ai, Q&Me Vietnam, VECOM, Ninja Van Reports). Một số con số là **ước lượng hợp lý** có ghi rõ `[ước lượng]` để nhóm xác minh thêm nếu cần.

---

## 1. Bối cảnh & lý do đề xuất

### 1.1. Đặt vấn đề bằng dữ liệu

Từ 2024, hành vi tìm kiếm của người dùng Việt Nam đã **dịch chuyển rõ rệt** từ Google sang các AI chatbot. Decision Lab (2025) khảo sát 78% người dùng internet Việt Nam đã dùng ít nhất 1 nền tảng AI trong 3 tháng gần nhất, 33% dùng hàng ngày. ChatGPT dẫn đầu với 81% thị phần sử dụng, Gemini 51%, Meta AI 36%.

SimilarWeb Việt Nam (07/2025) ghi nhận **21,5 triệu lượt AI referral traffic**, tăng **740% so với cùng kỳ 2024**. ChatGPT chiếm ~80% tổng AI traffic. Quan trọng hơn:

- **36% người dùng khám phá brand mới qua ChatGPT** (theo Decision Lab)
- **30% tin tưởng khuyến nghị từ AI** (Decision Lab)
- **Gần 50% dùng ChatGPT để học và ra quyết định** (Decision Lab)

**Đặc thù ngành E-commerce Việt Nam khiến bài toán cấp bách hơn:**

- Theo Q&Me Vietnam (2025) và VECOM, ngành **TMĐT Việt Nam đạt ~22 tỷ USD năm 2025**, tăng trưởng 20%+ YoY. SME E-commerce chiếm **~70% gian hàng** trên Shopee, Lazada, Tiki `[Nguồn: Q&Me 2025]`.
- **Hành vi mua hàng đã thay đổi:** Trước khi mua, người dùng thường hỏi AI: *"Shop bán [sản phẩm] nào uy tín?"*, *"So sánh giá [sản phẩm] ở Shopee vs [brand]?"*, *"[Brand] có phải shop lừa đảo không?"* → AI mention trở thành **điểm chạm pre-purchase cực kỳ quan trọng**.
- **Đối thủ cạnh tranh trực tiếp trên AI:** Cùng 1 sản phẩm "tai nghe bluetooth giá rẻ", nếu AI nhắc Shop A mà không nhắc Shop B → Shop B mất traffic organic không tốn tiền ads.
- **Rủi ro hallucination cao:** AI hay mô tả sai chính sách (ship, đổi trả), sai giá, sai đánh giá uy tín → ảnh hưởng trực tiếp conversion.

Nghĩa là: **AI đã trở thành một điểm chạm mới trong customer journey E-commerce**.

### 1.2. Vấn đề của SME E-commerce Việt Nam

Theo khảo sát Q&Me Vietnam, VECOM và AppLabX (2026), **các SME E-commerce Việt Nam** đang **mù mắt** trước kênh AI:

1. **Không biết AI đang nói gì về shop/brand mình** — AI có thể trả lời sai (nói shop lừa đảo dù shop uy tín), đề cập đối thủ thay vì mình, hoặc không nhắc đến → mất traffic pre-purchase.
2. **Không biết prompt nào đang đưa brand đối thủ ra trước** — Không có dashboard theo dõi AI visibility.
3. **Không biết cách tối ưu để AI "chọn" brand mình** — Khác hoàn toàn với SEO Google (backlink, keyword density) và khác cả review sàn (rating, comment).
4. **Công cụ quốc tế quá đắt hoặc không phù hợp thị trường VN** — Semrush AI Search add-on $139–199/mo, Ahrefs AI tracking $199/mo, Otterly $29/mo nhưng chỉ 1 AI.
5. **Công cụ Việt chưa có chuyên biệt cho E-commerce** — Kompa GEO đã ra mắt nhưng focus tổng quát, chưa có chuyên biệt cho E-commerce.

**Đặc thù riêng của E-commerce khiến việc monitor AI quan trọng hơn các ngành khác:**

| Đặc thù | Ý nghĩa với GEO |
|---------|-----------------|
| **Conversion trực tiếp** | AI mention → click → mua hàng (ít hơn 1 ngày) → mỗi mention bị mất = mất doanh thu trực tiếp |
| **So sánh giá liên tục** | Người dùng hay hỏi "shop nào rẻ hơn" → AI trở thành price comparison channel |
| **Đánh giá uy tín** | Câu hỏi "[brand] có lừa đảo không?" → AI sai = thiệt hại brand nghiêm trọng |
| **Tính mùa vụ cao** | Sale 11.11, 12.12, Tết — visibility trong 2 tuần cao điểm quyết định cả quý doanh thu |
| **Cạnh tranh khốc liệt** | Cùng 1 ngành hàng có 50–200 shop → AI chỉ nhắc 3–5 → đường đua vào top AI cực kỳ khắc nghiệt |

### 1.3. Tại sao là "GEO Agent cho E-commerce"

**GEO (Generative Engine Optimization)** là thuật ngữ mới nổi (xuất hiện mạnh từ 2024) dùng để chỉ các kỹ thuật tối ưu để thương hiệu được AI "chọn" trích dẫn và giới thiệu khi người dùng hỏi. Đây **không phải buzzword** — nó phản ánh sự thay đổi hành vi tìm kiếm đã được đo lường bằng dữ liệu.

Một **GEO Agent cho E-commerce** sẽ:

- **Tự động gửi hàng trăm prompt** (câu hỏi của người mua hàng) đến nhiều AI (ChatGPT, Gemini, Claude) **và Tavily-grounded search** để lấy citation chính xác
- **Trích xuất câu trả lời**, xác định shop/brand nào được nhắc đến, vị trí nào, sentiment gì
- **So sánh với đối thủ**, đo **visibility score** (tỷ lệ prompt mà brand được nhắc) và **SOV** trong ngành hàng
- **Phát hiện thông tin sai** về shop (hallucination về giá, ship, đánh giá) — đặc biệt quan trọng trong E-commerce
- **Đề xuất hành động tối ưu** dựa trên phân tích nguồn mà AI hay tham chiếu

**Vì sao E-commerce là vertical phù hợp nhất cho demo 5 tuần:**

1. **Dữ liệu prompt dồi dào:** Người mua hàng Việt có hàng trăm pattern câu hỏi → prompt library dễ xây.
2. **Brand dễ chọn & dễ verify:** Shop trên Shopee/Lazada có data public (rating, số đơn, review) → dễ đối chiếu kết quả AI.
3. **Đối thủ rõ ràng:** Cùng ngành hàng có 5–20 đối thủ cùng phân khúc → so sánh SOV rất trực quan.
4. **Hallucination cost cao & dễ thấy:** AI nói sai giá/ship/uy tín → khách bỏ mua ngay → impact đo được rõ.
5. **Có 2 brand mẫu điển hình:** Brand sàn (nhiều SKU, đối thủ nhiều) + Brand D2C (entity riêng, content-driven) → bao phủ 2 archetype chính.

---

## 2. Lộ trình 5 bước chọn giải pháp AI

> **Bài toán → Quy trình → Chỉ số → Giải pháp**

### Bước 1: Nhận diện bài toán

> Khi người dùng Việt Nam tìm kiếm sản phẩm/dịch vụ qua AI chatbot, **SME E-commerce không biết shop/brand mình có được nhắc đến không, được nhắc thế nào, đứng ở đâu so với đối thủ, và phải làm gì để được AI "chọn" trong các câu trả lời về mua sắm**.

### Bước 2: Hiểu quy trình hiện tại (đã rõ ở phần 10)

### Bước 3: Xác định chỉ số đo lường (đã rõ ở phần 11)

### Bước 4: Giải pháp AI

Sau khi chứng minh bài toán có thật, quy trình không scale, chỉ số đo lường rõ ràng:

→ **Giải pháp: AI Agent tự động hóa toàn bộ pipeline trên, có human-in-the-loop cho phần phân tích sentiment và verify hallucination.**

**Căn cứ học thuật cho thiết kế agent** (xem chi tiết phần 8):
- **Stability-aware Monitoring** theo Schulte et al. (arXiv 2604.07585): mỗi prompt chạy **N lần** (N=3 cho demo, N=7–8 cho production), tính Stability Score.
- **Evidence-grounded Diagnosis** theo Tian et al. (arXiv 2603.09296): mỗi gap đi kèm citation URL + claim quote.
- **Closed-loop Re-measurement** (tính năng nâng cao theo yêu cầu thầy): sau khi marketer đánh dấu task done → re-scan + bootstrap CI → phân loại Improved/No evidence/Regressed.

---

## 3. Tìm bài toán AI ở đâu (4 lăng kính)

### 3.1. Vấn đề có tồn tại thực sự không?

✅ **Có.** 36% người dùng Việt discover brand qua AI, 30% trust AI. 21,5 triệu AI referral traffic VN tháng 7/2025, tăng 740% YoY. Ngành TMĐT VN ~22 tỷ USD 2025, tăng 20% YoY.

### 3.2. Công việc tiêu tốn thời gian

✅ **Đúng.** Ước lượng một marketer E-commerce làm thủ công hết **~80 giờ/tháng** (chi tiết ở §10.3) chỉ để trả lời "AI có nhắc shop mình không, đối thủ đứng ở đâu, có thông tin sai nào về shop không".

### 3.3. Quy trình có thể automation

✅ **Có.** Quy trình gồm 7 bước lặp lại (liệt kê prompt → gửi đến AI → đọc câu trả lời → đếm shop → so sánh đối thủ → tổng hợp → đề xuất hành động). 90% bước có thể automation.

### 3.4. Điểm đau người dùng (Persona)

**Persona: Marketing Manager của SME E-commerce Việt Nam (shop trên Shopee/Lazada/Tiki hoặc brand D2C, 5–100 nhân viên)**

> *"Shop mình bán đồ gia dụng trên Shopee được 3 năm, doanh thu 5 tỷ/năm. Mình vừa mở ChatGPT hỏi thử: 'shop bán đồ gia dụng uy tín TPHCM' — không thấy shop mình, nhưng thấy 4 đối thủ. Mình thử tiếp 'nồi chiên không dầu loại nào tốt' — AI nhắc đối thủ X nhưng không nhắc sản phẩm mình. Mình thử hỏi 'shop Y có uy tín không' — AI trả lời mơ hồ, thậm chí có vài câu nghi ngờ giao hàng chậm (mà thực tế shop mình ship rất nhanh). Mình không biết đây là 1 lần hay xảy ra hàng ngày. Mình không biết phải làm gì để AI bắt đầu nhắc đến shop mình: viết bài blog SEO? Đẩy review Shopee? PR báo chí? Thuê KOL review trên TikTok để có entity trên web? Không ai cho mình một dashboard, không ai cho mình một action plan. Mình sợ mỗi tháng mình đang mất 20-30% traffic pre-purchase mà không biết."*

---

## 4. 5 câu hỏi stakeholder (và câu trả lời dựa trên nguồn công khai)

### Câu 1: Quy trình hiện tại của anh/chị là gì?

**Trả lời thay (quy trình hiện tại của SME E-commerce nếu không có công cụ):**

| Bước | Người thực hiện | Công cụ | Thời gian `[Ước lượng]` |
|------|----------------|---------|------------------|
| 1. Liệt kê prompts quan trọng (uy tín, giá, so sánh, review) cho 2–3 ngành hàng chính | Marketing Manager | Notion/Excel | 4 giờ (làm 1 lần) |
| 2. Gửi prompt đến ChatGPT, Gemini, Claude thủ công (Tavily thay cho Perplexity/Copilot) | Marketing Manager | 4 tab trình duyệt | 2 giờ/lần × 4 tuần = 8 giờ/tháng |
| 3. Đọc câu trả lời, note shop nào được nhắc, có thông tin sai về giá/ship/uy tín không | Marketing Manager | Notion | 3 giờ/lần × 4 = 12 giờ/tháng |
| 4. Lặp lại cho 2–3 đối thủ chính trong từng ngành hàng | Marketing Manager | Notion | 4 giờ/lần × 4 = 16 giờ/tháng |
| 5. Tổng hợp visibility, sentiment vào Excel/Sheet | Marketing Manager | Excel | 4 giờ/lần × 4 = 16 giờ/tháng |
| 6. So sánh với lần trước, viết báo cáo nội bộ + check hallucination | Marketing Manager | PowerPoint/Notion | 8 giờ/tháng |
| 7. Đề xuất hành động tối ưu | Marketing Manager + Content team | WordPress/PR | 12 giờ/tháng |

**Tổng: khoảng 80 giờ/tháng cho 2 brand E-commerce, 2–3 đối thủ, 4 AI platforms.** `[Ước lượng]`

### Câu 2: AI có làm tốt hơn con người ở tác vụ này không?

✅ **Có.** AI vượt trội ở:
- Parse câu trả lời dạng text tự nhiên (LLM).
- Phát hiện shop mention trong nhiều dạng paraphrase.
- Cross-check giá/ship với Tavily web-grounded.
- Chạy lặp N lần/prompt để có variance estimate (con người không thể).

### Câu 3: Thiệt hại (Cost) do vấn đề này gây ra là gì?

| Loại thiệt hại | Ước lượng `[Ước lượng]` |
|----------------|------------------------|
| Thời gian marketing manager | 80 giờ/tháng × $10/giờ = **$800/tháng** |
| Chi phí công cụ quốc tế (nếu mua Semrush) | **$139–199/tháng** |
| Chi phí PR/outreach | **$300–500/tháng** (nếu thuê agency) |
| Chi phí cơ hội (lost revenue) | **Rất cao trong E-commerce**: shop "vô hình" trên AI ≈ mất 20–30% pre-purchase traffic |
| Thiệt hại do AI nói sai về shop | Conversion drop ngay lập tức trong mùa sale |
| SLA hallucination | Mất uy tín trong vài giờ, khó hồi phục |

### Câu 4: AI sai sẽ gây hậu quả gì?

**Lớp 1 (AI upstream sai):** ChatGPT/Gemini/Claude nói sai giá/ship/uy tín → ảnh hưởng brand ngay lập tức.

**Lớp 2 (Agent của nhóm phân tích sai):** Đếm nhầm mention, sentiment sai, phát hiện nhầm hallucination → cross-check sai giá với Tavily cache cũ.

**Phạm vi tự chủ & HITL:**
- **AI Agent tự động:** Gửi prompt đến 3 LLM + 1 Tavily search, parse câu trả lời, đếm mention shop.
- **Cần HITL:** Sentiment analysis (sarcasm E-commerce), hallucination verification về giá/ship/uy tín.
- **AI chỉ hỗ trợ:** Đề xuất hành động tối ưu (cuối cùng marketer + shop admin vẫn quyết định).

### Câu 5: Giá trị mang lại có vượt trội chi phí và rủi ro?

✅ **Có (cho demo 5 tuần với 2 brand E-commerce).**
- **Giá trị:** Giảm 90% thời gian monitoring cho 2 brand, tăng 10× coverage (500 prompts/2 brand), phát hiện hallucination giá/ship trong 24h.
- **Chi phí vận hành (5 tuần demo):** < 500.000 VND tổng.
- **Chi phí vận hành (production scale):** < 4 triệu VND/tháng cho 2 brand × 4 nguồn AI.
- **Rủi ro:** Sai số có thể kiểm soát qua HITL + precision/recall monitoring.

→ **Agent + HITL là giải pháp tối ưu cho demo 5 tuần.**

---

## 5. Anti-patterns cần tránh

❌ **Định vị "GEO tool đầu tiên tại VN"** — Kompa, Fast Marketing, SEO Dạo, Hashmeta đều có.
❌ **"Agent thay thế SEO/GEO Specialist"** — Agent là hỗ trợ, không thay thế.
❌ **"Task do agent đề xuất chắc chắn tăng AI visibility"** — Cần closed-loop mới biết.
❌ **"Dashboard là đóng góp mới"** — Phổ biến rồi.
❌ **"Đo 1 lần là đủ"** — Schulte et al. đã chứng minh sai.

---

## 6. Quick Problem Card

| Trường | Nội dung |
|--------|----------|
| **Bài toán (1 câu)** | SME E-commerce Việt không biết AI đang nói gì về shop/brand mình trên ChatGPT, Gemini, Claude và kết quả tìm kiếm web (Tavily), không biết đứng ở đâu so với 2–3 đối thủ chính trong ngành hàng, và không biết phải làm gì để được AI "chọn". |
| **Đối tượng ảnh hưởng** | Marketing Manager, CMO, chủ shop, shop admin của **SME E-commerce Việt Nam**. Demo: **2 brand E-commerce** (1 sàn + 1 D2C). |
| **Phạm vi kỹ thuật** | **4 nguồn AI:** ChatGPT + Gemini + Claude + **Tavily** (web-grounded citation & claim verification). 100% **Thương mại điện tử**. |
| **Phạm vi ngôn ngữ** | Tiếng Việt. |
| **Quy trình hiện tại** | 7 bước thủ công. Tổng ~80 giờ/tháng cho 2 brand × 2–3 đối thủ. |
| **Nút thắt & Tác động** | Bước 2–5 tốn thời gian; sai số về giá/ship rất nguy hiểm; không scale; mất pre-purchase traffic; hallucination không phát hiện kịp. |
| **Chỉ số thành công** | (1) Thời gian: **80h → <8h/tháng** (giảm 90%); (2) Coverage: 50 → 500+ prompts/tháng (tăng 10×); (3) Visibility Rate real-time với Stability Score ≥ 0.7, precision ≥ 90%; (4) Hallucination recall ≥ 80% trong 24h; (5) SOV top 3; (6) **Closed-loop ≥ 75% phân loại đúng**. |
| **Tính năng nâng cao** | **Closed-loop Re-measurement**: khi marketer đánh dấu task done → re-scan + bootstrap CI → `Improved signal` / `No clear evidence` / `Regressed`. Đây là điểm khác biệt so với Profound, Peec, Otterly, Kompa. |
| **Định hướng giải pháp** | **Agent + HITL** (HITL chặt cho hallucination giá/ship vì E-commerce tolerance rất thấp). |

---

# 🟢 PART 2 — LÀM GÌ (WHAT)

> **Mục đích PART 2:** Trình bày thị trường, căn cứ học thuật, scope đã chốt, tính năng cốt lõi + nâng cao, khai thác bài toán chi tiết và định lượng hóa.

## 7. Thị trường GEO 2026

### 7.1. Phân khúc sản phẩm quốc tế

| Phân khúc | Sản phẩm | Giá (entry) | Điểm mạnh | Điểm yếu / chỗ trống |
|-----------|----------|-------------|-----------|----------------------|
| **Enterprise forensic** | Profound | $499/tháng (Starter $99 chỉ ChatGPT) | SOC2, 700+ enterprise customer (Target, Walmart, Ramp, MongoDB), Query Fanout | Đắt, Starter rất giới hạn |
| **Mid-market / Agency** | Peec AI | €85–95/tháng | Unlimited seats, Looker Studio, 4 engines ở base plan | Claude/GPT-5 Search chỉ Enterprise |
| **Lean/SMB** | Otterly.AI | $29/tháng (Lite) | Rẻ nhất, dễ dùng solo founder | Engine giới hạn entry |
| **SEO suite + AI add-on** | Semrush AI Visibility, Ahrefs Brand Radar | $139–199/tháng | Tận dụng SEO stack | GEO chỉ là add-on, không sâu |
| **Action/Agent layer** | Writesonic GEO Action Center | Enterprise tier | Phát hiện gap → ranked action → Article Writer | Action layer đang phát triển |

**Nguồn:** [Growth Engineer](https://growthengineer.ai/blog/profound-vs-otterly-vs-peec-ai), [Discovered Labs](https://discoveredlabs.com/blog/profound-vs-peec-vs-otterly-which-ai-visibility-platform-should-you-buy), [Clarity Digital](https://claritydigital.agency/blog/best-aeo-geo-tools-2026).

**Nhận xét chung:**
1. **"Don't Measure Once"** — Schulte et al. (arXiv 2604.07585, 2026): ≥ 7–8 lần/prompt/ngày, citation share có noise floor 5–7%.
2. Tất cả sản phẩm "diagnose but don't fix" hoặc "diagnose but don't measure".
3. Chưa sản phẩm nào công khai "closed-loop task evaluation".
4. Phân khúc enterprise bỏ qua SME Việt.

### 7.2. Phân khúc Việt Nam (cập nhật 2026)

| Bên | Loại hình | Năng lực GEO công khai | Điểm mạnh | Khoảng trống |
|-----|-----------|------------------------|-----------|--------------|
| **Kompa GEO** | Nền tảng + dịch vụ | AI Visibility Score 4 AI (ChatGPT, Gemini, Claude, Perplexity), real prompt discovery, benchmark, dashboard, alert, content recommendation | Lợi thế dữ liệu Social Listening Đông Nam Á; đã có khách hàng DN | Chưa công khai "agent tự tạo ticket, phân phòng ban, closed-loop evaluation" |
| **Hashmeta AI (Vietnam/SEA)** | Agency + AI SEO Writer | Managed GEO/AEO campaigns, AI SEO Writer (Việt + Anh) | GEO-integrated campaigns + content production | Workflow chưa công khai mức agent |
| **Fast Marketing** | Agency SEO/GEO | GEO Analytics cho ChatGPT, Claude, AIO; structured data lồng | Conversation content cho AI search | Thuần dịch vụ, không có platform riêng |
| **SEO Dạo** | Dịch vụ SEO/GEO | Tối ưu brand cho ChatGPT/Gemini/Perplexity | Local agency, tiếng Việt tốt | Không có platform agent |
| **DigiAI Platform (Digitech)** | Nền tảng AI marketing tổng | 13 agent cho brand profile, SEO audit, content, competitor radar, publishing, CSKH | Nền tảng agent rõ ràng, có nhiều case study | Chưa thấy module GEO visibility-to-task chuyên biệt |

**Nguồn:** [Kompa GEO](https://kompa.ai/giai-phap/kompa-geo), [geo.kompa.ai](https://geo.kompa.ai/), [Hashmeta AI Vietnam](https://www.hashmeta.ai/en/blog/geo-for-vietnam-the-emerging-ai-search-opportunity-vietnamese-brands-cannot-ignore), [Fast Marketing](https://fastmarketing.com.vn/dich-vu-geo), [DigiAI Platform](https://vndigitech.com/phan-mem/digiai-platform/).

### 7.3. Khoảng trống còn lại mà nhóm có thể nhắm

**Pain points KHÔNG nên tập trung (đã có tool tốt):**
- Đo visibility rate, citation, SOV, sentiment, dashboard, benchmark, alert.

**Pain points NHÓM CÓ THỂ NHẮM:**

| Pain point | Lý do | Bằng chứng |
|------------|-------|------------|
| **Đo lặp + stability score** | Công cụ thường chạy 1 lần → nhiễu | Schulte et al. arXiv 2604.07585 — "Don't Measure Once" |
| **Closed-loop evaluation** | Hầu hết công cụ dừng ở "task do con người xử lý" | arXiv 2603.08924 — Quantifying Uncertainty |
| **Phân task theo policy doanh nghiệp** | Cùng "AI nói sai giá" có thể thuộc Content, Product, Brand, Legal | Chưa thấy công cụ VN nào công khai routing |
| **Prompt tiếng Việt + entity Việt** | Tên có dấu/không dấu, viết tắt, địa danh | Công cụ quốc tế không tối ưu |
| **Giá thấp cho SME E-commerce VN** | Công cụ quốc tế đắt; Kompa enterprise-grade | Profound $99–499, Kompa báo giá riêng |
| **Methodology mở** | Công cụ thường là "black box" | Nghiên cứu 2026 chỉ ra vấn đề |
| **Tavily-grounded cho E-commerce VN** | Chưa ai làm | Gap rõ |

---

## 8. Căn cứ học thuật quan trọng

> Tài liệu không định vị "tool GEO đầu tiên tại VN". Định vị dựa trên **3 pain points chưa được giải quyết tốt**, có căn cứ học thuật rõ ràng.

### 8.1. Ba bài báo nền tảng

**1. "Don't Measure Once: Measuring Visibility in AI Search (GEO)"** (Schulte et al., arXiv 2604.07585, 2026)
- GEO là **stochastic, partially observable pipeline** — cùng 1 prompt, cùng 1 model có thể cho kết quả khác nhau giữa các lần chạy.
- Cần **≥ 7–8 lần chạy / prompt / ngày** để có standard error < 0.10.
- **Implication:** Agent phải có **Stability-aware Monitoring** — chạy prompt N lần (N=3 cho demo, 7–8 cho production), tính **Stability Score** = 1 - normalized variance. Gap chỉ vào diagnosis khi Stability ≥ 0.7.
- **E-commerce:** Visibility Rate dao động 5–15 điểm % giữa các lần → không thể kết luận "shop tăng/giảm" nếu đo 1 lần.

**2. "Quantifying Uncertainty in AI Visibility: A Statistical Framework"** (arXiv 2603.08924, 2026)
- Citation share có **noise floor 5–7 điểm phần trăm**.
- **Bootstrap confidence intervals** bắt buộc khi báo cáo hiệu quả action.
- **Implication:** Closed-loop Re-measurement phải dùng bootstrap 95% CI để phân loại `Improved signal` / `No clear evidence` / `Regressed`.
- **E-commerce:** Shop tối ưu listing → AI nhắc nhiều hơn 3 điểm % → KHÔNG kết luận "thành công" vì dưới noise floor.

**3. "Diagnosing and Repairing Citation Failures in GEO / AgentGEO"** (Tian et al., arXiv 2603.09296, 2026)
- Hệ thống agentic **diagnose-and-repair** cải thiện **40% citation rate** với chỉ **5% sửa đổi content**.
- **Implication:** Nền tảng cho **GEO Recommendation Agent** — đề xuất hành động sửa chữa có bằng chứng.
- **E-commerce:** AI không nhắc 1 shop → diagnose "thiếu schema.org Product" → đề xuất "thêm schema Product với price/availability" → re-scan → đo cải thiện.

### 8.1.1. Các bài liên quan khác (tham khảo thêm)

| Bài báo | Đóng góp chính | Ứng dụng cho dự án |
|---------|---------------|---------------------|
| **Martinez (2026)** — "Optimizing Visibility in Generative Engines: A Critical Survey of GEO (2023–2026)" [arXiv 2607.14035](https://arxiv.org/abs/2607.14035) | Survey toàn diện về kỹ thuật GEO | Căn cứ lý thuyết cho action plan |
| **Kim et al. (2026)** — "SAGEO Arena: A Realistic Environment for Evaluating Search-Augmented GEO" [arXiv 2602.12187](https://arxiv.org/abs/2602.12187) | Môi trường eval realistic | Tham khảo cho gold dataset design |
| **Aggarwal et al. (2023)** — "GEO: Generative Engine Optimization" [arXiv 2311.09785](https://arxiv.org/abs/2311.09785) | Foundational paper | Định nghĩa GEO |
| **Gao et al. (EMNLP 2023)** — "ALCE: Automatic LLMs' Citation Evaluation" | Citation evaluation framework | Tham khảo cho parser đánh giá citation quality |

### 8.2. 3 pain points nhóm tập trung

| Pain point | Bằng chứng từ học thuật | Bằng chứng từ thị trường | Nhóm nhắm |
|------------|-------------------------|--------------------------|-----------|
| **Đo lặp + Stability Score** | Schulte et al. ≥ 7 lần/prompt | Công cụ hiện tại chạy 1 lần | ✅ Cốt lõi #1 |
| **Evidence-grounded Diagnosis** | Tian et al. diagnose-and-repair | Kompa, Profound chỉ "diagnose" | ✅ Cốt lõi #2 |
| **Closed-loop Evaluation** | arXiv 2603.08924 — bootstrap CI | Chưa tool nào re-scan + CI | ✅ Nâng cao |

---

## 9. Đề xuất hướng đi

### 9.1. Tên dự án và định vị

**Tên dự kiến (tạm thời):** `VN-ECOM-GEO Agent` (hoặc tên nhóm chọn).

**Định vị một câu:**

> Công cụ theo dõi AI visibility cho shop/brand E-commerce Việt Nam trên **ChatGPT, Gemini, Claude và Tavily** — tập trung vào **đo lặp có kiểm soát (Stability-aware)**, **evidence-grounded diagnosis** (citation URL + claim quote + giá/ship cross-check), **closed-loop re-measurement** (đo lại sau action với bootstrap CI), và **đề xuất action plan có thể kiểm chứng** cho marketer E-commerce.

### 9.2. 2 tính năng cốt lõi (theo gợi ý của mentor)

**Tính năng cốt lõi #1: Stability-aware Visibility Monitoring**

- Gửi prompt đến **4 nguồn AI** (ChatGPT + Gemini + Claude + Tavily web-grounded).
- Mỗi prompt chạy lặp **3 lần / ngày** (N=7–8 cho production).
- **Prompt library E-commerce** chia **5 nhóm**: (1) Uy tín, (2) Giá, (3) So sánh, (4) Review sản phẩm, (5) Ship/dịch vụ.
- Tính: Visibility Rate, Mention Position, SOV, Sentiment, **Stability Score** = 1 - normalized variance.
- Lưu raw response + metadata (timestamp, model_version, ai_engine).
- **Stability Filter:** chỉ gap có Stability ≥ 0.7 mới vào diagnosis.

**Tính năng cốt lõi #2: Evidence-grounded Diagnosis & Action Plan**

- Với mỗi gap đủ ổn định, agent thu thập evidence:
  - Citation URL mà AI/Tavily đang tham chiếu.
  - **Cross-check giá/ship claim với Shopee/Lazada/web shop bằng Tavily web-grounded.**
  - Phát hiện claim sai / claim thiếu.
- Action plan có bằng chứng cho E-commerce: cập nhật listing, schema FAQ, outreach review site (Tinhte, Voz), PR blog.

### 9.3. 1 tính năng nâng cao (theo yêu cầu thầy)

**Closed-loop Re-measurement:**
- Sau khi marketer E-commerce đánh dấu task done → tự động re-scan (3 lần/prompt, 4 AI).
- So sánh pre/post với **bootstrap 95% CI**.
- Phân loại: `Improved signal` (vượt noise floor) / `No clear evidence` / `Regressed`.
- **E-commerce context:** Trong mùa sale (11.11, 12.12), closed-loop giúp biết action nào thật sự tăng visibility, action nào chỉ là placebo.

### 9.4. Phạm vi MVP 5 tuần

| Yếu tố | Phạm vi |
|---------|---------|
| **Brand demo** | **2 brand E-commerce** (1 sàn + 1 D2C) + 2–3 đối thủ / brand |
| **AI engines** | **4 nguồn**: ChatGPT + Gemini + Claude + Tavily |
| **Prompt set** | **~100 prompt** chia 5 nhóm (uy tín, giá, so sánh, review sản phẩm, ship/dịch vụ) |
| **Lặp / prompt** | 3 lần / ngày (mở rộng 7–8 cho production) |
| **Ngôn ngữ** | Tiếng Việt (chính), tiếng Anh (fallback) |
| **Tần suất scan** | 1 lần / ngày trong 4 tuần demo (Tuần 0 chuẩn bị + Tuần 1–5) |
| **Stakeholder thật** | Gửi **2 SME E-commerce VN** để duyệt demo |

### 9.5. Đối tượng sử dụng (E-commerce focus)

- **Primary user:** Marketing Manager / CMO / chủ shop của **SME E-commerce Việt Nam**.
- **Quy mô:** 5–100 nhân viên, đã có Shopee/Lazada/Tiki hoặc D2C, doanh thu ~1–20 tỷ VND/năm.
- **Ngành mục tiêu:** 100% Thương mại điện tử, 3 phân khúc:
  - **Sàn TMĐT:** shop bán đa ngành hàng trên Shopee/Lazada/Tiki.
  - **D2C brand:** brand có website riêng, content-driven.
  - **Retailer chuyển đổi số:** chuỗi cửa hàng truyền thống đẩy online.
- **Tiêu chí chọn 2 brand demo:**
  - Có mặt trên AI chatbot (đã được nhắc đến ở một số prompt).
  - Có 2–3 đối thủ trực tiếp cùng phân khúc.
  - Có thông tin public dễ verify (Shopee/Lazada listing, web có schema).
  - Có khả năng liên hệ stakeholder.
  - **1 brand sàn + 1 brand D2C** để bao phủ 2 archetype.

---

## 10. Khai thác bài toán chi tiết

### 10.1. Quy trình hiện tại: công cụ, bước, cơ chế bàn giao (E-commerce)

| Bước | Công cụ | Người làm | Output | Đầu ra chuyển tiếp |
|------|---------|-----------|--------|---------------------|
| Liệt kê prompts E-commerce | Notion/Excel | Marketing Manager | Prompt list chia 5 nhóm | Content team, Shop admin |
| Gửi prompts | 4 tab browser | Marketing Manager | Câu trả lời thô + web citations | — |
| Đọc & note shop mention, giá/ship claim | Notion | Marketing Manager | Bảng mention + claim đáng ngờ | — |
| Đếm & so sánh với 2–3 đối thủ | Excel | Marketing Manager | Bảng visibility, SOV | CMO/Chủ shop |
| Phân tích sentiment | Thủ công | Marketing Manager | Score -1/+1 | CMO/Chủ shop |
| So sánh đối thủ, kiểm tra hallucination giá/ship | Excel + web | Marketing Manager | SOV report + flag sai | CMO + Shop admin |
| Đề xuất hành động tối ưu | Notion/PPT | Marketing Manager + CMO | Action plan | Content team, PR agency, Shop admin |

### 10.2. Nút thắt nằm ở đâu?

- **Bước 2 (gửi prompt):** Thủ công 100%, không scale.
- **Bước 3 (đọc + check claim giá/ship):** Câu trả lời dài 200–500 từ, shop có thể ở giữa, dễ bỏ sót. **Nguy hiểm trong E-commerce**: AI nói sai giá/ship mà không phát hiện → khách mua theo thông tin sai → review 1 sao.
- **Bước 4:** 100 prompts × 4 nguồn AI × 2–3 đối thủ = 800–1200 dòng dữ liệu.
- **Bước 6:** Verify hallucination giá/ship thủ công → thêm 4–6 giờ/tuần.

### 10.3. Hao phí hiện tại `[Tất cả là ước lượng]`

| Hao phí | Con số |
|---------|--------|
| Thời gian marketing manager | 80 giờ/tháng |
| Chi phí nhân sự | ~20 triệu VND/tháng |
| Công cụ quốc tế | $139–199/mo ≈ 3.5–5 triệu VND |
| Chi phí cơ hội (mất pre-purchase traffic) | Với shop 5 tỷ VND/năm, ước lượng mất 700M–1.5 tỷ VND/năm |
| Chi phí xử lý sai thông tin | 5–10 triệu VND/tháng nếu hallucination không phát hiện kịp |
| **Tổng** | **~30–35 triệu VND/tháng** |

### 10.4. Tiêu chí thành công

- **Input metrics:** Số prompt track mỗi tháng (chia theo 5 nhóm), tỷ lệ sentiment verify, số hallucination phát hiện trong 24h, số citation source map.
- **Output metrics:** Thời gian 80h → <8h/tháng, Visibility Rate ≥ 20% sau 3 tháng, Hallucination recall ≥ 80%, **SOV top 3 cho 2 brand demo**, ROI <4 triệu VND/tháng.

### 10.5. HITL boundary

- **AI tự chủ:** Gửi prompt, parse, đếm, cross-check giá/ship với Tavily.
- **HITL bắt buộc:** Sentiment (sarcasm E-commerce), hallucination verification về giá/ship/uy tín.
- **Con người quyết:** Action plan (viết bài, đẩy review, PR, sửa listing).

### 10.6. Có giải pháp phi AI đơn giản hơn không?

| Giải pháp | Đánh giá |
|-----------|----------|
| **Checklist + Excel** | Không scale |
| **VA (virtual assistant)** | Vẫn 80h/tháng, lỗi cao |
| **Mua Semrush/Ahrefs** | $139–199/mo, chỉ 1 AI, không có hallucination detection chuyên E-commerce |
| **Thuê agency GEO** | $500–2000/tháng |
| **Tự build script scrape** | Tốn effort tương đương |
| **AI Agent (đề xuất)** | ✅ Tự động 90%, track 4 nguồn AI, phát hiện hallucination giá/ship, ~$30–50/tháng |

---

## 11. Định lượng hóa bài toán

### Hiện trạng

| Chỉ số | Con số `[Ước lượng]` |
|--------|----------------------|
| Thời gian GEO monitoring cho 2 brand E-commerce | 80 giờ/tháng |
| Số prompts track (uy tín, giá, so sánh, review, ship) | 50 prompts/2 brand/tháng |
| Số nguồn AI monitor | 1–2 (thường chỉ ChatGPT) |
| Tỷ lệ sót mention shop | 10–20% |
| Tỷ lệ sót hallucination giá/ship/uy tín | 20–30% |
| Stability Score | Không đo được (chạy 1 lần) |
| Đo lại hiệu quả action | Không có |
| Chi phí trực tiếp + gián tiếp | ~30–35 triệu VND/tháng |

### Mục tiêu

| Chỉ số | Target |
|--------|--------|
| Thời gian GEO monitoring | <8 giờ/tháng (giảm 90%) |
| Số prompts track | 100 prompts × N lần × 2 brand E-commerce/tháng |
| Số nguồn AI | 4 (ChatGPT, Gemini, Claude, Tavily) |
| **Stability Score (mỗi gap)** | ≥ 0.7 |
| **Số lần chạy / prompt / ngày** | N=3 demo (mở rộng 7–8 production) |
| Tỷ lệ sót mention shop | <5% |
| Tỷ lệ sót hallucination giá/ship | <5% |
| Thời gian phát hiện hallucination | <24 giờ |
| **Closed-loop evaluation accuracy** | ≥ 75% phân loại đúng |
| Chi phí vận hành | <4 triệu VND/tháng |
| SOV ngành hàng chính | Top 3 cho 2 brand demo |

---

## 12. Thiết lập chỉ số Output vs Input

### Output (kết quả cuối)
1. Thời lượng: 80h → 8h/tháng (giảm **90%**)
2. Phát hiện thông tin sai: từ "tình cờ" → **≥80% hallucination (giá/ship/uy tín) trong 24h**
3. Marketer biết AI nói gì về shop với **Stability Score** để phân biệt signal thật vs noise
4. **Closed-loop value:** Biết action nào thật sự tăng visibility (Improved signal) vs placebo (No evidence)

### Input (đòn bẩy)
1. Số prompt track: 50 → 100 × N lần × 2 brand
2. **Stability Score** của mỗi gap: ≥ 0.7 (gate)
3. Precision ≥ 90%, recall ≥ 85%
4. Số nguồn AI monitor: 1 → 4
5. Tỷ lệ hallucination verify: ≥ 80% trong 24h
6. Số action item tạo tự động mỗi tuần: 10+
7. **Closed-loop reports:** ≥ 3 reports/tuần

---

## 13. Ba bước quyết định AI theo PAIR

### Bước 1: Giao điểm — Bài toán có nằm trong nhóm AI làm tốt hơn rule/heuristic?

| Đặc điểm bài toán GEO | Phù hợp AI? |
|------------------------|--------------|
| Phải parse câu trả lời AI dài, không cấu trúc | ✅ |
| Phải đếm mention trong văn bản tự nhiên | ✅ |
| Phải phân tích sentiment (có sarcasm) | ✅ |
| Phải phát hiện hallucination | ✅ |
| Tổng hợp từ nhiều nguồn (4 AI platforms) | ✅ |

✅ **Bài toán nằm trong vùng thế mạnh AI.**

### Bước 2: Automate hay Augment?

| Tác vụ | Automate | Augment | Lý do |
|--------|----------|---------|-------|
| Gửi prompt | ✅ | | Không rủi ro |
| Parse câu trả lời | ✅ | | Có thể sửa bằng re-run |
| Đếm mention | ✅ | | Có thể sửa |
| Phân tích sentiment | | ✅ | Cần HITL (sarcasm) |
| Verify hallucination giá/ship | | ✅ | Cần HITL (tolerance thấp) |
| Đề xuất action | | ✅ | Marketer quyết cuối |

### Bước 3: Trade-off FP vs FN

| Loại sai | Hậu quả | Mức chấp nhận |
|----------|---------|---------------|
| Mention FP | Đếm nhầm, dashboard có noise | Chấp nhận được |
| Mention FN | Bỏ sót shop được nhắc | Nguy hiểm |
| Hallucination FP | Điều tra không cần thiết | Chấp nhận được |
| Hallucination FN | Brand bị nói sai, mất uy tín | **Nguy hiểm nhất** |

→ **Agent nên thiên về recall**, chấp nhận precision thấp hơn.

---

## 14. Khi nào AI có/không có lợi thế

| Đặc điểm | Áp dụng cho GEO | Lý do |
|----------|-----------------|-------|
| Hiểu ngôn ngữ tự nhiên | ✅ | Câu trả lời AI là text tự nhiên |
| Phát hiện cái hiếm và biến đổi | ✅ | Brand mention có thể ở nhiều dạng |
| Cá nhân hóa theo brand/ngành | ✅ | Mỗi brand E-commerce có prompt list riêng |
| Tổng hợp từ nhiều nguồn | ✅ | 4 nguồn AI × nhiều prompts |
| Tác vụ lặp lại | ✅ | Cùng prompt, cùng format |
| Đo lặp có kiểm soát (stability) | ✅ | LLM rẻ → chạy N lần/prompt khả thi |

**AI không tốt hơn khi:**
- Cần tính dự đoán được tuyệt đối → ⚠️ Cần HITL
- Thông tin tĩnh, ít thay đổi → ❌
- Lỗi quá tốn kém → ⚠️ Cần HITL cho hallucination
- Yêu cầu minh bạch tuyệt đối → ⚠️ Cần log đầy đủ

**Kết luận:** GEO tracking **không phải bài toán rule/heuristic** giải quyết tốt. AI hiện đại vượt trội về recall và độ robust.

---

## 15. Thang câu hỏi lựa chọn cấp độ giải pháp

| Cấp độ | Khi nào | Phù hợp? |
|--------|---------|----------|
| **Không cần làm gì** | Bài toán không tồn tại | ❌ Không phù hợp (đã chứng minh có bài toán) |
| **Rule-based** | Bài toán đơn giản, deterministic | ❌ Không phù hợp (câu trả lời AI vô số biến thể) |
| **ML cổ điển** | Cần tabular data, có training set | ❌ Không phù hợp (không có training data) |
| **LLM zero-shot** | Cần parse text tự nhiên | ⚠️ Có thể, nhưng thiếu tools |
| **LLM + Tools** | Cần verify với external source | ✅ **Phù hợp nhất** (parser + Tavily cross-check) |
| **AI Agent** | Cần nhiều bước lặp + HITL + closed-loop | ✅ **Phù hợp nhất cho 5 tuần** |

→ **Chọn: AI Agent với LLM + Tools (Tavily) + HITL + Closed-loop.**

---

## 16. Reward function

```python
reward = (
    + 1.0 if mention_extraction_f1 >= 0.85
    + 1.0 if stability_filter_false_alert_reduction >= 0.30
    + 1.0 if hallucination_recall >= 0.80
    + 1.0 if diagnosis_evidence_support_rate >= 0.70
    + 1.0 if action_acceptance_rate >= 0.60
    + 1.0 if rescan_classification_accuracy >= 0.75
    + 0.5 if cost_per_scan <= $0.30
    + 0.5 if stability_score_avg >= 0.7
    - 2.0 if closed_loop_misclassification_causes_wrong_action
    - 1.0 if hallucination_fn_on_price_or_ship > 0.05
)
```

**Trade-off FP vs FN:** FN > FP (mentioned recall trọng số cao hơn precision).

---

## 17. So sánh với 360 đề tài trong ngân hàng

Đã tìm trong `output/AI20K_Khoa3_4.pretty.json` với từ khóa: "GEO", "Generative Engine", "AI visibility", "AI search", "brand monitoring", "AI mention", "ChatGPT mention", "AI citation", **"E-commerce GEO"**, **"Shopee AI visibility"**, **"AI recommendation shop"**, **"Tavily"**. **Không tìm thấy đề tài nào trực tiếp về GEO/AI visibility tracking cho E-commerce.**

Các đề tài liên gần nhất:
- **MKT-12:** Brand sentiment analysis trên social media
- **DATA-08:** Web scraping + analytics (generic)
- **EDU-19:** AI-powered content recommendation (khác hoàn toàn)
- **ECOM-??:** Vài đề tài E-commerce focus recommendation/personalization

**Kết luận:** Đề tài **GEO Agent cho E-commerce VN** hoàn toàn mới, tập trung sâu vào 1 vertical cụ thể, không trùng lặp.

---

# 🟢 PART 3 — LÀM NHƯ THẾ NÀO (HOW)

> **Mục đích PART 3:** Kiến trúc hệ thống, tech stack, schema DB, roadmap 5 tuần (Tuần 0 chuẩn bị + Tuần 1–5 chạy chính), phân công nhóm, KPI, rủi ro, câu pitch. Phần này dùng khi code, planning sprint, demo.

## 18. Hệ thống AI = Model + Context + Planning + Tools

### 18.1. Model

| Tác vụ | Model | Lý do |
|--------|-------|-------|
| Parse câu trả lời AI về shop mention | GPT-4o-mini hoặc Claude Haiku | Rẻ, đủ tốt cho NER/sentiment |
| Phân tích sentiment | Claude Sonnet hoặc GPT-4o | Cần hiểu sarcasm/nuance E-commerce |
| Cross-check hallucination giá/ship | GPT-4o + **Tavily** | Verify với Shopee/Lazada/web shop |
| Embedding (clustering prompts) | text-embedding-3-small | Rẻ, hiệu quả |
| Tavily-grounded response | **Tavily API** | Citation built-in, depth control, rẻ hơn Google |

### 18.2. Context (Tri thức E-commerce)

- **Brand/Shop profile database:** Tên shop, URL Shopee/Lazada/Tiki/web, ngành hàng, 2–3 đối thủ, **giá sản phẩm chính thống, chính sách ship/đổi trả, thông tin uy tín (rating, số đơn)**.
- **Prompt library E-commerce:** ~100 prompt chia 5 nhóm (uy tín, giá, so sánh, review sản phẩm, ship/dịch vụ).
- **Historical scan results:** Phát hiện shift visibility và shift giá/ship.
- **Citation source map E-commerce:** Shopee reviews, Lazada ratings, Tinhte, Voz, Vatgia, blog review, báo, YouTube.

### 18.3. Planning & Tools

- **Planning:** LiteLLM (multi-model routing) cho MVP, có thể upgrade LangGraph sau.
- **Tools:** OpenAI API, Anthropic API, Google AI Studio, **Tavily API**, Playwright (fallback cho Shopee/Lazada).

---

## 19. Kiến trúc giải pháp Agent

### 19.1. Sơ đồ tổng quan

```text
[Brand KB E-commerce (2 brand + đối thủ)]   [Prompt Library ~100 prompts / 5 nhóm]
     │                                                  │
     ▼                                                  ▼
[Scheduler] → [Prompt Runner (4 AI: ChatGPT+Gemini+Claude+Tavily, 3 lần/ngày)]
                       │
                       ▼
              [PostgreSQL: raw responses + ai_engine metadata]
                       │
                       ▼
            [Visibility + Stability Engine]
                       │
                       ▼
                [Stability Filter (≥ 0.7)]
                  │         │
       <threshold>           <threshold>
              │              │
              ▼              ▼
        [Action Backlog]   [Observation DB]
              │
              ▼
       [Diagnosis Agent]
              │
   ┌──────────┼──────────┬──────────┐
   ▼          ▼          ▼          ▼
[fetch_citations] [compare_brand] [content_gap] [schema_check (Product/Review)]
   │          │          │          │
   └──────────┴──────────┴──────────┘
                       │
                       ▼
              [Evidence Package]
                       │
                       ▼
        [Action Recommender cho E-commerce]
                       │
                       ▼
             [HITL UI: duyệt/sửa (2 brand)]
                       │
                       ▼
              [Task DB / Board]
                       │
                       ▼ (khi task done)
        [Re-scan Engine] (3 lần / prompt × 4 AI)
                       │
                       ▼
       [Bootstrap CI: Improved/No evidence/Regressed]
                       │
                       ▼
             [Evaluation Report (per brand, per action)]
```

### 19.2. Tech stack

| Thành phần | Công nghệ |
|------------|-----------|
| **Frontend** | Next.js 14, Tailwind CSS, Recharts (dashboard E-commerce) |
| **Backend** | FastAPI (Python 3.11), Node.js (cho scheduler) |
| **Database** | PostgreSQL, Redis (cache), Qdrant (vector DB cho prompt E-commerce embedding) |
| **LLM orchestration** | LiteLLM (multi-model routing), LangGraph (Python) |
| **AI APIs (LLM)** | OpenAI (GPT-4o-mini, GPT-4o), Anthropic (Claude Haiku/Sonnet), Google AI Studio (Gemini) |
| **Web-grounded search** | **Tavily API** (citation + cross-check giá/ship/uy tín trên Shopee/Lazada/web shop) |
| **Scraper/parser** | Playwright (fallback cho Shopee/Lazada/Tiki khi Tavily không đủ fresh) |
| **Scheduler** | Celery + Redis |
| **Monitoring** | DeepEval, Ragas (cho AI eval), Prometheus + Grafana |
| **Deployment** | Docker, AWS/GCP free tier, Vercel (frontend) |

### 19.3. Cấu trúc dữ liệu (SQL schema)

```sql
-- Raw response (4 nguồn AI: ChatGPT, Gemini, Claude, Tavily)
CREATE TABLE responses (
  id SERIAL PRIMARY KEY,
  brand_id INT,                  -- 2 brand E-commerce (sàn + D2C)
  prompt_id INT,
  ai_engine TEXT,                -- 'chatgpt' | 'gemini' | 'claude' | 'tavily'
  model_version TEXT,
  response_text TEXT,
  citations JSONB,               -- URL citation mà AI/Tavily tham chiếu
  run_index INT,                 -- 1, 2, 3 (3 lần/prompt/ngày cho Stability)
  created_at TIMESTAMP
);

-- Extracted mention
CREATE TABLE mentions (
  id SERIAL PRIMARY KEY,
  response_id INT REFERENCES responses(id),
  brand_name TEXT,
  is_target_brand BOOLEAN,
  position INT,                  -- 1, 2, 3...
  sentiment FLOAT,               -- -1 to 1
  context_quote TEXT,
  claim_type TEXT                -- 'price' | 'ship' | 'review' | 'general'
);

-- Stability Score per prompt
CREATE TABLE stability_scores (
  id SERIAL PRIMARY KEY,
  brand_id INT,
  prompt_id INT,
  stability_score FLOAT,         -- 1 - normalized variance
  visibility_rate FLOAT,
  is_stable BOOLEAN,             -- TRUE if score >= 0.7
  computed_at TIMESTAMP
);

-- Diagnosis output
CREATE TABLE diagnoses (
  id SERIAL PRIMARY KEY,
  brand_id INT,
  prompt_id INT,
  is_stable BOOLEAN,
  stability_score FLOAT,
  hypotheses JSONB,              -- [{hypothesis, confidence, evidence_urls}]
  recommended_actions JSONB,
  status TEXT,                   -- 'pending_review' | 'approved' | 'rejected'
  reviewed_by TEXT,
  reviewed_at TIMESTAMP
);

-- Task tracking
CREATE TABLE tasks (
  id SERIAL PRIMARY KEY,
  brand_id INT,
  diagnosis_id INT REFERENCES diagnoses(id),
  action_type TEXT,              -- 'listing_update' | 'schema_add' | 'outreach' | 'content_pr'
  owner_team TEXT,
  status TEXT,                   -- 'todo' | 'in_progress' | 'done'
  pre_scan_id INT,
  post_scan_id INT,
  result TEXT,                   -- 'improved' | 'no_evidence' | 'regressed'
  ci_lower FLOAT,                -- bootstrap CI lower bound
  ci_upper FLOAT                 -- bootstrap CI upper bound
);
```

---

## 20. Roadmap 5 tuần

### 20.1. Tuần 0 (Tuần chuẩn bị — 1 tuần trước khi bắt đầu chính thức)

- Đăng ký API: OpenAI (ChatGPT), Anthropic (Claude), Google AI Studio (Gemini), **Tavily**.
- Chọn **2 brand E-commerce demo** (1 sàn + 1 D2C), mỗi brand có 2–3 đối thủ trực tiếp.
- Thu thập **brand knowledge base cho E-commerce:** URL Shopee/Lazada/web, bảng giá, FAQ, chính sách ship/đổi trả, thông tin uy tín.
- Liệt kê **~100 prompt tiếng Việt** chia **5 nhóm**.
- Tạo **gold dataset nhỏ (50–100 mẫu)** gán nhãn thủ công.

### 20.2. Tuần 1: Foundation + Stability-aware Baseline

- Xây **prompt library ~100 prompt** chia 5 nhóm.
- Xây **prompt runner**: gửi **3 lần / prompt / ngày** đến **4 nguồn AI**.
- Lưu raw response vào database (PostgreSQL).
- Tính visibility rate, mention position, SOV per ngành hàng, sentiment, **Stability Score** = 1 - normalized variance.
- **Stability Filter**: chỉ gap có **Stability Score ≥ 0.7** mới đưa vào diagnosis.
- Dashboard cơ bản (Next.js) hiển thị bảng + biểu đồ trend per ngành hàng.
- **Deliverable:** baseline scan report cho **2 brand + 4–6 đối thủ** với Stability Score.

### 20.3. Tuần 2: Diagnosis & Evidence Agent

- Xây **parser**: extract shop mention, context, citation URL bằng LLM (GPT-4o-mini).
- Xây **stability filter**: chỉ đưa gap vào diagnosis khi vượt ngưỡng ổn định (≥ 0.7).
- Xây **diagnosis tools cho E-commerce:**
  - `fetch_citations` — lấy URL AI/Tavily đang tham chiếu.
  - `compare_with_brand_source` — so sánh claim AI về **giá/ship/uy tín** với bảng giá/Shopee-Lazada listing/web shop.
  - `detect_content_gap` — kiểm tra trang web shop có đủ thông tin không.
  - `schema_check` — kiểm tra schema.org Product/Offer/Review.
- Xây **Tavily-grounded citation extractor**.
- Cross-check giá/ship claim với **Tavily web search + Shopee/Lazada public data**.
- Xây **evidence package**: URL + quote span + ngày truy cập + confidence.
- **Deliverable:** Diagnosis output cho ít nhất 5 gap thực tế của 2 brand E-commerce.

### 20.4. Tuần 3: Action Plan + Human-in-the-loop UI

- Xây **action recommender cho E-commerce**: đề xuất 1–3 action có bằng chứng:
  - Cập nhật listing Shopee/Lazada (schema Product, mô tả SEO).
  - Cập nhật nội dung web shop (FAQ, bảng giá, chính sách).
  - Thêm schema FAQ cho trang Y.
  - Outreach để cập nhật citation Z (Tinhte, Voz).
  - Tạo bài PR chất lượng cao trên blog.
- Xây **HITL UI**: dashboard hiển thị action, marketer duyệt / sửa / từ chối.
- Xây **task board** đơn giản (database).
- **Deliverable:** Action backlog có cấu trúc + workflow duyệt cho 2 brand.

### 20.5. Tuần 4: Closed-loop Re-measurement (tính năng nâng cao)

- Sau khi marketer E-commerce đánh dấu task "hoàn thành", hệ thống tự động **re-scan các prompt E-commerce liên quan** (3 lần / prompt, 4 nguồn AI).
- Tính **pre/post difference** với **bootstrap 95% CI**.
- Phân loại kết quả:
  - `Improved signal` (vượt noise floor 5–7 điểm %)
  - `No clear evidence` (chưa đủ dữ liệu)
  - `Regressed` (giảm)
- Xuất **evaluation report** cho từng task.
- **Đặc thù E-commerce:** Trong mùa sale (11.11, 12.12), closed-loop giúp biết action nào thật sự tăng visibility.
- **Deliverable:** Evaluation report của ít nhất 6 task (3 task × 2 brand).

### 20.6. Tuần 5: Polish + Demo + Gửi 2 doanh nghiệp duyệt

- Load test + cost optimization (chọn model phù hợp, tối ưu Tavily API calls).
- Viết tài liệu hướng dẫn sử dụng (cho marketer E-commerce).
- Quay demo video (5–10 phút) focus case 2 brand E-commerce.
- Viết **báo cáo đề xuất giải pháp** gửi 2 doanh nghiệp E-commerce.
- Chuẩn bị slide pitch (10–15 slide).
- Tổng kết evaluation: precision/recall, false alert rate, cost per scan, **Stability Score trung bình, Closed-loop classification accuracy**.

### 20.7. Tổng kết timeline

| Tuần | Output chính | KPI tuần |
|------|--------------|----------|
| 0 (prep) | API key (4 AI), brand profile 2 brand, prompt list 100, gold dataset | Dataset + brand profile ready |
| 1 | Baseline scan + dashboard cho 2 brand E-commerce + Stability Score | Dashboard chạy, ≥600 raw responses, Stability Score tính được |
| 2 | Diagnosis output cho 5 gap | 5 evidence packages có URL + quote (cho cả 2 brand) |
| 3 | Action backlog + HITL UI | 10+ actions được duyệt (chia đều 2 brand) |
| 4 | Closed-loop evaluation report | 6 reports (3 task × 2 brand) phân loại Improved/No evidence/Regressed |
| 5 | Demo video + báo cáo cho 2 brand | Precision ≥85%, Closed-loop ≥75% phân loại đúng |

---

## 21. Phân công nhóm 4 người

| Thành viên | Vai trò | Tuần 0–2 | Tuần 3–5 |
|------------|---------|----------|----------|
| **Đăng (Tech Lead)** | Backend chính + Database | FastAPI + PostgreSQL schema (4 AI + Stability + Task) + scheduler + API endpoints | Action recommender + Closed-loop re-scan engine + eval |
| **Lý (Agent Engineer)** | Orchestration + Tavily tools | Prompt runner (4 AI) + parser LLM + **Tavily cross-check giá/ship** + diagnosis agent | HITL UI logic + Tavily-grounded citation extractor |
| **Khôi (Data/NLP)** | Prompt Library E-commerce + Eval | Gold dataset 2 brand + prompt library ~100 prompt / 5 nhóm + stability analysis | Evaluation reports + precision/recall + bootstrap CI |
| **Hải (Frontend/Infra)** | UI + Deployment | Next.js dashboard E-commerce + chart viz | HITL approval UI + alert system (giá/ship hallucination) + demo deployment |

---

## 22. Đo lường thành công & demo flow

### 22.1. Metrics kỹ thuật (E-commerce)

| Metric | Baseline | Target MVP | Cách đo |
|--------|----------|------------|---------|
| **Mention extraction F1** | — | ≥ 0.85 | Gold dataset E-commerce 50–100 mẫu |
| **Stability Score** | Single-run baseline | ≥ 0.7 cho mỗi gap (gate cho diagnosis) | Tính từ 3 lần chạy/prompt/ngày |
| **Stability filter precision** | Single-run baseline | False alert giảm ≥ 30% | So sánh với chạy 1 lần |
| **Hallucination detection (giá/ship/uy tín)** | Không đo được | Recall ≥ 80% trong 24h | Manual review 20 cases |
| **Diagnosis evidence support rate** | Single LLM | ≥ 70% hypothesis có URL + quote | Manual review 20 diagnoses |
| **Action acceptance rate** | — | ≥ 60% marketer duyệt không sửa | Đếm trên 10 actions/brand |
| **Re-scan classification accuracy** | — | ≥ 75% đúng Improved/No evidence/Regressed | Manual review 6 reports (3 × 2 brand) |
| **Cost per scan** | — | ≤ $0.30 / scan (30 prompt × 3 lần × 4 AI) | Đếm API usage |

### 22.2. Demo flow (5–10 phút)

1. Mở dashboard → giới thiệu **2 brand E-commerce demo** (1 sàn + 1 D2C) + 4–6 đối thủ.
2. Hiển thị baseline scan → visibility rate, SOV per ngành hàng, trend.
3. Highlight một gap "AI nói sai giá sản phẩm X" → show Stability Score đã ổn định (≥ 0.7).
4. Mở diagnosis → show evidence package (URL + quote + Tavily cross-check với Shopee/Lazada + hypothesis + confidence).
5. Mở action plan → show 1–3 actions cho mỗi brand, marketer duyệt ngay trên UI.
6. Mở evaluation report (sau khi mock-complete task) → show pre/post với bootstrap CI.
7. Tổng kết → cost, time saving, ROI ước tính cho cả 2 brand E-commerce.

### 22.3. Cách demo tính năng nâng cao

Tính năng nâng cao là **closed-loop re-measurement**:

- Chuẩn bị sẵn 1 task đã mock-complete trong tuần 4.
- Trước mặt doanh nghiệp, bấm "re-scan" → hệ thống chạy 3 lần/prompt → show report.
- Giải thích: *"Đây là phần khác biệt so với Profound/Peec/Otterly/Kompa — họ dừng ở task, chúng tôi đo lại và báo hiệu quả có ý nghĩa thống kê."*

---

## 23. Rủi ro & hành động giảm thiểu (E-commerce focus)

| Rủi ro | Xác suất | Tác động | Giảm thiểu |
|--------|----------|----------|------------|
| API key không được duyệt / quota hết (4 AI) | Trung bình | Cao | Đăng ký sớm tuần 0; fallback scraper (Playwright cho Shopee/Lazada) |
| Câu trả lời AI không ổn định → nhiễu | Cao | Trung bình | Chạy lặp ≥ 3 lần, **Stability filter ≥ 0.7** |
| **Tavily cache cũ → cross-check sai giá** | Trung bình | Cao | Scrape trực tiếp Shopee/Lazada cho critical claim |
| **Hallucination giá/ship tolerance rất thấp** | Trung bình | Cao | HITL chặt, alert trong 24h, severity theo mức ảnh hưởng |
| Brand knowledge base sai/cũ | Trung bình | Trung bình | Versioning + cho phép marketer sửa + scrape lại hàng tuần |
| Gold dataset quá nhỏ | Cao | Trung bình | Tăng dần 50–100 mẫu, dùng bootstrap |
| Agent đề xuất action sai | Trung bình | Trung bình | HITL bắt buộc, đo acceptance rate |
| Task "đúng" nhưng visibility không tăng | Cao | Trung bình | Báo "no evidence" thay vì ép kết luận |
| Cost vượt budget | Trung bình | Trung bình | Giới hạn prompt × 3 lần / ngày, dùng GPT-4o-mini |
| Team không quen LLM orchestration | Trung bình | Thấp | Dùng LiteLLM thay về LangGraph cho MVP |
| Không tìm được 2 SME E-commerce duyệt | Trung bình | Cao | Liên hệ sớm tuần 0; demo với brand giả định + disclaimer |
| **Đối thủ quốc tế vào E-commerce VN** | Thấp | Trung bình | Focus tiếng Việt + giá rẻ + chuyên biệt E-commerce |

---

## 24. Câu pitch đề xuất

### 24.1. Pitch 30 giây (mentor/thầy)

> *"Chúng em xây dựng **GEO AI Agent cho E-commerce Việt Nam** — theo dõi AI visibility cho shop/brand E-commerce trên **ChatGPT, Gemini, Claude và Tavily** (web-grounded). Tập trung vào **đo lặp có kiểm soát** (Stability-aware Monitoring — khắc phục vấn đề AI không ổn định theo Schulte et al.), **evidence-grounded diagnosis** (Tavily cross-check giá/ship/uy tín với Shopee/Lazada/web shop + citation URL + trích dẫn), và **closed-loop evaluation** (đo lại sau khi thực hiện với bootstrap CI). 2 tính năng cốt lõi + 1 tính năng nâng cao nổi bật. Phạm vi 5 tuần: **2 brand E-commerce demo** (1 sàn + 1 D2C) + 4–6 đối thủ + ~100 prompt tiếng Việt chia 5 nhóm."*

### 24.2. Pitch 1–2 phút (doanh nghiệp E-commerce)

> *"Hiện nay nhiều công cụ GEO đã có mặt — từ Profound, Peec AI, Otterly ở nước ngoài cho đến Kompa GEO, Fast Marketing ở Việt Nam. Tuy nhiên, các công cụ này thường gặp 3 hạn chế: (1) chạy prompt 1 lần rồi vẽ dashboard, nhưng nghiên cứu học thuật cho thấy AI không ổn định — cần đo lặp ≥7 lần; (2) đề xuất action chung chung, thiếu bằng chứng; (3) không đo lại hiệu quả sau khi team thực hiện.*
>
> *Chúng tôi xây dựng một công cụ nhỏ gọn tập trung vào 3 điểm này: đo lặp có kiểm soát, evidence-grounded diagnosis với Tavily cross-check giá/ship/uy tín trực tiếp với Shopee/Lazada/web shop + URL và trích dẫn thật, và closed-loop evaluation với bootstrap CI. Trong 5 tuần, chúng tôi sẽ demo với **2 brand E-commerce** của anh/chị: chạy **~100 prompt tiếng Việt** trên **4 nguồn AI**, tìm các gap có bằng chứng, đề xuất action cụ thể, và đo lại hiệu quả sau khi team thực hiện."*

### 24.3. Pitch tính năng nâng cao

> *"Điểm khác biệt của chúng tôi là closed-loop evaluation: sau khi marketer đánh dấu task xong, hệ thống tự động re-scan và báo cáo 'Improved signal' / 'No clear evidence' / 'Regressed' với bootstrap confidence intervals. Phần này chưa thấy công cụ nào tại Việt Nam công khai làm tốt."*

---

## 25. Cam kết & giới hạn

### 25.1. Cam kết trung thực

- ✅ Tất cả số liệu thị trường đều có nguồn công khai và đã cite trong tài liệu.
- ✅ Mọi con số ước lượng được ghi rõ `[Ước lượng]`.
- ✅ Anti-patterns đã được phân tích thẳng thắn.
- ✅ HITL boundary xác định rõ, với 2 brand demo cụ thể (1 sàn + 1 D2C).
- ✅ Scope 5 tuần với 4 nguồn AI — bám sát hướng dẫn mentor (tập trung sâu).

### 25.2. Giới hạn cần nhóm xác minh

1. **Lựa chọn 2 brand demo cụ thể.** Chưa chốt tên. Cần theo tiêu chí: có mặt trên AI, có 2–3 đối thủ, có data public dễ verify, có thể liên hệ stakeholder.
2. **Chi phí vận hành** (< 4 triệu VND/tháng) phụ thuộc lượng prompt + model. Cần benchmark tuần 1. **Lưu ý:** Tavily pricing cần verify cho production.
3. **Precision/recall target** (≥85%) dựa ngành tương tự. Cần verify với gold dataset E-commerce.
4. **Hallucination detection accuracy** phụ thuộc brand profile DB + Tavily freshness. E-commerce đổi giá/ship theo giờ → cần scrape fallback cho critical claim.

### 25.3. Rủi ro E-commerce focus (xem chi tiết phần 23)

### 25.4. Khuyến nghị cho nhóm

1. Đọc kỹ PART 1 (WHY) và PART 3 (HOW) trước khi quyết định.
2. **Tuần 0 là then chốt:** Baseline scan E-commerce với 4 nguồn AI phải chạy sớm. Đặc biệt verify **Tavily** cho tiếng Việt + Shopee/Lazada.
3. **Chọn 2 brand E-commerce cẩn thận:** Ưu tiên brand có stakeholder có thể liên hệ, có data public nhiều, có 2–3 đối thủ rõ ràng. Tránh quá lớn (Tiki, Shopee) hoặc quá nhỏ.
4. **HITL cho hallucination giá/ship phải chặt:** E-commerce sai 1 câu = mất khách.
5. **Demo cuối kỳ phải show:** (a) Visibility Rate + SOV cho 2 brand, (b) ít nhất 1 hallucination giá/ship phát hiện & verified, (c) 1 closed-loop report phân loại Improved/No evidence.

---

# 📌 PHỤ LỤC

## A. Tóm tắt quyết định

| Tiêu chí | Đánh giá |
|----------|----------|
| **Bài toán có thật?** | ✅ 36% discover brand qua AI, 30% trust AI. 21,5M AI traffic VN +740% YoY. E-commerce VN ~22 tỷ USD 2025. |
| **AI có lợi thế?** | ✅ LLM parse text tự nhiên + Tavily web-grounded cho citation giá/ship. |
| **Quy trình không scale?** | ✅ 80h/tháng cho 2 brand × 4 AI × 2–3 đối thủ. |
| **Có căn cứ học thuật?** | ✅ Schulte et al. + arXiv 2603.08924 + Tian et al. |
| **Có điểm khác biệt?** | ✅ Stability + Evidence-grounded + Closed-loop. Kompa/Profound/Peec/Otterly đều dừng ở task. |
| **5 tuần khả thi?** | ✅ Tuần 0 prep + 5 tuần chạy chính. |
| **Phù hợp team 4 người?** | ✅ Backend (Đăng) + Agent/Tavily (Lý) + Data/NLP (Khôi) + Frontend (Hải). |
| **Có thị trường?** | ✅ SME E-commerce VN (Shopee/Lazada/Tiki, D2C, retailer). |
| **Có đối thủ?** | ⚠️ Kompa, Profound, Peec, Otterly. **Tavily-grounded cho E-commerce VN chưa ai làm.** |
| **Thương mại hóa?** | ✅ $20–50/tháng cho SME E-commerce VN (rẻ hơn Semrush 3–7×). |

**Kết luận:** Đề xuất **GEO AI Agent cho E-commerce VN** (2 brand demo, 4 AI: ChatGPT + Gemini + Claude + Tavily, 5 tuần) **hợp lý và bám sát lựa chọn của nhóm** — bài toán kinh doanh đã đo lường bằng dữ liệu, AI Agent là phương án duy nhất scale được với chi phí chấp nhận được.

**Scope chốt với nhóm:**
- **Đối tượng:** Marketing Manager / CMO của **SME E-commerce Việt Nam**.
- **Phạm vi thời gian:** **5 tuần**.
- **Phạm vi kỹ thuật:** **4 nguồn AI** (ChatGPT + Gemini + Claude + Tavily) × **Thương mại điện tử** × **2 brand demo** (1 sàn + 1 D2C, mỗi brand kèm 2–3 đối thủ).
- **Phạm vi ngôn ngữ:** Tiếng Việt.
- **Mục tiêu cuối:** Giảm 90% thời gian GEO monitoring, tăng 10× prompt coverage, phát hiện ≥ 80% hallucination (đặc biệt về giá/ship/uy tín) trong 24h, đo lại hiệu quả action với bootstrap CI.

---

## B. Nguồn tham khảo tổng hợp

### Nghiên cứu học thuật (căn cứ cho phương pháp luận)

1. **Schulte et al. (2026).** "Don't Measure Once: Measuring Visibility in AI Search (GEO)." [arXiv 2604.07585](https://arxiv.org/abs/2604.07585) — Nền tảng cho Stability-aware Monitoring.
2. **"Quantifying Uncertainty in AI Visibility: A Statistical Framework" (2026).** [arXiv 2603.08924](https://arxiv.org/abs/2603.08924) — Nền tảng cho Closed-loop Re-measurement.
3. **Tian et al. (2026).** "Diagnosing and Repairing Citation Failures in GEO / AgentGEO." [arXiv 2603.09296](https://arxiv.org/abs/2603.09296) — Nền tảng cho Evidence-grounded Diagnosis.
4. **Martinez (2026).** "Optimizing Visibility in Generative Engines: A Critical Survey of GEO (2023–2026)." [arXiv 2607.14035](https://arxiv.org/abs/2607.14035)
5. **Kim et al. (2026).** "SAGEO Arena: A Realistic Environment for Evaluating Search-Augmented GEO." [arXiv 2602.12187](https://arxiv.org/abs/2602.12187)
6. **Aggarwal et al. (2023).** "GEO: Generative Engine Optimization." [arXiv 2311.09785](https://arxiv.org/abs/2311.09785)
7. **Gao et al. (EMNLP 2023).** "ALCE: Automatic LLMs' Citation Evaluation."

### Sản phẩm quốc tế (đối thủ cạnh tranh)

1. **Profound** — enterprise GEO platform: [tryprofound.com](https://www.tryprofound.com/features/agents/content-optimization). $99–499/tháng.
2. **Peec AI** — AI search analytics: [peec.ai](https://peec.ai/). €85–95/tháng.
3. **Otterly.AI** — AI search monitoring: [otterly.ai](https://otterly.ai/). $29/tháng.
4. **Writesonic GEO Action Center**: [docs.writesonic.com/docs/action-center-actionables](https://docs.writesonic.com/docs/action-center-actionables)
5. **Semrush AI Visibility Toolkit**: $139–199/tháng.
6. **Ahrefs Brand Radar**: $199/tháng.
7. **AthenaHQ, Scrunch AI, Evertune, Orion, Ranketta, Daydream, BrightEdge, Conductor, Surfer, MarketMuse, SE Ranking, Ayzeo, Loudmink, HubSpot AEO** — các platform khác.

### Sản phẩm tại Việt Nam (đối thủ và tham khảo)

1. **Kompa GEO**: [kompa.ai/giai-phap/kompa-geo](https://kompa.ai/giai-phap/kompa-geo) — 4 AI, real prompt discovery.
2. **Hashmeta AI**: [hashmeta.ai blog Vietnam](https://www.hashmeta.ai/en/blog/geo-for-vietnam-the-emerging-ai-search-opportunity-vietnamese-brands-cannot-ignore)
3. **Fast Marketing**: [fastmarketing.com.vn/dich-vu-geo](https://fastmarketing.com.vn/dich-vu-geo)
4. **SEO Dạo**: [seodao.vn](https://seodao.vn/dich-vu-geo-seodao/)
5. **DigiAI Platform**: [vndigitech.com/phan-mem/digiai-platform](https://vndigitech.com/phan-mem/digiai-platform/)

### Báo cáo thị trường & số liệu Việt Nam

1. **Decision Lab (2025).** "State of Consumer AI in Vietnam 2025." 78% người dùng AI, ChatGPT 81%, Gemini 51%, 36% discover brand qua ChatGPT, 30% trust AI.
2. **SimilarWeb Vietnam (07/2025).** 21,5 triệu AI referrals, tăng 740% YoY.
3. **Q&Me Vietnam (2025) & VECOM.** Báo cáo TMĐT VN 2025. ~22 tỷ USD, tăng 20% YoY. SME E-commerce chiếm ~70% gian hàng.
4. **AppLabX (2026).** "155 AI Search and GEO in Vietnam Statistics."
5. **Vietnam.vn (2025).** "When ChatGPT becomes the new touchpoint."
6. **Ninja Van Vietnam E-commerce Reports (2025-2026).** Hành vi mua hàng online, top ngành hàng.

### Báo cáo đánh giá sản phẩm

1. **"Profound vs Otterly vs Peec AI"** — Growth Engineer: [growthengineer.ai](https://growthengineer.ai/blog/profound-vs-otterly-vs-peec-ai)
2. **"AEO & AI Visibility Tools Compared"** — Orion: [useorion.ai/compare](https://useorion.ai/compare)
3. **"GEO Platforms Compared 2026"** — Ayzeo: [ayzeo.com/comparisons/geo-platforms-compared](https://ayzeo.com/comparisons/geo-platforms-compared)
4. **"Best AEO and GEO Tools 2026"** — Clarity Digital: [claritydigital.agency/blog/best-aeo-geo-tools-2026](https://claritydigital.agency/blog/best-aeo-geo-tools-2026)
5. **"12 GEO KPIs: Formulas, Benchmarks, and Cadence Guide"** — Maximus Labs: [maximuslabs.ai](https://www.maximuslabs.ai/ai-search-101/geo/measurement/metrics-kpis)

### Công cụ & API cho demo

1. **Tavily (2026).** [tavily.com](https://tavily.com/) — Web-grounded search API tối ưu cho AI agent, pricing rẻ, citation built-in, hỗ trợ tiếng Việt.
2. **OpenAI API** (GPT-4o-mini, GPT-4o).
3. **Anthropic API** (Claude Haiku, Claude Sonnet).
4. **Google AI Studio API** (Gemini).
5. **Shopee Vietnam Seller Center, Lazada University (2026).** Listing optimization, schema, chính sách shop.
6. **Diễn đàn E-commerce VN: Tinhte.vn, Voz.vn, Vatgia.com.** Nguồn review sản phẩm/shop quan trọng cho AI search.

---