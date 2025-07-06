"use client";

import { useState, useEffect } from "react";
import {
  LineChart,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Line,
} from "recharts";
import DropDown from "../UI/DropDown";

export default function OverTimeChart({ compact = false }) {
  const [data, setData] = useState([]);
  const [regions, setRegions] = useState([]);
  const [metric, setMetric] = useState("price");
  const [type, setType] = useState("mean");
  const [region, setRegion] = useState("King County");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchData() {
      try {
        const dataRes = await fetch(
          `https://king-county-housing-price-analysis.onrender.com/api/price_trends/${region}/${metric}/${type}`
        );
        if (!dataRes.ok) {
          throw new Error("Network response was not ok " + dataRes.statusText);
        }

        let json = await dataRes.json();

        const formatted = json.map((item) => ({
          date: item.date,
          value: Number(item.value.toFixed(2)),
        }));

        setData(formatted);
      } catch (error) {
        setError(error);
      } finally {
        setLoading(false);
      }
    }

    async function fetchRegions() {
      try {
        const res = await fetch(
          `https://king-county-housing-price-analysis.onrender.com/api/regions`
        );
        if (!res.ok) {
          throw new Error("Network response was not ok " + res.statusText);
        }
        const regionsData = await res.json();
        setRegions(regionsData);
      } catch (error) {
        setError(error);
      }
    }

    fetchRegions();
    fetchData();
  }, [type, metric, region]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div
      className={`bg-white shadow-md rounded-lg ${
        compact
          ? "max-w-md mx-auto"
          : "p-1 w-full md:w-3/4 lg:w-5/6 mx-auto"
      }`}
    >
      <h2 className="text-2xl font-bold mb-4 text-center text-gray-800">
        Average Cost Over Time
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
              label="Region"
              value={region}
              onChange={setRegion}
              options={regions.map((r) => ({ label: r, value: r }))}
            />
          </div>
        </div>
      )}

      <div
        className="w-full"
        style={{
          height: compact ? "300px" : "calc(100vh - 220px)",
          minHeight: "300px",
        }}
      >
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <XAxis
              dataKey="date"
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
            <YAxis
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
            <Line
              type="monotone"
              dataKey="value"
              stroke="#8884d8"
              strokeWidth={2}
              dot={{ r: 2 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
