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
import { format, parseISO, set } from "date-fns";
import DropDown from "../UI/DropDown";
import Regions from "@/utils/Regions"

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
    <div className="flex items-center justify-center min-h-[300px] bg-white shadow-md rounded-lg">
      <div className="flex flex-col items-center space-y-4">
        <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
        <span className="text-gray-600 font-medium">Loading chart data...</span>
      </div>
    </div>
  );
  if (error) return <div>Error: {error.message}</div>;

  const firstYear = new Date(data[0]?.date).getFullYear() || "";

  return (
    <div
      className={`bg-white shadow-md rounded-lg ${
        compact ? "max-w-md mx-auto" : "p-1 w-full md:w-3/4 lg:w-5/6 mx-auto"
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
          height: compact ? "300px" : "calc(100vh - 180px)",
          minHeight: "300px",
        }}
      >
        <ResponsiveContainer width="100%" height="100%">
          <LineChart
            data={data}
            margin={{
              top: 20,
              right: 30,
              left: compact ? 0 : 80,
              bottom: 40,
            }}
          >
            <XAxis
              dataKey="date"
              scale="time"
              type="number"
              domain={["dataMin", "dataMax"]}
              tickFormatter={ (date) => format(new Date(date), "MMM")}
              tick={{ fontSize: 12 }}
              label={{
                value: firstYear,
                position: "insideBottomLeft",
                offset: -10,
                fontSize: 12,
              }}
            />
            <YAxis
              label={{
                value:
                  metric === "price"
                    ? "Average Price ($)"
                    : metric === "price_per_sqft"
                    ? "Average Price per Sqft ($)"
                    : "Average Square Footage",
                position: "insideLeft",
                offset: compact ? 30 : -50,
                fontSize: compact ? 14 : 18,
                angle: -90,
              }}
              tick={compact ? false : true}
            />
          <Tooltip
            wrapperStyle={{ backgroundColor: "#fff", border: "1px solid #ccc", fontSize: 14, color: "black" }}
            labelFormatter={(value) => format(new Date(value), "MMM d, yyyy")}
            formatter={(value) => [`$${value.toLocaleString()}`, "Value"]}
          />
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
