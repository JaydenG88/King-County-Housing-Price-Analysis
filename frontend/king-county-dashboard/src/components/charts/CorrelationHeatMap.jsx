"use client";

import { useState, useEffect } from "react";
import ReactApexChart from "react-apexcharts";

export default function CorrelationHeatMap({ compact = false }) {
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
        <div className={`bg-white shadow-md rounded-lg ${compact ? "max-w-md mx-auto" : "p-1 w-full md:w-3/4 lg:w-5/6 mx-auto"}`}>
            <h2 className="text-2xl font-bold mb-6 text-center text-gray-800">Correlation Heat Map</h2>
            {/* Responsive height container */}
            <div
                className="w-full"
                style={{
                height: compact ? "300px" : "calc(100vh - 220px)", 
                minHeight: "300px",
                }}
            >
            <ReactApexChart
            options={{
                chart: {
                type: "heatmap",
                height: "100%",
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
            height="100%"
            />
            </div>
        </div>
    )
}