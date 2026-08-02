import { TaskBoard } from "@/components/task/task-board";

export default function TasksPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Task Board</h1>
      <p className="text-gray-600">Quản lý action backlog cho 2 brand E-commerce.</p>
      <TaskBoard />
    </div>
  );
}
