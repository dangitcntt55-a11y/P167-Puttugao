# Weekly Report — Week 0

## Thông tin chung
- **Tuần**: 0 (Chuẩn bị)
- **Ngày**: 2026-08-02
- **Người viết**: Nhóm

## Tuần này đã làm gì?

### Đăng (Tech Lead)
- [ ] Đăng ký API keys (OpenAI, Anthropic, Google AI, Tavily)
- [ ] Setup repo: Git init, branch protection, .gitignore
- [ ] Tạo docker-compose (Postgres + Redis + Qdrant)
- [ ] Tạo schema.sql (copy từ GEO_AI_Agent_Ecommerce_VN.md §19.3)
- [ ] Setup Alembic

### Lý (Agent Engineer)
- [ ] Verify Tavily (tiếng Việt + Shopee/Lazada)
- [ ] Verify OpenAI, Anthropic, Gemini (response time, cost)
- [ ] Draft kiến trúc agent/

### Khôi (Data/NLP)
- [ ] Chọn 2 brand demo (1 sàn + 1 D2C) + 2-3 đối thủ/brand
- [ ] Thu thập Brand Knowledge Base
- [ ] Khởi tạo Gold dataset 20 mẫu pilot
- [ ] Liệt kê draft ~100 prompt tiếng Việt

### Hải (Frontend/Infra)
- [ ] Setup Next.js 14 + Tailwind + Recharts
- [ ] Wireframe dashboard
- [ ] Setup Vercel project
- [ ] Setup Prometheus + Grafana local

## KPI Tuần 0

| Metric | Target | Status |
|--------|--------|--------|
| API keys live | 4/4 | ✅/⚠️/❌ |
| Brand profile ready | 2 + 4-6 | ✅/⚠️/❌ |
| Prompt library draft | 100 prompts | ✅/⚠️/❌ |
| Gold dataset pilot | 20 mẫu | ✅/⚠️/❌ |
| Schema migrated | Yes | ✅/⚠️/❌ |

## Demo nội bộ

- Link video: N/A (tuần 0)
- Highlight: ...

## Blocker

1. ...
2. ...

## Plan tuần 1

- [ ] Đăng: FastAPI skeleton + scan endpoint
- [ ] Lý: Prompt runner 4 AI + retry
- [ ] Khôi: Hoàn thiện 100 prompts + 50 mẫu gold
- [ ] Hải: Dashboard page với chart
