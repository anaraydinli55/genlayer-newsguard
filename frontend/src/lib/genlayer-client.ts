import { createClient } from "genlayer-js";

export const NEWSGUARD_ADDRESS = "0xB2047950bbc68E7BdA744a326608cf62053ED371";

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
