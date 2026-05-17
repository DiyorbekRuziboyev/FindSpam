"use client";

import { useState } from "react";
import { PageHeader } from "@/components/ui/page-header";
import { DataTable } from "@/components/ui/data-table";
import { useQuery } from "@tanstack/react-query";
import { apiClient } from "@/shared/lib/api-client";
import { formatDateTime } from "@/shared/lib/utils";
import type { Column } from "@/components/ui/data-table";

interface AuditRecord {
  id: string;
  actorEmail: string;
  action: string;
  resourceType: string;
  resourceId: string;
  ipAddress: string | null;
  createdAt: string;
  metadata: Record<string, unknown>;
}

const COLUMNS: Column<AuditRecord>[] = [
  {
    key: "createdAt",
    header: "Time",
    sortable: true,
    width: "160px",
    render: (row) => (
      <span className="text-xs text-muted-foreground font-mono">
        {formatDateTime(row.createdAt)}
      </span>
    ),
  },
  {
    key: "actorEmail",
    header: "Actor",
    width: "200px",
    render: (row) => (
      <span className="text-xs text-foreground">{row.actorEmail}</span>
    ),
  },
  {
    key: "action",
    header: "Action",
    width: "160px",
    render: (row) => (
      <span className="rounded-md bg-muted/50 px-1.5 py-0.5 text-[10px] font-mono text-foreground ring-1 ring-border">
        {row.action}
      </span>
    ),
  },
  {
    key: "resourceType",
    header: "Resource",
    width: "120px",
    render: (row) => (
      <span className="text-xs text-muted-foreground">{row.resourceType}</span>
    ),
  },
  {
    key: "ipAddress",
    header: "IP",
    width: "130px",
    render: (row) => (
      <span className="font-mono text-xs text-muted-foreground">
        {row.ipAddress ?? "—"}
      </span>
    ),
  },
];

export default function AuditPage() {
  const [page, setPage] = useState(1);
  const { data, isLoading } = useQuery({
    queryKey: ["audit", page],
    queryFn: () =>
      apiClient.get<{ items: AuditRecord[]; total: number }>(
        `/audit?page=${page}&page_size=25`,
      ),
    placeholderData: (prev) => prev,
  });

  return (
    <div className="space-y-6">
      <PageHeader
        title="Audit Log"
        description="Immutable record of all admin actions and system mutations"
        breadcrumbs={[{ label: "Dashboard" }, { label: "Audit Log" }]}
      />

      <DataTable
        columns={COLUMNS}
        data={data?.items ?? []}
        getRowKey={(row) => row.id}
        loading={isLoading}
        emptyMessage="No audit records"
        totalCount={data?.total}
        pageSize={25}
        page={page}
        onPageChange={setPage}
      />
    </div>
  );
}
