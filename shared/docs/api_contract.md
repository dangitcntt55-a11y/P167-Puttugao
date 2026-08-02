# API Contract — Backend ↔ Frontend + Agent

> **Quy tắc**: Mọi thay đổi endpoint phải update file này + thông báo nhóm.

## Base URL

- Dev: `http://localhost:8000/api/v1`
- Prod: TBD

## Auth

- Optional `X-API-Key` header (cho service-to-service)
- Không có user auth trong MVP (giả định internal tool)

## Endpoints

### Brands

#### `GET /brands/`
List tất cả brands (target + competitors).

**Response 200:**
```json
[
  {
    "id": 1,
    "name": "Minh Long",
    "name_variants": ["Minh Long", "Minh Long Book", "MLB"],
    "brand_type": "d2c",
    "is_target": true,
    "category": "đồ gia dụng",
    "shopee_url": "https://shopee.vn/minhlong_official",
    "lazada_url": "https://www.lazada.vn/shop/minh-long",
    "website_url": "https://minhlong.com"
  }
]
```

### Prompts

#### `GET /prompts/?group=uy_tin`
List prompts (filter by group).

**Query params:**
- `group` (optional): `uy_tin` | `gia` | `so_sanh` | `review` | `ship`

**Response 200:**
```json
[
  {
    "id": 1,
    "text": "shop bán đồ gia dụng uy tín TPHCM?",
    "group": "uy_tin",
    "language": "vi",
    "tags": ["thành phố", "đồ gia dụng"],
    "difficulty": "easy"
  }
]
```

### Scan

#### `POST /scan/`
Trigger 1 scan (manual).

**Request body:**
```json
{
  "brand_id": 1,
  "prompt_ids": [1, 2, 3],  // optional, null = all
  "ai_engines": ["chatgpt", "claude"],  // optional, null = all 4
  "n_runs": 3
}
```

**Response 200:**
```json
{
  "task_id": "celery-task-uuid",
  "status": "queued",
  "brand_id": 1,
  "n_prompts": 100,
  "n_engines": 4
}
```

### Visibility

#### `GET /visibility/{brand_id}?days=7`
Get visibility metrics cho 1 brand.

**Query params:**
- `days`: 1-90 (default 7)

**Response 200:**
```json
{
  "brand_id": 1,
  "period_days": 7,
  "visibility_rate": 0.65,
  "sov": 0.42,
  "avg_stability": 0.78,
  "n_responses": 600,
  "trend": [
    {"date": "2026-08-01", "visibility_rate": 0.62, "stability": 0.75},
    {"date": "2026-08-02", "visibility_rate": 0.68, "stability": 0.80}
  ],
  "computed_at": "2026-08-02T09:00:00Z"
}
```

### Diagnoses

#### `GET /diagnoses/?brand_id=1&stable_only=true`
List diagnoses, default chỉ lấy stable (Stability ≥ 0.7).

**Query params:**
- `brand_id` (optional)
- `stable_only` (default true)
- `status` (optional): `pending_review` | `approved` | `rejected`

**Response 200:**
```json
[
  {
    "id": 1,
    "brand_id": 1,
    "prompt_id": 5,
    "is_stable": true,
    "stability_score": 0.78,
    "hypotheses": [
      {
        "hypothesis": "Brand không có schema Product trên web",
        "confidence": 0.85,
        "evidence_urls": ["https://minhlong.com/san-pham"]
      }
    ],
    "evidence_package": {
      "citations": [...],
      "tavily_cross_check": {...}
    },
    "recommended_actions": [
      {
        "action_type": "schema_add",
        "target_url": "https://minhlong.com/san-pham",
        "suggested_change": "Thêm schema Product với price=1200000"
      }
    ],
    "severity": "high",
    "status": "pending_review",
    "created_at": "2026-08-02T09:00:00Z"
  }
]
```

#### `POST /diagnoses/{diagnosis_id}/approve`
HITL approve → tạo task.

**Response 200:**
```json
{"diagnosis_id": 1, "status": "approved"}
```

#### `POST /diagnoses/{diagnosis_id}/reject`
HITL reject.

**Response 200:**
```json
{"diagnosis_id": 1, "status": "rejected"}
```

### Tasks

#### `GET /tasks/?brand_id=1&status=todo`
List tasks (cho Kanban).

**Query params:**
- `brand_id` (optional)
- `status` (optional): `todo` | `in_progress` | `done` | `cancelled`

**Response 200:**
```json
[
  {
    "id": 1,
    "brand_id": 1,
    "diagnosis_id": 1,
    "action_type": "schema_add",
    "owner_team": "content",
    "status": "todo",
    "result": null,
    "ci_lower": null,
    "ci_upper": null,
    "pre_visibility": null,
    "post_visibility": null,
    "created_at": "2026-08-02T09:00:00Z"
  }
]
```

#### `PATCH /tasks/{task_id}`
Update task status. Khi `status="done"` → trigger re-scan (Celery).

**Request body:**
```json
{"status": "done"}
```

**Response 200:**
```json
{"task_id": 1, "status": "done"}
```

### Evaluation

#### `GET /evaluation/{task_id}`
Closed-loop evaluation report.

**Response 200:**
```json
{
  "task_id": 1,
  "brand_id": 1,
  "action_type": "schema_add",
  "pre_visibility": 0.45,
  "post_visibility": 0.62,
  "ci_lower": 0.08,
  "ci_upper": 0.25,
  "result": "improved",
  "completed_at": "2026-08-02T15:00:00Z"
}
```

## Error codes

| Code | Meaning |
|------|---------|
| 400 | Bad request (validation) |
| 404 | Resource not found |
| 500 | Internal server error |
| 503 | Service unavailable (API quota / DB down) |

## Rate limiting

- MVP: không có rate limit
- Production: 100 req/min per IP (TODO)

## Versioning

- API v1 stable
- Breaking change → bump v2
