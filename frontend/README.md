# frontend/ — Frontend Engineer (Hải)

> **Phụ trách**: Hải (Frontend/Infra Engineer)
> **Stack**: Next.js 14, Tailwind CSS, Recharts, shadcn/ui, React Query, Docker

## 🎯 Trách nhiệm

1. **Dashboard Next.js**: trang chính cho demo (visibility, SOV, trend).
2. **HITL UI**: approve / reject diagnoses, edit actions.
3. **Task board** (Kanban): quản lý action backlog.
4. **Evaluation report UI**: hiển thị closed-loop với chart CI.
5. **Deployment**: Docker Compose, Vercel config, CI/CD.
6. **Monitoring**: Prometheus + Grafana setup.

## 📁 Cấu trúc folder

```
frontend/
├── README.md
├── package.json
├── tsconfig.json
├── next.config.js
├── tailwind.config.ts
├── .env.example
├── Dockerfile
├── app/                              ← Next.js 14 App Router
│   ├── layout.tsx
│   ├── page.tsx                      ← Trang chủ (overview)
│   ├── globals.css
│   ├── brands/
│   │   └── [brandId]/
│   │       └── page.tsx              ← Brand detail
│   ├── diagnoses/
│   │   └── [diagnosisId]/
│   │       └── page.tsx              ← Diagnosis detail với evidence
│   ├── tasks/
│   │   └── page.tsx                  ← Task board
│   ├── evaluation/
│   │   └── [taskId]/
│   │       └── page.tsx              ← Closed-loop report
│   └── api/                          ← (optional) Next.js API routes
├── components/
│   ├── ui/                           ← shadcn/ui components
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── badge.tsx
│   │   └── table.tsx
│   ├── layout/
│   │   ├── sidebar.tsx
│   │   ├── header.tsx
│   │   └── footer.tsx
│   ├── charts/
│   │   ├── visibility-trend.tsx      ← Line chart
│   │   ├── sov-chart.tsx             ← Bar chart
│   │   ├── stability-distribution.tsx
│   │   └── bootstrap-ci-chart.tsx    ← Closed-loop chart
│   ├── brand/
│   │   ├── brand-card.tsx
│   │   └── brand-comparison.tsx
│   ├── diagnosis/
│   │   ├── diagnosis-card.tsx
│   │   ├── evidence-package.tsx
│   │   └── hitl-actions.tsx
│   ├── task/
│   │   ├── task-board.tsx
│   │   ├── task-card.tsx
│   │   └── task-detail-modal.tsx
│   └── evaluation/
│       ├── evaluation-report.tsx
│       └── verdict-badge.tsx
├── lib/
│   ├── api.ts                        ← Backend API client
│   ├── types.ts                      ← TypeScript types
│   ├── utils.ts                      ← helpers (cn, formatNumber, ...)
│   └── constants.ts
├── hooks/
│   ├── use-brands.ts
│   ├── use-diagnoses.ts
│   ├── use-tasks.ts
│   └── use-evaluation.ts
├── public/
│   └── images/
├── styles/
│   └── globals.css
└── tests/
    └── ...
```

## 🚀 Quick start

```bash
# Install deps
npm install
# hoặc
pnpm install

# Setup env
cp .env.example .env.local
# → NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

# Run dev
npm run dev
# → http://localhost:3000

# Build
npm run build
npm run start
```

## 🎨 Design system

- **Color**: Blue (target brand) / Gray (competitor) / Green (improved) / Yellow (no_evidence) / Red (regressed)
- **Font**: Inter (sans-serif)
- **Components**: shadcn/ui (Radix + Tailwind)
- **Charts**: Recharts
- **Icons**: Lucide React

## 📱 Pages chính

### `/` Overview
- Top: 2 brand cards (1 sàn + 1 D2C)
- Middle: 4 chart cards (visibility trend, SOV, stability, top gaps)
- Bottom: recent diagnoses

### `/brands/[brandId]`
- Brand info
- Charts: visibility over time, per AI engine
- Bracketed: prompt group breakdown
- Link to diagnoses

### `/diagnoses/[diagnosisId]`
- Gap description
- Evidence package (URL + quote + Tavily cross-check)
- HITL actions: Approve / Reject / Edit

### `/tasks` (Kanban)
- 3 columns: To do / In progress / Done
- Cards: action type, brand, evidence URL, status

### `/evaluation/[taskId]`
- Pre/post visibility chart
- Bootstrap CI bar
- Verdict: improved / no_evidence / regressed
- Export PDF

## 🔗 Dependency với folder khác

- **`backend/`** (Đăng): gọi API qua `lib/api.ts`.
- **`agent/`** (Lý): KHÔNG gọi trực tiếp — qua backend.
- **`data/`** (Khôi): hiển thị reports.
- **`shared/`**: types, schema.

## ⚠️ Lưu ý quan trọng

1. **Tiếng Việt** cho UI label — KHÔNG dịch sang tiếng Anh.
2. **Responsive**: tối ưu mobile (marketer thường xem trên điện thoại).
3. **Loading skeleton**: dùng `loading.tsx` cho mỗi page.
4. **Error boundary**: bắt lỗi API, hiển thị user-friendly.
5. **Accessibility**: aria-label tiếng Việt, keyboard navigation.
6. **Performance**: lazy load chart, code splitting.

## 📋 Checklist riêng cho Hải

Xem `../tasks.md` chi tiết. Tóm tắt:

- **Tuần 0**: Next.js setup, wireframe (Figma hoặc vẽ tay), Vercel config
- **Tuần 1**: Dashboard cơ bản (visibility, SOV, trend)
- **Tuần 2**: Diagnosis detail page + HITL approval UI
- **Tuần 3**: Task board (Kanban) + alert hallucination
- **Tuần 4**: Evaluation report UI + PDF export
- **Tuần 5**: Polish UI, demo video, slide, deployment
