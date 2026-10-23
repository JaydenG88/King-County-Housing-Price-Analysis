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
            <div className={compact ? "p-4" : "p-5 border-b border-slate-100"}>
              <h2 className="text-base font-semibold text-slate-900">Correlation Heat Map</h2>
            </div>
            {/* Responsive height container */}
            <div
                className={`w-full ${compact ? "px-2 pb-3" : "px-2 pb-4"}`}
                style={{
                height: compact ? "260px" : "calc(100vh - 230px)",
                minHeight: "280px",
                }}
            >
            <ReactApexChart
            options={{
                chart: {
                type: "heatmap",
                height: "100%",
                fontFamily: "Inter, sans-serif",
                toolbar: { show: false },
                },
                dataLabels: {
                enabled: false
                },
                grid: {
                borderColor: "#e2e8f0",
                },
                xaxis: {
                categories: data.keys,
                labels: { style: { colors: "#64748b", fontSize: "11px" } },
                axisBorder: { color: "#e2e8f0" },
                axisTicks: { color: "#e2e8f0" },
                },
                yaxis: {
                labels: { style: { colors: "#64748b", fontSize: "11px" } },
                },
                colors: ["#2563eb"],
                plotOptions: {
                heatmap: {
                    shadeIntensity: 0.6,
                    colorScale: {
                    ranges: [
                        { from: -1, to: -0.01, color: "#f87171", name: "negative" },
                        { from: 0, to: 1, color: "#2563eb", name: "positive" },
                    ],
                    },
                },
                },
                tooltip: {
                custom: function({ series, seriesIndex, dataPointIndex, w }) {
                    const value = series[seriesIndex][dataPointIndex];
                    const x = w.globals.labels[dataPointIndex];
                    const y = w.config.series[seriesIndex].name;

                    return `
                    <div style="
                        color: #0f172a;
                        background-color: #fff;
                        border: 1px solid #e2e8f0;
                        padding: 10px;
                        font-size: 13px;
                        border-radius: 8px;
                        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.08);
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
