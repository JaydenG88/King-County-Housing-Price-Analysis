"use client";

import BestValueCard from "@/components/cards/BestValueCard";
import Regions from "@/utils/Regions";
import DropDown from "@/components/UI/DropDown";
import PageHeader from "@/components/UI/PageHeader";
import { useEffect, useState } from "react";

export default function BestValuedPage() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [region, setRegion] = useState("Seattle");
  const [regions, setRegions] = useState([]);

  useEffect(() => {

    async function fetchData() {

      try {
        const regionList = await Regions();
        if (regionList.length > 0) {
          setRegions(regionList);
        }
      } catch (error) {
        setError(error);
      }

      try {
        const res = await fetch(`https://king-county-housing-price-analysis.onrender.com/api/lowest_price_per_sqft/${region}`);
        if (!res.ok) {
          throw new Error("Network response was not ok" + res.statusText);
        }
        const data = await res.json();
        setData(data);
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setLoading(false);
      }
    }

    fetchData();

  }, [region]);

if (loading) return (
  <div className="max-w-6xl mx-auto">
    <PageHeader title="Best Valued Listings" subtitle="Current listings with the lowest price per square foot by region." />
    <div className="flex items-center justify-center min-h-[400px] bg-white border border-slate-200 rounded-xl">
      <div className="flex flex-col items-center space-y-3">
        <div className="w-8 h-8 border-2 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
        <span className="text-slate-500 text-sm font-medium">Loading best valued listings…</span>
      </div>
    </div>
  </div>
);
if (error) return <div className="text-sm text-red-600">Error: {error.message}</div>;

  return (
    <div className="max-w-6xl mx-auto">
      <PageHeader title="Best Valued Listings" subtitle="Current listings with the lowest price per square foot by region." />

      {/* Region Filter */}
      <div className="mb-5">
        <DropDown
          label="Region"
          value={region}
          onChange={setRegion}
          options={regions.map((r) => ({ label: r, value: r }))}
        />
      </div>

      {/* Card Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
        {data.map((item, index) => (
          <BestValueCard
            key={index}
            sqft={item.sqft}
            price={item.price}
            zip={item.zip}
            city={item.city}
            state={item.state}
            street_address={item.street_address}
            bedrooms={item.bedrooms}
            bathrooms={item.bathrooms}
            url={item.URL}
            image={item.image}
            price_per_sqft={item.price_per_sqft}
            price_category={item.price_category}
          />
        ))}
      </div>
    </div>
  );
}
