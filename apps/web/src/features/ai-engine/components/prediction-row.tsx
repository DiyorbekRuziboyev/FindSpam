import { ThreatBadge } from "@/components/ui/threat-badge";
import { formatConfidence, formatRelativeTime, truncate } from "@/shared/lib/utils";
import { cn } from "@/shared/lib/utils";
import type { AIPrediction } from "@findspam/types";

interface PredictionRowProps {
  prediction: AIPrediction;
}

export function PredictionRow({ prediction: p }: PredictionRowProps) {
  return (
    <div className="flex items-center gap-4 rounded-lg bg-muted/20 px-4 py-3">
      <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full text-xs font-bold"
        style={{
          background: p.isSpam ? "rgba(239,68,68,0.1)" : "rgba(34,197,94,0.1)",
          color: p.isSpam ? "#ef4444" : "#22c55e",
        }}
      >
        {p.isSpam ? "S" : "✓"}
      </div>

      <div className="min-w-0 flex-1">
        <p className="text-xs text-muted-foreground">
          {p.explanation.humanReadable
            ? truncate(p.explanation.humanReadable, 120)
            : "No explanation"}
        </p>
        <div className="mt-1 flex items-center gap-2">
          <ThreatBadge level={p.threatLevel} size="sm" showDot={false} />
          {p.spamCategory && (
            <span className="text-[10px] text-muted-foreground">
              {p.spamCategory.replace(/_/g, " ")}
            </span>
          )}
          <span className="text-[10px] text-muted-foreground">
            {p.processingMs}ms · {p.modelVersion}
          </span>
        </div>
      </div>

      <div className="shrink-0 text-right">
        <p className={cn(
          "text-sm font-bold",
          p.confidence >= 0.9 ? "text-red-400" :
          p.confidence >= 0.7 ? "text-amber-400" : "text-emerald-400",
        )}>
          {formatConfidence(p.confidence)}
        </p>
        <p className="text-[10px] text-muted-foreground">
          {formatRelativeTime(p.createdAt)}
        </p>
      </div>
    </div>
  );
}
