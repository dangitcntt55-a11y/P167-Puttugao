# Prompts — E-commerce GEO

> **5 nhóm prompt** (theo `GEO_AI_Agent_Ecommerce_VN.md` §9.2):
> 1. **uy_tin** — uy tín brand
> 2. **gia** — giá sản phẩm
> 3. **so_sanh** — so sánh
> 4. **review** — review sản phẩm
> 5. **ship** — chính sách ship/dịch vụ

## Format JSON

```json
{
  "id": 1,
  "text": "shop bán đồ gia dụng uy tín TPHCM?",
  "group": "uy_tin",
  "language": "vi",
  "tags": ["thành phố", "đồ gia dụng"],
  "difficulty": "easy",
  "expected_mentions": ["Minh Long", "Lock&Lock"]
}
```

## Trường

- `id`: unique int
- `text`: prompt tiếng Việt
- `group`: 1 trong 5 nhóm
- `language`: 'vi' (chính), 'en' (fallback)
- `tags`: list tag để filter
- `difficulty`: 'easy' | 'medium' | 'hard'
- `expected_mentions`: list brand nên được nhắc (cho eval)

## Nguyên tắc tạo prompt

1. **Paraphrase đa dạng** — cùng intent, nhiều cách hỏi
2. **Mix có dấu/không dấu/viết tắt** — "Minh Long" / "Minh Long Book" / "MLB"
3. **Mix chi tiết/chung** — "nồi chiên không dầu 5L" vs "nồi chiên"
4. **Avoid injection** — không chứa tên brand cụ thể trong prompt (vd: "shop ABC có tốt không?")
5. **Realistic** — phản ánh câu người dùng thật hỏi
