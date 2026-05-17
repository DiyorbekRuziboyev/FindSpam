"use client";

import { motion, AnimatePresence } from "framer-motion";
import { Activity } from "lucide-react";
import { ThreatBadge } from "@/components/ui/threat-badge";
import { ActionBadge } from "@/components/ui/action-badge";
import { EmptyState } from "@/components/ui/empty-state";
import { truncate, formatRelativeTime, formatConfidence } from "@/shared/lib/utils";
import { useRealtimeFeed } from "@/shared/hooks/use-realtime-feed";
import type { ThreatLevel, ModerationAction } from "@findspam/types";

export function LiveFeedWidget() {
  const { latestEvents } = useRealtimeFeed();

  return (
    <div className="glass-card rounded-xl p-5">
      <div className="mb-4 flex items-center justify-between">
        <div>
          <h3 className="text-sm font-semibold text-foreground">Live Feed</h3>
          <p className="mt-0.5 text-xs text-muted-foreground">Real-time moderation events</p>
        </div>
        <span className="flex items-center gap-1.5 text-xs text-emerald-400">
          <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse-dot" />
          Live
        </span>
      </div>

      <div className="space-y-2 max-h-[320px] overflow-y-auto pr-1">
        {latestEvents.length === 0 ? (
          <EmptyState
            icon={<Activity className="h-5 w-5" />}
            title="Waiting for events"
            description="New moderation events will appear here"
            className="border-0 py-8"
          />
        ) : (
          <AnimatePresence initial={false}>
            {latestEvents.slice(0, 20).map((ev) => (
              <motion.div
                key={ev.eventId}
                initial={{ opacity: 0, y: -8 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, height: 0 }}
                transition={{ duration: 0.2 }}
                className="flex items-start gap-3 rounded-lg bg-muted/20 p-3"
              >
                <ThreatBadge
                  level={ev.threatLevel as ThreatLevel}
                  size="sm"
                  showDot={false}
                />
                <div className="min-w-0 flex-1">
                  <p className="text-xs font-medium text-foreground">
                    {ev.groupTitle}
                  </p>
                  <p className="mt-0.5 text-xs text-muted-foreground">
                    {truncate(ev.messagePreview, 80)}
                  </p>
                </div>
                <div className="flex shrink-0 flex-col items-end gap-1">
                  <ActionBadge action={ev.action as ModerationAction} size="sm" />
                  <span className="text-[10px] text-muted-foreground">
                    {formatConfidence(ev.confidence)} · {formatRelativeTime(ev.timestamp)}
                  </span>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
        )}
      </div>
    </div>
  );
}
