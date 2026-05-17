import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { User, AuthTokens } from "@findspam/types";
import { apiClient } from "@/shared/lib/api-client";

interface AuthState {
  user: User | null;
  accessToken: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  login: (email: string, password: string) => Promise<void>;
  setSession: (user: User, tokens: AuthTokens) => void;
  clearSession: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      accessToken: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      login: async (email, password) => {
        set({ isLoading: true, error: null });
        try {
          const data = await apiClient.post<{ user: User; tokens: AuthTokens }>(
            "/auth/login",
            { email, password },
          );
          if (typeof window !== "undefined") {
            localStorage.setItem("access_token", data.tokens.accessToken);
          }
          set({
            user: data.user,
            accessToken: data.tokens.accessToken,
            isAuthenticated: true,
            isLoading: false,
          });
          window.location.replace("/dashboard/overview");
        } catch (err) {
          set({
            isLoading: false,
            error: err instanceof Error ? err.message : "Login failed",
          });
        }
      },

      setSession: (user, tokens) =>
        set({
          user,
          accessToken: tokens.accessToken,
          isAuthenticated: true,
        }),

      clearSession: () =>
        set({ user: null, accessToken: null, isAuthenticated: false }),
    }),
    { name: "findspam-auth", partialize: (s) => ({ user: s.user }) },
  ),
);
