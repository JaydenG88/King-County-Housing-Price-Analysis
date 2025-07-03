import CorrelationHeatMap from "@/components/charts/CorrelationHeatMap";
import SideBar from "@/components/UI/SideBar";

export default function CorrelationsPage() {
    return (
        <div className="p-4 bg-gray-100 min-h-screen">
          <SideBar />
          <CorrelationHeatMap />
      </div>
    );
    }