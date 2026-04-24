import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "SKYNET CORE",
  description: "Advanced Local AI Assistant Interface",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="antialiased bg-[#050505] text-[#ff1a1a]">
        {children}
      </body>
    </html>
  );
}
