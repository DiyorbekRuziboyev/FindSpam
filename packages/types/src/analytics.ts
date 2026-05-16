import type { ISODateString } from "./common";
import type { ModerationAction, ThreatLevel } from "./moderation";
import type { SpamCategory } from "./ai";

export interface DashboardStats {
  spamDetected24h: number;
  spamDetected24hDelta: number;
  activeGroupsCount: number;
  aiAccuracy7d: number;
  actionsExecuted24h: number;
  avgConfidenceScore: number;
}

export interface SpamTrendPoint {
  timestamp: ISODateString;
  total: number;
  spam: number;
  spamRate: number;
}

export interface ThreatDistribution {
  level: ThreatLevel;
  count: number;
  percentage: number;
}

export interface CategoryDistribution {
  category: SpamCategory;
  count: number;
  percentage: number;
}

export interface ActionBreakdown {
  action: ModerationAction;
  count: number;
}

export interface HourlyHeatmapPoint {
  hour: number;
  dayOfWeek: number;
  spamCount: number;
}

export interface GroupLeaderboardEntry {
  groupId: string;
  groupTitle: string;
  spamCount: number;
  spamRate: number;
  totalMessages: number;
}
