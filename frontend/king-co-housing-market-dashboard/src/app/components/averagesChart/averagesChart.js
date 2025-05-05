import { useState, useEffect, use } from "react";
import axios from "axios";
import { BarChart, XAxis, YAxis, Tooltip } from "recharts";

export default function AveragesChart() {
    const [averages, setAverages] = useState([]);
    const [type, setType] = useState("mean");
    const [metric, setMetric] = useState("price");

    useEffect(() => {
        axios.get(`https://king-county-housing-price-analysis.onrender.com/api/averages/${type}/${metric}`)
        .then((res) => (setAverages(res.data))
        .catch((err) => console.log(err)))}
    , [type, metric]);

    return (
        <main>

        </main>
    )
} 