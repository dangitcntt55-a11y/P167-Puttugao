# Confusion Matrix Template

> **Mục đích**: đánh giá FP/FN/TP/TN của mention parser.

## Cách tính

| | Predicted YES | Predicted NO |
|---|---|---|
| **Actual YES** | TP | FN |
| **Actual NO** | FP | TN |

## Công thức

- **Precision** = TP / (TP + FP) — trong các mention parser đoán, bao nhiêu % đúng?
- **Recall** = TP / (TP + FN) — trong các mention thật, parser đoán được bao nhiêu %?
- **F1** = 2 * (P * R) / (P + R)
- **Accuracy** = (TP + TN) / (TP + TN + FP + FN)

## Mục tiêu

- **Precision ≥ 0.90**
- **Recall ≥ 0.85** (ưu tiên recall hơn - FN nguy hiểm hơn FP trong GEO)
- **F1 ≥ 0.85**

## Phân tích theo nhóm

| Nhóm | Precision | Recall | F1 |
|------|-----------|--------|-----|
| uy_tin | ? | ? | ? |
| gia | ? | ? | ? |
| so_sanh | ? | ? | ? |
| review | ? | ? | ? |
| ship | ? | ? | ? |

## Phân tích theo AI engine

| Engine | Precision | Recall | F1 |
|--------|-----------|--------|-----|
| ChatGPT | ? | ? | ? |
| Gemini | ? | ? | ? |
| Claude | ? | ? | ? |
| Tavily | ? | ? | ? |

## Phân tích FP / FN

**Top 5 FP (parser đoán có mention nhưng thực tế không có):**
1. ?
2. ?
3. ?
4. ?
5. ?

**Top 5 FN (parser bỏ sót mention):**
1. ?
2. ?
3. ?
4. ?
5. ?

## Kết luận & hành động

- [ ] Cải thiện X
- [ ] Bổ sung Y
- [ ] Điều chỉnh prompt Z
