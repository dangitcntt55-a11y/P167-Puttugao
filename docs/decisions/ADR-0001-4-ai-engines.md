# ADR-0001: Chọn 4 nguồn AI (ChatGPT + Gemini + Claude + Tavily) thay vì 3

## Status
- [x] Accepted (2026-08-02)

## Context
- Đề tài GEO cần theo dõi AI visibility trên nhiều nguồn
- Tài liệu gốc đề cập nhiều tool: ChatGPT, Gemini, Claude, Tavily, Perplexity, Copilot
- Mentor + thầy yêu cầu tập trung 4 nguồn, không spread quá mỏng

## Decision
**Chọn 4 nguồn: ChatGPT + Gemini + Claude + Tavily**

Lý do:
- **ChatGPT**: 81% thị phần AI tại VN (Decision Lab 2025), không thể thiếu
- **Gemini**: 51% thị phần, quan trọng cho Google AI
- **Claude**: brand mention chất lượng cao, tốt cho evidence-grounded
- **Tavily**: web-grounded citation, đặc biệt quan trọng cho E-commerce VN (cross-check giá/ship với Shopee/Lazada)

## Consequences
### Positive
- Phủ 4 nguồn chính của E-commerce VN
- Tavily cho phép cross-check hallucination giá/ship — điểm khác biệt
- Đủ data để tính SOV + Stability Score có ý nghĩa

### Negative
- 4 API call × 3 lần × 100 prompts = 1200 calls/scan → cost ~$0.30/scan
- Phức tạp hơn nếu chỉ 2-3 nguồn

### Risks
- 1 API hết quota → fallback scraper (Playwright cho Shopee/Lazada)
- Tavily freshness với Shopee/Lazada cần verify ở tuần 0

## Alternatives considered
- **Option A**: Chỉ ChatGPT + Gemini → rẻ, nhưng mất 2 nguồn quan trọng
- **Option B**: 5-6 nguồn (thêm Perplexity, Copilot) → spread quá mỏng, cost cao
- **Option C**: Công cụ có sẵn (Profound, Peec) → đắt, không customization

## References
- Decision Lab 2025: State of Consumer AI in Vietnam
- GEO_AI_Agent_Ecommerce_VN.md §19 (kiến trúc)
