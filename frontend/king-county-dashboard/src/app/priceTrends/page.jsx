import OverTimeChart from "@/components/charts/OverTimeChart";
import SideBar from "@/components/UI/SideBar";

export default function priceTrendsPage() {
    return (
        <div className="p-4 bg-gray-100 min-h-screen">
            <OverTimeChart />
        </div>
    );
    }