"use client";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { WagmiProvider } from "wagmi";
import { RainbowKitProvider, getDefaultConfig } from "@rainbow-me/rainbowkit";
import { metaMaskWallet, rabbyWallet, walletConnectWallet, coinbaseWallet } from "@rainbow-me/rainbowkit/wallets";
import { testnetBradbury } from "genlayer-js/chains";
import { useState } from "react";

const config = getDefaultConfig({
  appName: "NewsGuard",
  projectId: "demo",
  chains: [testnetBradbury],
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
