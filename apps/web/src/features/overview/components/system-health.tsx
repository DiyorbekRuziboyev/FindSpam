"use client";

import { cn } from "@/shared/lib/utils";
import { useRealtimeFeed } from "@/shared/hooks/use-realtime-feed";
import type { SystemHealthStatus } from "@findspam/types";

type ServiceStatus = "healthy" | "degraded" | "down";

const STATUS_CONFIG: Record<ServiceStatus, { label: string; dot: string; text: string }> = {
  healthy: { label: "Healthy", dot: "status-dot-green", text: "text-emerald-400" },
  degraded: { label: "Degraded", dot: "status-dot-yellow", text: "text-amber-400" },
  down: { label: "Down", dot: "status-dot-red", text: "text-red-400" },
};

const SERVICES: Array<{ key: keyof SystemHealthStatus; label: string }> = [
  { key: "api", label: "API" },
  { key: "database", label: "Database" },
  { key: "redis", label: "Redis" },
  { key: "aiEngine", label: "AI Engine" },
  { key: "bot", label: "Telegram Bot" },
];

function ServiceRow({
  label,
  status,
}: {
  label: string;
  status: ServiceStatus;
}) {
  const cfg = STATUS_CONFIG[status];
  return (
    <div className="flex items-center justify-between">
      <span className="text-xs text-muted-foreground">{label}</span>
      <div className="flex items-center gap-1.5">
        <span className={cn("h-1.5 w-1.5 rounded-full", cfg.dot)} />
        <span className={cn("text-xs font-medium", cfg.text)}>{cfg.label}</span>
      </div>
    </div>
  );
}

export function SystemHealth() {
  const { systemHealth } = useRealtimeFeed();

  const placeholder: SystemHealthStatus = {
    api: "healthy",
    database: "healthy",
    redis: "healthy",
    aiEngine: "healthy",
    bot: "healthy",
  };

  const health = systemHealth ?? placeholder;

  return (
    <div className="glass-card rounded-xl p-5">
      <div className="mb-4">
        <h3 className="text-sm font-semibold text-foreground">System Health</h3>
        <p className="mt-0.5 text-xs text-muted-foreground">Real-time service status</p>
      </div>
      <div className="space-y-3">
        {SERVICES.map(({ key, label }) => (
          <ServiceRow
            key={key}
            label={label}
            status={health[key] as ServiceStatus}
          />
        ))}
      </div>
    </div>
  );
}
