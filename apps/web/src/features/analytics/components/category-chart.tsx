"use client";

import { ChartCard } from "@/components/ui/chart-card";
import { BarChart } from "@/components/charts/bar-chart";
import { useCategoryDistribution } from "../hooks/use-analytics";

const CATEGORY_COLORS = [
  "#ef4444",
  "#f59e0b",
  "#8b5cf6",
  "#3b82f6",
  "#06b6d4",
  "#22c55e",
  "#f97316",
];

export function CategoryChart() {
  const { data, isLoading } = useCategoryDistribution();

  const chartData = (data ?? []).map((d) => ({
    name: d.category.replace(/_/g, " "),
    count: d.count,
  }));

  return (
    <ChartCard
      title="Spam by Category"
      description="Distribution of detected spam types"
      loading={isLoading}
    >
      <BarChart
        data={chartData}
        dataKey="count"
        xKey="name"
        colorByValue
        colors={CATEGORY_COLORS}
        height={260}
      />
    </ChartCard>
  );
}
