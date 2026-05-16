"use client";

import { useEffect, useRef } from "react";
import type { WebSocketMessage, WebSocketChannel } from "@findspam/types";

const WS_BASE = process.env.NEXT_PUBLIC_WS_URL ?? "ws://localhost:8000";
const RECONNECT_DELAY_MS = 3000;
const MAX_RECONNECT_ATTEMPTS = 10;

export function useWebSocket(
  channel: WebSocketChannel,
  onMessage: (msg: WebSocketMessage) => void,
) {
  const wsRef = useRef<WebSocket | null>(null);
  const attemptsRef = useRef(0);
  const onMessageRef = useRef(onMessage);
  onMessageRef.current = onMessage;

  useEffect(() => {
    let destroyed = false;

    function connect() {
      if (destroyed) return;
      const token =
        typeof window !== "undefined"
          ? (localStorage.getItem("access_token") ?? "")
          : "";
      const ws = new WebSocket(
        `${WS_BASE}/ws/v1/${channel}?token=${token}`,
      );
      wsRef.current = ws;

      ws.onmessage = (e) => {
        try {
          const msg = JSON.parse(e.data as string) as WebSocketMessage;
          onMessageRef.current(msg);
        } catch {
          // malformed frame — ignore
        }
      };

      ws.onclose = () => {
        if (!destroyed && attemptsRef.current < MAX_RECONNECT_ATTEMPTS) {
          attemptsRef.current += 1;
          setTimeout(connect, RECONNECT_DELAY_MS);
        }
      };

      ws.onopen = () => {
        attemptsRef.current = 0;
      };
    }

    connect();
    return () => {
      destroyed = true;
      wsRef.current?.close();
    };
  }, [channel]);
}
