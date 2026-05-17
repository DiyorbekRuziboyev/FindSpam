"use client";

import { motion } from "framer-motion";
import { cn } from "@/shared/lib/utils";

interface ChartCardProps {
  title: string;
  description?: string;
  action?: React.ReactNode;
  children: React.ReactNode;
  className?: string;
  loading?: boolean;
  minHeight?: number;
}

export function ChartCard({
  title,
  description,
  action,
  children,
  className,
  loading = false,
  minHeight = 260,
}: ChartCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, ease: "easeOut" }}
      className={cn("glass-card rounded-xl p-5", className)}
    >
      <div className="mb-4 flex items-start justify-between gap-4">
        <div>
          <h3 className="text-sm font-semibold text-foreground">{title}</h3>
          {description && (
            <p className="mt-0.5 text-xs text-muted-foreground">{description}</p>
          )}
        </div>
        {action && <div className="shrink-0">{action}</div>}
      </div>

      {loading ? (
        <div
          className="animate-pulse rounded-lg bg-muted/30"
          style={{ minHeight }}
        />
      ) : (
        <div style={{ minHeight }}>{children}</div>
      )}
    </motion.div>
  );
}
