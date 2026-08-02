"use client";

import Link from "next/link";
import { Home, FileSearch, ListTodo, TrendingUp } from "lucide-react";

export function Sidebar() {
  return (
    <aside className="w-64 border-r bg-gray-50 p-4">
      <div className="text-xl font-bold mb-6">GEO AI Agent</div>
      <nav className="space-y-2">
        <Link href="/" className="flex items-center gap-2 rounded px-3 py-2 hover:bg-gray-200">
          <Home size={18} />
          Tổng quan
        </Link>
        <Link href="/brands/1" className="flex items-center gap-2 rounded px-3 py-2 hover:bg-gray-200">
          <TrendingUp size={18} />
          Brand detail
        </Link>
        <Link href="/diagnoses/1" className="flex items-center gap-2 rounded px-3 py-2 hover:bg-gray-200">
          <FileSearch size={18} />
          Diagnosis
        </Link>
        <Link href="/tasks" className="flex items-center gap-2 rounded px-3 py-2 hover:bg-gray-200">
          <ListTodo size={18} />
          Tasks
        </Link>
      </nav>
    </aside>
  );
}
