"use client";

import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, ReferenceLine } from "recharts";
import { useEffect, useState } from "react";

export function StabilityDistribution() {
  const [data, setData] = useState<Array<{ range: string; count: number }>>([]);

  useEffect(() => {
    setData([
      { range: "0.0-0.2", count: 3 },
      { range: "0.2-0.4", count: 5 },
      { range: "0.4-0.6", count: 12 },
      { range: "0.6-0.7", count: 18 },
      { range: "0.7-0.8", count: 25 },
      { range: "0.8-0.9", count: 30 },
      { range: "0.9-1.0", count: 27 },
    ]);
  }, []);

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="range" />
        <YAxis />
        <Tooltip />
        <ReferenceLine x="0.7-0.8" stroke="#10b981" label="Threshold ≥ 0.7" />
        <Bar dataKey="count" fill="#3b82f6" />
      </BarChart>
    </ResponsiveContainer>
  );
}
