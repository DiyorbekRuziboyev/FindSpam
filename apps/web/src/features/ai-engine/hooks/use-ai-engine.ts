"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { apiClient } from "@/shared/lib/api-client";
import type { AIPrediction, ModelVersion, ModelMetrics, PaginatedResponse } from "@findspam/types";
import { toast } from "sonner";

interface PredictionFilters {
  page?: number;
  pageSize?: number;
  isSpam?: boolean;
  minConfidence?: number;
  threatLevel?: string;
}

function buildQuery(f: PredictionFilters): string {
  const p = new URLSearchParams();
  if (f.page) p.set("page", String(f.page));
  if (f.pageSize) p.set("page_size", String(f.pageSize));
  if (f.isSpam !== undefined) p.set("is_spam", String(f.isSpam));
  if (f.minConfidence) p.set("min_confidence", String(f.minConfidence));
  if (f.threatLevel) p.set("threat_level", f.threatLevel);
  return p.toString() ? `?${p.toString()}` : "";
}

export function usePredictions(filters: PredictionFilters = {}) {
  return useQuery({
    queryKey: ["ai", "predictions", filters],
    queryFn: () =>
      apiClient.get<PaginatedResponse<AIPrediction>>(
        `/ai/predictions${buildQuery(filters)}`,
      ),
    placeholderData: (prev) => prev,
  });
}

export function useModelVersions() {
  return useQuery({
    queryKey: ["ai", "models"],
    queryFn: () => apiClient.get<ModelVersion[]>("/ai/models"),
  });
}

export function useActiveModel() {
  return useQuery({
    queryKey: ["ai", "models", "active"],
    queryFn: () => apiClient.get<ModelVersion>("/ai/models/active"),
  });
}

export function useTriggerTraining() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (config: Record<string, unknown>) =>
      apiClient.post("/ai/training/trigger", config),
    onSuccess: () => {
      toast.success("Training job started");
      qc.invalidateQueries({ queryKey: ["ai"] });
    },
    onError: () => {
      toast.error("Failed to start training job");
    },
  });
}

export function useDeployModel() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (modelId: string) =>
      apiClient.post(`/ai/models/${modelId}/deploy`, {}),
    onSuccess: () => {
      toast.success("Model deployed successfully");
      qc.invalidateQueries({ queryKey: ["ai", "models"] });
    },
  });
}
