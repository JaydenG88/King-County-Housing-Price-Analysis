"use client";

import dynamic from "next/dynamic";

const CorrelationHeatMap = dynamic(() => import('@/components/charts/CorrelationHeatMap'), {
    ssr: false,
});

export default function CorrelationsPage() {
    return (
      <div className="p-4 bg-gray-100 min-h-screen">
          <CorrelationHeatMap />
      </div>
    );
    }