=============================================================================
NEWSGUARD DEPLOY TALIMATLARI
=============================================================================
1. LINT KONTROLU (ZORUNLU)
Contract'i deploy etmeden once mutlaka lint calistir:
bash
genvm-linter check NewsGuard.py
# veya
genlayer lint --contract NewsGuard.py
HATA alirsan, hatayi buraya yapistir, duzeltelim.
2. DEPLOY
Yontem A: GenLayer CLI
bash
# Bradbury testnet'e deploy et
genlayer deploy --contract ./NewsGuard.py   --rpc https://rpc-bradbury.genlayer.com   --network testnet-bradbury

# Cikti ornegi:
# Contract deployed at: 0x1234567890abcdef...
# Transaction hash: 0x...
Yontem B: GenLayer Studio (Daha kolay)
https://studio.genlayer.com ac
"New Project" -> "Import Contract"
NewsGuard.py icerigini yapistir
"Deploy" butonuna tikla
MetaMask'te onayla
3. EXPLORER DOGRULAMA
Deploy edilen adresi Explorer'da kontrol et:
plain
https://explorer-bradbury.genlayer.com/address/<DEPLOY_ADDRESS>
Sayfada "Contract Code" veya "Verified" gormen lazim.
Gormuyorsan = deploy basarisiz olmus veya adres yanlis.
4. FRONTEND GUNCELLEME
frontend/src/lib/genlayer-client.ts icindeki adresi degistir:
TypeScript
export const NEWSGUARD_ADDRESS = "0x<GERCEK_DEPLOY_ADRESIN>";
5. README GUNCELLEME
README.md'ye ekle:
markdown
## Deploy

- **Network:** GenLayer Bradbury Testnet
- **Contract Address:** `0x<GERCEK_DEPLOY_ADRESIN>`
- **Explorer:** https://explorer-bradbury.genlayer.com/address/0x<GERCEK_DEPLOY_ADRESIN>
6. TEST
Studio veya CLI ile test et:
bash
# init cagir (one-time)
genlayer write 0x<ADRES> init --network testnet-bradbury

# news verify et
genlayer write 0x<ADRES> verifyNews   --args "https://example.com/news" "Earth is flat" "science"   --network testnet-bradbury

# sonuclari oku
genlayer call 0x<ADRES> getAllChecks --network testnet-bradbury
7. SUBMIT
Formu doldur:
Title: NewsGuard — Decentralized Fake News Verifier on GenLayer
Description: (asagida hazir metin)
GitHub: https://github.com/anaraydinli55/genlayer-newsguard
Evidence: Explorer adresi + (opsiyonel) demo video
SUBMISSION METNI (kopyala-yapistir)
Title:
NewsGuard — Decentralized Fake News Verifier on GenLayer
Notes / Description:
NewsGuard is a trustless news verification platform that solves the
centralized fact-checking problem through GenLayer's Optimistic Democracy
consensus. Users submit a URL and claim via the frontend; each validator
independently fetches the webpage and runs an LLM analysis, then strict_eq
enforces bit-exact consensus on a normalized verdict (TRUE / MISLEADING /
FALSE / UNVERIFIABLE) with confidence scoring.
What it does: Decentralized fake news detection using multi-LLM consensus
with independent web evidence fetching per validator.
Problem it solves: Centralized fact-checkers are opaque, biased, and
censorable. NewsGuard replaces them with a transparent, auditable,
consensus-driven process.
How to use it: Clone the repo, run npm install in frontend/, configure
the GenLayer contract address in genlayer-client.ts, run npm run dev,
connect wallet, and submit news via the UI. Or interact directly via
GenLayer Explorer / CLI.
Tech stack: GenLayer Intelligent Contracts (Python), Next.js 14,
TypeScript, Tailwind CSS, shadcn/ui, wagmi.
GitHub Repository URL:
https://github.com/anaraydinli55/genlayer-newsguard
Explorer Address:
0x<GERCEK_DEPLOY_ADRESIN>
