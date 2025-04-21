import { useState, useEffect, use } from "react";

export default function AveragesChart() {
    const [averages, setAverages] = useState([]);
    const [type, setType] = useState("mean");
    const [metric, setMetric] = useState("price");

    useEffect(() => {
        const fetchData = async () => {
            const response = await fetch(`https://king-county-housing-price-analysis.onrender.com/api/city_averages`);
            const data = await response.json();
            setAverages(data);
        };
        fetchData();
    }
    , [region, type, metric]);
    return (
        <main>

        </main>
    )
}