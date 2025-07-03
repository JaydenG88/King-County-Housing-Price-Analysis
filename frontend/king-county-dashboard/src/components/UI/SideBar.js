import Link from "next/link";

export default function SideBar() {
  const navItems = [
    { name: "Home", href: "/" },
    { name: "Averages Chart", href: "/averages" },
    { name: "Price Trends Chart", href: "/priceTrends" },
    { name: "Correlations Chart", href: "/correlations" },
    { name: "Price Categories Chart", href: "/priceCategories" },
    { name: "Best Valued Homes", href: "/bestValued" },
  ];

  return (
    <div className="w-64 bg-white shadow-md rounded-xl p-4 fixed top-6 left-6 h-[90vh] z-20 overflow-y-auto">
      <nav>
        <ul className="space-y-2">
          {navItems.map((item, index) => (
            <li key={index}>
              <Link
                href={item.href}
                className="block px-3 py-2 rounded hover:bg-gray-100 text-gray-800 font-medium transition-colors"
              >
                {item.name}
              </Link>
            </li>
          ))}
        </ul>
      </nav>
    </div>
  );
}