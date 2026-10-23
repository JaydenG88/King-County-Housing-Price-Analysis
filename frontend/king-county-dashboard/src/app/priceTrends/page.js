import OverTimeChart from "@/components/charts/OverTimeChart";
import PageHeader from "@/components/UI/PageHeader";

export default function PriceTrendsPage() {
    return (
        <div className="max-w-6xl mx-auto">
            <PageHeader title="Average Cost Over Time" subtitle="Track how price and price per square foot have moved over time by region." />
            <OverTimeChart />
        </div>
    );
}
