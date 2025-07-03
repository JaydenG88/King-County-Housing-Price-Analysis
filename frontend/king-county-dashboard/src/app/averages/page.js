import AveragesChart from "@/components/charts/AveragesChart";
import SideBar from "@/components/UI/SideBar";
export default function AveragesPage() {
  return (
        <div className="p-4 bg-gray-100 min-h-screen">
          <SideBar />
          <AveragesChart/>
      </div>
  );
}