"use client";

import { useState, useEffect } from "react";
import { BarChart, XAxis, YAxis, Tooltip, ResponsiveContainer, Bar } from "recharts";
import DropDown from "./DropDown";

export default function PriceCategoryChart() {
    const [data, setData] = useState([]);
    const [region, setRegion] = useState("all");
    const [regions, setRegions] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function fetchData() {
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

       async function fetchRegions() {
            try {
                const res = await fetch(`https://king-county-housing-price-analysis.onrender.com/api/regions`)
                if (!res.ok) {
                    throw new Error("Network response was not ok" + res.statusText);
                }
                const regionsData = await res.json();
                const filtered = regionsData.filter(region => region.toLowerCase() !== "king county");

                setRegions(filtered);
            } catch (error) {
                setError(error);
            }
        }

        fetchData();
        fetchRegions();

    }, [region])

    if (loading) {
        return <div>Loading...</div>;
    }
    console.log(data);
    return (
        <div className="bg-white shadow-lg rounded-lg p-1 w-full md:w-3/4 lg:w-5/6 ml-auto">
            <h2 className="text-2xl font-bold mb-6 text-center text-gray-800">Price Category Frequency</h2>
            <div className="mb-6 flex flex-col md:flex-row justify-center items-center gap-4">
            <DropDown
                label="Region"
                value={region}
                onChange={setRegion}
                options={ regions.map(r => ({ label: r, value: r }))}
                /> 

            </div>
            <ResponsiveContainer width="100%" height={300}>
            <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                <XAxis dataKey="category" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#8884d8" />
            </BarChart>
            </ResponsiveContainer>
        </div>
    );
}