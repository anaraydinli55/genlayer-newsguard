"use client"

import { useState, useCallback } from "react"
import { useAccount, useWalletClient } from "wagmi"
import { createClient } from "genlayer-js"
import { testnetBradbury } from "genlayer-js/chains"
import { NEWSGUARD_ADDRESS } from "@/lib/genlayer-client"

export function useNewsGuard() {
  const { address, isConnected } = useAccount()
  const { data: walletClient } = useWalletClient()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const getReadClient = useCallback(() => {
    return createClient({
      chain: testnetBradbury,
      endpoint: "https://rpc-bradbury.genlayer.com",
    })
  }, [])

  const getWriteClient = useCallback(() => {
    if (!walletClient?.account?.address) {
      throw new Error("No wallet connected.")
    }
    const ethProvider = (window as any).ethereum
    if (!ethProvider) {
      throw new Error("No Ethereum provider found.")
    }
    return createClient({
      chain: testnetBradbury,
      endpoint: "https://rpc-bradbury.genlayer.com",
      account: walletClient.account.address,
      provider: ethProvider,
    })
  }, [walletClient])

  const verifyNews = useCallback(async (url: string, claim: string, category: string = "general") => {
    if (!isConnected) throw new Error("Wallet not connected")
    setLoading(true)
    setError(null)
    try {
      const client = getWriteClient()
      return await client.writeContract({
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
  }, [isConnected, getWriteClient])

  const getAllChecks = useCallback(async () => {
    const client = getReadClient()
    return await client.readContract({
      address: NEWSGUARD_ADDRESS,
      functionName: "getAllChecks",
      args: [],
    })
  }, [getReadClient])

  const getStats = useCallback(async () => {
    const client = getReadClient()
    return await client.readContract({
      address: NEWSGUARD_ADDRESS,
      functionName: "getStats",
      args: [],
    })
  }, [getReadClient])

  return { verifyNews, getAllChecks, getStats, loading, error, isConnected, address }
}
