"use client";

import {
  LineChart as RechartsLine,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";

interface LineSeries {
  key: string;
  label: string;
  color: string;
  dashed?: boolean;
}

interface LineChartProps {
  data: Record<string, unknown>[];
  series: LineSeries[];
  xKey: string;
  height?: number;
  formatY?: (v: number) => string;
  connectNulls?: boolean;
}

const GRID_COLOR = "rgba(255,255,255,0.05)";
const AXIS_COLOR = "rgba(255,255,255,0.25)";

export function LineChart({
  data,
  series,
  xKey,
  height = 240,
  formatY,
  connectNulls = false,
}: LineChartProps) {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <RechartsLine data={data} margin={{ top: 4, right: 4, bottom: 0, left: 0 }}>
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
        />
        {series.length > 1 && (
          <Legend
            wrapperStyle={{ fontSize: "12px", paddingTop: "12px" }}
            formatter={(value) => series.find((s) => s.key === value)?.label ?? value}
          />
        )}
        {series.map((s) => (
          <Line
            key={s.key}
            type="monotone"
            dataKey={s.key}
            name={s.key}
            stroke={s.color}
            strokeWidth={2}
            strokeDasharray={s.dashed ? "4 4" : undefined}
            dot={false}
            activeDot={{ r: 4, strokeWidth: 0 }}
            connectNulls={connectNulls}
          />
        ))}
      </RechartsLine>
    </ResponsiveContainer>
  );
}
