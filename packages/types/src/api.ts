export interface WebSocketMessage<T = unknown> {
  channel: string;
  event: string;
  payload: T;
  timestamp: string;
}

export type WebSocketChannel =
  | "moderation"
  | "analytics"
  | "system"
  | "ai";

export interface RealtimeModerationEvent {
  eventId: string;
  groupTitle: string;
  messagePreview: string;
  confidence: number;
  threatLevel: string;
  action: string;
  timestamp: string;
}

export interface RealtimeStatsUpdate {
  spamCount: number;
  actionCount: number;
  avgConfidence: number;
  windowMinutes: number;
}

export interface SystemHealthStatus {
  api: "healthy" | "degraded" | "down";
  database: "healthy" | "degraded" | "down";
  redis: "healthy" | "degraded" | "down";
  aiEngine: "healthy" | "degraded" | "down";
  bot: "healthy" | "degraded" | "down";
}
