"use client";

import { useQuery } from "@tanstack/react-query";
import { listDiagnoses } from "@/lib/api";
import { severityColor } from "@/lib/utils";
import { Link } from "lucide-react";

export function TopGaps() {
  const { data, isLoading } = useQuery({
    queryKey: ["diagnoses-top"],
    queryFn: () => listDiagnoses({ stableOnly: true }),
  });

  if (isLoading) return <div>Loading...</div>;
  const top = data?.slice(0, 5) || [];

  return (
    <div className="space-y-2">
      {top.map((d) => (
        <div key={d.id} className="flex items-center justify-between rounded border p-3 hover:bg-gray-50">
          <div className="flex-1">
            <div className="font-medium">Diagnosis #{d.id}</div>
            <div className="text-sm text-gray-500">Brand #{d.brand_id} • Prompt #{d.prompt_id}</div>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-sm">Stability: {d.stability_score.toFixed(2)}</span>
            <span className={`rounded-full px-2 py-1 text-xs ${severityColor(d.severity)}`}>{d.severity}</span>
          </div>
        </div>
      ))}
    </div>
  );
}
