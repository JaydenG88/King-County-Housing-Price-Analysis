import AveragesChart from "@/components/charts/AveragesChart";
import PageHeader from "@/components/UI/PageHeader";

export default function AveragesPage() {
  return (
    <div className="max-w-6xl mx-auto">
      <PageHeader title="Averages by Region" subtitle="Compare mean and median price, price per square foot, and square footage across regions." />
      <AveragesChart />
    </div>
  );
}
