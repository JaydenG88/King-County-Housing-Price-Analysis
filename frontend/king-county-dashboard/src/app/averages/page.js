import AveragesChart from "@/components/charts/AveragesChart";

export default function AveragesPage() {
  return (
    <div className="p-4 bg-gray-100 min-h-screen">
          {/* Averages Chart */}
          <div className="relative bg-gray-50 rounded-lg shadow p-3 hover:shadow-md transition">
            <AveragesChart/>
          </div>
    </div> 
  );
}