"use client";

import { useState } from "react";
import { PageHeader } from "@/components/ui/page-header";
import { DataTable } from "@/components/ui/data-table";
import { SearchInput } from "@/components/ui/search-input";
import { useUsers, useUpdateUserRole, useDeactivateUser } from "@/features/users/hooks/use-users";
import { formatRelativeTime } from "@/shared/lib/utils";
import { cn } from "@/shared/lib/utils";
import type { User, UserRole } from "@findspam/types";
import type { Column } from "@/components/ui/data-table";

const ROLE_STYLES: Record<UserRole, string> = {
  SUPER_ADMIN: "bg-violet-500/10 text-violet-400 ring-violet-500/20",
  ADMIN: "bg-blue-500/10 text-blue-400 ring-blue-500/20",
  ANALYST: "bg-cyan-500/10 text-cyan-400 ring-cyan-500/20",
  MODERATOR: "bg-emerald-500/10 text-emerald-400 ring-emerald-500/20",
};

const ROLES: UserRole[] = ["SUPER_ADMIN", "ADMIN", "ANALYST", "MODERATOR"];

function RoleSelect({ user }: { user: User }) {
  const { mutate: updateRole, isPending } = useUpdateUserRole();
  return (
    <select
      value={user.role}
      onChange={(e) => updateRole({ userId: user.id, role: e.target.value as UserRole })}
      disabled={isPending}
      className="h-7 rounded-md border border-border/50 bg-muted/30 px-2 text-xs text-foreground focus:outline-none focus:ring-1 focus:ring-ring disabled:opacity-50"
    >
      {ROLES.map((r) => (
        <option key={r} value={r}>{r.replace(/_/g, " ")}</option>
      ))}
    </select>
  );
}

function DeactivateButton({ user }: { user: User }) {
  const { mutate: deactivate, isPending } = useDeactivateUser();
  if (!user.isActive) return <span className="text-xs text-muted-foreground">Inactive</span>;
  return (
    <button
      onClick={() => deactivate(user.id)}
      disabled={isPending}
      className="rounded-md bg-red-500/10 px-2 py-1 text-[10px] font-medium text-red-400 hover:bg-red-500/20 disabled:opacity-50 transition-colors"
    >
      Deactivate
    </button>
  );
}

const buildColumns = (): Column<User>[] => [
  {
    key: "email",
    header: "User",
    render: (row) => (
      <div>
        <p className="text-xs font-medium text-foreground">{row.email}</p>
      </div>
    ),
  },
  {
    key: "role",
    header: "Role",
    width: "140px",
    render: (row) => <RoleSelect user={row} />,
  },
  {
    key: "isActive",
    header: "Status",
    width: "90px",
    render: (row) => (
      <span
        className={cn(
          "inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-[10px] font-medium ring-1",
          row.isActive
            ? "bg-emerald-500/10 text-emerald-400 ring-emerald-500/20"
            : "bg-muted/50 text-muted-foreground ring-border",
        )}
      >
        {row.isActive ? "Active" : "Inactive"}
      </span>
    ),
  },
  {
    key: "createdAt",
    header: "Joined",
    sortable: true,
    width: "110px",
    render: (row) => (
      <span className="text-xs text-muted-foreground">
        {formatRelativeTime(row.createdAt)}
      </span>
    ),
  },
  {
    key: "actions",
    header: "",
    width: "100px",
    render: (row) => <DeactivateButton user={row} />,
  },
];

export default function UsersPage() {
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState("");
  const { data, isLoading } = useUsers(page, search || undefined);

  return (
    <div className="space-y-6">
      <PageHeader
        title="Users"
        description="Admin user accounts, roles, and access control"
        breadcrumbs={[{ label: "Dashboard" }, { label: "Users" }]}
      />

      <SearchInput
        placeholder="Search by email…"
        value={search}
        onChange={(s) => { setSearch(s); setPage(1); }}
        className="max-w-xs"
      />

      <DataTable
        columns={buildColumns()}
        data={data?.items ?? []}
        getRowKey={(row) => row.id}
        loading={isLoading}
        emptyMessage="No users found"
        totalCount={data?.total}
        pageSize={20}
        page={page}
        onPageChange={setPage}
      />
    </div>
  );
}
