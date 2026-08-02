"use client";

import { useQuery } from "@tanstack/react-query";
import { getEvaluationReport } from "@/lib/api";
import { verdictColor, verdictText, formatPercent } from "@/lib/utils";
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, ReferenceLine } from "recharts";

export function EvaluationReport({ taskId }: { taskId: number }) {
  const { data, isLoading } = useQuery({
    queryKey: ["evaluation", taskId],
    queryFn: () => getEvaluationReport(taskId),
  });

  if (isLoading) return <div>Loading...</div>;
  if (!data) return <div>Not found</div>;

  const chartData = [
    { name: "Pre", value: data.pre_visibility || 0 },
    { name: "Post", value: data.post_visibility || 0 },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Evaluation Report #{data.task_id}</h1>
        <span className={`rounded-full px-4 py-2 text-sm font-semibold ${verdictColor(data.result)}`}>
          {verdictText(data.result)}
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="rounded-lg border p-4">
          <div className="text-sm text-gray-500">Pre Visibility</div>
          <div className="text-2xl font-bold">{formatPercent(data.pre_visibility || 0)}</div>
        </div>
        <div className="rounded-lg border p-4">
          <div className="text-sm text-gray-500">Post Visibility</div>
          <div className="text-2xl font-bold">{formatPercent(data.post_visibility || 0)}</div>
        </div>
        <div className="rounded-lg border p-4">
          <div className="text-sm text-gray-500">CI Lower</div>
          <div className="text-2xl font-bold">{(data.ci_lower || 0).toFixed(3)}</div>
        </div>
        <div className="rounded-lg border p-4">
          <div className="text-sm text-gray-500">CI Upper</div>
          <div className="text-2xl font-bold">{(data.ci_upper || 0).toFixed(3)}</div>
        </div>
      </div>

      <div className="rounded-lg border p-4">
        <h2 className="text-lg font-semibold mb-3">Pre vs Post Visibility</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <ReferenceLine y={0.06} stroke="#10b981" label="Noise floor 6%" />
            <Bar dataKey="value" fill="#3b82f6" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
