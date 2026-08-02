# Slide Outline — 10-15 slide

## Slide 1: Title
- GEO AI Agent cho E-commerce Việt Nam
- Nhóm: Đăng, Lý, Khôi, Hải
- Ngày: 2026-08-02

## Slide 2: Vấn đề
- 36% người dùng VN discover brand qua AI
- 30% trust AI recommendation
- E-commerce VN ~22 tỷ USD 2025
- **SME E-commerce không biết AI đang nói gì về shop mình**

## Slide 3: Khoảng trống thị trường
- Kompa, Profound, Peec, Otterly: đều dừng ở "task do con người xử lý"
- KHÔNG có ai làm **closed-loop re-measurement**
- KHÔNG có ai focus chuyên E-commerce VN với giá rẻ

## Slide 4: Giải pháp
- 3 trụ cột:
  1. **Stability-aware Monitoring** (đo lặp ≥ 3 lần)
  2. **Evidence-grounded Diagnosis** (citation URL + Tavily cross-check)
  3. **Closed-loop Re-measurement** (đo lại sau action với bootstrap CI)

## Slide 5: Kiến trúc tổng quan
- Sơ đồ data flow (xem shared/docs/data_flow.md)
- 4 nguồn AI: ChatGPT + Gemini + Claude + Tavily
- 2 brand demo: 1 sàn + 1 D2C

## Slide 6: Tech stack
- Backend: FastAPI + PostgreSQL + Redis + Celery
- Agent: LiteLLM + Tavily
- Frontend: Next.js 14 + Tailwind + Recharts
- Analysis: numpy + scipy + bootstrap CI

## Slide 7: Demo flow (5-10 phút)
- Mở dashboard
- 2 brand + 4-6 đối thủ
- Visibility + SOV charts
- Highlight 1 gap có evidence → diagnosis → action → closed-loop

## Slide 8: Kết quả demo
- Mention extraction F1: ? (target ≥ 0.85)
- Stability Score avg: ? (target ≥ 0.7)
- Hallucination recall: ? (target ≥ 80%)
- Closed-loop accuracy: ? (target ≥ 75%)
- Cost per scan: ? (target ≤ $0.30)

## Slide 9: So sánh với đối thủ
| Tính năng | Kompa | Profound | Peec | **GEO Agent** |
|-----------|-------|----------|------|---------------|
| 4 nguồn AI | ✅ | ✅ | ⚠️ | ✅ |
| Tiếng Việt + E-commerce | ⚠️ | ❌ | ❌ | ✅ |
| Closed-loop | ❌ | ❌ | ❌ | ✅ |
| Evidence-grounded | ⚠️ | ✅ | ⚠️ | ✅ |
| Giá (SME VN) | ? | $99 | €85 | ~$30 |

## Slide 10: Căn cứ học thuật
- Schulte et al. arXiv 2604.07585 (2026) — Stability-aware
- arXiv 2603.08924 (2026) — Bootstrap CI
- Tian et al. arXiv 2603.09296 (2026) — Agentic repair

## Slide 11: KPI thực đạt
- Bảng 8-10 metric (từ slide 8)
- Highlight: closed-loop classification accuracy, đây là điểm khác biệt

## Slide 12: Bài học + hạn chế
- Bài học:
  - Tavily freshness với Shopee/Lazada cần scrape fallback
  - Sarcasm E-commerce khó detect, cần HITL
  - 3 lần/prompt compromise giữa cost và accuracy
- Hạn chế:
  - Chỉ 2 brand demo (mở rộng được)
  - Không monitor social media (TikTok, Facebook)

## Slide 13: Thương mại hóa
- Pricing: $20-50/tháng/brand (SME VN)
- ROI: < 4 triệu VND/tháng, tiết kiệm 20-30 triệu VND/năm
- 3 phân khúc: sàn TMĐT, D2C, retailer chuyển đổi số

## Slide 14: Next steps
- Scale lên 7-8 lần/prompt (production)
- Thêm peec.ai, Perplexity, Copilot
- Tích hợp social listening
- B2B SaaS (multi-tenant)

## Slide 15: Q&A
- Cảm ơn
- Link repo: github.com/...
- Liên hệ: email
