"use client";

import { Shield, Activity, Target, TrendingUp } from "lucide-react";
import { StatCard } from "@/components/ui/stat-card";
import { formatPercent } from "@/shared/lib/utils";
import { useDashboardStats } from "../hooks/use-overview";

export function StatsRow() {
  const { data: stats, isLoading } = useDashboardStats();

  return (
    <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
      <StatCard
        label="Spam Detected (24h)"
        value={stats?.spamDetected24h ?? 0}
        delta={stats?.spamDetected24hDelta}
        deltaLabel="vs yesterday"
        icon={<Shield className="h-5 w-5" />}
        iconClassName="bg-red-500/10 text-red-400"
        loading={isLoading}
      />
      <StatCard
        label="Actions Executed (24h)"
        value={stats?.actionsExecuted24h ?? 0}
        icon={<Activity className="h-5 w-5" />}
        iconClassName="bg-blue-500/10 text-blue-400"
        loading={isLoading}
      />
      <StatCard
        label="AI Accuracy (7d)"
        value={stats ? formatPercent(stats.aiAccuracy7d) : "–"}
        icon={<Target className="h-5 w-5" />}
        iconClassName="bg-emerald-500/10 text-emerald-400"
        loading={isLoading}
        format="raw"
      />
      <StatCard
        label="Avg Confidence"
        value={stats ? formatPercent(stats.avgConfidenceScore) : "–"}
        icon={<TrendingUp className="h-5 w-5" />}
        iconClassName="bg-violet-500/10 text-violet-400"
        loading={isLoading}
        format="raw"
      />
    </div>
  );
}
