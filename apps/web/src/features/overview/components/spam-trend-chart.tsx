"use client";

import { useState } from "react";
import { ChartCard } from "@/components/ui/chart-card";
import { AreaChart } from "@/components/charts/area-chart";
import { useSpamTrend } from "../hooks/use-overview";
import { formatNumber } from "@/shared/lib/utils";

const RANGE_OPTIONS = [
  { label: "6h", hours: 6 },
  { label: "24h", hours: 24 },
  { label: "7d", hours: 168 },
];

export function SpamTrendChart() {
  const [hours, setHours] = useState(24);
  const { data, isLoading } = useSpamTrend(hours);

  const chartData = (data ?? []).map((p) => ({
    time: new Date(p.timestamp).toLocaleTimeString("en-GB", {
      hour: "2-digit",
      minute: "2-digit",
    }),
    spam: p.spam,
    total: p.total,
  }));

  return (
    <ChartCard
      title="Spam Detection Trend"
      description="Messages analyzed vs spam detected"
      loading={isLoading}
      action={
        <div className="flex rounded-lg border border-border/50 overflow-hidden">
          {RANGE_OPTIONS.map((opt) => (
            <button
              key={opt.hours}
              onClick={() => setHours(opt.hours)}
              className={`px-3 py-1 text-xs transition-colors ${
                hours === opt.hours
                  ? "bg-primary/20 text-primary font-medium"
                  : "text-muted-foreground hover:text-foreground"
              }`}
            >
              {opt.label}
            </button>
          ))}
        </div>
      }
    >
      <AreaChart
        data={chartData}
        xKey="time"
        series={[
          { key: "spam", label: "Spam", color: "#ef4444" },
          { key: "total", label: "Total", color: "#3b82f6" },
        ]}
        formatY={formatNumber}
      />
    </ChartCard>
  );
}
