"use client";

import { useState, useEffect } from "react";
import { BarChart, XAxis, YAxis, Tooltip, ResponsiveContainer, Bar } from "recharts";
import dropDown from "./DropDown";

export default function PriceCategoryChart() {
    const [data, setData] = useState([]);
    const [region, setRegion] = useState("all");
    const [loading, setLoading] = useState(true);
}