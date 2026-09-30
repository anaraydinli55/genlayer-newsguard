# NewsGuard — Decentralized News Verifier on GenLayer

A GenLayer Intelligent Contract that verifies a news claim against a web page. Every validator fetches the page and runs the LLM analysis independently; consensus is reached on the **normalized verdict** (TRUE / MISLEADING / FALSE / UNVERIFIABLE) and on evidence that actually appears in the page. Any fetch or parse failure resolves to UNVERIFIABLE.

## How consensus works

`verifyNews(url, claim, category)` uses `gl.vm.run_nondet_unsafe(leader_fn, validator_fn)`:

- **Leader** fetches the page, asks the LLM, and returns `{verdict, confidence, key_evidence}`.
- **Each validator** fetches the page itself and re-runs the analysis, then accepts the leader only if:
  1. its own verdict equals the leader's verdict, and
  2. (for non-UNVERIFIABLE verdicts) the leader's `key_evidence` quote occurs in the page the validator fetched.
- Free-form text and raw page content are never compared. `confidence` (0-100) is informational only and is **not** part of consensus.
- Fetch error, empty page, LLM error, unparsable output, or an unknown verdict all become `UNVERIFIABLE` with confidence 0.

## Contract API

| Method | Type | Description |
|---|---|---|
| `init()` | write | Sets the caller as owner |
| `verifyNews(url, claim, category)` | write | Runs validator-checked verification, stores and returns the check id |
| `getCheck(check_id)` | view | One check |
| `getAllChecks()` | view | All checks |
| `getChecksByVerdict(verdict)` | view | Filter by verdict |
| `getChecksByCategory(category)` | view | Filter by category |
| `getStats()` | view | Counts per verdict (returned as strings) |

Categories: politics, health, technology, finance, sports, science, general.
Stored fields per check: `id, creator, url, claim, category, verdict, confidence, key_evidence, status`.

## Pinned versions and one-command check

- Contract runner is pinned by hash on line 1 of `NewsGuard.py` (`py-genlayer:1jb45aa8…`).
- `genlayer-js` is pinned to exactly `1.1.8` in both `package.json` files.
- Deployed and tested with GenLayer CLI `0.39.2`.

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements-dev.txt
(cd frontend && npm ci)
./scripts/check.sh
```

`scripts/check.sh` verifies the runner pin, the exact SDK version match, contract syntax, the contract tests, and the frontend type check.

**Scope of the tests:** `tests/test_newsguard.py` loads `NewsGuard.py` against a stubbed `gl` object, so it covers the contract logic (failure handling, verdict normalization, validator acceptance/rejection rules) but not GenVM itself. Real consensus is demonstrated by the live transactions below.

## Deploy

```bash
genlayer network set testnet-bradbury
genlayer deploy --contract NewsGuard.py
```

## Frontend

Single client configuration: `frontend/src/lib/genlayer-client.ts` (Bradbury chain from `genlayer-js/chains`). The contract address comes from `NEXT_PUBLIC_NEWSGUARD_ADDRESS` (see `frontend/.env.example`) and defaults to the deployment below. The write call sends exactly the contract's three arguments.

```bash
cd frontend && npm ci && npm run dev
```

## Live deployment (Bradbury Testnet, chain 4221)

- Contract: `0x970aB8503378c9cAdc81a269C63412a24886d9eC`
- Explorer: https://explorer-bradbury.genlayer.com/address/0x970aB8503378c9cAdc81a269C63412a24886d9eC
- Deploy tx: `0xfa283f62e2fd15433f09b83fedfe0254663a747bc16b3574614ba401355f8339` (ACCEPTED, AGREE, FINISHED_WITH_RETURN)

Verified on this deployment:

| Input | Result | Validators |
|---|---|---|
| `https://example.com` + matching claim | `TRUE`, confidence 100, evidence quoted from the page | 3 AGREE, 2 TIMEOUT (accepted) |
| unreachable `.invalid` domain | `UNVERIFIABLE`, confidence 0, empty evidence | 5 AGREE |

Note: on the testnet some validators can time out while fetching and calling the LLM; the transaction is still accepted when the majority agrees.

## License

MIT
