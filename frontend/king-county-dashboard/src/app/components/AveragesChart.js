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
                const data = await res.json();
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
    console.log(averages);

    return (
   
<div style={{ width: '100%', height: 650 }}>
  <ResponsiveContainer width="100%" height="100%">
    <BarChart
      data={averages}
      layout="vertical"
      margin={{ top: 20, right: 30, left: 100, bottom: 20 }}
      barGap={0}
    >
      <XAxis type="number" />
      <YAxis
        dataKey="region"
        type="category"
        width={150}
        interval={0}
      />
      <Tooltip />
      <Bar dataKey="value" fill="#8884d8" />
    </BarChart>
  </ResponsiveContainer>
</div>

      
    )
} 