import Header from "@/components/UI/Header";
import SideBar from "@/components/UI/SideBar";
import "@/app/globals.css"; // adjust if yours is elsewhere

export const metadata = {
  title: "King County Housing Dashboard",
  description: "Visualizing trends across King County real estate",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" className="h-full overflow-hidden">
      <body className="h-full overflow-hidden">
        <div className="flex flex-col h-screen">
          {/* Top Header */}
          <Header />

          {/* Main area below header */}
          <div className="flex flex-1 overflow-hidden">
            {/* Sidebar */}
            <SideBar />

            {/* Main scrollable content */}
            <main className="flex-1 overflow-y-auto bg-slate-50 p-6 md:pl-[15.5rem]">
              {children}
            </main>
          </div>
        </div>
      </body>
    </html>
  );
}
