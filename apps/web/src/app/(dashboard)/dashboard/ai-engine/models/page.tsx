"use client";

import { PageHeader } from "@/components/ui/page-header";
import { ModelCard } from "@/features/ai-engine/components/model-card";
import { useModelVersions, useDeployModel } from "@/features/ai-engine/hooks/use-ai-engine";
import { SkeletonCard } from "@/components/ui/skeleton";
import { EmptyState } from "@/components/ui/empty-state";
import { Package } from "lucide-react";

export default function ModelsPage() {
  const { data: models, isLoading } = useModelVersions();
  const { mutate: deploy, isPending, variables } = useDeployModel();

  return (
    <div className="space-y-6">
      <PageHeader
        title="Model Registry"
        description="All trained model versions with performance metrics"
        breadcrumbs={[
          { label: "Dashboard" },
          { label: "AI Engine" },
          { label: "Models" },
        ]}
      />

      {isLoading ? (
        <div className="space-y-4">
          {[1, 2, 3].map((i) => <SkeletonCard key={i} />)}
        </div>
      ) : !models?.length ? (
        <EmptyState
          icon={<Package className="h-5 w-5" />}
          title="No models found"
          description="Train your first model to see it here"
        />
      ) : (
        <div className="space-y-4">
          {models.map((model) => (
            <ModelCard
              key={model.id}
              model={model}
              onDeploy={deploy}
              deploying={isPending && variables === model.id}
            />
          ))}
        </div>
      )}
    </div>
  );
}
