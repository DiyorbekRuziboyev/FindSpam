import type { Metadata } from "next";
import { PageHeader } from "@/components/ui/page-header";
import { TrainingControls } from "@/features/ai-engine/components/training-controls";
import { ModelMetricsChart } from "@/features/analytics/components/model-metrics-chart";

export const metadata: Metadata = { title: "AI Training" };

export default function TrainingPage() {
  return (
    <div className="space-y-6">
      <PageHeader
        title="AI Training"
        description="Trigger model retraining and monitor training job progress"
        breadcrumbs={[
          { label: "Dashboard" },
          { label: "AI Engine" },
          { label: "Training" },
        ]}
      />
      <TrainingControls />
      <ModelMetricsChart />
    </div>
  );
}
