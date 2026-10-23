"use client";

export default function DropDown({ label, options, value, onChange }) {
    return (
        <label className="flex items-center gap-2 text-sm">
            <span className="text-slate-500 font-medium">{label}</span>
            <select
                value={value}
                onChange={(e) => onChange(e.target.value)}
                className="border border-slate-300 bg-white text-slate-800 rounded-md pl-3 pr-8 py-1.5 text-sm font-medium focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 hover:border-slate-400 transition-colors"
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
