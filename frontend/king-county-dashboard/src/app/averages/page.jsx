import AveragesChart from "@/components/charts/AveragesChart";
import SideBar from "@/components/UI/SideBar";

export default function AveragesPage() {
  return (
    <div className="flex min-h-screen">
      <main className="flex-grow p-6 bg-gray-100">
        <div className="w-full max-w-7xl mx-auto">
          <AveragesChart />
        </div>
      </main>
    </div>
  );
}
