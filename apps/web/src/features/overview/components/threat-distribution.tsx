"use client";

import { ChartCard } from "@/components/ui/chart-card";
import { DonutChart } from "@/components/charts/donut-chart";
import { useThreatDistribution } from "../hooks/use-overview";

const THREAT_COLORS: Record<string, string> = {
  NONE: "#22c55e",
  LOW: "#84cc16",
  MEDIUM: "#f59e0b",
  HIGH: "#ef4444",
  CRITICAL: "#7c3aed",
};

export function ThreatDistributionChart() {
  const { data, isLoading } = useThreatDistribution();

  const total = (data ?? []).reduce((sum, d) => sum + d.count, 0);
  const chartData = (data ?? [])
    .filter((d) => d.count > 0)
    .map((d) => ({
      name: d.level,
      value: d.count,
      color: THREAT_COLORS[d.level] ?? "#6b7280",
    }));

  return (
    <ChartCard
      title="Threat Distribution"
      description="By severity level (last 24h)"
      loading={isLoading}
    >
      <DonutChart
        data={chartData}
        centerLabel="total"
        centerValue={total.toLocaleString()}
      />
    </ChartCard>
  );
}
