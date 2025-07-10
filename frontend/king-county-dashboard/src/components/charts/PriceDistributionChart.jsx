"use client";

import { useState, useEffect } from "react";
import { BarChart, XAxis, YAxis, Tooltip, ResponsiveContainer, Bar } from "recharts";
import DropDown from "../UI/DropDown";

export default function PriceDistributionChart({ compact = false }) {
    const [data, setData] = useState([]);
    const [region, setRegion] = useState("Seattle");
    const [regions, setRegions] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function fetchData() {
            try {
                const res = await fetch(`https://king-county-housing-price-analysis.onrender.com/api/price_category_frequency/${region}`);
                if (!res.ok) {
                    throw new Error("Network response was not ok" + res.statusText);
                }
                let data = await res.json();
                setData(data);
            } catch (error) {
                console.error("Error fetching data:", error);
            } finally {
                setLoading(false);
            }
        }

       async function fetchRegions() {
            try {
                const res = await fetch(`https://king-county-housing-price-analysis.onrender.com/api/regions`)
                if (!res.ok) {
                    throw new Error("Network response was not ok" + res.statusText);
                }
                const regionsData = await res.json();
                const filtered = regionsData.filter(region => region.toLowerCase() !== "king county");

                setRegions(filtered);
            } catch (error) {
                setError(error);
            }
        }

        fetchData();
        fetchRegions();

    }, [region])

    if (loading) {
        return <div>Loading...</div>;
    }

    const order = ["Q1 (Lowest 25%)", "Q2 (25%-50%)", "Q3 (50%-75%)", "Q4 (Top 25%)"];
    const chartData = data.sort((a, b) => {
    return order.indexOf(a.category) - order.indexOf(b.category);
    });



    return (
      <div
        className={`bg-white shadow-md rounded-lg ${
          compact
            ? "max-w-md mx-auto"
            : "p-1 w-full md:w-3/4 lg:w-5/6 mx-auto"
        }`}
      >
        <h2 className="text-2xl font-bold mb-6 text-center text-gray-800">Price Bracket Distribution (Quartiles): {region}</h2>
        
        {!compact && (
            <div className="mb-6 flex flex-col md:flex-row justify-center items-center gap-4">
            <DropDown
                label="Region"
                value={region}
                onChange={setRegion}
                options={ regions.map(r => ({ label: r, value: r }))}
                /> 
            </div>
        )}
    <div
        className="w-full"
        style={{
          height: compact ? "300px" : "calc(100vh - 220px)",
          minHeight: "300px",
        }}
      >
        <ResponsiveContainer width="100%" >
            <BarChart data={chartData}             
            margin={{
              top: 20,
              right: 30,
              left: compact ? 0 : 80,
              bottom: 40,
            }}>
                <XAxis dataKey="category" 
                    label={{
                        value: "Quartiles",
                        position: "insideBottom",
                        offset: compact ? 0 : -5,
                        fontSize: compact ? 14 : 18,
                    }}

                    tick={{ fontSize: compact ? 10 : 12 }}
                 />
                <YAxis 
                    type="number"
                    domain={[0, "dataMax"]}
                    label={{
                        value: "Number of Listings",
                        angle: -90,
                        position: "insideLeft",
                        fontSize: compact ? 14 : 18,
                        offset: compact ? 20 : 0,
                    }}
                    tick={{ fontSize: compact ? 10 : 12 }}
                />

                <Tooltip
                    wrapperStyle={{ backgroundColor: "#fff", border: "1px solid #ccc", fontSize: 14, color: "black" }}
                />
                <Bar dataKey="value" fill="#8884d8" />
            </BarChart>
            </ResponsiveContainer>
        </div>
    </div>
    );
}