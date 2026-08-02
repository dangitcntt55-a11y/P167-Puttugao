# Gold Dataset

> **Mục đích**: đánh giá precision/recall/F1 của mention parser.
> **50-100 mẫu** gán nhãn thủ công để làm ground truth.

## Format CSV

```csv
response_id,ai_engine,prompt_id,brand_name,is_target_brand,position,sentiment,claim_type,evidence_quote,is_correct
1,chatgpt,1,Minh Long,1,1,0.5,general,"Minh Long là thương hiệu đồ gia dụng uy tín",true
2,chatgpt,1,Lock&Lock,1,2,0.7,review,"Lock&Lock có nồi chiên tốt",true
```

## Trường

- `response_id`: ID của response trong DB
- `ai_engine`: chatgpt | gemini | claude | tavily
- `prompt_id`: ID prompt
- `brand_name`: tên brand được nhắc
- `is_target_brand`: 1 (target) | 0 (đối thủ)
- `position`: 1, 2, 3...
- `sentiment`: -1 to +1
- `claim_type`: price | ship | review | general
- `evidence_quote`: đoạn text chứa mention
- `is_correct`: label đúng/sai (cho eval)

## Label guideline

1. **Sarcasm**: sentiment ngược với nghĩa đen
2. **Negation**: "không tệ" = tích cực nhẹ
3. **Viết tắt**: "MLB" = "Minh Long Book"
4. **Không dấu**: "Minh Long" = "Minh Long"
5. **Implicit mention**: "thương hiệu X" không nói tên → không tính

## Confusion matrix template

Xem `confusion_matrix_template.md` để biết cách đánh giá FP/FN/TP/TN.
