"use client";
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

  // Read-only client (no wallet required for view calls)
  const getReadClient = useCallback(() => {
    return createClient({
      chain: bradbury as any,
      endpoint: "https://rpc-bradbury.genlayer.com",
    });
  }, []);

  // Write client (wallet required for state-changing calls)
  const getWriteClient = useCallback(() => {
    if (!walletClient?.account?.address) {
      throw new Error("No wallet connected.");
    }
    return createClient({
      chain: bradbury as any,
      endpoint: "https://rpc-bradbury.genlayer.com",
      account: { address: walletClient.account.address },
    });
  }, [walletClient]);

  const verifyNews = useCallback(
    async (url: string, claim: string, category: string = "general") => {
      if (!isConnected) throw new Error("Wallet not connected");
      setLoading(true);
      setError(null);
      try {
        const client = getWriteClient();
        return await client.writeContract({
          address: NEWSGUARD_ADDRESS,
          functionName: "verifyNews",
          args: [url, claim, category],
        });
      } catch (err: any) {
        setError(err.message);
        throw err;
      } finally {
        setLoading(false);
      }
    },
    [isConnected, getWriteClient]
  );

  const getAllChecks = useCallback(async () => {
    const client = getReadClient();
    return await client.readContract({
      address: NEWSGUARD_ADDRESS,
      functionName: "getAllChecks",
      args: [],
    });
  }, [getReadClient]);

  const getStats = useCallback(async () => {
    const client = getReadClient();
    return await client.readContract({
      address: NEWSGUARD_ADDRESS,
      functionName: "getStats",
      args: [],
    });
  }, [getReadClient]);

  return {
    verifyNews,
    getAllChecks,
    getStats,
    loading,
    error,
    isConnected,
    address,
  };
}
