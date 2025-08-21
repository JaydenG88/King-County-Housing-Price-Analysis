import AveragesChart from "../components/charts/AveragesChart";
import OverTimeChart from "../components/charts/OverTimeChart";
import CorrelationHeatMap from "../components/charts/CorrelationHeatMap";
import PriceDistributionChart from "../components/charts/PriceDistributionChart";
import Link from "next/link";

export default function HomePage() {
  return (
    <main className="flex-1 p-6 overflow-y-auto bg-gray-100">
      <div className="p-4 bg-gray-100 min-h-screen">
        <div className="bg-white rounded-xl shadow-lg p-4">
          <h1 className="text-3xl font-bold mb-6 text-center text-gray-800">
            King County Housing Price Analysis Overview
          </h1>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="relative bg-gray-50 rounded-lg shadow p-3 hover:scale-102 hover:shadow-lg transition-transform duration-300">
              <AveragesChart compact />
              <Link href="/averages" className="absolute inset-0 z-10" aria-label="Go to Averages Page" />
            </div>
            <div className="relative bg-gray-50 rounded-lg shadow p-3 hover:scale-102 hover:shadow-lg transition-transform duration-300">
              <OverTimeChart compact />
              <Link href="/priceTrends" className="absolute inset-0 z-10" aria-label="Go to Over Time Page" />
            </div>
            <div className="relative bg-gray-50 rounded-lg shadow p-3 hover:scale-102 hover:shadow-lg transition-transform duration-300">
              <CorrelationHeatMap compact />
              <Link href="/correlations" className="absolute inset-0 z-10" aria-label="Go to Correlations Page" />
            </div>
            <div className="relative bg-gray-50 rounded-lg shadow p-3 hover:scale-102 hover:shadow-lg transition-transform duration-300">
              <PriceDistributionChart compact />
              <Link href="/priceDistributions" className="absolute inset-0 z-10" aria-label="Go to Price Distribution Page" />
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
