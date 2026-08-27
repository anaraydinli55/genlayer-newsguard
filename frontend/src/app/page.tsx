"use client";
import { ConnectButton } from "@rainbow-me/rainbowkit";
import { Shield, Newspaper } from "lucide-react";
import { StatsCards } from "@/components/stats-cards";
import { SubmitNewsForm } from "@/components/submit-news-form";
import { NewsList } from "@/components/news-list";
export default function Home() {
  return <main className="min-h-screen bg-background"><header className="border-b bg-card/50 backdrop-blur-sm sticky top-0 z-50"><div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between"><div className="flex items-center gap-3"><div className="w-10 h-10 rounded-xl bg-violet-600 flex items-center justify-center"><Shield className="w-5 h-5 text-white" /></div><div><h1 className="text-lg font-bold">NewsGuard</h1><p className="text-xs text-muted-foreground">AI-Powered News Verification</p></div></div><ConnectButton /></div></header><div className="max-w-6xl mx-auto px-4 py-8 space-y-8"><StatsCards /><div className="grid lg:grid-cols-3 gap-8"><div className="lg:col-span-1"><SubmitNewsForm /></div><div className="lg:col-span-2"><div className="flex items-center gap-2 mb-4"><Newspaper className="w-5 h-5 text-muted-foreground" /><h2 className="text-xl font-semibold">Verified News</h2></div><NewsList /></div></div></div></main>;
}
