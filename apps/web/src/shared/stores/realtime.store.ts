import { create } from "zustand";
import type { RealtimeModerationEvent, SystemHealthStatus } from "@findspam/types";

type ConnectionStatus = "connecting" | "connected" | "disconnected" | "error";

interface RealtimeState {
  status: ConnectionStatus;
  latestEvents: RealtimeModerationEvent[];
  systemHealth: SystemHealthStatus | null;
  setStatus: (status: ConnectionStatus) => void;
  pushEvent: (event: RealtimeModerationEvent) => void;
  setSystemHealth: (health: SystemHealthStatus) => void;
}

const MAX_EVENTS = 100;

export const useRealtimeStore = create<RealtimeState>()((set) => ({
  status: "disconnected",
  latestEvents: [],
  systemHealth: null,
  setStatus: (status) => set({ status }),
  pushEvent: (event) =>
    set((state) => ({
      latestEvents: [event, ...state.latestEvents].slice(0, MAX_EVENTS),
    })),
  setSystemHealth: (health) => set({ systemHealth: health }),
}));
