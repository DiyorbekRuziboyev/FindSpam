"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { apiClient } from "@/shared/lib/api-client";
import { toast } from "sonner";

export interface BlacklistEntry {
  id: string;
  type: "DOMAIN" | "PATTERN" | "PHRASE";
  value: string;
  reason: string | null;
  addedBy: string;
  createdAt: string;
  isActive: boolean;
}

export function useBlacklist(type?: string, page = 1) {
  return useQuery({
    queryKey: ["blacklist", type, page],
    queryFn: () => {
      const params = new URLSearchParams({ page: String(page) });
      if (type) params.set("type", type);
      return apiClient.get<{ items: BlacklistEntry[]; total: number }>(
        `/blacklist?${params.toString()}`,
      );
    },
    placeholderData: (prev) => prev,
  });
}

export function useAddBlacklistEntry() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (entry: Pick<BlacklistEntry, "type" | "value" | "reason">) =>
      apiClient.post("/blacklist", entry),
    onSuccess: () => {
      toast.success("Entry added to blacklist");
      qc.invalidateQueries({ queryKey: ["blacklist"] });
    },
    onError: () => toast.error("Failed to add entry"),
  });
}

export function useRemoveBlacklistEntry() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => apiClient.delete(`/blacklist/${id}`),
    onSuccess: () => {
      toast.success("Entry removed");
      qc.invalidateQueries({ queryKey: ["blacklist"] });
    },
  });
}
