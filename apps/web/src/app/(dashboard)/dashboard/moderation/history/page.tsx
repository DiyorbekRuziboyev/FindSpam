"use client";

import { useState } from "react";
import { PageHeader } from "@/components/ui/page-header";
import { DataTable } from "@/components/ui/data-table";
import { ModerationFilters } from "@/features/moderation/components/moderation-filters";
import { ThreatBadge } from "@/components/ui/threat-badge";
import { ActionBadge } from "@/components/ui/action-badge";
import { useModerationHistory } from "@/features/moderation/hooks/use-moderation";
import { formatRelativeTime, formatConfidence, truncate } from "@/shared/lib/utils";
import type { ModerationEvent } from "@findspam/types";
import type { Column } from "@/components/ui/data-table";

const COLUMNS: Column<ModerationEvent>[] = [
  {
    key: "createdAt",
    header: "Time",
    sortable: true,
    width: "120px",
    render: (row) => (
      <span className="text-xs text-muted-foreground">
        {formatRelativeTime(row.createdAt)}
      </span>
    ),
  },
  {
    key: "messageText",
    header: "Message",
    render: (row) => (
      <span className="text-xs text-foreground">{truncate(row.messageText, 100)}</span>
    ),
  },
  {
    key: "threatLevel",
    header: "Threat",
    width: "100px",
    render: (row) => <ThreatBadge level={row.threatLevel} size="sm" />,
  },
  {
    key: "actionTaken",
    header: "Action",
    width: "80px",
    render: (row) => <ActionBadge action={row.actionTaken} size="sm" />,
  },
  {
    key: "confidence",
    header: "Confidence",
    sortable: true,
    width: "100px",
    render: (row) => (
      <span className="text-xs font-mono text-foreground">
        {formatConfidence(row.prediction.confidence)}
      </span>
    ),
  },
];

export default function ModerationHistoryPage() {
  const [page, setPage] = useState(1);
  const [filters, setFilters] = useState({ search: "", threatLevel: "", action: "" });

  const { data, isLoading } = useModerationHistory({
    page,
    pageSize: 20,
    search: filters.search || undefined,
    threatLevel: filters.threatLevel || undefined,
    action: filters.action || undefined,
  });

  return (
    <div className="space-y-6">
      <PageHeader
        title="Moderation History"
        description="All recorded moderation events with full audit trail"
        breadcrumbs={[
          { label: "Dashboard" },
          { label: "Moderation" },
          { label: "History" },
        ]}
      />

      <ModerationFilters
        filters={filters}
        onChange={(f) => {
          setFilters((prev) => ({ ...prev, ...f }));
          setPage(1);
        }}
      />

      <DataTable
        columns={COLUMNS}
        data={data?.items ?? []}
        getRowKey={(row) => row.id}
        loading={isLoading}
        emptyMessage="No moderation events found"
        totalCount={data?.total}
        pageSize={20}
        page={page}
        onPageChange={setPage}
      />
    </div>
  );
}
