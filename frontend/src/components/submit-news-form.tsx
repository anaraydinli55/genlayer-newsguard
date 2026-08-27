"use client"
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
