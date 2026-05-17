"use client";

import { useQuery } from "@tanstack/react-query";
import { apiClient } from "@/shared/lib/api-client";
import type { DashboardStats, SpamTrendPoint, ThreatDistribution, ActionBreakdown } from "@findspam/types";

export function useDashboardStats() {
  return useQuery({
    queryKey: ["dashboard", "stats"],
    queryFn: () => apiClient.get<DashboardStats>("/analytics/dashboard/stats"),
    refetchInterval: 30_000,
  });
}

export function useSpamTrend(hours = 24) {
  return useQuery({
    queryKey: ["analytics", "spam-trend", hours],
    queryFn: () =>
      apiClient.get<SpamTrendPoint[]>(`/analytics/spam-trend?hours=${hours}`),
    refetchInterval: 60_000,
  });
}

export function useThreatDistribution() {
  return useQuery({
    queryKey: ["analytics", "threat-distribution"],
    queryFn: () =>
      apiClient.get<ThreatDistribution[]>("/analytics/threat-distribution"),
    refetchInterval: 60_000,
  });
}

export function useActionBreakdown() {
  return useQuery({
    queryKey: ["analytics", "action-breakdown"],
    queryFn: () =>
      apiClient.get<ActionBreakdown[]>("/analytics/action-breakdown"),
    refetchInterval: 60_000,
  });
}
