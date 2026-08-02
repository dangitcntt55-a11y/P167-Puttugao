# Brands — Knowledge Base cho 2 brand demo + 4-6 đối thủ

> **Format**: JSON với thông tin public dễ verify (URL Shopee/Lazada/web, bảng giá, FAQ, ship policy).

## Chọn 2 brand (theo tiêu chí trong `GEO_AI_Agent_Ecommerce_VN.md` §9.5)

- 1 brand sàn (shop bán đa ngành hàng trên Shopee/Lazada/Tiki)
- 1 brand D2C (có website riêng, content-driven)
- Mỗi brand có 2-3 đối thủ trực tiếp

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
