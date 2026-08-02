"use client";

import { useQuery } from "@tanstack/react-query";
import { getEvaluationReport } from "@/lib/api";

export function useEvaluation(taskId: number) {
  return useQuery({
    queryKey: ["evaluation", taskId],
    queryFn: () => getEvaluationReport(taskId),
  });
}
