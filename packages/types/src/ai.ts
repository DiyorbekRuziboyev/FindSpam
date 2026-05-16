import type { UUID, ISODateString } from "./common";

export type ThreatLevel = "NONE" | "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
export type SpamCategory =
  | "SCAM"
  | "PHISHING"
  | "ADVERTISEMENT"
  | "FAKE_GIVEAWAY"
  | "SOCIAL_ENGINEERING"
  | "SUSPICIOUS_URL"
  | "OTHER";
export type Language = "UZ_LAT" | "UZ_CYR" | "RU" | "EN" | "UNKNOWN";

export interface ModelContributions {
  xlmRoberta: number;
  mBert: number;
  tfidfLr: number;
  ruleEngine: number;
}

export interface TokenExplanation {
  token: string;
  shapValue: number;
  contribution: "positive" | "negative";
}

export interface PredictionExplanation {
  topTokens: TokenExplanation[];
  topFeatures: Array<{ feature: string; importance: number }>;
  humanReadable: string;
}

export interface AIPrediction {
  id: UUID;
  isSpam: boolean;
  confidence: number;
  threatLevel: ThreatLevel;
  spamCategory: SpamCategory | null;
  language: Language;
  modelContributions: ModelContributions;
  explanation: PredictionExplanation;
  processingMs: number;
  modelVersion: string;
  createdAt: ISODateString;
}

export interface ModelVersion {
  id: UUID;
  versionTag: string;
  modelType: string;
  metrics: ModelMetrics;
  isActive: boolean;
  deployedAt: ISODateString | null;
  trainedAt: ISODateString;
}

export interface ModelMetrics {
  f1Score: number;
  precision: number;
  recall: number;
  auc: number;
  accuracy: number;
  falsePositiveRate: number;
}

export interface AIFeedback {
  predictionId: UUID;
  isCorrect: boolean;
  correctLabel?: boolean;
}
