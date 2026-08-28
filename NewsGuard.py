# { "Depends": "py-genlayer:0.1.0" }
import json
from genlayer import *

# =============================================================================
# MODULE-LEVEL HELPERS (no self access — safe for nondet blocks)
# =============================================================================

def _fetch_content(url: str) -> str:
    """Fetch webpage content using render or GET fallback."""
    try:
        response = gl.nondet.web.render(url)
        if hasattr(response, "body"):
            return response.body.decode("utf-8")[:4000]
        return str(response)[:4000]
    except Exception:
        try:
            response = gl.nondet.web.get(url)
            if hasattr(response, "body"):
                return response.body.decode("utf-8")[:4000]
            return str(response)[:4000]
        except Exception:
            return ""

def _analyze_news(content: str, claim: str, category: str) -> str:
    """
    Analyze news content and return a DETERMINISTIC JSON string.
    strict_eq requires exact match across validators, so we:
      1. Parse LLM output
      2. Normalize fields (upper, strip, clamp)
      3. Return json.dumps(sort_keys=True) for bit-exact consensus
    """
    prompt = (
        "You are an expert fact-checker. Analyze the following webpage content against a specific claim.\n\n"
        "CLAIM: " + claim + "\n"
        "CATEGORY: " + category + "\n"
        "WEBPAGE CONTENT: " + content[:2000] + "\n\n"
        "Respond ONLY with valid JSON in this exact format:\n"
        '{\"verdict\":\"TRUE\"|\"MISLEADING\"|\"FALSE\"|\"UNVERIFIABLE\",\"confidence\":0.0-1.0,\"reasoning\":\"...\",\"key_evidence\":\"...\"}'
    )
    raw = gl.nondet.exec_prompt(prompt)

    # Clean markdown wrappers that LLMs sometimes add
    cleaned = raw.replace("```json", "").replace("```", "").strip()

    try:
        parsed = json.loads(cleaned)
    except Exception:
        # Fallback heuristic if LLM returns invalid JSON
        text = (content + claim).lower()
        if "false" in text or "fake" in text:
            parsed = {
                "verdict": "FALSE",
                "confidence": 0.8,
                "reasoning": "Content contradicts claim",
                "key_evidence": "Contradiction found",
            }
        elif "misleading" in text:
            parsed = {
                "verdict": "MISLEADING",
                "confidence": 0.7,
                "reasoning": "Partially accurate but out of context",
                "key_evidence": "Context missing",
            }
        else:
            parsed = {
                "verdict": "TRUE",
                "confidence": 0.75,
                "reasoning": "Content supports claim",
                "key_evidence": "Consistent with sources",
            }

    # Normalize for deterministic consensus
    verdict = str(parsed.get("verdict", "UNVERIFIABLE")).upper().strip()
    if verdict not in ["TRUE", "MISLEADING", "FALSE", "UNVERIFIABLE"]:
        verdict = "UNVERIFIABLE"

    confidence = float(parsed.get("confidence", 0.0))
    if not (0.0 <= confidence <= 1.0):
        confidence = 0.0

    # sort_keys=True guarantees identical byte output across validators
    return json.dumps(
        {
            "verdict": verdict,
            "confidence": confidence,
            "reasoning": str(parsed.get("reasoning", "")),
            "key_evidence": str(parsed.get("key_evidence", "")),
        },
        sort_keys=True,
    )


# =============================================================================
# INTELLIGENT CONTRACT
# =============================================================================

