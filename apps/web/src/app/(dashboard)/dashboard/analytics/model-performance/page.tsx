import type { Metadata } from "next";
import { PageHeader } from "@/components/ui/page-header";
import { ModelMetricsChart } from "@/features/analytics/components/model-metrics-chart";

export const metadata: Metadata = { title: "Model Performance" };

export default function ModelPerformancePage() {
  return (
    <div className="space-y-6">
      <PageHeader
        title="Model Performance"
        description="Historical AI model metrics — F1, Precision, Recall, AUC"
        breadcrumbs={[
          { label: "Dashboard" },
          { label: "Analytics" },
          { label: "Model Performance" },
        ]}
      />
      <ModelMetricsChart />
    </div>
  );
}
