"use client";

import { motion } from "framer-motion";
import { formatRelativeTime, formatConfidence, truncate } from "@/shared/lib/utils";
import { ThreatBadge } from "@/components/ui/threat-badge";
import { ActionBadge } from "@/components/ui/action-badge";
import type { ModerationEvent } from "@findspam/types";

interface EventCardProps {
  event: ModerationEvent;
  showActions?: boolean;
  onAction?: (eventId: string, action: string) => void;
}

export function EventCard({ event, showActions = false, onAction }: EventCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 4 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass-card rounded-xl p-4"
    >
      <div className="flex items-start justify-between gap-4">
        <div className="min-w-0 flex-1 space-y-1.5">
          <p className="text-sm text-foreground leading-relaxed">
            {truncate(event.messageText, 200)}
          </p>
          <div className="flex flex-wrap items-center gap-2">
            <ThreatBadge level={event.threatLevel} size="sm" />
            <ActionBadge action={event.actionTaken} size="sm" />
            {event.spamCategory && (
              <span className="rounded-md bg-muted/50 px-1.5 py-0.5 text-[10px] font-medium text-muted-foreground ring-1 ring-border">
                {event.spamCategory.replace(/_/g, " ")}
              </span>
            )}
            <span className="text-[10px] text-muted-foreground">
              {formatConfidence(event.prediction.confidence)} confidence ·{" "}
              {formatRelativeTime(event.createdAt)}
            </span>
          </div>
        </div>
      </div>

      {showActions && onAction && (
        <div className="mt-3 flex gap-2 border-t border-border/50 pt-3">
          <button
            onClick={() => onAction(event.id, "APPROVE")}
            className="rounded-md bg-emerald-500/10 px-3 py-1.5 text-xs font-medium text-emerald-400 hover:bg-emerald-500/20 transition-colors"
          >
            Approve
          </button>
          <button
            onClick={() => onAction(event.id, "OVERRIDE")}
            className="rounded-md bg-amber-500/10 px-3 py-1.5 text-xs font-medium text-amber-400 hover:bg-amber-500/20 transition-colors"
          >
            Override
          </button>
          <button
            onClick={() => onAction(event.id, "BAN")}
            className="rounded-md bg-red-500/10 px-3 py-1.5 text-xs font-medium text-red-400 hover:bg-red-500/20 transition-colors"
          >
            Ban User
          </button>
        </div>
      )}
    </motion.div>
  );
}
