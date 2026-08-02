# ADR-0003: Tách ai_engine thành llm_engine + search_engine

## Status
- [x] Accepted (2026-08-02)

## Context
Schema hiện tại (ADR-0002 / schema.sql §3) gộp tất cả 4 nguồn AI — ChatGPT, Gemini, Claude (LLM) và Tavily (search engine) — vào chung 1 cột `ai_engine` trong bảng `responses`.

Tavily không phải LLM:
- Tavily là **search engine web-grounded**, không sinh text từ prompt như LLM.
- Cost model khác: Tavily tính theo search call (~$0.005/search), không phải token.
- Stability của Tavily measure theo *consistency of web results* (URL set overlap), không phải *generation consistency*.
- Khi tính visibility rate hay stability score, việc gộp Tavily vào LLM trong cùng aggregate sẽ gây bias (Tavily có citation gần như luôn nhắc đến brand nếu có trong top result web, trong khi LLM mới dùng reasoning để nhắc).

Ngoài ra, hiện tại `engines/base.py` đã tách `ai_engine: str` (Tavily = "tavily") nhưng semantic không khớp schema.

## Decision
Tách thành **2 cột enum** riêng biệt trong bảng `responses`:

| Cột | Enum | Mô tả |
|-----|------|-------|
| `llm_engine` | NULL \| `chatgpt` \| `gemini` \| `claude` | NULL = row này không phải LLM (vd: Tavily). |
| `search_engine` | NULL \| `tavily` | NULL = row này không phải search engine (vd: LLM). |

Mỗi row sẽ có đúng 1 trong 2 cột là NOT NULL (constraint CHECK).

## Consequences

### Positive
- Phân biệt rõ giữa LLM-generated response và Search-returned result.
- Stability score có thể tính riêng cho LLM vs search.
- Không bị "Tavily bias" trong aggregate LLM-based visibility.
- Mở rộng dễ — nếu sau này thêm Perplexity (hybrid) hay Google SGE, có thể tách tiếp.

### Negative
- Phải update tất cả code gọi `ai_engine` → `llm_engine` / `search_engine`.
- Phải update Alembic migration nếu DB đã có data.
- API contract cũ phải deprecate dần (giữ `ai_engine` virtual column nếu cần backward compat).

### Risks
- Nếu DB đã có data scan thật → cần migration script để move values từ `ai_engine` → đúng cột mới.
- Frontend có thể đang query field `ai_engine` → cần update hooks.

## Alternatives considered

1. **Dùng 1 cột `source_type` enum lớn**: `('llm_chatgpt', 'llm_claude', 'llm_gemini', 'search_tavily')`
   - Nhược: khó aggregate visibility theo LLM vs search.
   - Chọn: NO.

2. **Giữ 1 cột `ai_engine`, thêm 1 cột `engine_kind` enum (llm|search)**:
   - Nhược: cồng kềnh, vẫn có khả năng inconsistent giữa 2 cột.
   - Chọn: NO.

3. **Tách thành 2 bảng riêng `llm_responses` và `search_responses`**:
   - Nhược: mất tính nhất quán schema, query phức tạp hơn.
   - Chọn: NO.

4. **Tách thành 2 cột trong cùng bảng (CHỌN)**:
   - Ưu: giữ được cấu trúc responses, query đơn giản, partition tự nhiên.
   - OK.

## Implementation plan
1. Update `shared/schema.sql`:
   - Drop cột `ai_engine`, thêm 2 cột `llm_engine` + `search_engine`.
   - Thêm CHECK constraint: `(llm_engine IS NOT NULL) <> (search_engine IS NOT NULL)`.
2. Tạo `backend/alembic/versions/XXXX_split_ai_engine.py` migration.
3. Update `shared/config/settings.example.json`: enum mới.
4. Update `agent/agent/engines/*` và `orchestrator.py`: dùng `llm_engine` cho LLM, `search_engine` cho Tavily.
5. Update `backend/app/api/*` endpoints + serializers.
6. Update `frontend/lib/api.ts` + hooks.
7. Ghi migration script move data cũ (nếu có).

## References
- GEO_AI_Agent_Ecommerce_VN.md §3, §11
- ADR-0002 (Stability threshold)
- ADR-0004 (Brand change đồ gia dụng → điện tử)
