"use client";

import { useQuery } from "@tanstack/react-query";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { approveDiagnosis, getEvaluationReport, listDiagnoses, rejectDiagnosis } from "@/lib/api";
import { formatDate, severityColor } from "@/lib/utils";

export function DiagnosisDetail({ diagnosisId }: { diagnosisId: number }) {
  const queryClient = useQueryClient();
  const { data, isLoading } = useQuery({
    queryKey: ["diagnosis", diagnosisId],
    queryFn: async () => {
      const all = await listDiagnoses({ stableOnly: false });
      return all.find((d) => d.id === diagnosisId);
    },
  });

  const approve = useMutation({
    mutationFn: () => approveDiagnosis(diagnosisId),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["diagnosis"] }),
  });

  const reject = useMutation({
    mutationFn: () => rejectDiagnosis(diagnosisId),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["diagnosis"] }),
  });

  if (isLoading) return <div>Loading...</div>;
  if (!data) return <div>Not found</div>;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Diagnosis #{data.id}</h1>
        <span className={`rounded-full px-3 py-1 text-sm ${severityColor(data.severity)}`}>{data.severity}</span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="rounded-lg border p-4">
          <div className="text-sm text-gray-500">Brand</div>
          <div className="text-xl font-semibold">#{data.brand_id}</div>
        </div>
        <div className="rounded-lg border p-4">
          <div className="text-sm text-gray-500">Prompt</div>
          <div className="text-xl font-semibold">#{data.prompt_id}</div>
        </div>
        <div className="rounded-lg border p-4">
          <div className="text-sm text-gray-500">Stability Score</div>
          <div className="text-xl font-semibold">{data.stability_score.toFixed(2)}</div>
        </div>
      </div>

      {/* Hypotheses */}
      <section className="rounded-lg border p-4">
        <h2 className="text-lg font-semibold mb-2">Hypotheses</h2>
        <ul className="space-y-2">
          {data.hypotheses.map((h, i) => (
            <li key={i} className="rounded border p-3">
              <div className="font-medium">{h.hypothesis}</div>
              <div className="text-sm text-gray-600">Confidence: {h.confidence.toFixed(2)}</div>
              <div className="text-sm text-blue-600 space-x-2">
                {h.evidence_urls.map((url, j) => (
                  <a key={j} href={url} target="_blank" rel="noreferrer" className="hover:underline">
                    {url}
                  </a>
                ))}
              </div>
            </li>
          ))}
        </ul>
      </section>

      {/* Recommended Actions */}
      <section className="rounded-lg border p-4">
        <h2 className="text-lg font-semibold mb-2">Recommended Actions</h2>
        <ul className="space-y-2">
          {data.recommended_actions.map((a, i) => (
            <li key={i} className="rounded border p-3">
              <div className="font-medium capitalize">{a.action_type.replace("_", " ")}</div>
              <div className="text-sm text-gray-600">{a.target_url}</div>
              <div className="text-sm">{a.suggested_change}</div>
            </li>
          ))}
        </ul>
      </section>

      {/* HITL */}
      <div className="flex gap-4">
        <button
          onClick={() => approve.mutate()}
          disabled={approve.isPending}
          className="rounded bg-green-600 px-4 py-2 text-white hover:bg-green-700 disabled:opacity-50"
        >
          Approve
        </button>
        <button
          onClick={() => reject.mutate()}
          disabled={reject.isPending}
          className="rounded bg-red-600 px-4 py-2 text-white hover:bg-red-700 disabled:opacity-50"
        >
          Reject
        </button>
      </div>
    </div>
  );
}
