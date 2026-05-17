"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { apiClient } from "@/shared/lib/api-client";
import type { User, UserRole, PaginatedResponse } from "@findspam/types";
import { toast } from "sonner";

export function useUsers(page = 1, search?: string) {
  return useQuery({
    queryKey: ["users", page, search],
    queryFn: () => {
      const p = new URLSearchParams({ page: String(page) });
      if (search) p.set("search", search);
      return apiClient.get<PaginatedResponse<User>>(`/users?${p.toString()}`);
    },
    placeholderData: (prev) => prev,
  });
}

export function useUpdateUserRole() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ userId, role }: { userId: string; role: UserRole }) =>
      apiClient.patch(`/users/${userId}/role`, { role }),
    onSuccess: () => {
      toast.success("User role updated");
      qc.invalidateQueries({ queryKey: ["users"] });
    },
    onError: () => toast.error("Failed to update role"),
  });
}

export function useDeactivateUser() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (userId: string) =>
      apiClient.patch(`/users/${userId}/deactivate`, {}),
    onSuccess: () => {
      toast.success("User deactivated");
      qc.invalidateQueries({ queryKey: ["users"] });
    },
  });
}
