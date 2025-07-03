import AveragesChart from "../components/charts/AveragesChart"
import OverTimeChart from "../components/charts/OverTimeChart"
import CorrelationHeatMap from "../components/charts/CorrelationHeatMap"
import PriceCategoryChart from "../components/charts/PriceCategoryChart"
import SideBar from "@/components/UI/SideBar"
import Link from "next/link";

export default function HomePage() {
  return (
    <div className="p-4 bg-gray-100 min-h-screen">
      <SideBar />
      <div className="max-w-6xl mx-auto bg-white rounded-xl shadow-lg p-4">
        <h1 className="text-3xl font-bold mb-6 text-center text-gray-800">King County Housing Price Analysis Overview</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Averages Chart */}
          <div className="relative bg-gray-50 rounded-lg shadow p-3 hover:shadow-md transition">
            <AveragesChart compact />
            <Link href="/averages" passHref legacyBehavior>
              <a className="absolute inset-0 z-10" aria-label="Go to Averages Page" />
            </Link>
          </div>

          {/* Over Time Chart */}
          <div className="relative bg-gray-50 rounded-lg shadow p-3 hover:shadow-md transition">
            <OverTimeChart compact />
            <Link href="/priceTrends" passHref legacyBehavior>
              <a className="absolute inset-0 z-10" aria-label="Go to Over Time Page" />
            </Link>
          </div>

          {/* Correlation Heat Map */}
          <div className="relative bg-gray-50 rounded-lg shadow p-3 hover:shadow-md transition">
            <CorrelationHeatMap compact />
            <Link href="/correlations" passHref legacyBehavior>
              <a className="absolute inset-0 z-10" aria-label="Go to Correlations Page" />
            </Link>
          </div>

          {/* Price Category Chart */}
          <div className="relative bg-gray-50 rounded-lg shadow p-3 hover:shadow-md transition">
            <PriceCategoryChart compact />
            <Link href="/priceCategories" passHref legacyBehavior>
              <a className="absolute inset-0 z-10" aria-label="Go to Category Frequency Page" />
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}