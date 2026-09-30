"use client"

import { useState, useCallback } from "react"
import { useAccount, useWalletClient } from "wagmi"
import { NEWSGUARD_ADDRESS, getReadClient, getWriteClient } from "@/lib/genlayer-client"

export function useNewsGuard() {
  const { address, isConnected } = useAccount()
  const { data: walletClient } = useWalletClient()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const verifyNews = useCallback(async (url: string, claim: string, category: string = "general") => {
    if (!isConnected) throw new Error("Wallet not connected")
    const account = walletClient?.account?.address
    const provider = (window as any).ethereum
    if (!account || !provider) throw new Error("No wallet connected.")
    setLoading(true)
    setError(null)
    try {
      return await getWriteClient(account, provider).writeContract({
        address: NEWSGUARD_ADDRESS,
        functionName: "verifyNews",
        args: [url, claim, category],
        value: BigInt(0),
      })
    } catch (err: any) {
      setError(err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }, [isConnected, walletClient])

  const getAllChecks = useCallback(
    () => getReadClient().readContract({ address: NEWSGUARD_ADDRESS, functionName: "getAllChecks", args: [] }),
    [])

  const getStats = useCallback(
    () => getReadClient().readContract({ address: NEWSGUARD_ADDRESS, functionName: "getStats", args: [] }),
    [])

  return { verifyNews, getAllChecks, getStats, loading, error, isConnected, address }
}
