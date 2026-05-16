import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { User, AuthTokens } from "@findspam/types";

interface AuthState {
  user: User | null;
  accessToken: string | null;
  isAuthenticated: boolean;
  setSession: (user: User, tokens: AuthTokens) => void;
  clearSession: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      accessToken: null,
      isAuthenticated: false,
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
