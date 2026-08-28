#!/usr/bin/env python3
import os

BASE = os.path.expanduser("~/genlayer-newsguard/frontend")
os.system("rm -rf " + BASE)
os.makedirs(BASE, exist_ok=True)
os.makedirs(BASE + "/src/app", exist_ok=True)
os.makedirs(BASE + "/src/components/ui", exist_ok=True)
os.makedirs(BASE + "/src/hooks", exist_ok=True)
os.makedirs(BASE + "/src/lib", exist_ok=True)

FILES = {
    "package.json": '''{
  "name": "newsguard-frontend",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  },
  "dependencies": {
    "next": "^15.0.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "genlayer-js": "^0.6.0",
    "viem": "^2.0.0",
    "wagmi": "^2.0.0",
    "@rainbow-me/rainbowkit": "^2.0.0",
    "@tanstack/react-query": "^5.0.0",
    "@radix-ui/react-slot": "^1.0.0",
    "lucide-react": "^0.400.0",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.2.0",
    "tailwindcss-animate": "^1.0.7"
  },
  "devDependencies": {
    "typescript": "^5.3.0",
    "@types/node": "^20.0.0",
    "@types/react": "^19.0.0",
    "@types/react-dom": "^19.0.0",
    "tailwindcss": "^3.4.0",
    "postcss": "^8.4.0",
    "autoprefixer": "^10.4.0"
  }
}''',

    "tsconfig.json": '''{
  "compilerOptions": {
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "paths": { "@/*": ["./src/*"] }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}''',

    "next.config.js": '''/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "export",
  distDir: "dist",
  images: { unoptimized: true },
};
module.exports = nextConfig;
''',

    "postcss.config.js": '''module.exports = {
  plugins: { tailwindcss: {}, autoprefixer: {} },
};
''',

    "tailwind.config.ts": '''import type { Config } from "tailwindcss";
const config: Config = {
  darkMode: ["class"],
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: { DEFAULT: "hsl(var(--primary))", foreground: "hsl(var(--primary-foreground))" },
        secondary: { DEFAULT: "hsl(var(--secondary))", foreground: "hsl(var(--secondary-foreground))" },
        destructive: { DEFAULT: "hsl(var(--destructive))", foreground: "hsl(var(--destructive-foreground))" },
        muted: { DEFAULT: "hsl(var(--muted))", foreground: "hsl(var(--muted-foreground))" },
        accent: { DEFAULT: "hsl(var(--accent))", foreground: "hsl(var(--accent-foreground))" },
        popover: { DEFAULT: "hsl(var(--popover))", foreground: "hsl(var(--popover-foreground))" },
        card: { DEFAULT: "hsl(var(--card))", foreground: "hsl(var(--card-foreground))" },
      },
      borderRadius: { lg: "var(--radius)", md: "calc(var(--radius) - 2px)", sm: "calc(var(--radius) - 4px)" },
    },
  },
  plugins: [require("tailwindcss-animate")],
};
export default config;
''',

    "next-env.d.ts": '''/// <reference types="next" />
/// <reference types="next/image-types/global" />
''',

    "src/app/globals.css": '''@tailwind base;
@tailwind components;
@tailwind utilities;
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 222.2 84% 4.9%;
    --radius: 0.5rem;
  }
  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;
    --popover: 222.2 84% 4.9%;
    --popover-foreground: 210 40% 98%;
    --primary: 210 40% 98%;
    --primary-foreground: 222.2 47.4% 11.2%;
    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;
    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;
    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;
    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 212.7 26.8% 83.9%;
  }
}
@layer base {
  * { @apply border-border; }
  body { @apply bg-background text-foreground; }
}
''',

    "src/lib/utils.ts": '''import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";
export function cn(...inputs: ClassValue[]) { return twMerge(clsx(inputs)); }
export function formatAddress(addr: string) { if (!addr || addr.length < 10) return addr; return addr.slice(0, 6) + "..." + addr.slice(-4); }
export function formatDate(ts: number) { if (!ts || ts === 0) return "—"; const d = new Date(ts * 1000); return d.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric", hour: "2-digit", minute: "2-digit" }); }
export function getVerdictColor(verdict: string) {
  switch (verdict?.toUpperCase()) {
    case "TRUE": return "bg-emerald-500/10 text-emerald-400 border-emerald-500/20";
    case "FALSE": return "bg-red-500/10 text-red-400 border-red-500/20";
    case "MISLEADING": return "bg-amber-500/10 text-amber-400 border-amber-500/20";
    case "UNVERIFIABLE": return "bg-slate-500/10 text-slate-400 border-slate-500/20";
    default: return "bg-muted text-muted-foreground";
  }
}
export function getCategoryLabel(cat: string) {
  const labels: Record<string, string> = { politics: "Politics", health: "Health", technology: "Technology", finance: "Finance", sports: "Sports", science: "Science", general: "General" };
  return labels[cat] || cat;
}
''',

    "src/lib/genlayer-client.ts": '''import { createClient } from "genlayer-js";
import { testnetBradbury } from "genlayer-js/chains";
export const NEWSGUARD_ADDRESS = "0x4e691dfA2857CB394928166F1158718B1d429257";
export const genlayerClient = createClient({ chain: testnetBradbury, endpoint: "https://rpc-bradbury.genlayer.com" });
''',

    "src/hooks/use-newsguard.ts": '''"use client"
import { useState, useCallback } from "react";
import { useAccount, useWalletClient } from "wagmi";
import { createClient } from "genlayer-js";
import { testnetBradbury } from "genlayer-js/chains";
import { NEWSGUARD_ADDRESS } from "@/lib/genlayer-client";
export function useNewsGuard() {
  const { address, isConnected } = useAccount();
  const { data: walletClient } = useWalletClient();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const getClient = useCallback(() => {
    if (!walletClient) throw new Error("No wallet connected.");
    return createClient({ chain: testnetBradbury, endpoint: "https://rpc-bradbury.genlayer.com", account: walletClient.account });
  }, [walletClient]);
  const verifyNews = useCallback(async (url: string, claim: string, category: string = "general") => {
    if (!isConnected) throw new Error("Wallet not connected");
    setLoading(true); setError(null);
    try { const client = getClient(); return await client.writeContract({ address: NEWSGUARD_ADDRESS, functionName: "verifyNews", value: BigInt(0), args: [url, claim, category] }); }
    catch (err: any) { setError(err.message); throw err; } finally { setLoading(false); }
  }, [isConnected, getClient]);
  const getAllChecks = useCallback(async () => { const client = getClient(); return await client.readContract({ address: NEWSGUARD_ADDRESS, functionName: "getAllChecks", args: [] }); }, [getClient]);
  const getStats = useCallback(async () => { const client = getClient(); return await client.readContract({ address: NEWSGUARD_ADDRESS, functionName: "getStats", args: [] }); }, [getClient]);
  return { verifyNews, getAllChecks, getStats, loading, error, isConnected, address };
}
''',

    "src/components/ui/badge.tsx": '''import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";
const badgeVariants = cva("inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors", { variants: { variant: { default: "border-transparent bg-primary text-primary-foreground", secondary: "border-transparent bg-secondary text-secondary-foreground", destructive: "border-transparent bg-destructive text-destructive-foreground", outline: "text-foreground" } }, defaultVariants: { variant: "default" } });
export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement>, VariantProps<typeof badgeVariants> {}
function Badge({ className, variant, ...props }: BadgeProps) { return <div className={cn(badgeVariants({ variant }), className)} {...props} />; }
export { Badge, badgeVariants };
''',

    "src/components/ui/button.tsx": '''import * as React from "react";
import { Slot } from "@radix-ui/react-slot";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";
const buttonVariants = cva("inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50", { variants: { variant: { default: "bg-primary text-primary-foreground hover:bg-primary/90", destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90", outline: "border border-input bg-background hover:bg-accent hover:text-accent-foreground", secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80", ghost: "hover:bg-accent hover:text-accent-foreground", link: "text-primary underline-offset-4 hover:underline" }, size: { default: "h-10 px-4 py-2", sm: "h-9 rounded-md px-3", lg: "h-11 rounded-md px-8", icon: "h-10 w-10" } }, defaultVariants: { variant: "default", size: "default" } });
export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement>, VariantProps<typeof buttonVariants> { asChild?: boolean }
const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(({ className, variant, size, asChild = false, ...props }, ref) => { const Comp = asChild ? Slot : "button"; return <Comp className={cn(buttonVariants({ variant, size, className }))} ref={ref} {...props} />; });
Button.displayName = "Button";
export { Button, buttonVariants };
''',

    "src/components/ui/card.tsx": '''import * as React from "react";
import { cn } from "@/lib/utils";
const Card = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(({ className, ...props }, ref) => <div ref={ref} className={cn("rounded-lg border bg-card text-card-foreground shadow-sm", className)} {...props} />); Card.displayName = "Card";
const CardHeader = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(({ className, ...props }, ref) => <div ref={ref} className={cn("flex flex-col space-y-1.5 p-6", className)} {...props} />); CardHeader.displayName = "CardHeader";
const CardTitle = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLHeadingElement>>(({ className, ...props }, ref) => <h3 ref={ref} className={cn("text-2xl font-semibold leading-none tracking-tight", className)} {...props} />); CardTitle.displayName = "CardTitle";
const CardDescription = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLParagraphElement>>(({ className, ...props }, ref) => <p ref={ref} className={cn("text-sm text-muted-foreground", className)} {...props} />); CardDescription.displayName = "CardDescription";
const CardContent = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(({ className, ...props }, ref) => <div ref={ref} className={cn("p-6 pt-0", className)} {...props} />); CardContent.displayName = "CardContent";
export { Card, CardHeader, CardTitle, CardDescription, CardContent };
''',

    "src/components/ui/input.tsx": '''import * as React from "react";
import { cn } from "@/lib/utils";
export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {}
const Input = React.forwardRef<HTMLInputElement, InputProps>(({ className, type, ...props }, ref) => <input type={type} className={cn("flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50", className)} ref={ref} {...props} />);
Input.displayName = "Input";
export { Input };
''',

    "src/components/ui/select.tsx": '''"use client";
import * as React from "react";
import { cn } from "@/lib/utils";
interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {}
const Select = React.forwardRef<HTMLSelectElement, SelectProps>(({ className, children, ...props }, ref) => <select className={cn("flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50", className)} ref={ref} {...props}>{children}</select>);
Select.displayName = "Select";
export { Select };
''',

    "src/components/stats-cards.tsx": '''"use client"
import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { CheckCircle, XCircle, AlertTriangle, HelpCircle, BarChart3 } from "lucide-react";
import { genlayerClient, NEWSGUARD_ADDRESS } from "@/lib/genlayer-client";
interface Stats { total_checks?: string; true?: string; false?: string; misleading?: string; unverifiable?: string; accuracy?: string; }
export function StatsCards() {
  const [stats, setStats] = useState<Stats>({});
  const [loading, setLoading] = useState(true);
  useEffect(() => { async function load() { try { const result = await genlayerClient.readContract({ address: NEWSGUARD_ADDRESS, functionName: "getStats", args: [] }) as Stats; setStats(result); } catch (e) { console.error(e); } finally { setLoading(false); } } load(); }, []);
  const items = [
    { label: "Total", value: stats.total_checks || "0", icon: BarChart3, color: "text-blue-400" },
    { label: "True", value: stats.true || "0", icon: CheckCircle, color: "text-emerald-400" },
    { label: "False", value: stats.false || "0", icon: XCircle, color: "text-red-400" },
    { label: "Misleading", value: stats.misleading || "0", icon: AlertTriangle, color: "text-amber-400" },
    { label: "Unverifiable", value: stats.unverifiable || "0", icon: HelpCircle, color: "text-slate-400" },
  ];
  return <div className="grid grid-cols-2 md:grid-cols-5 gap-4">{items.map((item) => <Card key={item.label} className="bg-card/50"><CardHeader className="flex flex-row items-center justify-between pb-2"><CardTitle className="text-sm font-medium text-muted-foreground">{item.label}</CardTitle><item.icon className={`w-4 h-4 ${item.color}`} /></CardHeader><CardContent><div className="text-2xl font-bold">{loading ? "—" : item.value}</div></CardContent></Card>)}</div>;
}
''',

    "src/components/submit-news-form.tsx": '''"use client"
import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { useNewsGuard } from "@/hooks/use-newsguard";
import { Newspaper, Link2, FileText } from "lucide-react";
const CATEGORIES = [
  { value: "general", label: "General" }, { value: "politics", label: "Politics" }, { value: "health", label: "Health" },
  { value: "technology", label: "Technology" }, { value: "finance", label: "Finance" }, { value: "sports", label: "Sports" }, { value: "science", label: "Science" },
];
export function SubmitNewsForm() {
  const [url, setUrl] = useState("");
  const [claim, setClaim] = useState("");
  const [category, setCategory] = useState("general");
  const { verifyNews, loading, isConnected } = useNewsGuard();
  const handleSubmit = async (e: React.FormEvent) => { e.preventDefault(); if (!url.trim() || !claim.trim()) return; try { await verifyNews(url.trim(), claim.trim(), category); setUrl(""); setClaim(""); alert("✅ News submitted for verification!"); window.location.reload(); } catch (err: any) { alert(`❌ Failed: ${err.message}`); } };
  return <Card className="bg-card/50"><CardHeader><CardTitle className="flex items-center gap-2"><Newspaper className="w-5 h-5" />Verify News Claim</CardTitle></CardHeader><CardContent><form onSubmit={handleSubmit} className="space-y-4"><div className="space-y-2"><label className="text-sm font-medium flex items-center gap-2"><Link2 className="w-4 h-4 text-muted-foreground" />Source URL</label><Input placeholder="https://example.com/news-article" value={url} onChange={(e) => setUrl(e.target.value)} required /></div><div className="space-y-2"><label className="text-sm font-medium flex items-center gap-2"><FileText className="w-4 h-4 text-muted-foreground" />Claim to Verify</label><Input placeholder="e.g., 'The Earth is flat'" value={claim} onChange={(e) => setClaim(e.target.value)} required /></div><div className="space-y-2"><label className="text-sm font-medium">Category</label><Select value={category} onChange={(e) => setCategory(e.target.value)}>{CATEGORIES.map((c) => <option key={c.value} value={c.value}>{c.label}</option>)}</Select></div><Button type="submit" className="w-full" disabled={loading || !isConnected}>{loading ? "Verifying..." : !isConnected ? "Connect Wallet" : "Submit for Verification"}</Button></form></CardContent></Card>;
}
''',

    "src/components/news-list.tsx": '''"use client"
import { useEffect, useState } from "react";
import { Search, ExternalLink, ShieldCheck } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { formatAddress, formatDate, getVerdictColor, getCategoryLabel } from "@/lib/utils";
import { genlayerClient, NEWSGUARD_ADDRESS } from "@/lib/genlayer-client";
interface Check { id: string; creator: string; url: string; claim: string; category: string; verdict: string; confidence?: number; reasoning?: string; created_at: number; }
export function NewsList() {
  const [checks, setChecks] = useState<Check[]>([]);
  const [filter, setFilter] = useState("");
  const [verdictFilter, setVerdictFilter] = useState("all");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  useEffect(() => { async function load() { try { setLoading(true); setError(""); const allChecks = await genlayerClient.readContract({ address: NEWSGUARD_ADDRESS, functionName: "getAllChecks", args: [] }) as any[]; const parsed: Check[] = (allChecks || []).map((raw: any) => ({ id: String(raw?.id ?? ""), creator: String(raw?.creator ?? ""), url: String(raw?.url ?? ""), claim: String(raw?.claim ?? ""), category: String(raw?.category ?? ""), verdict: String(raw?.verdict ?? "UNVERIFIABLE"), confidence: parseFloat(raw?.confidence ?? "0"), reasoning: String(raw?.reasoning ?? ""), created_at: Number(raw?.created_at ?? 0) })); setChecks(parsed.reverse()); } catch (err) { console.error(err); setError("Checks could not be loaded."); setChecks([]); } finally { setLoading(false); } } load(); }, []);
  const filtered = checks.filter((check) => { const query = filter.toLowerCase(); const matchesSearch = check.claim.toLowerCase().includes(query) || check.url.toLowerCase().includes(query); const matchesVerdict = verdictFilter === "all" || check.verdict === verdictFilter; return matchesSearch && matchesVerdict; });
  const verdicts = ["all", "TRUE", "FALSE", "MISLEADING", "UNVERIFIABLE"];
  return <div className="space-y-6"><div className="flex flex-col sm:flex-row gap-4 items-center"><div className="relative flex-1 w-full"><Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" /><Input placeholder="Search claims..." className="pl-10" value={filter} onChange={(e) => setFilter(e.target.value)} /></div><div className="flex gap-2 flex-wrap">{verdicts.map((v) => <button key={v} onClick={() => setVerdictFilter(v)} className={`px-3 py-1.5 rounded-full text-xs font-medium transition-all ${verdictFilter === v ? "bg-violet-600 text-white" : "bg-muted text-muted-foreground hover:bg-muted/80"}`}>{v === "all" ? "All" : v}</button>)}</div></div>{loading && <div className="text-center py-12 text-muted-foreground">Loading checks...</div>}{!loading && error && <div className="text-center py-12 text-red-400">{error}</div>}{!loading && !error && filtered.length === 0 && <div className="text-center py-12 text-muted-foreground">No checks found.</div>}<div className="grid gap-4">{filtered.map((check) => <Card key={check.id} className="hover:shadow-md transition-all"><CardContent className="p-6"><div className="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-4"><div className="flex-1 space-y-3"><div className="flex items-center gap-3 flex-wrap"><span className="text-sm font-mono text-muted-foreground">#{check.id}</span><Badge variant="outline" className={getVerdictColor(check.verdict)}>{check.verdict}</Badge><Badge variant="secondary" className="text-xs">{getCategoryLabel(check.category)}</Badge></div><p className="text-sm font-medium">{check.claim}</p>{check.reasoning && <p className="text-xs text-muted-foreground italic">"{check.reasoning}"</p>}<div className="flex items-center gap-2 text-xs text-muted-foreground flex-wrap"><span>By {formatAddress(check.creator)}</span><span>&bull;</span><span>{formatDate(check.created_at)}</span>{check.confidence !== undefined && check.confidence > 0 && <><span>&bull;</span><span className="flex items-center gap-1"><ShieldCheck className="w-3 h-3" />Confidence: {(check.confidence * 100).toFixed(0)}%</span></>}</div></div><div className="flex gap-2">{check.url && <a href={check.url} target="_blank" rel="noopener noreferrer"><Button variant="ghost" size="sm" className="gap-1"><ExternalLink className="w-4 h-4" />Source</Button></a>}</div></div></CardContent></Card>)}</div></div>;
}
''',

    "src/app/providers.tsx": '''"use client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { WagmiProvider } from "wagmi";
import { RainbowKitProvider, getDefaultConfig } from "@rainbow-me/rainbowkit";
import { testnetBradbury } from "genlayer-js/chains";
import { useState } from "react";
const config = getDefaultConfig({ appName: "NewsGuard", projectId: "YOUR_WALLETCONNECT_PROJECT_ID", chains: [testnetBradbury as any], ssr: true });
export function Providers({ children }: { children: React.ReactNode }) { const [queryClient] = useState(() => new QueryClient()); return <WagmiProvider config={config}><QueryClientProvider client={queryClient}><RainbowKitProvider>{children}</RainbowKitProvider></QueryClientProvider></WagmiProvider>; }
''',

    "src/app/layout.tsx": '''import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Providers } from "./providers";
const inter = Inter({ subsets: ["latin"] });
export const metadata: Metadata = { title: "NewsGuard — AI-Powered News Verification", description: "Verify news claims using GenLayer Intelligent Contracts" };
export default function RootLayout({ children }: { children: React.ReactNode }) { return <html lang="en" className="dark"><body className={inter.className}><Providers>{children}</Providers></body></html>; }
''',

    "src/app/page.tsx": '''"use client";
import { ConnectButton } from "@rainbow-me/rainbowkit";
import { Shield, Newspaper } from "lucide-react";
import { StatsCards } from "@/components/stats-cards";
import { SubmitNewsForm } from "@/components/submit-news-form";
import { NewsList } from "@/components/news-list";
export default function Home() {
  return <main className="min-h-screen bg-background"><header className="border-b bg-card/50 backdrop-blur-sm sticky top-0 z-50"><div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between"><div className="flex items-center gap-3"><div className="w-10 h-10 rounded-xl bg-violet-600 flex items-center justify-center"><Shield className="w-5 h-5 text-white" /></div><div><h1 className="text-lg font-bold">NewsGuard</h1><p className="text-xs text-muted-foreground">AI-Powered News Verification</p></div></div><ConnectButton /></div></header><div className="max-w-6xl mx-auto px-4 py-8 space-y-8"><StatsCards /><div className="grid lg:grid-cols-3 gap-8"><div className="lg:col-span-1"><SubmitNewsForm /></div><div className="lg:col-span-2"><div className="flex items-center gap-2 mb-4"><Newspaper className="w-5 h-5 text-muted-foreground" /><h2 className="text-xl font-semibold">Verified News</h2></div><NewsList /></div></div></div></main>;
}
''',
}

for fname, content in FILES.items():
    path = os.path.join(BASE, fname)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    print(f"  ✅ {fname}")

print(f"\n🎉 All files created in {BASE}")
print("Next: cd ~/genlayer-newsguard/frontend && npm install && npm run build")
