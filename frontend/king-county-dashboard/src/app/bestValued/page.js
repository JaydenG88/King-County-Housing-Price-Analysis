"use client";

import BestValueCard from "@/components/cards/BestValueCard";
import Regions from "@/utils/Regions";
import DropDown from "@/components/UI/DropDown";
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
  <div className="w-full max-w-7xl mx-auto p-4 bg-gray-100 min-h-screen">
    <div className="bg-white rounded-xl shadow-lg p-6">
      <h1 className="text-3xl font-bold mb-6 text-center text-gray-800">
        Best Valued Listings
      </h1>
      
      {/* Loading content area */}
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="flex flex-col items-center space-y-4">
          <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
          <span className="text-gray-600 font-medium text-lg">Loading best valued listings...</span>
          <div className="flex space-x-1 mt-2">
            <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce"></div>
            <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
            <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
          </div>
        </div>
      </div>
    </div>
  </div>
);
if (error) return <div>Error: {error.message}</div>;

  return (
    <div className="w-full max-w-7xl mx-auto p-4 bg-gray-100 min-h-screen">
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h1 className="text-3xl font-bold mb-6 text-center text-gray-800">
          Best Valued Listings
        </h1>

        {/* Region Filter */}
        <div className="mb-6 flex flex-col md:flex-row justify-center items-center gap-4">
          <DropDown
            label="Region"
            value={region}
            onChange={setRegion}
            options={regions.map((r) => ({ label: r, value: r }))}
          />
        </div>

        {/* Card Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 justify-center mx-auto max-w-4xl">
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
    </div>
  );
}
