"use client";

import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";
import { useEffect, useState } from "react";
import { AI_ENGINE_LABELS } from "@/lib/constants";

export function SovChart() {
  const [data, setData] = useState<Array<{ engine: string; sov: number }>>([]);

  useEffect(() => {
    setData([
      { engine: AI_ENGINE_LABELS.chatgpt, sov: 0.42 },
      { engine: AI_ENGINE_LABELS.gemini, sov: 0.38 },
      { engine: AI_ENGINE_LABELS.claude, sov: 0.35 },
      { engine: AI_ENGINE_LABELS.tavily, sov: 0.55 },
    ]);
  }, []);

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="engine" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="sov" fill="#3b82f6" name="SOV" />
      </BarChart>
    </ResponsiveContainer>
  );
}
