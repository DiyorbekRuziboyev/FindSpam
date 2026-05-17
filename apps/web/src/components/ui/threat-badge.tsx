import { cn } from "@/shared/lib/utils";
import type { ThreatLevel } from "@findspam/types";

interface ThreatBadgeProps {
  level: ThreatLevel;
  size?: "sm" | "md";
  showDot?: boolean;
}

const CONFIG: Record<ThreatLevel, { label: string; className: string; dot: string }> = {
  NONE: {
    label: "None",
    className: "bg-emerald-500/10 text-emerald-400 ring-emerald-500/20",
    dot: "bg-emerald-400",
  },
  LOW: {
    label: "Low",
    className: "bg-lime-500/10 text-lime-400 ring-lime-500/20",
    dot: "bg-lime-400",
  },
  MEDIUM: {
    label: "Medium",
    className: "bg-amber-500/10 text-amber-400 ring-amber-500/20",
    dot: "bg-amber-400",
  },
  HIGH: {
    label: "High",
    className: "bg-red-500/10 text-red-400 ring-red-500/20",
    dot: "bg-red-400",
  },
  CRITICAL: {
    label: "Critical",
    className: "bg-violet-500/10 text-violet-400 ring-violet-500/20",
    dot: "bg-violet-400",
  },
};

export function ThreatBadge({ level, size = "md", showDot = true }: ThreatBadgeProps) {
  const cfg = CONFIG[level] ?? CONFIG.NONE;
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded-full font-medium ring-1",
        cfg.className,
        size === "sm" ? "px-2 py-0.5 text-[10px]" : "px-2.5 py-1 text-xs",
      )}
    >
      {showDot && (
        <span className={cn("h-1.5 w-1.5 rounded-full", cfg.dot)} />
      )}
      {cfg.label}
    </span>
  );
}
