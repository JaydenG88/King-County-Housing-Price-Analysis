"use client";

import { useState, useEffect } from "react";
import { BarChart, XAxis, YAxis, Tooltip, ResponsiveContainer, Bar } from "recharts";
import DropDown from "../UI/DropDown";

export default function AveragesChart({ compact = false }) {
  const [averages, setAverages] = useState([]);
  const [type, setType] = useState("mean");
  const [sort, setSort] = useState("Name");
  const [metric, setMetric] = useState("price");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchData() {
      try {
        const res = await fetch(
          `https://king-county-housing-price-analysis.onrender.com/api/averages/${metric}/${type}`
        );
        if (!res.ok) {
          throw new Error("Network response was not ok" + res.statusText);
        }
        let data = await res.json();

        data = data.map((item) => ({
          region: item.region,
          value: Number(item.value.toFixed(2)),
        }));

        if (sort === "Name") {
          data.sort((a, b) => a.region.localeCompare(b.region));
        } else if (sort === "Lowest") {
          data.sort((a, b) => a.value - b.value);
        } else if (sort === "Highest") {
          data.sort((a, b) => b.value - a.value);
        }

        setAverages(data);
      } catch (error) {
        setError(error);
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, [type, metric, sort]);

if (loading) return (
  <div className="flex items-center justify-center min-h-[300px] bg-white shadow-md rounded-lg">
    <div className="flex flex-col items-center space-y-4">
      <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
      <span className="text-gray-600 font-medium">Loading chart data...</span>
    </div>
  </div>
);
if (error) return <div>Error: {error.message}</div>;

  return (
    <div className={`bg-white shadow-md rounded-lg ${compact ? "max-w-md mx-auto" : "p-1 w-full md:w-3/4 lg:w-5/6 mx-auto"}`}>
      <h2 className="text-2xl font-bold mb-4 text-center text-gray-800">
        Averages by Region
      </h2>

      {!compact && (
        <div className="px-4">
          <div className="mb-6 flex flex-col md:flex-row justify-center items-center gap-4">
            <DropDown
              label="Metric"
              value={metric}
              onChange={setMetric}
              options={[
                { label: "Price", value: "price" },
                { label: "Price per Square Foot", value: "price_per_sqft" },
                { label: "Square Footage", value: "sqft" },
              ]}
            />
            <DropDown
              label="Type"
              value={type}
              onChange={setType}
              options={[
                { label: "Mean", value: "mean" },
                { label: "Median", value: "median" },
              ]}
            />
            <DropDown
              label="Sort By"
              value={sort}
              onChange={setSort}
              options={[
                { label: "Name", value: "Name" },
                { label: "Lowest", value: "Lowest" },
                { label: "Highest", value: "Highest" },
              ]}
            />
          </div>
        </div>
      )}

      {/* Responsive height container */}
      <div
        className="w-full"
        style={{
          height: compact ? "300px" : "calc(100vh - 150px)", 
          minHeight: "300px",
        }}
      >
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={averages}
            layout="vertical"
            margin={{ top: 20, right: 30, left: compact ? 0 : 80, bottom: 40 }}
            barGap={0}
          >
            <XAxis
              type="number"
              label={{
                value:
                  metric === "price"
                    ? "Average Price ($)"
                    : metric === "price_per_sqft"
                    ? "Average Price per Sqft ($)"
                    : "Average Square Footage",
                position: "bottom",
                offset: 10,
                fontSize: compact ? 14 : 18,
              }}
            />
            <YAxis
              dataKey="region"
              type="category"
              width={compact ? 90 : 150}
              interval={0}
              label={{
                value: "King County Regions",
                angle: -90,
                position: "insideLeft",
                offset: compact ? 50 : 0,
                fontSize: compact ? 14 : 18,
              }}
              tick={({ x, y, payload }) => (
                <text
                  x={x}
                  y={y}
                  fill="#000"
                  fontSize={compact ? 10 : 12}
                  textAnchor="end"
                  alignmentBaseline="middle"
                >
                  {!compact ? payload.value : ""}
                </text>
              )}
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
