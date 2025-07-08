"use client";

import BestValueCard from "@/components/cards/BestValueCard";
import DropDown from "@/components/UI/DropDown";
import { useEffect, useState } from "react";

export default function BestValuedPage() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [region, setRegion] = useState("Seattle");
  const [regions, setRegions] = useState([]);

  useEffect(() => {
    async function fetchRegions() {
      try {
        const res = await fetch("https://king-county-housing-price-analysis.onrender.com/api/regions");
        if (!res.ok) {
          throw new Error("Network response was not ok" + res.statusText);
        }
        const data = await res.json();
        setRegions(data);
      } catch (error) {
        console.error("Error fetching regions:", error);
      }
    }

    async function fetchData() {
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

    fetchRegions();
    fetchData();
    
  }, [region]);

  if (loading) {
    return <div className="w-full max-w-7xl mx-auto p-4">Loading...</div>;
  }

  return (
      <div className="w-full max-w-7xl mx-auto">
        <p>Best Value Page</p>
        <DropDown
          label="Region"
          value={region}
          onChange={setRegion}
          options={regions.map((r) => ({ label: r, value: r }))}
        />
      </div>
  );
}
