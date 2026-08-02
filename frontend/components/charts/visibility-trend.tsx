"use client";

import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, Legend } from "recharts";
import { useEffect, useState } from "react";

export function VisibilityTrend() {
  const [data, setData] = useState<Array<{ date: string; target: number; competitor: number }>>([]);

  useEffect(() => {
    // Mock data — TODO: fetch from API
    setData([
      { date: "T2", target: 0.65, competitor: 0.45 },
      { date: "T3", target: 0.68, competitor: 0.48 },
      { date: "T4", target: 0.72, competitor: 0.50 },
      { date: "T5", target: 0.70, competitor: 0.47 },
      { date: "T6", target: 0.75, competitor: 0.52 },
      { date: "T7", target: 0.78, competitor: 0.55 },
      { date: "CN", target: 0.82, competitor: 0.58 },
    ]);
  }, []);

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="target" stroke="#3b82f6" name="Brand target" />
        <Line type="monotone" dataKey="competitor" stroke="#94a3b8" name="Đối thủ" />
      </LineChart>
    </ResponsiveContainer>
  );
}
