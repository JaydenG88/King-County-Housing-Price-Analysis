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
import { format } from "date-fns";
import DropDown from "../UI/DropDown";
import Regions from "@/utils/Regions"

function OverTimeTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  return (
    <div className="bg-white border border-slate-200 rounded-lg shadow-md px-3 py-2">
      <div className="text-xs font-semibold text-slate-900">{format(new Date(label), "MMM d, yyyy")}</div>
      <div className="text-xs text-blue-600 font-medium mt-0.5">${payload[0].value.toLocaleString()}</div>
    </div>
  );
}

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
        const regionList = await Regions();
        if (regionList.length > 0) {
          setRegions(regionList);
        }
      } catch (error) {
        setError(error);
      }

      try {
        const res = await fetch(
          `https://king-county-housing-price-analysis.onrender.com/api/price_trends/${region}/${metric}/${type}`
        );
        if (!res.ok) throw new Error("Network response was not ok");

        const json = await res.json();

        const formatted = json.map((item) => ({
          date: new Date(item.date).getTime(),
          value: Number(item.value.toFixed(2)),
        }));

        setData(formatted);
      } catch (error) {
        setError(error);
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, [type, metric, region]);

  if (loading) return (
    <div className="flex items-center justify-center min-h-[300px] bg-white border border-slate-200 rounded-xl">
      <div className="flex flex-col items-center space-y-3">
        <div className="w-7 h-7 border-2 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
        <span className="text-slate-500 text-sm font-medium">Loading chart data…</span>
      </div>
    </div>
  );
  if (error) return <div className="text-sm text-red-600">Error: {error.message}</div>;

  const firstYear = new Date(data[0]?.date).getFullYear() || "";

  return (
    <div className={`bg-white border border-slate-200 rounded-xl shadow-sm ${compact ? "max-w-md mx-auto" : "w-full"}`}>
      <div className={`flex flex-col gap-3 ${compact ? "p-4" : "p-5"} ${!compact ? "md:flex-row md:items-center md:justify-between border-b border-slate-100" : ""}`}>
        <h2 className="text-base font-semibold text-slate-900">
          Average Cost Over Time
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
          <LineChart
            data={data}
            margin={{
              top: 16,
              right: 24,
              left: compact ? 0 : 60,
              bottom: 30,
            }}
          >
            <XAxis
              dataKey="date"
              scale="time"
              type="number"
              domain={["dataMin", "dataMax"]}
              tickFormatter={ (date) => format(new Date(date), "MMM")}
              tick={{ fontSize: 11, fill: "#64748b" }}
              axisLine={{ stroke: "#e2e8f0" }}
              tickLine={false}
              label={{
                value: firstYear,
                position: "insideBottomLeft",
                offset: -6,
                fontSize: 12,
                fill: "#64748b",
              }}
            />
            <YAxis
              tick={compact ? false : { fontSize: 11, fill: "#64748b" }}
              axisLine={{ stroke: "#e2e8f0" }}
              tickLine={false}
              label={{
                value:
                  metric === "price"
                    ? "Average Price ($)"
                    : metric === "price_per_sqft"
                    ? "Average Price per Sqft ($)"
                    : "Average Square Footage",
                position: "insideLeft",
                offset: compact ? 10 : -45,
                fontSize: compact ? 12 : 13,
                angle: -90,
                fill: "#64748b",
              }}
            />
          <Tooltip content={<OverTimeTooltip />} />
            <Line
              type="monotone"
              dataKey="value"
              stroke="#2563eb"
              strokeWidth={2.5}
              dot={false}
              activeDot={{ r: 4 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
