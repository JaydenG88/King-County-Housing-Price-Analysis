"use client";
export default function Header() {

  const date = UpdateDate();
  return (
    <header className="bg-gradient-to-r from-indigo-600 to-purple-600 shadow-md px-6 py-4 flex items-center justify-between">
      <h1 className="text-xl md:text-2xl font-bold text-white tracking-wide">
        King County Housing Dashboard
      </h1>
      <div className="hidden md:block">
        <span className="text-sm text-indigo-100">Updated: {}</span>
      </div>
    </header>
  );
}
