"use client";
import { useState, useEffect } from 'react';
import Link from 'next/link';
import UpdateDate from "@/utils/UpdateDate";

export default function Header() {
  const [date, setDate] = useState(null);

  useEffect(() => {
    const fetchDate = async () => {
      const result = await UpdateDate();
      setDate(result);
    };
    fetchDate();
  }, []);

  return (
    <header className="bg-white border-b border-slate-200 px-6 py-3.5 flex items-center justify-between">
      <Link href="/" className="flex items-center gap-2">
        <span className="flex items-center justify-center w-8 h-8 rounded-md bg-blue-600 text-white font-bold text-sm">
          KC
        </span>
        <span className="text-base font-semibold text-slate-900 tracking-tight">
          King County Housing
        </span>
      </Link>
      <div className="hidden md:flex items-center gap-2 text-xs text-slate-500">
        <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
        <span>Data updated {date ?? "…"}</span>
      </div>
    </header>
  );
}
