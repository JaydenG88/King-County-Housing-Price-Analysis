import AveragesChart from "../components/charts/AveragesChart"
import OverTimeChart from "../components/charts/OverTimeChart"
import CorrelationHeatMap from "../components/charts/CorrelationHeatMap"
import PriceCategoryChart from "../components/charts/PriceCategoryChart"
import SideBar from "@/components/UI/SideBar"
import Link from "next/link";
export default function HomePage() {
  return (
    <div className="flex min-h-screen bg-gray-100">
        <SideBar />
      <main className="flex-1 p-6">
        <div className="w-full max-w-7xl mx-auto">
          <div className="bg-white rounded-xl shadow-lg p-4">
            <h1 className="text-3xl font-bold mb-6 text-center text-gray-800">
              King County Housing Price Analysis Overview
            </h1>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="relative bg-gray-50 rounded-lg shadow p-3 hover:shadow-md transition">
                <AveragesChart compact />
                <Link href="/averages" className="absolute inset-0 z-10" aria-label="Go to Averages Page" />
              </div>
              <div className="relative bg-gray-50 rounded-lg shadow p-3 hover:shadow-md transition">
                <OverTimeChart compact />
                <Link href="/priceTrends" className="absolute inset-0 z-10" aria-label="Go to Over Time Page" />
              </div>
              <div className="relative bg-gray-50 rounded-lg shadow p-3 hover:shadow-md transition">
                <CorrelationHeatMap compact />
                <Link href="/correlations" className="absolute inset-0 z-10" aria-label="Go to Correlations Page" />
              </div>
              <div className="relative bg-gray-50 rounded-lg shadow p-3 hover:shadow-md transition">
                <PriceCategoryChart compact />
                <Link href="/priceCategories" className="absolute inset-0 z-10" aria-label="Go to Category Frequency Page" />
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}