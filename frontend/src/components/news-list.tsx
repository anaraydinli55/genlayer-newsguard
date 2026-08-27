"use client"
import { useEffect, useState } from "react";
import { Search, ExternalLink, ShieldCheck } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { formatAddress, formatDate, getVerdictColor, getCategoryLabel } from "@/lib/utils";
import { genlayerClient, NEWSGUARD_ADDRESS } from "@/lib/genlayer-client";
import type { Address } from "viem";

interface Check { id: string; creator: string; url: string; claim: string; category: string; verdict: string; confidence?: number; reasoning?: string; created_at: number; }

export function NewsList() {
  const [checks, setChecks] = useState<Check[]>([]);
  const [filter, setFilter] = useState("");
  const [verdictFilter, setVerdictFilter] = useState("all");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function load() {
      try {
        setLoading(true); setError("");
        const allChecks = await genlayerClient.readContract({
          address: NEWSGUARD_ADDRESS as Address,
          functionName: "getAllChecks",
          args: [],
        }) as any[];
        const parsed: Check[] = (allChecks || []).map((raw: any) => ({
          id: String(raw?.id ?? ""), creator: String(raw?.creator ?? ""),
          url: String(raw?.url ?? ""), claim: String(raw?.claim ?? ""),
          category: String(raw?.category ?? ""), verdict: String(raw?.verdict ?? "UNVERIFIABLE"),
          confidence: parseFloat(raw?.confidence ?? "0"), reasoning: String(raw?.reasoning ?? ""),
          created_at: Number(raw?.created_at ?? 0),
        }));
        setChecks(parsed.reverse());
      } catch (err) { console.error(err); setError("Checks could not be loaded."); setChecks([]); }
      finally { setLoading(false); }
    }
    load();
  }, []);

  const filtered = checks.filter((check) => {
    const query = filter.toLowerCase();
    return (check.claim.toLowerCase().includes(query) || check.url.toLowerCase().includes(query)) &&
           (verdictFilter === "all" || check.verdict === verdictFilter);
  });

  const verdicts = ["all", "TRUE", "FALSE", "MISLEADING", "UNVERIFIABLE"];

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row gap-4 items-center">
        <div className="relative flex-1 w-full">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
          <Input placeholder="Search claims..." className="pl-10" value={filter} onChange={(e) => setFilter(e.target.value)} />
        </div>
        <div className="flex gap-2 flex-wrap">
          {verdicts.map((v) => (
            <button key={v} onClick={() => setVerdictFilter(v)} className={`px-3 py-1.5 rounded-full text-xs font-medium transition-all ${verdictFilter === v ? "bg-violet-600 text-white" : "bg-muted text-muted-foreground hover:bg-muted/80"}`}>
              {v === "all" ? "All" : v}
            </button>
          ))}
        </div>
      </div>
      {loading && <div className="text-center py-12 text-muted-foreground">Loading checks...</div>}
      {!loading && error && <div className="text-center py-12 text-red-400">{error}</div>}
      {!loading && !error && filtered.length === 0 && <div className="text-center py-12 text-muted-foreground">No checks found.</div>}
      <div className="grid gap-4">
        {filtered.map((check) => (
          <Card key={check.id} className="hover:shadow-md transition-all">
            <CardContent className="p-6">
              <div className="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-4">
                <div className="flex-1 space-y-3">
                  <div className="flex items-center gap-3 flex-wrap">
                    <span className="text-sm font-mono text-muted-foreground">#{check.id}</span>
                    <Badge variant="outline" className={getVerdictColor(check.verdict)}>{check.verdict}</Badge>
                    <Badge variant="secondary" className="text-xs">{getCategoryLabel(check.category)}</Badge>
                  </div>
                  <p className="text-sm font-medium">{check.claim}</p>
                  {check.reasoning && <p className="text-xs text-muted-foreground italic">"{check.reasoning}"</p>}
                  <div className="flex items-center gap-2 text-xs text-muted-foreground flex-wrap">
                    <span>By {formatAddress(check.creator)}</span><span>&bull;</span><span>{formatDate(check.created_at)}</span>
                    {check.confidence !== undefined && check.confidence > 0 && <><span>&bull;</span><span className="flex items-center gap-1"><ShieldCheck className="w-3 h-3" />Confidence: {(check.confidence * 100).toFixed(0)}%</span></>}
                  </div>
                </div>
                <div className="flex gap-2">
                  {check.url && <a href={check.url} target="_blank" rel="noopener noreferrer"><Button variant="ghost" size="sm" className="gap-1"><ExternalLink className="w-4 h-4" />Source</Button></a>}
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
