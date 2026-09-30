import { createClient } from "genlayer-js";
import { testnetBradbury } from "genlayer-js/chains";

export const NEWSGUARD_ADDRESS = (process.env.NEXT_PUBLIC_NEWSGUARD_ADDRESS ??
  "0x970aB8503378c9cAdc81a269C63412a24886d9eC") as `0x${string}`;
export const RPC_ENDPOINT = "https://rpc-bradbury.genlayer.com";

export const getReadClient = () =>
  createClient({ chain: testnetBradbury, endpoint: RPC_ENDPOINT });

export const getWriteClient = (account: `0x${string}`, provider: unknown) =>
  createClient({ chain: testnetBradbury, endpoint: RPC_ENDPOINT, account, provider: provider as any });
