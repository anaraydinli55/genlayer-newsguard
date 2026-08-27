import { type ClassValue, clsx } from "clsx";
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
