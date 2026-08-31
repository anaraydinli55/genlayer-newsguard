import { createClient } from "genlayer-js";
import { testnetBradbury } from "genlayer-js/chains";

export const NEWSGUARD_ADDRESS = "0xB2047950bbc68E7BdA744a326608cf62053ED371" as `0x${string}`;

export const genlayerClient = createClient({
  chain: testnetBradbury,
  endpoint: "https://rpc-bradbury.genlayer.com",
});
