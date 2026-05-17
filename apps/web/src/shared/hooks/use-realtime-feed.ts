"use client";

import { useWebSocket } from "./useWebSocket";
import { useRealtimeStore } from "@/shared/stores/realtime.store";
import type { WebSocketMessage, RealtimeModerationEvent, SystemHealthStatus } from "@findspam/types";

export function useRealtimeFeed() {
  const { status, latestEvents, systemHealth, pushEvent, setSystemHealth } =
    useRealtimeStore();

  const handleMessage = (msg: WebSocketMessage) => {
    if (msg.event === "moderation_event") {
      pushEvent(msg.payload as RealtimeModerationEvent);
    } else if (msg.event === "system_health") {
      setSystemHealth(msg.payload as SystemHealthStatus);
    }
  };

  useWebSocket("moderation", handleMessage);

  return { status, latestEvents, systemHealth };
}
