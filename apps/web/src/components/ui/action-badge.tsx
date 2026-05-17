import { cn } from "@/shared/lib/utils";
import type { ModerationAction } from "@findspam/types";

interface ActionBadgeProps {
  action: ModerationAction;
  size?: "sm" | "md";
}

const CONFIG: Record<ModerationAction, { label: string; className: string }> = {
  NONE: { label: "None", className: "bg-muted/50 text-muted-foreground ring-border" },
  WARN: { label: "Warn", className: "bg-amber-500/10 text-amber-400 ring-amber-500/20" },
  DELETE: { label: "Delete", className: "bg-red-500/10 text-red-400 ring-red-500/20" },
  MUTE: { label: "Mute", className: "bg-blue-500/10 text-blue-400 ring-blue-500/20" },
  KICK: { label: "Kick", className: "bg-orange-500/10 text-orange-400 ring-orange-500/20" },
  BAN: { label: "Ban", className: "bg-red-600/10 text-red-500 ring-red-600/20" },
};

export function ActionBadge({ action, size = "md" }: ActionBadgeProps) {
  const cfg = CONFIG[action] ?? CONFIG.NONE;
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-md font-medium ring-1",
        cfg.className,
        size === "sm" ? "px-1.5 py-0.5 text-[10px]" : "px-2 py-0.5 text-xs",
      )}
    >
      {cfg.label}
    </span>
  );
}
