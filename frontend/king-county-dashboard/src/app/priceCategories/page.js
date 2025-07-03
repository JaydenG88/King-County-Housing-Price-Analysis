import PriceCategoryChart from "@/components/charts/PriceCategoryChart";
import SideBar from "@/components/UI/SideBar";

export default function PriceCategoriesPage() {
  return (
        <div className="p-4 bg-gray-100 min-h-screen">
          <SideBar />
          <PriceCategoryChart/>
      </div>
  );
}