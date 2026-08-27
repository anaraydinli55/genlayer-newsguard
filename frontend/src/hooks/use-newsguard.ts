"use client"
import { useState, useCallback } from "react";
import { useAccount, useWalletClient } from "wagmi";
import { createClient } from "genlayer-js";
import { NEWSGUARD_ADDRESS } from "@/lib/genlayer-client";

const bradbury = {
  id: 1,
  name: "GenLayer Testnet",
  nativeCurrency: { name: "ETH", symbol: "ETH", decimals: 18 },
  rpcUrls: { default: { http: ["https://rpc-bradbury.genlayer.com"] } },
} as const;

export function useNewsGuard() {
  const { address, isConnected } = useAccount();
  const { data: walletClient } = useWalletClient();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const getClient = useCallback(() => {
    if (!walletClient) throw new Error("No wallet connected.");
    return createClient({ chain: bradbury as any, endpoint: "https://rpc-bradbury.genlayer.com", account: walletClient.account });
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
