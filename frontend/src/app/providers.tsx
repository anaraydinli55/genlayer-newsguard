"use client";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { WagmiProvider } from "wagmi";
import { RainbowKitProvider, getDefaultConfig } from "@rainbow-me/rainbowkit";
import { metaMaskWallet, rabbyWallet, walletConnectWallet, coinbaseWallet } from "@rainbow-me/rainbowkit/wallets";
import { useState } from "react";

const bradbury = {
  id: 1,
  name: "GenLayer Testnet",
  nativeCurrency: { name: "ETH", symbol: "ETH", decimals: 18 },
  rpcUrls: { default: { http: ["https://rpc-bradbury.genlayer.com"] } },
} as const;

const config = getDefaultConfig({
  appName: "NewsGuard",
  projectId: "demo",
  chains: [bradbury as any],
  wallets: [
    { groupName: "EVM Wallets", wallets: [metaMaskWallet, rabbyWallet, coinbaseWallet, walletConnectWallet] },
  ],
  ssr: true,
});

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient());
  return (
    <WagmiProvider config={config}>
      <QueryClientProvider client={queryClient}>
        <RainbowKitProvider>{children}</RainbowKitProvider>
      </QueryClientProvider>
    </WagmiProvider>
  );
}
