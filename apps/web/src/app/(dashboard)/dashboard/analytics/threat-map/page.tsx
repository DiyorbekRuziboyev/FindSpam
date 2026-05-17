"use client";

import { PageHeader } from "@/components/ui/page-header";
import { ChartCard } from "@/components/ui/chart-card";
import { useHeatmap } from "@/features/analytics/hooks/use-analytics";
import { cn } from "@/shared/lib/utils";

const DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
const HOURS = Array.from({ length: 24 }, (_, i) =>
  i === 0 ? "12am" : i < 12 ? `${i}am` : i === 12 ? "12pm" : `${i - 12}pm`,
);

export default function ThreatMapPage() {
  const { data, isLoading } = useHeatmap();

  const maxCount = Math.max(...(data ?? []).map((p) => p.spamCount), 1);

  const getCell = (hour: number, day: number) =>
    data?.find((p) => p.hour === hour && p.dayOfWeek === day)?.spamCount ?? 0;

  return (
    <div className="space-y-6">
      <PageHeader
        title="Threat Map"
        description="Spam activity heatmap by day and hour (last 30 days)"
        breadcrumbs={[
          { label: "Dashboard" },
          { label: "Analytics" },
          { label: "Threat Map" },
        ]}
      />

      <ChartCard
        title="Spam Activity Heatmap"
        description="Darker cells indicate higher spam volume"
        loading={isLoading}
        minHeight={360}
      >
        <div className="overflow-x-auto">
          <div className="min-w-[640px]">
            {/* Hour labels */}
            <div className="ml-12 mb-1 flex">
              {HOURS.filter((_, i) => i % 3 === 0).map((h) => (
                <div key={h} className="flex-1 text-center text-[10px] text-muted-foreground">
                  {h}
                </div>
              ))}
            </div>

            {DAYS.map((day, dayIdx) => (
              <div key={day} className="flex items-center gap-1 mb-1">
                <span className="w-10 text-right text-[10px] text-muted-foreground pr-2">
                  {day}
                </span>
                {HOURS.map((_, hour) => {
                  const count = getCell(hour, dayIdx);
                  const intensity = count / maxCount;
                  return (
                    <div
                      key={hour}
                      title={`${day} ${HOURS[hour]}: ${count} spam`}
                      className="flex-1 h-7 rounded-sm transition-all"
                      style={{
                        background: intensity === 0
                          ? "rgba(255,255,255,0.03)"
                          : `rgba(239, 68, 68, ${0.1 + intensity * 0.85})`,
                      }}
                    />
                  );
                })}
              </div>
            ))}

            {/* Legend */}
            <div className="ml-12 mt-3 flex items-center gap-2">
              <span className="text-[10px] text-muted-foreground">Less</span>
              {[0.05, 0.2, 0.4, 0.6, 0.8, 1].map((v) => (
                <div
                  key={v}
                  className="h-3 w-3 rounded-sm"
                  style={{ background: `rgba(239, 68, 68, ${v})` }}
                />
              ))}
              <span className="text-[10px] text-muted-foreground">More</span>
            </div>
          </div>
        </div>
      </ChartCard>
    </div>
  );
}