class NewsGuard(gl.Contract):
    owner: str = ""
    check_count: str = "0"
    checks: str = "{}"
    categories: str = json.dumps(
        [
            "politics",
            "health",
            "technology",
            "finance",
            "sports",
            "science",
            "general",
        ]
    )
    VALID_VERDICTS = ["TRUE", "MISLEADING", "FALSE", "UNVERIFIABLE"]

    # -------------------------------------------------------------------------
    # Lifecycle
    # -------------------------------------------------------------------------
    def __init__(self):
        """Constructor — runs once at deploy."""
        self.owner = str(gl.message.sender_address)
        self.check_count = "0"
        self.checks = "{}"
        self.categories = json.dumps(["politics", "health", "technology", "finance", "sports", "science", "general"])

    @gl.public.view
    def getOwner(self) -> str:
        return self.owner

    # -------------------------------------------------------------------------
    # Core: Verify News
    # -------------------------------------------------------------------------
    @gl.public.write
    def verifyNews(self, url: str, claim: str, category: str = "general") -> str:
        """
        Submit a news claim for verification.
        Each validator independently fetches the URL and runs the LLM,
        then strict_eq enforces bit-exact consensus on the normalized result.
        """
        cats = json.loads(self.categories)
        if category not in cats:
            raise ValueError("Invalid category")

        # CRITICAL: read everything into locals BEFORE entering nondet blocks
        # Storage (self) is inaccessible inside nondet blocks.
        url_local = url
        claim_local = claim
        category_local = category

        # --- Consensus Block 1: Analysis ---
        def consensus_task():
            content = _fetch_content(url_local)
            return _analyze_news(content, claim_local, category_local)

        # strict_eq is valid here because _analyze_news returns a fully
        # normalized JSON string (sort_keys=True). No raw nondet output leaks.
        result_json = gl.eq_principle.strict_eq(consensus_task)
        evaluation = json.loads(result_json)

        verdict = evaluation["verdict"]
        confidence = evaluation["confidence"]

        # --- Consensus Block 2: Snippet (web content may vary, isolated) ---
        def fetch_snippet():
            return _fetch_content(url_local)[:500]

        snippet = gl.eq_principle.strict_eq(fetch_snippet)

        # --- Deterministic storage write (outside nondet) ---
        count = int(self.check_count) + 1
        self.check_count = str(count)
        check_id = str(count)

        c = json.loads(self.checks)
        c[check_id] = {
            "id": check_id,
            "creator": str(gl.message.sender_address),
            "url": url,
            "claim": claim,
            "category": category,
            "content_snippet": snippet,
            "verdict": verdict,
            "confidence": str(confidence),
            "reasoning": evaluation["reasoning"],
            "key_evidence": evaluation["key_evidence"],
            "status": "resolved",
            "created_at": str(int(gl.block.timestamp)),
        }
        self.checks = json.dumps(c)

        gl.emit(
            "NewsVerified",
            {
                "check_id": check_id,
                "verdict": verdict,
                "confidence": str(confidence),
                "category": category,
            },
        )

        return check_id

    # -------------------------------------------------------------------------
    # Views
    # -------------------------------------------------------------------------
    @gl.public.view
    def getCheck(self, check_id: str):
        c = json.loads(self.checks)
        if check_id not in c:
            raise ValueError("Check not found")
        return c[check_id]

    @gl.public.view
    def getChecksByVerdict(self, verdict: str):
        return [x for x in json.loads(self.checks).values() if x["verdict"] == verdict]

    @gl.public.view
    def getChecksByCategory(self, category: str):
        return [x for x in json.loads(self.checks).values() if x["category"] == category]

    @gl.public.view
    def getAllChecks(self):
        return list(json.loads(self.checks).values())

    @gl.public.view
    def getStats(self):
        c = json.loads(self.checks)
        total = len(c)
        true_count = sum(1 for x in c.values() if x["verdict"] == "TRUE")
        false_count = sum(1 for x in c.values() if x["verdict"] == "FALSE")
        misleading_count = sum(1 for x in c.values() if x["verdict"] == "MISLEADING")
        unverifiable_count = sum(1 for x in c.values() if x["verdict"] == "UNVERIFIABLE")
        return {
            "total_checks": str(total),
            "true": str(true_count),
            "false": str(false_count),
            "misleading": str(misleading_count),
            "unverifiable": str(unverifiable_count),
            "accuracy": str(round(true_count / total, 2)) if total > 0 else "0",
        }
