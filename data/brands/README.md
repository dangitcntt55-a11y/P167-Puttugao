# Brands — Knowledge Base cho 2 brand demo + 6 đối thủ

> **Format**: JSON với thông tin public dễ verify (URL Shopee/Lazada/web, bảng giá, FAQ, ship policy).
> **Quyết định**: chọn ngành **điện tử** theo `docs/decisions/ADR-0004-brand-change.md`.

## File trong folder này

| File | Mô tả | ID |
|------|-------|----|
| `brand_1_san_dmx.json` | Brand sàn target #1: **Điện Máy Xanh** | 1 |
| `brand_2_d2c_samsung.json` | Brand D2C target #2: **Samsung Vietnam** | 2 |
| `competitors.json` | 6 đối thủ: Nguyễn Kim, PICO, FPT Shop, CellphoneS, Apple VN, Xiaomi VN | 3-8 |
| `_ARCHIVED_brand_1_d2c_minhlong.json` | (Đã archive — Minh Long, đồ gia dụng, xem ADR-0004) | - |
| `_ARCHIVED_brand_2_d2c_locknlock.json` | (Đã archive — Lock&Lock, đồ gia dụng, xem ADR-0004) | - |

## Chọn 2 brand (theo tiêu chí trong `GEO_AI_Agent_Ecommerce_VN.md` §3)

- 1 brand sàn (multi-SKU, nhiều đối thủ): **Điện Máy Xanh**
- 1 brand D2C (entity riêng, content-driven): **Samsung Vietnam**
- Mỗi brand có 3 đối thủ trực tiếp cùng ngành hàng

## Lý do chọn ngành điện tử

- GEO gap rõ: Samsung VN được AI nhắc nhiều nhưng hay nói sai giá/policy VN → có gap để diagnose.
- Hallucination risk cao về giá/ship (giá điện tử biến động liên tục → AI dễ sai).
- Schema markup tốt → demo Schema Audit hiệu quả.
- 6 đối thủ cùng ngành → tính SOV có ý nghĩa.

## Format Brand KB

```json
{
  "id": 1,
  "name": "Minh Long",
  "name_variants": ["Minh Long", "Minh Long Book", "MLB"],
  "brand_type": "d2c",
  "category": "đồ gia dụng",
  "is_target": true,
  "shopee_url": "https://shopee.vn/minhlong_official",
  "lazada_url": "https://www.lazada.vn/shop/minh-long",
  "website_url": "https://minhlong.com",
  "knowledge_base": {
    "price_table": {
      "nồi chiên không dầu 5L": 1200000,
      "bộ nồi inox 5 món": 2500000
    },
    "ship_policy": {
      "freeship": "đơn từ 500k",
      "nội địa": "1-3 ngày",
      "phí ship": 30000
    },
    "return_policy": "7 ngày đổi trả",
    "warranty": "12 tháng",
    "rating": 4.7,
    "n_reviews": 15000,
    "shopee_rating": 4.8,
    "shopee_n_orders": 250000
  }
}
```

## Lưu ý

- **Verify tất cả URL còn live** trước khi commit
- **Giá cập nhật theo quý** (E-commerce thay đổi liên tục)
- **Note thời điểm verify** để biết data freshness
