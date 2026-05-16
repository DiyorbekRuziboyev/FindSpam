import type { UUID, ISODateString } from "./common";

export interface TelegramGroup {
  id: UUID;
  telegramGroupId: number;
  title: string;
  username: string | null;
  memberCount: number;
  settings: GroupSettings;
  isActive: boolean;
  spamRate: number;
  registeredAt: ISODateString;
}

export interface GroupSettings {
  autoDelete: boolean;
  autoMute: boolean;
  autoBan: boolean;
  spamThreshold: number;
  muteDurationSeconds: number;
  notifyAdmins: boolean;
  language: "UZ_LAT" | "UZ_CYR" | "RU" | "EN";
}

export interface TelegramUser {
  id: UUID;
  telegramId: number;
  username: string | null;
  firstName: string;
  lastName: string | null;
  riskScore: number;
  isBlacklisted: boolean;
  warningCount: number;
  createdAt: ISODateString;
  lastSeenAt: ISODateString;
}

export interface TelegramBotEvent {
  id: UUID;
  groupId: UUID;
  userId: UUID;
  eventType: string;
  payload: Record<string, unknown>;
  processedAt: ISODateString;
}
