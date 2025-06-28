"use client";
import Image from "next/image";

export default function BestValueCard({ sqft, price, zip, city, state, street_address, bedrooms, bathrooms, url, image, price_per_sqft, price_category }) {

    return (
        <div className="w-full max-w-sm rounded-2xl shadow-md overflow-hidden border border-gray-200 bg-white">
            <a href={url} target="_blank" rel="noopener noreferrer">
            <img src={image} alt="House" className="w-full h-48 object-cover" />
            <div className="p-4">
            <div className="text-xl font-semibold text-gray-900">${price.toLocaleString()}</div>
            <div className="text-sm text-gray-600">{street_address}, {city}, {state} {zip}</div>
            <div className="text-sm text-gray-700 mt-1">
                {bedrooms} bd • {bathrooms} ba • {sqft.toLocaleString()} sqft
            </div>
            <div className="mt-2 text-sm text-blue-700 font-medium">
                ${price_per_sqft.toFixed(2)} / sqft
            </div>
            <span className={`inline-block mt-2 px-2 py-1 text-xs font-bold rounded 
                ${price_category === 'Great Deal' ? 'bg-green-100 text-green-800' : 
                price_category === 'Fair' ? 'bg-yellow-100 text-yellow-800' : 
                'bg-gray-100 text-gray-800'}`}>
                {price_category}
            </span>
            </div>
            </a>
        </div>

    )
}