import type { Metadata } from "next";
import "./globals.css";
import { Sidebar } from "@/components/layout/sidebar";
import { Header } from "@/components/layout/header";

export const metadata: Metadata = {
  title: "GEO AI Agent for E-commerce VN",
  description: "Stability-aware Visibility Monitoring + Evidence-grounded Diagnosis + Closed-loop Re-measurement",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="vi">
      <body>
        <div className="flex min-h-screen">
          <Sidebar />
          <div className="flex-1">
            <Header />
            <main className="px-6 py-6">{children}</main>
          </div>
        </div>
      </body>
    </html>
  );
}
