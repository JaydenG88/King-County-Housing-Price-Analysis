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

                let data = await res.json()
                data = data.map(item => {
                    return {
                        x: item.x,
                        y: item.y,
                        value: Number(item.value.toFixed(2))
                    };
                });
                

              } catch (error) {
                setError(error);
            }
        }

    })
}