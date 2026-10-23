import PriceCategoryChart from "@/components/charts/PriceDistributionChart";
import PageHeader from "@/components/UI/PageHeader";

export default function PriceDistributionsPage() {
  return (
      <div className="max-w-6xl mx-auto">
          <PageHeader title="Price Bracket Distribution" subtitle="See how listings break down across price quartiles by region." />
          <PriceCategoryChart/>
      </div>
  );
}
