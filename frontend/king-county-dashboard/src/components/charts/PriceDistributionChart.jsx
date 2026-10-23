"use client";

import { useState, useEffect } from "react";
import { BarChart, XAxis, YAxis, Tooltip, ResponsiveContainer, Bar } from "recharts";
import DropDown from "../UI/DropDown";
import Regions from "@/utils/Regions";

function PriceDistributionTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  return (
    <div className="bg-white border border-slate-200 rounded-lg shadow-md px-3 py-2">
      <div className="text-xs font-semibold text-slate-900">{label}</div>
      <div className="text-xs text-blue-600 font-medium mt-0.5">{payload[0].value.toLocaleString()} listings</div>
    </div>
  );
}

export default function PriceDistributionChart({ compact = false }) {
    const [data, setData] = useState([]);
    const [region, setRegion] = useState("Seattle");
    const [regions, setRegions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function fetchData() {
            try {
                const regionList = await Regions();
                const filteredRegions = regionList.filter(r => r !== "King County");
                if (filteredRegions.length > 0) {
                    setRegions(filteredRegions);
                }
            } catch (error) {
                setError(error);
            }

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

        fetchData();


    }, [region])

    if (loading) return (
      <div className="flex items-center justify-center min-h-[300px] bg-white border border-slate-200 rounded-xl">
        <div className="flex flex-col items-center space-y-3">
          <div className="w-7 h-7 border-2 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
          <span className="text-slate-500 text-sm font-medium">Loading chart data…</span>
        </div>
      </div>
    );
    if (error) return <div className="text-sm text-red-600">Error: {error.message}</div>;

    const order = ["Q1 (Lowest 25%)", "Q2 (25%-50%)", "Q3 (50%-75%)", "Q4 (Top 25%)"];
    const chartData = data.sort((a, b) => {
    return order.indexOf(a.category) - order.indexOf(b.category);
    });



    return (
      <div className={`bg-white border border-slate-200 rounded-xl shadow-sm ${compact ? "max-w-md mx-auto" : "w-full"}`}>
        <div className={`flex flex-col gap-3 ${compact ? "p-4" : "p-5"} ${!compact ? "md:flex-row md:items-center md:justify-between border-b border-slate-100" : ""}`}>
          <h2 className="text-base font-semibold text-slate-900">
            Price Bracket Distribution (Quartiles) — {region}
          </h2>

          {!compact && (
              <DropDown
                  label="Region"
                  value={region}
                  onChange={setRegion}
                  options={ regions.map(r => ({ label: r, value: r }))}
                  />
          )}
        </div>
        <div
            className={`w-full ${compact ? "px-2 pb-3" : "px-2 pb-4"}`}
            style={{
              height: compact ? "260px" : "calc(100vh - 230px)",
              minHeight: "280px",
            }}
          >
            <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData}
                margin={{
                  top: 16,
                  right: 24,
                  left: compact ? 0 : 60,
                  bottom: 30,
                }}>
                    <XAxis dataKey="category"
                        tick={{ fontSize: compact ? 10 : 12, fill: "#64748b" }}
                        axisLine={{ stroke: "#e2e8f0" }}
                        tickLine={false}
                        label={{
                            value: "Quartiles",
                            position: "insideBottom",
                            offset: compact ? 0 : -5,
                            fontSize: compact ? 12 : 13,
                            fill: "#64748b",
                        }}
                     />
                    <YAxis
                        type="number"
                        domain={[0, "dataMax"]}
                        tick={{ fontSize: compact ? 10 : 12, fill: "#64748b" }}
                        axisLine={{ stroke: "#e2e8f0" }}
                        tickLine={false}
                        label={{
                            value: "Number of Listings",
                            angle: -90,
                            position: "insideLeft",
                            fontSize: compact ? 12 : 13,
                            offset: compact ? 15 : -5,
                            fill: "#64748b",
                        }}
                    />

                    <Tooltip
                        cursor={{ fill: "#f1f5f9" }}
                        content={<PriceDistributionTooltip />}
                    />
                    <Bar dataKey="value" fill="#2563eb" radius={[4, 4, 0, 0]} />
                </BarChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
}
