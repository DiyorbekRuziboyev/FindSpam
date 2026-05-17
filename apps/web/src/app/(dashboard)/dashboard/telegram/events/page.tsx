"use client";

import { useState } from "react";
import { PageHeader } from "@/components/ui/page-header";
import { DataTable } from "@/components/ui/data-table";
import { useTelegramEvents } from "@/features/telegram/hooks/use-telegram";
import { formatRelativeTime } from "@/shared/lib/utils";
import type { TelegramBotEvent } from "@findspam/types";
import type { Column } from "@/components/ui/data-table";

const COLUMNS: Column<TelegramBotEvent>[] = [
  {
    key: "processedAt",
    header: "Time",
    sortable: true,
    width: "130px",
    render: (row) => (
      <span className="text-xs text-muted-foreground">
        {formatRelativeTime(row.processedAt)}
      </span>
    ),
  },
  {
    key: "eventType",
    header: "Event",
    width: "160px",
    render: (row) => (
      <span className="rounded-md bg-muted/50 px-1.5 py-0.5 text-[10px] font-medium text-foreground ring-1 ring-border">
        {row.eventType.replace(/_/g, " ")}
      </span>
    ),
  },
  {
    key: "payload",
    header: "Details",
    render: (row) => (
      <span className="font-mono text-[11px] text-muted-foreground">
        {JSON.stringify(row.payload).slice(0, 120)}
      </span>
    ),
  },
];

export default function TelegramEventsPage() {
  const [page, setPage] = useState(1);
  const { data, isLoading } = useTelegramEvents(page);

  return (
    <div className="space-y-6">
      <PageHeader
        title="Bot Events"
        description="Raw Telegram bot event log for debugging and audit"
        breadcrumbs={[
          { label: "Dashboard" },
          { label: "Telegram" },
          { label: "Events" },
        ]}
      />

      <DataTable
        columns={COLUMNS}
        data={data?.items ?? []}
        getRowKey={(row) => row.id}
        loading={isLoading}
        emptyMessage="No bot events recorded"
        totalCount={data?.total}
        pageSize={20}
        page={page}
        onPageChange={setPage}
      />
    </div>
  );
}
