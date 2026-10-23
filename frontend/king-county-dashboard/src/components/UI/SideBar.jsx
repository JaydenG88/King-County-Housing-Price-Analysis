'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { ChevronLeft, ChevronRight, Home, BarChart2, TrendingUp, Grid, Star } from 'lucide-react';

const navItems = [
  { name: "Overview", href: "/", icon: Home },
  { name: "Averages", href: "/averages", icon: BarChart2 },
  { name: "Cost Over Time", href: "/priceTrends", icon: TrendingUp },
  { name: "Correlations", href: "/correlations", icon: Grid },
  { name: "Price Distribution", href: "/priceDistributions", icon: BarChart2 },
  { name: "Best Valued Listings", href: "/bestValued", icon: Star },
];

export default function SideNav() {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const pathname = usePathname();

  return (
    <div
      className={`bg-white border-r border-slate-200 h-[calc(100vh-57px)] top-[57px] left-0 z-40 fixed transition-all duration-200 ${
        isCollapsed ? 'w-16' : 'w-60'
      }`}
    >
      <div className="flex justify-end px-2 py-2">
        <button
          onClick={() => setIsCollapsed(!isCollapsed)}
          className="p-1.5 rounded-md text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition-colors"
          aria-label="Toggle sidebar"
        >
          {isCollapsed ? <ChevronRight size={18} /> : <ChevronLeft size={18} />}
        </button>
      </div>

      <nav className="px-2">
        <ul className="space-y-0.5">
          {navItems.map((item) => {
            const Icon = item.icon;
            const active = pathname === item.href;
            return (
              <li key={item.href}>
                <Link
                  href={item.href}
                  className={`flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    active
                      ? 'bg-blue-50 text-blue-700'
                      : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
                  }`}
                >
                  <Icon size={18} className={active ? 'text-blue-600' : 'text-slate-400'} />
                  {!isCollapsed && <span className="truncate">{item.name}</span>}
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>
    </div>
  );
}
