"use client";

import { useQuery } from "@tanstack/react-query";
import { apiClient } from "@/shared/lib/api-client";
import type {
  SpamTrendPoint,
  CategoryDistribution,
  HourlyHeatmapPoint,
  GroupLeaderboardEntry,
} from "@findspam/types";
import type { ModelMetrics } from "@findspam/types";

export function useSpamTrends(days = 30) {
  return useQuery({
    queryKey: ["analytics", "trends", days],
    queryFn: () =>
      apiClient.get<SpamTrendPoint[]>(`/analytics/spam-trend?days=${days}`),
  });
}

export function useCategoryDistribution(days = 30) {
  return useQuery({
    queryKey: ["analytics", "categories", days],
    queryFn: () =>
      apiClient.get<CategoryDistribution[]>(
        `/analytics/category-distribution?days=${days}`,
      ),
  });
}

export function useHeatmap() {
  return useQuery({
    queryKey: ["analytics", "heatmap"],
    queryFn: () =>
      apiClient.get<HourlyHeatmapPoint[]>("/analytics/heatmap"),
  });
}

export function useGroupLeaderboard() {
  return useQuery({
    queryKey: ["analytics", "group-leaderboard"],
    queryFn: () =>
      apiClient.get<GroupLeaderboardEntry[]>("/analytics/group-leaderboard"),
  });
}

export function useModelMetricsHistory() {
  return useQuery({
    queryKey: ["analytics", "model-metrics"],
    queryFn: () =>
      apiClient.get<Array<ModelMetrics & { date: string }>>("/ai/metrics/history"),
  });
}
