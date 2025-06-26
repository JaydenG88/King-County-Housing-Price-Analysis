"use client";

import { useState, useEffect } from "react";
import { LineChart, XAxis, YAxis, Tooltip, ResponsiveContainer, Line } from "recharts";
import DropDown from "./DropDown";

export default function OverTimeChart() {
    const [data, setData] = useState([]);
    const [metric, setMetric] = useState("price");
    const[type, setType] = useState("mean");
    const [region, setRegion] = useState("King County");
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function fetchData() {
            try {
                const res = await fetch(`https://king-county-housing-price-analysis.onrender.com/api/price_trends/${region}/${metric}/${type}`)
                if (!res.ok) {
                    throw new Error("Network response was not ok" + res.statusText);
                }
                let data = await res.json();

                data = data.map(item => {
                    return {
                      date: item.date,
                      value: Number(item.value.toFixed(2))
                    };
                })

                setData(data);

            } catch (error) {
                setError(error);
            }
            finally {
                setLoading(false);
            }
        }
        fetchData();
    },[type, metric, region]);

    if (loading) {
        return <div>Loading...</div>;
    }
    if (error) {
        return <div>Error: {error.message}</div>;
    }

    return (
        <div className="bg-white shadow-lg rounded-lg p-1 w-full md:w-3/4 lg:w-5/6 ml-auto">
            <h2 className="text-2xl font-bold mb-6 text-center text-gray-800">Average Cost Over Time</h2>
            <div className="mb-6 flex flex-col md:flex-row justify-center items-center gap-4">
            
            </div>

             <div className="w-full" style={{ height: `700px`, maxHeight: "700px", width: "100%" }}>
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={data}>
                        <XAxis dataKey="date" />
                        <YAxis />
                        <Tooltip />
                        <Line type="monotone" dataKey="value" stroke="#8884d8" />
                    </LineChart>
                </ResponsiveContainer>

             </div>
        </div>
    )
       

}