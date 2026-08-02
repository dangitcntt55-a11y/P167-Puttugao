"use client";

import { useQuery } from "@tanstack/react-query";
import { listTasks } from "@/lib/api";

export function useTasks(params: { brandId?: number; status?: string } = {}) {
  return useQuery({
    queryKey: ["tasks", params],
    queryFn: () => listTasks(params),
  });
}
