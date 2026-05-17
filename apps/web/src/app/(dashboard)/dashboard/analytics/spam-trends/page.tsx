import type { Metadata } from "next";
import { PageHeader } from "@/components/ui/page-header";
import { SpamTrendsChart } from "@/features/analytics/components/spam-trends-chart";
import { CategoryChart } from "@/features/analytics/components/category-chart";

export const metadata: Metadata = { title: "Spam Trends" };

export default function SpamTrendsPage() {
  return (
    <div className="space-y-6">
      <PageHeader
        title="Spam Trends"
        description="Historical spam volume and category breakdown"
        breadcrumbs={[
          { label: "Dashboard" },
          { label: "Analytics" },
          { label: "Spam Trends" },
        ]}
      />
      <SpamTrendsChart />
      <CategoryChart />
    </div>
  );
}
