"use client";

import { useState } from "react";
import { ChartCard } from "@/components/ui/chart-card";
import { AreaChart } from "@/components/charts/area-chart";
import { useSpamTrends } from "../hooks/use-analytics";
import { formatNumber } from "@/shared/lib/utils";

const RANGES = [
  { label: "7d", days: 7 },
  { label: "30d", days: 30 },
  { label: "90d", days: 90 },
];

export function SpamTrendsChart() {
  const [days, setDays] = useState(30);
  const { data, isLoading } = useSpamTrends(days);

  const chartData = (data ?? []).map((p) => ({
    date: new Date(p.timestamp).toLocaleDateString("en-GB", {
      day: "2-digit",
      month: "short",
    }),
    spam: p.spam,
    total: p.total,
    rate: Math.round(p.spamRate * 100),
  }));

  return (
    <ChartCard
      title="Spam Volume Trends"
      description={`Daily spam vs total messages — last ${days} days`}
      loading={isLoading}
      action={
        <div className="flex rounded-lg border border-border/50 overflow-hidden">
          {RANGES.map((r) => (
            <button
              key={r.days}
              onClick={() => setDays(r.days)}
              className={`px-3 py-1 text-xs transition-colors ${
                days === r.days
                  ? "bg-primary/20 text-primary font-medium"
                  : "text-muted-foreground hover:text-foreground"
              }`}
            >
              {r.label}
            </button>
          ))}
        </div>
      }
      minHeight={300}
    >
      <AreaChart
        data={chartData}
        xKey="date"
        series={[
          { key: "spam", label: "Spam", color: "#ef4444" },
          { key: "total", label: "Total", color: "#3b82f6" },
        ]}
        height={300}
        formatY={formatNumber}
      />
    </ChartCard>
  );
}
