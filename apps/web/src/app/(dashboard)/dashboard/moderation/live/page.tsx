"use client";

import { PageHeader } from "@/components/ui/page-header";
import { LiveFeedWidget } from "@/features/overview/components/live-feed-widget";
import { useRealtimeFeed } from "@/shared/hooks/use-realtime-feed";

export default function ModerationLivePage() {
  useRealtimeFeed();

  return (
    <div className="space-y-6">
      <PageHeader
        title="Live Moderation Feed"
        description="Real-time stream of all moderation events across monitored groups"
        breadcrumbs={[
          { label: "Dashboard" },
          { label: "Moderation" },
          { label: "Live Feed" },
        ]}
      />
      <LiveFeedWidget />
    </div>
  );
}
