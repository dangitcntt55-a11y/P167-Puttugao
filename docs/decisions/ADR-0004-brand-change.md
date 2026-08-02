# ADR-0004: Brand demo change — Đồ gia dụng → Điện tử

## Status
- [x] Accepted (2026-08-02)

## Context
- Data KB ban đầu (`data/brands/brand_1_d2c.json`, `brand_2_d2c.json`) đang là Minh Long + Lock&Lock (ngành đồ gia dụng), do Khôi (Data) khởi tạo ở Tuần 0 trước khi team chốt ngành chính thức.
- Ngày 2026-08-02, team đã chốt chọn **ngành điện tử** vì:
  - GEO gap rõ giữa "thực tế thị trường" và "AI visibility" (vd: Samsung VN được nhắc nhiều nhưng AI hay nói sai giá/policy VN).
  - Hallucination risk cao về giá/ship (lý tưởng cho Core Feature #2 Evidence-grounded Diagnosis).
  - Schema markup tốt → dễ demo Schema Audit.
  - 4-6 đối thủ cùng ngành → dễ tính SOV.

Brand mới chốt:
- **1 brand sàn**: Điện Máy Xanh (đa ngành điện máy, có nhiều SKU).
- **1 brand D2C**: Samsung Vietnam (entity riêng, content-driven).

## Decision
Update toàn bộ `data/brands/` theo ngành điện tử:

| Brand | Type | ID | Category |
|-------|------|----|---------| 
| Điện Máy Xanh | sàn (target) | 1 | điện máy/điện tử |
| Samsung Vietnam | D2C (target) | 2 | điện tử (điện thoại, TV, gia dụng) |
| Nguyễn Kim | competitor (cùng DMX) | 3 | điện máy |
| PICO | competitor (cùng DMX) | 4 | điện máy |
| FPT Shop | competitor (cùng DMX) | 5 | điện tử (phone/laptop) |
| CellphoneS | competitor (cùng Samsung) | 6 | điện thoại |
| Apple Vietnam | competitor (cùng Samsung) | 7 | điện thoại/laptop |
| Xiaomi Vietnam | competitor (cùng Samsung) | 8 | điện thoại |

## Consequences

### Positive
- Phù hợp với ngành điện tử — hot market ở VN, nhiều public data.
- Có 4 đối thủ trực tiếp cho DMX + 3 đối thủ cho Samsung → đủ so sánh SOV.
- AI engines thường có nhiều data sai về giá/policy VN (vd: ship fee, warranty) → dễ demo hallucination.

### Negative
- Phải thu thập lại KB cho 8 brand (URL, price table, ship policy).
- Prompt library mới (~100 prompt theo sub-agent #3) đã được viết cho DMX + Samsung → cần update lại prompt library nếu domain là electronics-specific.
- Schema DB không đổi (brand table generic) — nhưng content seed data cần update.

### Risks
- Nếu chưa verify URL thật (Shopee/Lazada/web) → risk cho Tavily cross-check.
- Nếu KB không khớp thực tế → model sẽ hallucinate response → diagnosis output sai.
- Có thể miss KB trong vòng 1 tuần đầu → Tuần 1 chỉ chạy với placeholder data.

## Implementation plan
1. Viết lại 3 file:
   - `data/brands/brand_1_san_dmx.json` (Điện Máy Xanh)
   - `data/brands/brand_2_d2c_samsung.json` (Samsung VN)
   - `data/brands/competitors.json` (6 đối thủ)
2. Xóa file cũ `brand_1_d2c.json`, `brand_2_d2c.json` sau khi xác nhận không ai còn reference.
3. Update `data/brands/README.md` để link tới file mới.
4. Verify tất cả URL Shopee/Lazada/web còn live (Khôi làm).
5. Update `data/prompts/*.json` nếu cần (đã viết theo DMX + Samsung sẵn).

## References
- ADR-0003 (tách ai_engine — schema đã chuẩn bị sẵn cho brand mới)
- GEO_AI_Agent_Ecommerce_VN.md §3 (scope: 1 sàn + 1 D2C + 4-6 đối thủ)
- tasks.md Tuần 0 (Khôi chọn brand)
