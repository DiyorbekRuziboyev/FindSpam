"use client";

import { useState } from "react";
import { PageHeader } from "@/components/ui/page-header";
import { PredictionRow } from "@/features/ai-engine/components/prediction-row";
import { usePredictions } from "@/features/ai-engine/hooks/use-ai-engine";
import { SearchInput } from "@/components/ui/search-input";
import { EmptyState } from "@/components/ui/empty-state";
import { SkeletonCard } from "@/components/ui/skeleton";
import { ChevronLeft, ChevronRight, Zap } from "lucide-react";

export default function PredictionsPage() {
  const [page, setPage] = useState(1);
  const [threatFilter, setThreatFilter] = useState("");

  const { data, isLoading } = usePredictions({
    page,
    pageSize: 25,
    threatLevel: threatFilter || undefined,
  });

  return (
    <div className="space-y-6">
      <PageHeader
        title="AI Predictions"
        description="Full history of AI inference results with explanations"
        breadcrumbs={[
          { label: "Dashboard" },
          { label: "AI Engine" },
          { label: "Predictions" },
        ]}
      />

      <div className="flex items-center gap-3">
        <select
          value={threatFilter}
          onChange={(e) => { setThreatFilter(e.target.value); setPage(1); }}
          className="h-9 rounded-lg border border-border/50 bg-muted/30 px-3 text-sm text-foreground focus:outline-none focus:ring-1 focus:ring-ring"
        >
          <option value="">All threats</option>
          {["NONE", "LOW", "MEDIUM", "HIGH", "CRITICAL"].map((l) => (
            <option key={l} value={l}>{l}</option>
          ))}
        </select>
      </div>

      {isLoading ? (
        <div className="space-y-3">
          {[1, 2, 3, 4, 5].map((i) => <SkeletonCard key={i} />)}
        </div>
      ) : !data?.items.length ? (
        <EmptyState
          icon={<Zap className="h-5 w-5" />}
          title="No predictions found"
          description="AI predictions will appear here as messages are analyzed"
        />
      ) : (
        <div className="space-y-2">
          {data.items.map((p) => (
            <PredictionRow key={p.id} prediction={p} />
          ))}
        </div>
      )}

      {data && data.totalPages > 1 && (
        <div className="flex items-center justify-between">
          <p className="text-xs text-muted-foreground">
            Page {page} of {data.totalPages} — {data.total.toLocaleString()} total
          </p>
          <div className="flex items-center gap-1">
            <button
              onClick={() => setPage((p) => p - 1)}
              disabled={page <= 1}
              className="flex h-7 w-7 items-center justify-center rounded-md border border-border/50 text-muted-foreground hover:bg-muted/60 hover:text-foreground disabled:opacity-40 disabled:cursor-not-allowed"
            >
              <ChevronLeft className="h-3.5 w-3.5" />
            </button>
            <button
              onClick={() => setPage((p) => p + 1)}
              disabled={page >= data.totalPages}
              className="flex h-7 w-7 items-center justify-center rounded-md border border-border/50 text-muted-foreground hover:bg-muted/60 hover:text-foreground disabled:opacity-40 disabled:cursor-not-allowed"
            >
              <ChevronRight className="h-3.5 w-3.5" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
