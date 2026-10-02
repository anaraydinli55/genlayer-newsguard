import { createClient } from "genlayer-js";
import { testnetBradbury } from "genlayer-js/chains";

export const NEWSGUARD_ADDRESS = "0xfd25C0aB8adB63996573Ae37224B40A66d93B5A0" as `0x${string}`;

export function getReadClient() {
  return createClient({
    chain: testnetBradbury,
  });
}

export function getWriteClient(account: `0x${string}`, provider: any) {
  return createClient({
    chain: testnetBradbury,
    account,
    provider,
  });
}
