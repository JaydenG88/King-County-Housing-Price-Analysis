'use client';

import { useState } from 'react';
import Link from 'next/link';
import { ChevronLeft, ChevronRight, Home, BarChart2, TrendingUp, Grid, Star } from 'lucide-react';

const navItems = [
  { name: "Home", href: "/", icon: <Home size={20} /> },
  { name: "Averages", href: "/averages", icon: <BarChart2 size={20} /> },
  { name: "Cost Over Time", href: "/priceTrends", icon: <TrendingUp size={20} /> },
  { name: "Correlations", href: "/correlations", icon: <Grid size={20} /> },
  { name: "Price Bracket Distribution", href: "/priceDistributions", icon: <BarChart2 size={20} /> },
  { name: "Best Valued Listings", href: "/bestValued", icon: <Star size={20} /> },
];

export default function SideNav() {
  const [isCollapsed, setIsCollapsed] = useState(false);

  return (
    <div
      className={`bg-white border-r h-[calc(100vh-64px)] top-16 left-0 z-40 fixed transition-all duration-300 ${
        isCollapsed ? 'w-16' : 'w-64'
      }`}
    >
      <div className="flex justify-end px-2 py-2 border-b">
        <button onClick={() => setIsCollapsed(!isCollapsed)}>
          {isCollapsed ? <ChevronRight size={20} /> : <ChevronLeft size={20} />}
        </button>
      </div>

      <nav className="mt-2">
        <ul className="space-y-1">
          {navItems.map((item, index) => (
            <li key={index}>
              <Link href={item.href} className="flex items-center gap-3 px-4 py-2 text-gray-700 hover:bg-gray-100 rounded transition">
                {item.icon}
                {!isCollapsed && <span>{item.name}</span>}
              </Link>
            </li>
          ))}
        </ul>
      </nav>
    </div>
  );
}
