import { createClient } from "genlayer-js";

// =============================================================================
// CONTRACT ADDRESS — DEGISTIR: Deploy sonrasi gercek adresi buraya yapistr
// =============================================================================
export const NEWSGUARD_ADDRESS = "0x4e691dfA2857CB394928166F1158718B1d429257";

const bradbury = {
  id: 1,
  name: "GenLayer Testnet",
  nativeCurrency: { name: "ETH", symbol: "ETH", decimals: 18 },
  rpcUrls: { default: { http: ["https://rpc-bradbury.genlayer.com"] } },
} as const;

export const genlayerClient = createClient({
  chain: bradbury as any,
  endpoint: "https://rpc-bradbury.genlayer.com",
});
