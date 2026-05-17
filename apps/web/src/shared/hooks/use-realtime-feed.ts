"use client";

import { useEffect } from "react";
import { useWebSocket } from "./useWebSocket";
import { useRealtimeStore } from "@/shared/stores/realtime.store";
import type { WebSocketMessage, RealtimeModerationEvent, SystemHealthStatus } from "@findspam/types";

export function useRealtimeFeed() {
  const { status, latestEvents, systemHealth, setStatus, pushEvent, setSystemHealth } =
    useRealtimeStore();

  const handleMessage = (msg: WebSocketMessage) => {
    if (msg.type === "moderation_event") {
      pushEvent(msg.data as RealtimeModerationEvent);
    } else if (msg.type === "system_health") {
      setSystemHealth(msg.data as SystemHealthStatus);
    } else if (msg.type === "connection_status") {
      setStatus((msg.data as { status: "connecting" | "connected" | "disconnected" | "error" }).status);
    }
  };

  useWebSocket("moderation", handleMessage);

  useEffect(() => {
    setStatus("connecting");
  }, [setStatus]);

  return { status, latestEvents, systemHealth };
}
