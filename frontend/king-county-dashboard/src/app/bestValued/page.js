import BestValueCard from "@/components/cards/BestValueCard";
import SideBar from "@/components/UI/SideBar";
export default function BestValuedPage() {
  return (
        <div className="p-4 bg-gray-100 min-h-screen">
          <SideBar />
          <BestValueCard/>
      </div>
  );
}