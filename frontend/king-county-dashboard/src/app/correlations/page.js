"use client";

import dynamic from "next/dynamic";
import PageHeader from "@/components/UI/PageHeader";

const CorrelationHeatMap = dynamic(() => import('@/components/charts/CorrelationHeatMap'), {
    ssr: false,
});

export default function CorrelationsPage() {
    return (
      <div className="max-w-6xl mx-auto">
          <PageHeader title="Correlation Heat Map" subtitle="Explore how housing metrics relate to one another across King County." />
          <CorrelationHeatMap />
      </div>
    );
}
