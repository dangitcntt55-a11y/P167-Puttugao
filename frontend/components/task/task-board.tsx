"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { listTasks, updateTaskStatus } from "@/lib/api";
import { ACTION_LABELS, TASK_STATUS_LABELS } from "@/lib/constants";

export function TaskBoard() {
  const queryClient = useQueryClient();
  const { data, isLoading } = useQuery({
    queryKey: ["tasks"],
    queryFn: () => listTasks(),
  });

  const update = useMutation({
    mutationFn: ({ id, status }: { id: number; status: string }) => updateTaskStatus(id, status),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["tasks"] }),
  });

  if (isLoading) return <div>Loading...</div>;
  const tasks = data || [];

  const columns = ["todo", "in_progress", "done"] as const;

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      {columns.map((status) => (
        <div key={status} className="rounded-lg border p-4">
          <h2 className="text-lg font-semibold mb-3">{TASK_STATUS_LABELS[status]}</h2>
          <div className="space-y-2">
            {tasks
              .filter((t) => t.status === status)
              .map((t) => (
                <div key={t.id} className="rounded border p-3 bg-white hover:shadow">
                  <div className="font-medium">{ACTION_LABELS[t.action_type] || t.action_type}</div>
                  <div className="text-sm text-gray-600">Brand #{t.brand_id}</div>
                  {status === "in_progress" && (
                    <button
                      onClick={() => update.mutate({ id: t.id, status: "done" })}
                      className="mt-2 rounded bg-green-600 px-2 py-1 text-xs text-white hover:bg-green-700"
                    >
                      Đánh dấu xong
                    </button>
                  )}
                  {status === "todo" && (
                    <button
                      onClick={() => update.mutate({ id: t.id, status: "in_progress" })}
                      className="mt-2 rounded bg-blue-600 px-2 py-1 text-xs text-white hover:bg-blue-700"
                    >
                      Bắt đầu
                    </button>
                  )}
                </div>
              ))}
          </div>
        </div>
      ))}
    </div>
  );
}
