# Demo Script — 5-10 phút

> **Lead**: Lead tuần 5 (xoay vòng)
> **Ngày**: Tuần 5, ngày cuối
> **Khán giả**: Doanh nghiệp E-commerce + mentor + thầy

## Cấu trúc (8 phút)

### 1. Introduction (30s)
> "Chào anh/chị, hôm nay em xin demo GEO AI Agent cho E-commerce Việt Nam. Đây là công cụ theo dõi AI visibility cho shop/brand E-commerce trên **ChatGPT, Gemini, Claude và Tavily** (web-grounded). 3 trụ cột: Stability-aware Monitoring, Evidence-grounded Diagnosis, và **Closed-loop Re-measurement** — tính năng nổi bật so với Profound, Peec, Otterly, Kompa."

### 2. Bối cảnh + vấn đề (30s)
> "Trước khi mua hàng, 36% người dùng Việt hỏi AI. AI mention trở thành điểm chạm pre-purchase. Câu hỏi: shop mình có được AI nhắc đến không? AI có nói sai giá/ship không? Shop đối thủ đang đứng ở đâu?"

### 3. Demo 2 brand E-commerce (1 phút)
- Mở dashboard
- Show 2 brand: **Minh Long** (D2C) + **Shop bán đồ gia dụng TPHCM** (sàn)
- 4-6 đối thủ
- Highlight: 100 prompts đã scan, 4 nguồn AI, 3 lần/prompt

### 4. Visibility & SOV (1 phút)
- Biểu đồ visibility rate 7 ngày
- SOV per AI engine (ChatGPT: 42%, Gemini: 38%, ...)
- Highlight: **Brand target đang top 3 trong 3/4 AI**

### 5. Stability-aware (1 phút)
- Highlight 1 gap: "AI không nhắc brand target trong prompt uy tín"
- Show 3 lần chạy khác nhau → variance
- **Stability Score ≥ 0.7** → đủ gate, vào diagnosis
- Counter-example: 1 gap khác có variance cao → observation only

### 6. Evidence-grounded Diagnosis (1.5 phút)
- Mở diagnosis detail
- Show evidence package:
  - Citation URL AI đang tham chiếu
  - Tavily cross-check: claim "freeship TPHCM" vs Shopee listing
  - Hypothesis + confidence score
- Recommend 1-3 actions cụ thể

### 7. HITL Action (1 phút)
- Marketer "approve" diagnosis
- Task tự động tạo
- Sang task board, "đánh dấu xong"
- **Tính năng nâng cao**: closed-loop tự động re-scan

### 8. Closed-loop Re-measurement (1.5 phút)
- Mở evaluation report
- Pre vs Post visibility chart
- Bootstrap 95% CI bar
- **Verdict**: "Cải thiện" với CI > noise floor 6%
- Export PDF (optional)

### 9. Tổng kết + ROI (30s)
- So sánh: 80h/tháng → <8h/tháng (giảm 90%)
- Cost: $0.30/scan
- 4 doanh nghiệp đã pilot? (nếu có)
- Next steps: thêm brand, scale prompt library

## Tips

- **Máy chiếu full HD 1080p**
- **Hardcode dữ liệu backup** (nếu API chậm)
- **Tập trung vào closed-loop** — đó là tính năng KHÁC BIỆT
- **Tránh jargon** — giải thích "Stability Score" = "đo lặp để biết kết quả có ổn định không"
- **Backup video** — nếu live demo lỗi

## Câu hỏi dự kiến

- Q: Tại sao 3 lần mà không 7-8 lần?
  - A: Demo 5 tuần, cost compromise. Production có thể scale lên 7-8 lần.

- Q: Tavily có đủ fresh với Shopee/Lazada?
  - A: Có scrape fallback Playwright cho critical claim.

- Q: Làm sao biết AI nói đúng/sai?
  - A: Tavily cross-check + schema check + content gap detection, mark "requires HITL" cho mọi claim giá/ship.

- Q: Kompa/Profound khác gì?
  - A: Họ dừng ở "task do con người xử lý". Chúng tôi đo lại hiệu quả sau action bằng bootstrap CI — đó là closed-loop.
