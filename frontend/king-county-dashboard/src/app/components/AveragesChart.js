"use client";

import { useState, useEffect } from "react";
import { BarChart, XAxis, YAxis, Tooltip, ResponsiveContainer, Bar } from "recharts";

export default function AveragesChart() {
    const [averages, setAverages] = useState([]);
    const [type, setType] = useState("mean");
    const [metric, setMetric] = useState("price");
    const [loading, setLoading] = useState(true);
    const[error, setError] = useState(null);
    
    useEffect(() => {
        async function fetchData() {
            try {
                const res = await fetch(`https://king-county-housing-price-analysis.onrender.com/api/averages/${metric}/${type}`)
                if (!res.ok) {
                    throw new Error("Network response was not ok" + res.statusText);
                }
                let data = await res.json();

                data = data.map(item => {
                    return {
                      region: item.region,
                      value: Number(item.value.toFixed(2))
                    };
                })

                setAverages(data);

            } catch (error) {
                setError(error);
            }
            finally {
                setLoading(false);
            }
        }

    fetchData();

    },[type, metric]);

    if (loading) {
        return <div>Loading...</div>;
    }
    if (error) {
        return <div>Error: {error.message}</div>;
    }

    return (
      <div className="bg-white shadow-lg rounded-lg p-1 w-full md:w-3/4 lg:w-5/6 ml-auto">
        <h2 className="text-2xl font-bold mb-6 text-center text-gray-800">Averages by Region</h2>
        <div className="mb-6 flex flex-col md:flex-row justify-center items-center gap-4">
        <label className="flex items-center text-gray-700">
          <span className="mr-2">Type:</span>
          <select
          value={type}
          onChange={(e) => setType(e.target.value)}
          className="border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
          <option value="mean">Mean</option>
          <option value="median">Median</option>
          </select>
        </label>

        <label className="flex items-center text-gray-700">
          <span className="mr-2">Metric:</span>
          <select
          value={metric}
          onChange={(e) => setMetric(e.target.value)}
          className="border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
          <option value="price">Price</option>
          <option value="sqft">Square Feet</option>
          <option value="price_per_sqft">Price per Sqft</option>
          </select>
        </label>
        </div>

        <div className="w-full" style={{ height: `${averages.length * 20}px`, maxHeight: "700px", width: "100%" }}>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
          data={averages}
          layout="vertical"
          margin={{ top: 0, right: 30, left: 0, bottom: 20 }}
          barGap={0}
          >
          <XAxis type="number" />
          <YAxis
            dataKey="region"
            type="category"
            width={150}
            interval={0}
            tick={({ x, y, payload }) => (
              <text x={x} y={y} fill="#000" fontSize={12} text-anchor="end" >  
                {payload.value}
              </text>
            ) }
          />
          <Tooltip />
          <Bar dataKey="value" fill="#8884d8" />
          </BarChart>
        </ResponsiveContainer>
        </div>
      </div>
    );
} 