import type { Metadata } from "next";
import { PageHeader } from "@/components/ui/page-header";
import { StatsRow } from "@/features/overview/components/stats-row";
import { SpamTrendChart } from "@/features/overview/components/spam-trend-chart";
import { ThreatDistributionChart } from "@/features/overview/components/threat-distribution";
import { LiveFeedWidget } from "@/features/overview/components/live-feed-widget";
import { SystemHealth } from "@/features/overview/components/system-health";

export const metadata: Metadata = { title: "Overview" };

export default function OverviewPage() {
  return (
    <div className="space-y-6">
      <PageHeader
        title="Overview"
        description="Real-time platform health and spam detection summary"
        breadcrumbs={[{ label: "Dashboard" }, { label: "Overview" }]}
      />

      <StatsRow />

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <SpamTrendChart />
        </div>
        <ThreatDistributionChart />
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <LiveFeedWidget />
        </div>
        <SystemHealth />
      </div>
    </div>
  );
}
