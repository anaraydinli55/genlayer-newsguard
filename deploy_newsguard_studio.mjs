import { createClient } from "genlayer-js";
import { studionet } from "genlayer-js/chains";
import { privateKeyToAccount } from "viem/accounts";
import fs from "fs";

const rawKey = process.env.GENLAYER_PRIVATE_KEY || process.env.PRIVATE_KEY;
if (!rawKey) {
  console.error("❌ PRIVATE_KEY bulunamadı!");
  process.exit(1);
}

const privateKey = rawKey.startsWith("0x") ? rawKey : "0x" + rawKey;
const account = privateKeyToAccount(privateKey);

const client = createClient({
  chain: studionet,
  account,
});

console.log("🔑 Deployer:", account.address);
console.log("⛓️  Ağ:     ", studionet.name);

async function main() {
  const contractCode = fs.readFileSync("NewsGuard.py", "utf8");

  console.log("\n🚀 NewsGuard kontratı deploy ediliyor...");
  const txHash = await client.deployContract({
    code: contractCode,
    args: [],
    leaderOnly: false,
  });

  console.log("⏳ Deploy tx gönderildi:", txHash);
  console.log("⏳ Onay bekleniyor (15 sn)...");
  await new Promise(r => setTimeout(r, 15000));

  const tx = await client.getTransaction({ hash: txHash });
  const contractAddress = tx.to_address || tx.contract_address || tx.recipient || (tx.data && tx.data.contract_address);

  console.log("\n=======================================================");
  console.log("✅ KONTRAT BAŞARIYLA DAĞITILDI!");
  console.log("📍 Kontrat Adresi:", contractAddress);
  console.log("🔗 RESMİ EXPLORER KANIT LİNKİ:");
  console.log(`https://explorer-studio.genlayer.com/address/${contractAddress}`);
  console.log("=======================================================\n");

  console.log("🔧 init() çağrılıyor...");
  const initTx = await client.writeContract({
    address: contractAddress,
    functionName: "init",
    args: [],
  });
  console.log("⏳ init tx:", initTx);
  await new Promise(r => setTimeout(r, 10000));
  console.log("✅ init() tamamlandı!");

  // Frontend config dosyasını güncelle
  const clientPath = "frontend/src/lib/genlayer-client.ts";
  let content = fs.readFileSync(clientPath, "utf8");
  content = content.replace(/export const NEWSGUARD_ADDRESS = "0x[a-fA-F0-9]+" as `0x\${string}`;/, `export const NEWSGUARD_ADDRESS = "${contractAddress}" as \`0x\${string}\`;`);
  fs.writeFileSync(clientPath, content);
  console.log("✅ frontend/src/lib/genlayer-client.ts yeni adresle güncellendi!");
}

main().catch(err => {
  console.error("❌ Hata:", err);
  process.exit(1);
});
