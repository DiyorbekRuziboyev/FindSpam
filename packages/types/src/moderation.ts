import type { UUID, ISODateString } from "./common";
import type { ThreatLevel, SpamCategory, AIPrediction } from "./ai";

export type ModerationAction =
  | "NONE"
  | "WARN"
  | "DELETE"
  | "MUTE"
  | "KICK"
  | "BAN";

export type ReviewStatus = "AUTO" | "PENDING" | "APPROVED" | "OVERRIDDEN";

export interface ModerationEvent {
  id: UUID;
  groupId: UUID;
  telegramUserId: UUID;
  messageText: string;
  messageId: number;
  prediction: AIPrediction;
  actionTaken: ModerationAction;
  actionReason: string | null;
  reviewStatus: ReviewStatus;
  reviewedBy: UUID | null;
  threatLevel: ThreatLevel;
  spamCategory: SpamCategory | null;
  createdAt: ISODateString;
}

export interface ModerationAction_Record {
  id: UUID;
  eventId: UUID;
  actionType: ModerationAction;
  executedAt: ISODateString;
  executedBy: "BOT" | "ADMIN";
  durationSeconds: number | null;
  success: boolean;
}

export interface ModerationQueueItem {
  event: ModerationEvent;
  priority: "LOW" | "MEDIUM" | "HIGH";
  queuedAt: ISODateString;
}
