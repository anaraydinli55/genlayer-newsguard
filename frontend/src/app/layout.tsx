import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Providers } from "./providers";
const inter = Inter({ subsets: ["latin"] });
export const metadata: Metadata = { title: "NewsGuard — AI-Powered News Verification", description: "Verify news claims using GenLayer Intelligent Contracts" };
export default function RootLayout({ children }: { children: React.ReactNode }) { return <html lang="en" className="dark"><body className={inter.className}><Providers>{children}</Providers></body></html>; }
