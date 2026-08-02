"""Action templates — template content cho mỗi loại action."""


LISTING_UPDATE_TEMPLATE = """Cập nhật listing Shopee/Lazada:

1. Tiêu đề: {title}
   - Front-load từ khóa chính
   - Bao gồm: thương hiệu + sản phẩm + đặc điểm nổi bật
   - VD: "[Minh Long] Nồi chiên không dầu 5L - Inox 304 - Bảo hành 12 tháng"

2. Mô tả:
   - Bullet 1: Công dụng chính
   - Bullet 2: Thông số kỹ thuật
   - Bullet 3: Chính sách (ship, đổi trả, bảo hành)
   - Bullet 4: So sánh với đối thủ (USP)

3. Schema Product (Shopee/Lazada tự sinh, nhưng verify có đủ attributes)

4. Hình ảnh: 5-7 ảnh chất lượng cao, có text overlay chính
"""


CONTENT_ADD_TEMPLATE = """Thêm nội dung FAQ/TOPIC trên web shop:

- URL: {url}
- Topic: {topic}
- Nội dung:
  - 200-500 từ, có FAQ schema
  - Trả lời các câu hỏi phổ biến (giá, ship, đổi trả, bảo hành)
  - Có schema FAQPage
  - Internal link về trang sản phẩm
- Goal: AI có thể trích dẫn khi user hỏi
"""


SCHEMA_ADD_TEMPLATE = """Thêm schema markup:

URL: {url}
Schema cần thêm:
- Product: name, image, description, sku, brand
- Offer: price, priceCurrency, availability, seller
- Review: nếu có review thật
- FAQPage: nếu có FAQ

JSON-LD inline trong <head>:
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Product",
  ...
}}
</script>
"""


OUTREACH_TEMPLATE = """Outreach cập nhật citation:

- Citation URL hiện tại: {current_url}
- Author/Editor: {author}
- Channel: Tinhte / Voz / Vatgia / blog review
- Action:
  1. Liên hệ author qua email/form
  2. Cung cấp thông tin cập nhật (giá mới, sản phẩm mới, chính sách mới)
  3. Đề nghị cập nhật bài viết
  4. Follow-up sau 1 tuần
"""


CONTENT_PR_TEMPLATE = """Viết bài PR chất lượng cao:

- Topic: {topic}
- Target: blog/review site có DA > 30
- Nội dung:
  - 1500-2500 từ
  - Original research / data
  - Có infographic
  - SEO optimization
  - External link về trang sản phẩm
- Goal: AI có thể trích dẫn là nguồn uy tín
"""


TEMPLATES = {
    "listing_update": LISTING_UPDATE_TEMPLATE,
    "content_add": CONTENT_ADD_TEMPLATE,
    "schema_add": SCHEMA_ADD_TEMPLATE,
    "outreach": OUTREACH_TEMPLATE,
    "content_pr": CONTENT_PR_TEMPLATE,
}


def get_template(action_type: str) -> str:
    if action_type not in TEMPLATES:
        raise ValueError(f"Unknown action_type: {action_type}")
    return TEMPLATES[action_type]
