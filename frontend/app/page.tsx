import { Suspense } from "react";
import { BrandCard } from "@/components/brand/brand-card";
import { VisibilityTrend } from "@/components/charts/visibility-trend";
import { SovChart } from "@/components/charts/sov-chart";
import { StabilityDistribution } from "@/components/charts/stability-distribution";
import { TopGaps } from "@/components/brand/top-gaps";

export default function HomePage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Tổng quan GEO AI Agent</h1>
      <p className="text-gray-600">
        Dashboard theo dõi AI visibility cho 2 brand E-commerce Việt Nam trên ChatGPT, Gemini, Claude, Tavily.
      </p>

      {/* Brand cards */}
      <section className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Suspense fallback={<div>Loading...</div>}>
          <BrandCard brandId={1} />
          <BrandCard brandId={2} />
        </Suspense>
      </section>

      {/* Charts */}
      <section className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="rounded-lg border p-4">
          <h2 className="text-lg font-semibold mb-2">Visibility Rate</h2>
          <VisibilityTrend />
        </div>
        <div className="rounded-lg border p-4">
          <h2 className="text-lg font-semibold mb-2">Share of Voice</h2>
          <SovChart />
        </div>
      </section>

      <section className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="rounded-lg border p-4">
          <h2 className="text-lg font-semibold mb-2">Phân bố Stability Score</h2>
          <StabilityDistribution />
        </div>
        <div className="rounded-lg border p-4">
          <h2 className="text-lg font-semibold mb-2">Top Gap cần xử lý</h2>
          <TopGaps />
        </div>
      </section>
    </div>
  );
}
