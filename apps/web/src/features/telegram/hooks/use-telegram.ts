"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { apiClient } from "@/shared/lib/api-client";
import type { TelegramGroup, TelegramBotEvent, GroupSettings, PaginatedResponse } from "@findspam/types";
import { toast } from "sonner";

export function useTelegramGroups() {
  return useQuery({
    queryKey: ["telegram", "groups"],
    queryFn: () => apiClient.get<TelegramGroup[]>("/telegram/groups"),
  });
}

export function useTelegramEvents(page = 1, pageSize = 20) {
  return useQuery({
    queryKey: ["telegram", "events", page],
    queryFn: () =>
      apiClient.get<PaginatedResponse<TelegramBotEvent>>(
        `/telegram/events?page=${page}&page_size=${pageSize}`,
      ),
    placeholderData: (prev) => prev,
  });
}

export function useUpdateGroupSettings() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ groupId, settings }: { groupId: string; settings: Partial<GroupSettings> }) =>
      apiClient.patch(`/telegram/groups/${groupId}/settings`, settings),
    onSuccess: () => {
      toast.success("Group settings updated");
      qc.invalidateQueries({ queryKey: ["telegram", "groups"] });
    },
    onError: () => toast.error("Failed to update settings"),
  });
}
