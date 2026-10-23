"use client";

import { useState, useEffect } from "react";
import { BarChart, XAxis, YAxis, Tooltip, ResponsiveContainer, Bar } from "recharts";
import DropDown from "../UI/DropDown";

function AveragesTooltip({ active, payload, label, metric }) {
  if (!active || !payload?.length) return null;
  const value = payload[0].value;
  const formatted =
    metric === "sqft" ? `${value.toLocaleString()} sqft` : `$${value.toLocaleString()}`;
  return (
    <div className="bg-white border border-slate-200 rounded-lg shadow-md px-3 py-2">
      <div className="text-xs font-semibold text-slate-900">{label}</div>
      <div className="text-xs text-blue-600 font-medium mt-0.5">{formatted}</div>
    </div>
  );
}

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
    <div className="flex items-center justify-center min-h-[300px] bg-white border border-slate-200 rounded-xl">
      <div className="flex flex-col items-center space-y-3">
        <div className="w-7 h-7 border-2 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
        <span className="text-slate-500 text-sm font-medium">Loading chart data…</span>
      </div>
    </div>
  );
  if (error) return <div className="text-sm text-red-600">Error: {error.message}</div>;

  return (
    <div className={`bg-white border border-slate-200 rounded-xl shadow-sm ${compact ? "max-w-md mx-auto" : "w-full"}`}>
      <div className={`flex flex-col gap-3 ${compact ? "p-4" : "p-5"} ${!compact ? "md:flex-row md:items-center md:justify-between border-b border-slate-100" : ""}`}>
        <h2 className="text-base font-semibold text-slate-900">
          Averages by Region
        </h2>

        {!compact && (
          <div className="flex flex-wrap items-center gap-3">
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
              label="Sort"
              value={sort}
              onChange={setSort}
              options={[
                { label: "Name", value: "Name" },
                { label: "Lowest", value: "Lowest" },
                { label: "Highest", value: "Highest" },
              ]}
            />
          </div>
        )}
      </div>

      {/* Responsive height container */}
      <div
        className={`w-full ${compact ? "px-2 pb-3" : "px-2 pb-4"}`}
        style={{
          height: compact ? "260px" : "calc(100vh - 230px)",
          minHeight: "280px",
        }}
      >
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={averages}
            layout="vertical"
            margin={{ top: 16, right: 24, left: compact ? 0 : 80, bottom: 30 }}
            barGap={0}
          >
            <XAxis
              type="number"
              tick={{ fontSize: 11, fill: "#64748b" }}
              axisLine={{ stroke: "#e2e8f0" }}
              tickLine={false}
              label={{
                value:
                  metric === "price"
                    ? "Average Price ($)"
                    : metric === "price_per_sqft"
                    ? "Average Price per Sqft ($)"
                    : "Average Square Footage",
                position: "bottom",
                offset: 8,
                fontSize: compact ? 12 : 13,
                fill: "#64748b",
              }}
            />
            <YAxis
              dataKey="region"
              type="category"
              width={compact ? 90 : 150}
              interval={0}
              axisLine={{ stroke: "#e2e8f0" }}
              tickLine={false}
              tick={({ x, y, payload }) => (
                <text
                  x={x}
                  y={y}
                  fill="#334155"
                  fontSize={compact ? 10 : 12}
                  textAnchor="end"
                  alignmentBaseline="middle"
                >
                  {!compact ? payload.value : ""}
                </text>
              )}
            />
            <Tooltip
              cursor={{ fill: "#f1f5f9" }}
              content={<AveragesTooltip metric={metric} />}
            />
            <Bar dataKey="value" fill="#2563eb" radius={[0, 4, 4, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
