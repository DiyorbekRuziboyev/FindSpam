"use client";

import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Save } from "lucide-react";
import { toast } from "sonner";
import { PageHeader } from "@/components/ui/page-header";
import { apiClient } from "@/shared/lib/api-client";

interface PlatformSettings {
  spamConfidenceThreshold: number;
  suspiciousThreshold: number;
  rateLimit: number;
  rateLimitWindow: number;
  floodThreshold: number;
  floodMuteDuration: number;
  raidJoinThreshold: number;
  raidWindow: number;
  defaultLanguage: string;
}

function SettingRow({
  label,
  description,
  children,
}: {
  label: string;
  description?: string;
  children: React.ReactNode;
}) {
  return (
    <div className="flex items-center justify-between gap-6 py-4 border-b border-border/30 last:border-0">
      <div>
        <p className="text-sm font-medium text-foreground">{label}</p>
        {description && (
          <p className="mt-0.5 text-xs text-muted-foreground">{description}</p>
        )}
      </div>
      <div className="shrink-0">{children}</div>
    </div>
  );
}

export default function SettingsPage() {
  const qc = useQueryClient();
  const { data: settings, isLoading } = useQuery({
    queryKey: ["settings"],
    queryFn: () => apiClient.get<PlatformSettings>("/settings"),
  });

  const { mutate: save, isPending } = useMutation({
    mutationFn: (s: Partial<PlatformSettings>) =>
      apiClient.patch("/settings", s),
    onSuccess: () => {
      toast.success("Settings saved");
      qc.invalidateQueries({ queryKey: ["settings"] });
    },
    onError: () => toast.error("Failed to save settings"),
  });

  const [local, setLocal] = useState<Partial<PlatformSettings>>({});
  const merged = { ...settings, ...local };

  const set = (key: keyof PlatformSettings, value: number | string) =>
    setLocal((prev) => ({ ...prev, [key]: value }));

  return (
    <div className="space-y-6">
      <PageHeader
        title="Platform Settings"
        description="Global configuration for spam detection, rate limiting, and moderation"
        breadcrumbs={[{ label: "Dashboard" }, { label: "Settings" }]}
        action={
          <button
            onClick={() => save(local)}
            disabled={isPending || !Object.keys(local).length}
            className="flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90 disabled:opacity-50 transition-all"
          >
            <Save className="h-4 w-4" />
            Save Changes
          </button>
        }
      />

      {isLoading ? (
        <div className="glass-card rounded-xl p-5 animate-pulse space-y-4">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="h-10 rounded bg-muted/30" />
          ))}
        </div>
      ) : (
        <div className="glass-card rounded-xl px-5">
          <h3 className="py-4 text-xs font-semibold uppercase tracking-wider text-muted-foreground border-b border-border/30">
            Detection Thresholds
          </h3>

          <SettingRow
            label="Spam Confidence Threshold"
            description="Minimum confidence to classify a message as spam (0–1)"
          >
            <input
              type="number"
              min={0}
              max={1}
              step={0.01}
              value={merged.spamConfidenceThreshold ?? 0.8}
              onChange={(e) => set("spamConfidenceThreshold", parseFloat(e.target.value))}
              className="w-24 h-8 rounded-lg border border-border/50 bg-muted/30 px-2 text-sm text-right text-foreground focus:outline-none focus:ring-1 focus:ring-ring"
            />
          </SettingRow>

          <SettingRow
            label="Suspicious Threshold"
            description="Below this, messages are flagged for review instead of auto-action"
          >
            <input
              type="number"
              min={0}
              max={1}
              step={0.01}
              value={merged.suspiciousThreshold ?? 0.6}
              onChange={(e) => set("suspiciousThreshold", parseFloat(e.target.value))}
              className="w-24 h-8 rounded-lg border border-border/50 bg-muted/30 px-2 text-sm text-right text-foreground focus:outline-none focus:ring-1 focus:ring-ring"
            />
          </SettingRow>

          <h3 className="py-4 text-xs font-semibold uppercase tracking-wider text-muted-foreground border-b border-border/30">
            Rate Limiting
          </h3>

          <SettingRow label="Rate Limit" description="Max messages per user per window">
            <input
              type="number"
              min={1}
              value={merged.rateLimit ?? 20}
              onChange={(e) => set("rateLimit", parseInt(e.target.value))}
              className="w-24 h-8 rounded-lg border border-border/50 bg-muted/30 px-2 text-sm text-right text-foreground focus:outline-none focus:ring-1 focus:ring-ring"
            />
          </SettingRow>

          <SettingRow label="Flood Threshold" description="Messages before auto-mute">
            <input
              type="number"
              min={1}
              value={merged.floodThreshold ?? 5}
              onChange={(e) => set("floodThreshold", parseInt(e.target.value))}
              className="w-24 h-8 rounded-lg border border-border/50 bg-muted/30 px-2 text-sm text-right text-foreground focus:outline-none focus:ring-1 focus:ring-ring"
            />
          </SettingRow>

          <SettingRow
            label="Flood Mute Duration (seconds)"
            description="How long a flooder is muted"
          >
            <input
              type="number"
              min={60}
              step={60}
              value={merged.floodMuteDuration ?? 300}
              onChange={(e) => set("floodMuteDuration", parseInt(e.target.value))}
              className="w-24 h-8 rounded-lg border border-border/50 bg-muted/30 px-2 text-sm text-right text-foreground focus:outline-none focus:ring-1 focus:ring-ring"
            />
          </SettingRow>

          <h3 className="py-4 text-xs font-semibold uppercase tracking-wider text-muted-foreground border-b border-border/30">
            Anti-Raid
          </h3>

          <SettingRow label="Raid Join Threshold" description="Joins within window to trigger raid alert">
            <input
              type="number"
              min={3}
              value={merged.raidJoinThreshold ?? 10}
              onChange={(e) => set("raidJoinThreshold", parseInt(e.target.value))}
              className="w-24 h-8 rounded-lg border border-border/50 bg-muted/30 px-2 text-sm text-right text-foreground focus:outline-none focus:ring-1 focus:ring-ring"
            />
          </SettingRow>

          <SettingRow label="Default Language">
            <select
              value={merged.defaultLanguage ?? "UZ_LAT"}
              onChange={(e) => set("defaultLanguage", e.target.value)}
              className="h-8 rounded-lg border border-border/50 bg-muted/30 px-3 text-sm text-foreground focus:outline-none focus:ring-1 focus:ring-ring"
            >
              <option value="UZ_LAT">Uzbek (Latin)</option>
              <option value="UZ_CYR">Uzbek (Cyrillic)</option>
              <option value="RU">Russian</option>
              <option value="EN">English</option>
            </select>
          </SettingRow>
        </div>
      )}
    </div>
  );
}
