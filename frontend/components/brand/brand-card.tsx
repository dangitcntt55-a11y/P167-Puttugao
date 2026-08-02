"use client";

import { useQuery } from "@tanstack/react-query";
import { getBrandVisibility } from "@/lib/api";
import { formatPercent } from "@/lib/utils";

export function BrandCard({ brandId }: { brandId: number }) {
  const { data, isLoading } = useQuery({
    queryKey: ["brand-visibility", brandId],
    queryFn: () => getBrandVisibility(brandId, 7),
  });

  if (isLoading) return <div className="rounded-lg border p-4">Loading...</div>;
  if (!data) return null;

  return (
    <div className="rounded-lg border p-4 hover:shadow-md transition">
      <div className="text-sm text-gray-500">Brand ID #{brandId}</div>
      <div className="text-2xl font-bold mt-1">{formatPercent(data.visibility_rate)}</div>
      <div className="text-sm text-gray-600">Visibility Rate (7 ngày)</div>
      <div className="mt-4 grid grid-cols-2 gap-2 text-sm">
        <div>
          <span className="text-gray-500">SOV:</span> {formatPercent(data.sov)}
        </div>
        <div>
          <span className="text-gray-500">Stability:</span> {formatPercent(data.avg_stability)}
        </div>
      </div>
    </div>
  );
}
