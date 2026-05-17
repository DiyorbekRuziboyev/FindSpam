import { cn, formatPercent } from "@/shared/lib/utils";
import type { TelegramGroup } from "@findspam/types";

interface GroupRowProps {
  group: TelegramGroup;
}

export function GroupRow({ group }: GroupRowProps) {
  const spamRatePct = group.spamRate;
  const riskClass =
    spamRatePct >= 0.3
      ? "text-red-400"
      : spamRatePct >= 0.1
      ? "text-amber-400"
      : "text-emerald-400";

  return (
    <div className="flex items-center gap-4 rounded-lg border border-border/30 bg-card/30 px-4 py-3">
      <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-primary/10 text-sm font-bold text-primary">
        {group.title.charAt(0).toUpperCase()}
      </div>

      <div className="min-w-0 flex-1">
        <div className="flex items-center gap-2">
          <p className="text-sm font-medium text-foreground truncate">{group.title}</p>
          {group.username && (
            <span className="text-xs text-muted-foreground">@{group.username}</span>
          )}
        </div>
        <p className="text-xs text-muted-foreground">
          {group.memberCount.toLocaleString()} members · ID {group.telegramGroupId}
        </p>
      </div>

      <div className="shrink-0 text-right space-y-1">
        <p className={cn("text-sm font-semibold", riskClass)}>
          {formatPercent(spamRatePct)} spam
        </p>
        <div className="flex items-center justify-end gap-1.5">
          <span
            className={cn(
              "h-1.5 w-1.5 rounded-full",
              group.isActive ? "bg-emerald-400" : "bg-red-400",
            )}
          />
          <span className="text-[10px] text-muted-foreground">
            {group.isActive ? "Active" : "Inactive"}
          </span>
        </div>
      </div>
    </div>
  );
}
