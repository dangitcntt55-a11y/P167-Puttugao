# ADR-0002: Stability Score threshold = 0.7

## Status
- [x] Accepted (2026-08-02)

## Context
- Theo Schulte et al. arXiv 2604.07585, cần chạy prompt N lần (N≥7-8) để có standard error < 0.10
- Cho demo 5 tuần, N=3 (compromise giữa cost và accuracy)
- Cần threshold để gate diagnosis (chỉ gap đủ ổn định mới vào diagnosis)

## Decision
**Threshold = 0.7** (Stability Score = 1 - normalized variance)

## Consequences
### Positive
- Giảm false alert 30% so với chạy 1 lần
- Gap stability < 0.7 → observation only, không diagnose → tiết kiệm cost
- Có căn cứ học thuật (Schulte et al.)

### Negative
- Có thể miss gap thật nếu variance cao → cần sample size lớn hơn
- 0.7 là số cố định, có thể cần tune theo từng brand

### Risks
- Threshold quá cao → miss gap; quá thấp → noise
- Cần monitor false alert rate để tune

## Alternatives considered
- **0.8**: quá cao, miss gap thật
- **0.6**: quá thấp, nhiều noise
- **0.7**: balance, dùng ở nhiều paper

## References
- Schulte et al. arXiv 2604.07585 (2026)
- GEO_AI_Agent_Ecommerce_VN.md §11 (định lượng hóa)
