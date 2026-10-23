import AveragesChart from "../components/charts/AveragesChart";
import OverTimeChart from "../components/charts/OverTimeChart";
import CorrelationHeatMap from "../components/charts/CorrelationHeatMap";
import PriceDistributionChart from "../components/charts/PriceDistributionChart";
import PageHeader from "@/components/UI/PageHeader";
import Link from "next/link";

export default function HomePage() {
  return (
    <div className="max-w-6xl mx-auto">
      <PageHeader
        title="King County Housing Price Analysis"
        subtitle="Explore pricing trends, correlations, and listing value across King County regions."
      />
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        <div className="relative group rounded-xl transition-transform duration-200 hover:-translate-y-0.5">
          <AveragesChart compact />
          <Link href="/averages" className="absolute inset-0 z-10 rounded-xl ring-0 group-hover:ring-2 group-hover:ring-blue-500/30" aria-label="Go to Averages Page" />
        </div>
        <div className="relative group rounded-xl transition-transform duration-200 hover:-translate-y-0.5">
          <OverTimeChart compact />
          <Link href="/priceTrends" className="absolute inset-0 z-10 rounded-xl ring-0 group-hover:ring-2 group-hover:ring-blue-500/30" aria-label="Go to Over Time Page" />
        </div>
        <div className="relative group rounded-xl transition-transform duration-200 hover:-translate-y-0.5">
          <CorrelationHeatMap compact />
          <Link href="/correlations" className="absolute inset-0 z-10 rounded-xl ring-0 group-hover:ring-2 group-hover:ring-blue-500/30" aria-label="Go to Correlations Page" />
        </div>
        <div className="relative group rounded-xl transition-transform duration-200 hover:-translate-y-0.5">
          <PriceDistributionChart compact />
          <Link href="/priceDistributions" className="absolute inset-0 z-10 rounded-xl ring-0 group-hover:ring-2 group-hover:ring-blue-500/30" aria-label="Go to Price Distribution Page" />
        </div>
      </div>

      <Link
        href="/bestValued"
        className="mt-5 flex items-center justify-between gap-4 rounded-xl border border-slate-200 bg-white shadow-sm p-5 hover:shadow-md hover:border-slate-300 transition-all duration-200"
      >
        <div>
          <h2 className="text-base font-semibold text-slate-900">Best Valued Listings</h2>
          <p className="text-sm text-slate-500 mt-1">Browse current listings with the lowest price per square foot by region.</p>
        </div>
        <span className="text-sm font-medium text-blue-600 whitespace-nowrap">View listings →</span>
      </Link>
    </div>
  );
}
