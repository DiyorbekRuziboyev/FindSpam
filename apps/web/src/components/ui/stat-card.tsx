"use client";

import { motion } from "framer-motion";
import { TrendingUp, TrendingDown, Minus } from "lucide-react";
import { cn, formatNumber } from "@/shared/lib/utils";

interface StatCardProps {
  label: string;
  value: number | string;
  delta?: number;
  deltaLabel?: string;
  icon: React.ReactNode;
  iconClassName?: string;
  loading?: boolean;
  format?: "number" | "percent" | "raw";
}

export function StatCard({
  label,
  value,
  delta,
  deltaLabel,
  icon,
  iconClassName,
  loading = false,
  format = "number",
}: StatCardProps) {
  const displayValue =
    typeof value === "number" && format === "number"
      ? formatNumber(value)
      : value;

  const deltaPositive = delta !== undefined && delta > 0;
  const deltaNegative = delta !== undefined && delta < 0;

  if (loading) {
    return (
      <div className="glass-card rounded-xl p-5">
        <div className="animate-pulse space-y-3">
          <div className="h-4 w-24 rounded bg-muted/50" />
          <div className="h-8 w-32 rounded bg-muted/50" />
          <div className="h-3 w-20 rounded bg-muted/50" />
        </div>
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.25, ease: "easeOut" }}
      className="glass-card shine rounded-xl p-5 hover:neon-glow transition-all duration-300"
    >
      <div className="flex items-start justify-between">
        <div className="space-y-1">
          <p className="text-xs font-medium uppercase tracking-wider text-muted-foreground">
            {label}
          </p>
          <p className="text-2xl font-bold tracking-tight text-foreground">
            {displayValue}
          </p>
        </div>
        <div
          className={cn(
            "flex h-10 w-10 items-center justify-center rounded-lg",
            iconClassName ?? "bg-primary/10 text-primary",
          )}
        >
          {icon}
        </div>
      </div>

      {delta !== undefined && (
        <div className="mt-3 flex items-center gap-1.5">
          {deltaPositive ? (
            <TrendingUp className="h-3.5 w-3.5 text-emerald-500" />
          ) : deltaNegative ? (
            <TrendingDown className="h-3.5 w-3.5 text-red-500" />
          ) : (
            <Minus className="h-3.5 w-3.5 text-muted-foreground" />
          )}
          <span
            className={cn(
              "text-xs font-medium",
              deltaPositive && "text-emerald-500",
              deltaNegative && "text-red-500",
              !deltaPositive && !deltaNegative && "text-muted-foreground",
            )}
          >
            {deltaPositive ? "+" : ""}
            {delta.toFixed(1)}%
          </span>
          {deltaLabel && (
            <span className="text-xs text-muted-foreground">{deltaLabel}</span>
          )}
        </div>
      )}
    </motion.div>
  );
}
