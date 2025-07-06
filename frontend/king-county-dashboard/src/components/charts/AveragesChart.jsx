"use client";

import { useState, useEffect } from "react";
import { BarChart, XAxis, YAxis, Tooltip, ResponsiveContainer, Bar } from "recharts";
import DropDown from "../UI/DropDown";

export default function AveragesChart({ compact = false }) {
  const [averages, setAverages] = useState([]);
  const [type, setType] = useState("mean");
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

        setAverages(data);
      } catch (error) {
        setError(error);
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, [type, metric]);

  if (loading) return <div>Loading...</div>;
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
          </div>
        </div>
      )}

      {/* Responsive height container */}
      <div
        className="w-full"
        style={{
          height: compact ? "300px" : "calc(100vh - 220px)", 
          minHeight: "300px",
        }}
      >
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={averages}
            layout="vertical"
            margin={{ top: 0, right: 30, left: compact ? -20 : 0, bottom: 20 }}
            barGap={0}
          >
            <XAxis type="number" />
            <YAxis
              dataKey="region"
              type="category"
              width={compact ? 90 : 150}
              interval={0}
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
            <Tooltip />
            <Bar dataKey="value" fill="#8884d8" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
