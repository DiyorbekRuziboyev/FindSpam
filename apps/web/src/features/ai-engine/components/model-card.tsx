"use client";

import { motion } from "framer-motion";
import { CheckCircle2, Package } from "lucide-react";
import { cn, formatPercent, formatDateTime } from "@/shared/lib/utils";
import type { ModelVersion } from "@findspam/types";

interface ModelCardProps {
  model: ModelVersion;
  onDeploy?: (id: string) => void;
  deploying?: boolean;
}

export function ModelCard({ model, onDeploy, deploying }: ModelCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      className={cn(
        "glass-card rounded-xl p-5",
        model.isActive && "ring-1 ring-primary/30",
      )}
    >
      <div className="flex items-start justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className={cn(
            "flex h-9 w-9 items-center justify-center rounded-lg",
            model.isActive ? "bg-primary/10 text-primary" : "bg-muted/50 text-muted-foreground",
          )}>
            <Package className="h-4 w-4" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-sm font-semibold text-foreground">
                {model.versionTag}
              </span>
              {model.isActive && (
                <span className="flex items-center gap-1 rounded-full bg-emerald-500/10 px-2 py-0.5 text-[10px] font-medium text-emerald-400 ring-1 ring-emerald-500/20">
                  <CheckCircle2 className="h-2.5 w-2.5" />
                  Active
                </span>
              )}
            </div>
            <p className="mt-0.5 text-xs text-muted-foreground">
              {model.modelType} · Trained {formatDateTime(model.trainedAt)}
            </p>
          </div>
        </div>
        {!model.isActive && onDeploy && (
          <button
            onClick={() => onDeploy(model.id)}
            disabled={deploying}
            className="rounded-lg bg-primary/10 px-3 py-1.5 text-xs font-medium text-primary hover:bg-primary/20 disabled:opacity-50 transition-colors"
          >
            {deploying ? "Deploying…" : "Deploy"}
          </button>
        )}
      </div>

      <div className="mt-4 grid grid-cols-3 gap-3">
        {[
          { label: "F1", value: formatPercent(model.metrics.f1Score) },
          { label: "Precision", value: formatPercent(model.metrics.precision) },
          { label: "Recall", value: formatPercent(model.metrics.recall) },
          { label: "AUC", value: formatPercent(model.metrics.auc) },
          { label: "Accuracy", value: formatPercent(model.metrics.accuracy) },
          { label: "FP Rate", value: formatPercent(model.metrics.falsePositiveRate) },
        ].map(({ label, value }) => (
          <div key={label} className="rounded-lg bg-muted/30 p-2.5 text-center">
            <p className="text-[10px] uppercase tracking-wider text-muted-foreground">{label}</p>
            <p className="mt-0.5 text-sm font-semibold text-foreground">{value}</p>
          </div>
        ))}
      </div>
    </motion.div>
  );
}
