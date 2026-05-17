"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { apiClient } from "@/shared/lib/api-client";
import type { ModerationEvent, ModerationQueueItem, PaginatedResponse } from "@findspam/types";

interface ModerationFilters {
  page?: number;
  pageSize?: number;
  threatLevel?: string;
  action?: string;
  groupId?: string;
  search?: string;
  from?: string;
  to?: string;
}

function buildQuery(filters: ModerationFilters): string {
  const params = new URLSearchParams();
  if (filters.page) params.set("page", String(filters.page));
  if (filters.pageSize) params.set("page_size", String(filters.pageSize));
  if (filters.threatLevel) params.set("threat_level", filters.threatLevel);
  if (filters.action) params.set("action", filters.action);
  if (filters.groupId) params.set("group_id", filters.groupId);
  if (filters.search) params.set("search", filters.search);
  if (filters.from) params.set("from", filters.from);
  if (filters.to) params.set("to", filters.to);
  return params.toString() ? `?${params.toString()}` : "";
}

export function useModerationHistory(filters: ModerationFilters = {}) {
  return useQuery({
    queryKey: ["moderation", "history", filters],
    queryFn: () =>
      apiClient.get<PaginatedResponse<ModerationEvent>>(
        `/moderation/events${buildQuery(filters)}`,
      ),
    placeholderData: (prev) => prev,
  });
}

export function useModerationQueue() {
  return useQuery({
    queryKey: ["moderation", "queue"],
    queryFn: () => apiClient.get<ModerationQueueItem[]>("/moderation/queue"),
    refetchInterval: 5_000,
  });
}

export function useApproveAction() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ eventId, action }: { eventId: string; action: string }) =>
      apiClient.post(`/moderation/events/${eventId}/action`, { action }),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["moderation"] });
    },
  });
}
