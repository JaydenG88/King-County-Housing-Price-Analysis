"use client";

import { useState, useEffect } from "react";

export default function DropDown({ label, options, value, onChange}) {

    return (
        <label className="flex items-center text-gray-700">
            <span className="mr-2">{label}:</span>
            <select
                value={value}
                onChange={(e) => onChange(e.target.value)}
                className="border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
                {options.map((option) => (
                    <option key={option.value} value={option.value}>
                        {option.label}
                    </option>
                ))}
            </select>
        </label> 
    )
}