"use client";

import { useState, useEffect } from "react";
import dynamic from "next/dynamic";

const ReactApexChart = dynamic(() => import("react-apexcharts"), { ssr: false });

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

    if (loading) return (
    <div className="flex items-center justify-center min-h-[300px] bg-white shadow-md rounded-lg">
        <div className="flex flex-col items-center space-y-4">
        <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
        <span className="text-gray-600 font-medium">Loading chart data...</span>
        </div>
    </div>
    );
    if (error) return <div>Error: {error.message}</div>;


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
                colors: ["#FF0000", "#00A100"],
                tooltip: {
                custom: function({ series, seriesIndex, dataPointIndex, w }) {
                    const value = series[seriesIndex][dataPointIndex];
                    const x = w.globals.labels[dataPointIndex];
                    const y = w.config.series[seriesIndex].name;

                    return `
                    <div style="
                        color: #000000;  /* 👈 black font color */
                        background-color: #fff;
                        border: 1px solid #ccc;
                        padding: 10px;
                        font-size: 14px;
                        border-radius: 6px;
                    ">
                        <div><strong>${y} vs ${x}</strong></div>
                        <div>Value: ${value.toFixed(2)}</div>
                    </div>
                    `;
                }
                }
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