"use client";

import { PageHeader } from "@/components/ui/page-header";
import { EmptyState } from "@/components/ui/empty-state";
import { EventCard } from "@/features/moderation/components/event-card";
import { useModerationQueue, useApproveAction } from "@/features/moderation/hooks/use-moderation";
import { SkeletonCard } from "@/components/ui/skeleton";
import { ListChecks } from "lucide-react";

export default function ModerationQueuePage() {
  const { data: queue, isLoading } = useModerationQueue();
  const { mutate: approve } = useApproveAction();

  return (
    <div className="space-y-6">
      <PageHeader
        title="Moderation Queue"
        description="Pending review items requiring admin decision"
        breadcrumbs={[
          { label: "Dashboard" },
          { label: "Moderation" },
          { label: "Queue" },
        ]}
      />

      {isLoading ? (
        <div className="space-y-4">
          {[1, 2, 3].map((i) => (
            <SkeletonCard key={i} />
          ))}
        </div>
      ) : !queue?.length ? (
        <EmptyState
          icon={<ListChecks className="h-5 w-5" />}
          title="Queue is empty"
          description="All flagged messages have been reviewed"
        />
      ) : (
        <div className="space-y-4">
          {queue.map((item) => (
            <EventCard
              key={item.event.id}
              event={item.event}
              showActions
              onAction={(eventId, action) => approve({ eventId, action })}
            />
          ))}
        </div>
      )}
    </div>
  );
}
