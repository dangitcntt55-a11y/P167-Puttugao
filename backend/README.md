# backend/ — Tech Lead (Đăng)

> **Phụ trách**: Đăng (Tech Lead)
> **Stack**: FastAPI + PostgreSQL + Redis + Celery + SQLAlchemy + Alembic
> **Schema chuẩn**: xem `../shared/schema.sql` (copy từ `GEO_AI_Agent_Ecommerce_VN.md` §19.3)

## 🎯 Trách nhiệm

1. **API layer** (FastAPI): expose endpoints cho frontend + agent.
2. **Database** (PostgreSQL): schema, migration, query tối ưu.
3. **Scheduler** (Celery + Redis): chạy scan theo lịch, re-scan sau task done.
4. **Closed-loop re-scan engine**: trigger + bootstrap CI + phân loại.
5. **Deployment**: Docker Compose, monitoring, cost tracking.

## 📁 Cấu trúc folder

```
backend/
├── README.md                      ← file này
├── requirements.txt
├── .env.example
├── alembic.ini
├── docker-compose.yml             ← (optional, có thể share ở root)
├── app/
│   ├── __init__.py
│   ├── main.py                    ← FastAPI entrypoint
│   ├── config.py                  ← Settings (pydantic)
│   ├── deps.py                    ← Dependency injection
│   ├── db/
│   │   ├── __init__.py
│   │   ├── session.py             ← SQLAlchemy session
│   │   ├── base.py                ← Base model
│   │   └── models/
│   │       ├── __init__.py
│   │       ├── brand.py
│   │       ├── prompt.py
│   │       ├── response.py
│   │       ├── mention.py
│   │       ├── stability_score.py
│   │       ├── diagnosis.py
│   │       └── task.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py          ← aggregate routers
│   │       ├── brands.py          ← /api/v1/brands
│   │       ├── prompts.py         ← /api/v1/prompts
│   │       ├── scan.py            ← /api/v1/scan
│   │       ├── visibility.py      ← /api/v1/visibility
│   │       ├── diagnoses.py       ← /api/v1/diagnoses
│   │       ├── tasks.py           ← /api/v1/tasks
│   │       └── evaluation.py      ← /api/v1/evaluation
│   ├── schemas/                   ← Pydantic schemas (DTO)
│   │   ├── __init__.py
│   │   ├── brand.py
│   │   ├── response.py
│   │   ├── diagnosis.py
│   │   └── task.py
│   ├── services/                  ← Business logic
│   │   ├── __init__.py
│   │   ├── visibility.py          ← Compute visibility_rate, SOV
│   │   ├── stability.py           ← Compute Stability Score
│   │   ├── closed_loop.py         ← Re-scan + bootstrap CI
│   │   └── cost_tracker.py        ← Track API cost per scan
│   ├── workers/                   ← Celery tasks
│   │   ├── __init__.py
│   │   ├── celery_app.py
│   │   ├── scan_tasks.py          ← Periodic scan
│   │   ├── rescan_tasks.py        ← Re-scan after task done
│   │   └── eval_tasks.py          ← Compute bootstrap CI
│   └── core/
│       ├── __init__.py
│       ├── logging.py
│       ├── security.py
│       └── exceptions.py
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       └── 0001_initial_schema.py
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── test_visibility.py
    ├── test_stability.py
    └── test_closed_loop.py
```

## 🚀 Quick start

```bash
# 1. Setup venv
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt

# 2. Setup env
cp .env.example .env
# → điền DATABASE_URL, REDIS_URL, OPENAI_API_KEY, etc.

# 3. Run migration
alembic upgrade head

# 4. Run dev server
uvicorn app.main:app --reload --port 8000
# → API tại http://localhost:8000/docs
```

## 📡 API endpoints chính

| Method | Path | Mục đích |
|--------|------|----------|
| `GET` | `/api/v1/brands/` | List 2 brand demo + đối thủ |
| `GET` | `/api/v1/prompts/` | List prompt library |
| `POST` | `/api/v1/scan/` | Manual trigger 1 scan |
| `GET` | `/api/v1/visibility/{brand_id}` | Visibility Rate + SOV |
| `GET` | `/api/v1/diagnoses/` | List diagnoses (qua Stability filter) |
| `POST` | `/api/v1/diagnoses/{id}/approve` | HITL approve |
| `POST` | `/api/v1/diagnoses/{id}/reject` | HITL reject |
| `GET` | `/api/v1/tasks/` | List task (cho Hải UI) |
| `PATCH` | `/api/v1/tasks/{id}` | Update task status |
| `GET` | `/api/v1/evaluation/{task_id}` | Closed-loop report |

## 🧪 Test

```bash
pytest                          # all tests
pytest tests/test_visibility.py # specific
pytest --cov=app                # coverage
```

## 🔗 Dependency với folder khác

- **`agent/`** (Lý): gọi API backend để lưu raw response + diagnoses.
- **`data/`** (Khôi): đọc Gold dataset + chạy eval scripts.
- **`frontend/`** (Hải): gọi API để hiển thị dashboard.
- **`shared/`**: đọc `schema.sql` + `prompts/` + `config/`.

## 📋 Checklist riêng cho Đăng

Xem chi tiết task từng tuần ở `../tasks.md`. Tóm tắt:

- **Tuần 0**: API keys, setup repo, schema, Alembic
- **Tuần 1**: FastAPI skeleton, models, scan endpoint, Celery
- **Tuần 2**: Diagnoses endpoints, HITL approve/reject
- **Tuần 3**: Tasks endpoints, trigger re-scan
- **Tuần 4**: **Closed-loop re-scan engine + bootstrap CI**
- **Tuần 5**: Load test, deploy, cost optimization

## ⚠️ Lưu ý quan trọng

- **Không tự ý thêm cột DB** — phải update `shared/schema.sql` + tạo migration Alembic.
- **API key KHÔNG commit** — chỉ dùng `.env`.
- **Mỗi response phải có `run_index`** (1, 2, 3) để tính Stability.
- **Closed-loop classification** (`improved` / `no_evidence` / `regressed`) phải dùng **bootstrap 95% CI**, KHÔNG dùng point estimate.
- **Noise floor 5–7 điểm %** — improved phải vượt ngưỡng này.
