// app/layout.jsx
import "./globals.css";
import SideBar from "@/components/UI/SideBar";
import Header from "@/components/UI/Header";

export const metadata = {
  title: "King County Housing Dashboard",
  description: "Explore trends and insights from King County housing data",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="antialiased text-gray-900">
        <Header />
        <div className="flex h-screen">
          {/* Sidebar */}
          <SideBar />
          {/* Main Content */}
          <div className="flex flex-col flex-1">
            {/* Page Content */}
            <main className="flex-1 overflow-y-auto p-6 bg-gray-100">
              {children}
            </main>
          </div>
        </div>
      </body>
    </html>
  );
}
