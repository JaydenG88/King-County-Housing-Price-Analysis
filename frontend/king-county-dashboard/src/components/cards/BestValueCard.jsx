"use client";

const badgeStyles = {
    'Great Deal': 'bg-emerald-50 text-emerald-700 ring-1 ring-emerald-200',
    'Fair': 'bg-amber-50 text-amber-700 ring-1 ring-amber-200',
};

export default function BestValueCard({ sqft, price, zip, city, state, street_address, bedrooms, bathrooms, url, image, price_per_sqft, price_category }) {

    return (
        <a
            href={url}
            target="_blank"
            rel="noopener noreferrer"
            className="group block w-full rounded-xl overflow-hidden border border-slate-200 bg-white shadow-sm hover:shadow-md hover:border-slate-300 transition-all duration-200"
        >
            <div className="relative">
                <img src={image} alt="House" className="w-full h-48 object-cover" />
                <span className={`absolute top-3 left-3 px-2 py-1 text-xs font-semibold rounded-full ${badgeStyles[price_category] ?? 'bg-slate-100 text-slate-700 ring-1 ring-slate-200'}`}>
                    {price_category}
                </span>
            </div>
            <div className="p-4">
                <div className="text-xl font-bold text-slate-900">${price.toLocaleString()}</div>
                <div className="text-sm text-slate-500 mt-0.5">{street_address}, {city}, {state} {zip}</div>
                <div className="flex items-center gap-2 text-sm text-slate-700 mt-2">
                    <span>{bedrooms} bd</span>
                    <span className="text-slate-300">•</span>
                    <span>{bathrooms} ba</span>
                    <span className="text-slate-300">•</span>
                    <span>{sqft.toLocaleString()} sqft</span>
                </div>
                <div className="mt-3 pt-3 border-t border-slate-100 text-sm font-medium text-blue-600">
                    ${price_per_sqft.toFixed(2)} / sqft
                </div>
            </div>
        </a>
    )
}
