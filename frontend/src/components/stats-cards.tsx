"use client"
import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { CheckCircle, XCircle, AlertTriangle, HelpCircle, BarChart3 } from "lucide-react";
import { genlayerClient, NEWSGUARD_ADDRESS } from "@/lib/genlayer-client";
import type { Address } from "viem";

interface Stats { total_checks?: string; true?: string; false?: string; misleading?: string; unverifiable?: string; accuracy?: string; }

export function StatsCards() {
  const [stats, setStats] = useState<Stats>({});
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    async function load() {
      try {
        const result = await genlayerClient.readContract({
          address: NEWSGUARD_ADDRESS as Address,
          functionName: "getStats",
          args: [],
        }) as Stats;
        setStats(result);
      } catch (e) { console.error(e); }
      finally { setLoading(false); }
    }
    load();
  }, []);
  const items = [
    { label: "Total", value: stats.total_checks || "0", icon: BarChart3, color: "text-blue-400" },
    { label: "True", value: stats.true || "0", icon: CheckCircle, color: "text-emerald-400" },
    { label: "False", value: stats.false || "0", icon: XCircle, color: "text-red-400" },
    { label: "Misleading", value: stats.misleading || "0", icon: AlertTriangle, color: "text-amber-400" },
    { label: "Unverifiable", value: stats.unverifiable || "0", icon: HelpCircle, color: "text-slate-400" },
  ];
  return <div className="grid grid-cols-2 md:grid-cols-5 gap-4">{items.map((item) => <Card key={item.label} className="bg-card/50"><CardHeader className="flex flex-row items-center justify-between pb-2"><CardTitle className="text-sm font-medium text-muted-foreground">{item.label}</CardTitle><item.icon className={`w-4 h-4 ${item.color}`} /></CardHeader><CardContent><div className="text-2xl font-bold">{loading ? "—" : item.value}</div></CardContent></Card>)}</div>;
}
