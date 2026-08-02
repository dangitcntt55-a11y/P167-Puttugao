"use client";

import { useQuery } from "@tanstack/react-query";
import { getBrandVisibility } from "@/lib/api";
import { formatPercent } from "@/lib/utils";

export function BrandDetail({ brandId }: { brandId: number }) {
  const { data, isLoading } = useQuery({
    queryKey: ["brand-detail", brandId],
    queryFn: () => getBrandVisibility(brandId, 30),
  });

  if (isLoading) return <div>Loading...</div>;
  if (!data) return null;

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Brand #{brandId}</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="rounded-lg border p-4">
          <div className="text-sm text-gray-500">Visibility Rate</div>
          <div className="text-2xl font-bold">{formatPercent(data.visibility_rate)}</div>
        </div>
        <div className="rounded-lg border p-4">
          <div className="text-sm text-gray-500">SOV</div>
          <div className="text-2xl font-bold">{formatPercent(data.sov)}</div>
        </div>
        <div className="rounded-lg border p-4">
          <div className="text-sm text-gray-500">Stability</div>
          <div className="text-2xl font-bold">{formatPercent(data.avg_stability)}</div>
        </div>
      </div>
    </div>
  );
}
