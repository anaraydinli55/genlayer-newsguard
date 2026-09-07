import { createClient } from "genlayer-js";

export const NEWSGUARD_ADDRESS = "0xfd25C0aB8adB63996573Ae37224B40A66d93B5A0" as `0x${string}`;

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
