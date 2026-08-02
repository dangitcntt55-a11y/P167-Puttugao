# data/ — Data/NLP (Khôi)

> **Phụ trách**: Khôi (Data/NLP Engineer)
> **Stack**: Python, pandas, numpy, scipy, jupyter, label-studio (optional)

## 🎯 Trách nhiệm

1. **Prompt library E-commerce**: ~100 prompts chia 5 nhóm (uy tín, giá, so sánh, review, ship).
2. **Gold dataset**: 50-100 mẫu gán nhãn thủ công (cho F1 evaluation).
3. **Stability analysis**: phân tích variance, tỷ lệ gap đạt Stability ≥ 0.7.
4. **Evaluation**: precision/recall/F1, bootstrap CI, hallucination detection.
5. **Reports**: weekly eval, final eval.

## 📁 Cấu trúc folder

```
data/
├── README.md
├── requirements.txt
├── prompts/
│   ├── README.md                       ← giải thích 5 nhóm + format
│   ├── uy_tin.json                     ← ~20 prompts uy tín
│   ├── gia.json                        ← ~20 prompts giá
│   ├── so_sanh.json                    ← ~20 prompts so sánh
│   ├── review.json                     ← ~20 prompts review
│   ├── ship.json                       ← ~20 prompts ship
│   └── all_prompts.json                ← consolidate
├── brands/
│   ├── README.md                       ← format Brand Knowledge Base
│   ├── brand_1_san.json                ← 1 brand sàn (vd: Shop bán đồ gia dụng)
│   ├── brand_2_d2c.json                ← 1 brand D2C
│   └── competitors.json                ← 4-6 đối thủ
├── gold_dataset/
│   ├── README.md                       ← label guideline
│   ├── gold_v1.csv                     ← 50-100 mẫu
│   └── confusion_matrix_template.md
├── analysis/
│   ├── stability_analysis.py           ← phân tích Stability Score
│   ├── bootstrap_ci.py                 ← bootstrap CI implementation
│   ├── evaluation_metrics.py           ← precision/recall/F1
│   └── hallucination_review.md
├── reports/
│   ├── weekly/
│   │   └── template.md
│   └── final/
│       └── template.md
└── notebooks/
    ├── 01_explore_prompts.ipynb
    ├── 02_stability_analysis.ipynb
    └── 03_evaluation.ipynb
```

## 🚀 Quick start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# Stats
python analysis/stability_analysis.py
python analysis/bootstrap_ci.py

# Eval
python analysis/evaluation_metrics.py

# Jupyter
jupyter notebook notebooks/
```

## 📊 5 nhóm prompt E-commerce

| Nhóm | Mục đích | Số prompt (target) | VD |
|------|----------|-------------------|-----|
| **uy_tin** | Hỏi về độ uy tín brand | ~20 | "shop bán đồ gia dụng uy tín TPHCM?" |
| **gia** | Hỏi về giá | ~20 | "nồi chiên không dầu giá bao nhiêu?" |
| **so_sanh** | So sánh brand | ~20 | "so sánh Minh Long và Lock&Lock" |
| **review** | Review sản phẩm | ~20 | "nồi chiên nào tốt, review?" |
| **ship** | Chính sách ship/dịch vụ | ~20 | "Minh Long có freeship không?" |

## 📋 Checklist riêng cho Khôi

Xem `../tasks.md` chi tiết. Tóm tắt:

- **Tuần 0**: Chọn 2 brand, thu thập KB, gold dataset 20 mẫu pilot, draft prompt library
- **Tuần 1**: Hoàn thiện 100 prompts, gold dataset 50-100 mẫu, baseline scan analysis
- **Tuần 2**: F1 evaluation, confusion matrix, sentiment manual review
- **Tuần 3**: Action acceptance rate, document 5 loại action
- **Tuần 4**: **Bootstrap CI implementation**, evaluation reports 6 task
- **Tuần 5**: Final eval (precision/recall/F1/Stability/Closed-loop), data slides

## ⚠️ Lưu ý quan trọng

1. **Prompt library PHẢI đa dạng** — paraphrase cùng intent, edge case (có dấu/không dấu/viết tắt).
2. **Gold dataset phải CÂN BẰNG** — 5 nhóm, mention & non-mention, sentiment positive/negative.
3. **Bootstrap CI theo arXiv 2603.08924** — 1000 iterations, alpha=0.05.
4. **Noise floor 5-7%** — improved phải vượt ngưỡng này.
5. **Closed-loop accuracy ≥ 75%** — đo trên 6 reports (3 × 2 brand).
