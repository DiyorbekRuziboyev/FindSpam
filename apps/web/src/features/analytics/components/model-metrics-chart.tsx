"use client";

import { ChartCard } from "@/components/ui/chart-card";
import { LineChart } from "@/components/charts/line-chart";
import { useModelMetricsHistory } from "../hooks/use-analytics";
import { formatPercent } from "@/shared/lib/utils";

export function ModelMetricsChart() {
  const { data, isLoading } = useModelMetricsHistory();

  const chartData = (data ?? []).map((m) => ({
    date: new Date(m.date).toLocaleDateString("en-GB", {
      day: "2-digit",
      month: "short",
    }),
    f1: Math.round(m.f1Score * 100),
    precision: Math.round(m.precision * 100),
    recall: Math.round(m.recall * 100),
    auc: Math.round(m.auc * 100),
  }));

  return (
    <ChartCard
      title="Model Performance Over Time"
      description="F1, Precision, Recall, AUC — historical trend"
      loading={isLoading}
      minHeight={300}
    >
      <LineChart
        data={chartData}
        xKey="date"
        height={300}
        series={[
          { key: "f1", label: "F1 Score", color: "#3b82f6" },
          { key: "precision", label: "Precision", color: "#8b5cf6" },
          { key: "recall", label: "Recall", color: "#06b6d4" },
          { key: "auc", label: "AUC", color: "#22c55e", dashed: true },
        ]}
        formatY={(v) => `${v}%`}
      />
    </ChartCard>
  );
}
