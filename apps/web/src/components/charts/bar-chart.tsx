"use client";

import {
  BarChart as RechartsBar,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";

interface BarChartProps {
  data: Record<string, unknown>[];
  dataKey: string;
  xKey: string;
  height?: number;
  color?: string;
  colorByValue?: boolean;
  colors?: string[];
  formatY?: (v: number) => string;
  radius?: number;
}

const GRID_COLOR = "rgba(255,255,255,0.05)";
const AXIS_COLOR = "rgba(255,255,255,0.25)";

export function BarChart({
  data,
  dataKey,
  xKey,
  height = 240,
  color = "#3b82f6",
  colorByValue = false,
  colors = [],
  formatY,
  radius = 4,
}: BarChartProps) {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <RechartsBar data={data} margin={{ top: 4, right: 4, bottom: 0, left: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke={GRID_COLOR} vertical={false} />
        <XAxis
          dataKey={xKey}
          tick={{ fontSize: 11, fill: AXIS_COLOR }}
          axisLine={false}
          tickLine={false}
          dy={6}
        />
        <YAxis
          tick={{ fontSize: 11, fill: AXIS_COLOR }}
          axisLine={false}
          tickLine={false}
          tickFormatter={formatY}
          dx={-4}
        />
        <Tooltip
          contentStyle={{
            background: "hsl(222 47% 7%)",
            border: "1px solid rgba(255,255,255,0.07)",
            borderRadius: "8px",
            fontSize: "12px",
          }}
          cursor={{ fill: "rgba(255,255,255,0.04)" }}
        />
        <Bar dataKey={dataKey} radius={[radius, radius, 0, 0]} fill={color}>
          {colorByValue &&
            data.map((_, i) => (
              <Cell
                key={i}
                fill={colors[i % colors.length] ?? color}
              />
            ))}
        </Bar>
      </RechartsBar>
    </ResponsiveContainer>
  );
}
