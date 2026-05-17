"use client";

import { useState } from "react";
import { Trash2 } from "lucide-react";
import { PageHeader } from "@/components/ui/page-header";
import { BlacklistEntryForm } from "@/features/blacklist/components/blacklist-entry-form";
import { DataTable } from "@/components/ui/data-table";
import {
  useBlacklist,
  useRemoveBlacklistEntry,
  type BlacklistEntry,
} from "@/features/blacklist/hooks/use-blacklist";
import { formatRelativeTime } from "@/shared/lib/utils";
import type { Column } from "@/components/ui/data-table";

const COLUMNS: Column<BlacklistEntry>[] = [
  {
    key: "type",
    header: "Type",
    width: "100px",
    render: (row) => (
      <span className="rounded-md bg-muted/50 px-1.5 py-0.5 text-[10px] font-medium text-foreground ring-1 ring-border">
        {row.type}
      </span>
    ),
  },
  {
    key: "value",
    header: "Value",
    render: (row) => (
      <span className="font-mono text-xs text-foreground">{row.value}</span>
    ),
  },
  {
    key: "reason",
    header: "Reason",
    render: (row) => (
      <span className="text-xs text-muted-foreground">{row.reason ?? "—"}</span>
    ),
  },
  {
    key: "createdAt",
    header: "Added",
    sortable: true,
    width: "120px",
    render: (row) => (
      <span className="text-xs text-muted-foreground">
        {formatRelativeTime(row.createdAt)}
      </span>
    ),
  },
  {
    key: "actions",
    header: "",
    width: "60px",
    render: (_row) => <RemoveButton id={_row.id} />,
  },
];

function RemoveButton({ id }: { id: string }) {
  const { mutate: remove, isPending } = useRemoveBlacklistEntry();
  return (
    <button
      onClick={() => remove(id)}
      disabled={isPending}
      className="flex h-7 w-7 items-center justify-center rounded-md text-muted-foreground hover:bg-red-500/10 hover:text-red-400 disabled:opacity-50 transition-colors"
    >
      <Trash2 className="h-3.5 w-3.5" />
    </button>
  );
}

export default function BlacklistPage() {
  const [page, setPage] = useState(1);
  const [typeFilter, setTypeFilter] = useState("");
  const { data, isLoading } = useBlacklist(typeFilter || undefined, page);

  return (
    <div className="space-y-6">
      <PageHeader
        title="Blacklist"
        description="Domains, patterns, and phrases permanently blocked from all groups"
        breadcrumbs={[{ label: "Dashboard" }, { label: "Blacklist" }]}
      />

      <BlacklistEntryForm />

      <div className="flex items-center gap-3">
        <select
          value={typeFilter}
          onChange={(e) => { setTypeFilter(e.target.value); setPage(1); }}
          className="h-9 rounded-lg border border-border/50 bg-muted/30 px-3 text-sm text-foreground focus:outline-none focus:ring-1 focus:ring-ring"
        >
          <option value="">All types</option>
          <option value="DOMAIN">Domain</option>
          <option value="PATTERN">Pattern</option>
          <option value="PHRASE">Phrase</option>
        </select>
      </div>

      <DataTable
        columns={COLUMNS}
        data={data?.items ?? []}
        getRowKey={(row) => row.id}
        loading={isLoading}
        emptyMessage="Blacklist is empty"
        totalCount={data?.total}
        pageSize={20}
        page={page}
        onPageChange={setPage}
      />
    </div>
  );
}
