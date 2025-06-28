"use client";

import { useState, useEffect } from "react";
import ReactApexChart from "react-apexcharts";

export default function CorrelationHeatMap() {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function fetchData() {
            try {
                const res = await fetch (`https://king-county-housing-price-analysis.onrender.com/api/correlations`)
                if (!res.ok) {
                    throw new Error("Network response was not ok" + res.statusText);
                }

                let data = await res.json();
                console.log(data)
                setData(data);
              } catch (error) {
                setError(error);
            } finally {
                setLoading(false);
            }

        }

        fetchData();
    }, []);

    if (loading) {
        return <div>Loading...</div>;
    }
    if (error) {
        return <div>Error: {error.message}</div>;
    }

    return (
        <div className="bg-white shadow-lg rounded-lg p-1 w-full md:w-3/4 lg:w-5/6 ml-auto">
            <h2 className="text-2xl font-bold mb-6 text-center text-gray-800">Correlation Heat Map</h2>
            <ReactApexChart
            options={{
                chart: {
                type: "heatmap",
                height: 350
                },
                dataLabels: {
                enabled: false
                },
                xaxis: {
                categories: data.keys
                },
                colors: ["#FF0000", "#00A100"]
            }}
            series={data.keys.map((rowLabel, i) => ({
                name: rowLabel,
                data: data.keys.map((colLabel, j) => ({
                x: colLabel,
                y: data.matrix[i][j]
                }))
            }))}
            type="heatmap"
            height={700}
            />
        </div>
    )
}