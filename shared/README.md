# shared/ — Tài nguyên chung (schema, prompts, config)

> **Dùng chung** cho cả 4 team. Bất kỳ thay đổi nào PR phải có 1 reviewer.

## 📁 Cấu trúc

```
shared/
├── README.md
├── schema.sql                       ← DB schema SQL (chốt từ GEO_AI_Agent_Ecommerce_VN.md §19.3)
├── prompts/
│   └── (link symlink đến ../data/prompts/ — single source of truth)
├── brands/
│   └── (link symlink đến ../data/brands/)
├── config/
│   ├── settings.example.json        ← config mẫu
│   └── ai_engines.json              ← AI engine metadata
└── docs/
    ├── api_contract.md              ← API contract giữa backend ↔ frontend/agent
    └── data_flow.md                 ← Data flow diagram
```

## 🔗 Quy tắc

1. **Schema thay đổi** → update `schema.sql` + tạo Alembic migration + ADR
2. **Prompts thay đổi** → update `../data/prompts/*.json` (single source of truth)
3. **Config thay đổi** → update `config/settings.example.json` + ADR
4. **API contract thay đổi** → update `docs/api_contract.md` + thông báo nhóm
