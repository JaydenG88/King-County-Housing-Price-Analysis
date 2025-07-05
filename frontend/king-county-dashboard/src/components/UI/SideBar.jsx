"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { ChevronRight, ChevronLeft } from "lucide-react";

export default function SideBar( ) {
  const navItems = [
    { name: "Home", href: "/" },
    { name: "Averages Chart", href: "/averages" },
    { name: "Price Trends Chart", href: "/priceTrends" },
    { name: "Correlations Chart", href: "/correlations" },
    { name: "Price Categories Chart", href: "/priceCategories" },
    { name: "Best Valued Homes", href: "/bestValued" },
  ];

  const [isCollapsed, setIsCollapsed] = useState(false);
  const toggleCollapse = () => {
    setIsCollapsed(!isCollapsed);
  };


  return (
    <div
      className={`${
        isCollapsed ? "w-16" : "w-64"
      } border-r border-gray-200 bg-white duration-300 ease-in-out transform hidden sm:flex flex-col h-screen`}
    >
      {/* Toggle Button */}
      <button
        onClick={toggleCollapse}
        className="p-2 self-end m-2 text-gray-600 hover:text-gray-800"
        aria-label={isCollapsed ? "Expand Sidebar" : "Collapse Sidebar"}
      >
        {isCollapsed ? <ChevronRight size={20} /> : <ChevronLeft size={20} />}
      </button>

      {/* Optional nav items go here */}
      <nav className="flex-1 mt-4">
        {/* Example placeholder */}
        <ul className="space-y-2 px-2">
          <li className="text-gray-700">🏠 Dashboard</li>
        </ul>
      </nav>
    </div>
  );
}