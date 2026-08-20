# NewsGuard — AI-Powered On-Chain News Verification

A reusable GenLayer Intelligent Contract primitive that verifies news claims by fetching webpage content and using LLM consensus to classify claims as TRUE, MISLEADING, FALSE, or UNVERIFIABLE.

## Features

- **Web Evidence Fetching** — Renders JS-heavy pages or falls back to plain GET
- **LLM Consensus** — Uses `gl.eq_principle.json_eq` for structured validator agreement
- **7 News Categories** — politics, health, technology, finance, sports, science, general
- **Confidence Scoring** — 0.0 to 1.0 confidence with reasoning
- **On-Chain Results** — Verdicts stored permanently with evidence snippets

## Contract API

### Write Methods
| Method | Description |
|--------|-------------|
| `init()` | Initialize contract, sets deployer as owner |
| `verifyNews(url, claim, category)` | Submit a news claim for verification |

### View Methods
| Method | Description |
|--------|-------------|
| `getCheck(check_id)` | Get full check details |
| `getChecksByVerdict(verdict)` | Filter by verdict |
| `getChecksByCategory(category)` | Filter by category |
| `getAllChecks()` | List all checks |
| `getStats()` | Platform statistics |

## Deploy

Deployed on GenLayer Bradbury Testnet.

## License

MIT
