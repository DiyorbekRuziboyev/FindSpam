"use client";

import { PageHeader } from "@/components/ui/page-header";
import { GroupRow } from "@/features/telegram/components/group-row";
import { useTelegramGroups } from "@/features/telegram/hooks/use-telegram";
import { SkeletonCard } from "@/components/ui/skeleton";
import { EmptyState } from "@/components/ui/empty-state";
import { SearchInput } from "@/components/ui/search-input";
import { Users } from "lucide-react";
import { useState, useMemo } from "react";
import type { TelegramGroup } from "@findspam/types";

export default function TelegramGroupsPage() {
  const { data: groups, isLoading } = useTelegramGroups();
  const [search, setSearch] = useState("");

  const filtered = useMemo(
    () =>
      (groups ?? []).filter(
        (g: TelegramGroup) =>
          !search ||
          g.title.toLowerCase().includes(search.toLowerCase()) ||
          (g.username ?? "").toLowerCase().includes(search.toLowerCase()),
      ),
    [groups, search],
  );

  return (
    <div className="space-y-6">
      <PageHeader
        title="Telegram Groups"
        description="All monitored groups with spam stats and configuration"
        breadcrumbs={[
          { label: "Dashboard" },
          { label: "Telegram" },
          { label: "Groups" },
        ]}
      />

      <SearchInput
        placeholder="Search groups…"
        value={search}
        onChange={setSearch}
        className="max-w-xs"
      />

      {isLoading ? (
        <div className="space-y-3">
          {[1, 2, 3, 4].map((i) => <SkeletonCard key={i} />)}
        </div>
      ) : !filtered.length ? (
        <EmptyState
          icon={<Users className="h-5 w-5" />}
          title="No groups found"
          description="Add the bot to a Telegram group to start monitoring"
        />
      ) : (
        <div className="space-y-2">
          {filtered.map((group: TelegramGroup) => (
            <GroupRow key={group.id} group={group} />
          ))}
        </div>
      )}
    </div>
  );
}
