"use client";

import { useQuery } from "@tanstack/react-query";
import { listDiagnoses } from "@/lib/api";

export function useDiagnoses(params: { brandId?: number; stableOnly?: boolean } = {}) {
  return useQuery({
    queryKey: ["diagnoses", params],
    queryFn: () => listDiagnoses(params),
  });
}
