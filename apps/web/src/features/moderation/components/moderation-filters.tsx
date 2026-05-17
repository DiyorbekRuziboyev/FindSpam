"use client";

import { SearchInput } from "@/components/ui/search-input";

interface ModerationFilters {
  search: string;
  threatLevel: string;
  action: string;
}

interface ModerationFiltersProps {
  filters: ModerationFilters;
  onChange: (filters: Partial<ModerationFilters>) => void;
}

const THREAT_LEVELS = ["", "NONE", "LOW", "MEDIUM", "HIGH", "CRITICAL"];
const ACTIONS = ["", "NONE", "WARN", "DELETE", "MUTE", "KICK", "BAN"];

export function ModerationFilters({ filters, onChange }: ModerationFiltersProps) {
  return (
    <div className="flex flex-wrap items-center gap-3">
      <SearchInput
        placeholder="Search messages, users…"
        value={filters.search}
        onChange={(search) => onChange({ search })}
        className="w-64"
      />

      <select
        value={filters.threatLevel}
        onChange={(e) => onChange({ threatLevel: e.target.value })}
        className="h-9 rounded-lg border border-border/50 bg-muted/30 px-3 text-sm text-foreground focus:outline-none focus:ring-1 focus:ring-ring"
      >
        <option value="">All threats</option>
        {THREAT_LEVELS.filter(Boolean).map((l) => (
          <option key={l} value={l}>
            {l}
          </option>
        ))}
      </select>

      <select
        value={filters.action}
        onChange={(e) => onChange({ action: e.target.value })}
        className="h-9 rounded-lg border border-border/50 bg-muted/30 px-3 text-sm text-foreground focus:outline-none focus:ring-1 focus:ring-ring"
      >
        <option value="">All actions</option>
        {ACTIONS.filter(Boolean).map((a) => (
          <option key={a} value={a}>
            {a}
          </option>
        ))}
      </select>
    </div>
  );
}
