# { "Depends": "py-genlayer:latest" }
from genlayer import *
import json

class NewsGuard(gl.Contract):
    owner: str
    check_count: str
    checks: str

    def __init__(self):
        self.owner = ""
        self.check_count = "0"
        self.checks = "{}"

    @gl.public.write
    def init(self) -> None:
        self.owner = str(gl.message.sender_address)

    @gl.public.view
    def getOwner(self) -> str:
        return self.owner

    @gl.public.write
    def verifyNews(self, url: str, claim: str, category: str = "general") -> str:
        """Consensus-bound verification: Fetches webpage content and runs LLM fact-checking inside validator consensus."""
        cats = ["politics", "health", "technology", "finance", "sports", "science", "general"]
        if category not in cats:
            raise gl.vm.UserError("Invalid category")

        def evaluate_consensus():
            try:
                response = gl.nondet.web.render(url, mode="text")
                if hasattr(response, "body"):
                    content = response.body.decode("utf-8")[:4000]
                else:
                    content = str(response)[:4000]
            except Exception:
                content = ""

            if not content:
                return json.dumps({
                    "verdict": "UNVERIFIABLE",
                    "confidence": 0.0,
                    "reasoning": "Failed to fetch webpage content",
                    "key_evidence": ""
                }, sort_keys=True)

            prompt = (
                "You are an expert fact-checker. Analyze the following webpage content against the given claim.\n\n"
                f"CLAIM: {claim}\n"
                f"CATEGORY: {category}\n"
                f"WEBPAGE CONTENT:\n{content[:2000]}\n\n"
                "Respond ONLY with valid JSON in this exact format:\n"
                '{"verdict":"TRUE"|"MISLEADING"|"FALSE"|"UNVERIFIABLE","confidence":0.0-1.0,"reasoning":"...","key_evidence":"..."}'
            )
            result = gl.nondet.exec_prompt(prompt)

            try:
                if isinstance(result, str):
                    cleaned = result.replace("```json", "").replace("```", "").strip()
                    s_idx = cleaned.find("{")
                    e_idx = cleaned.rfind("}")
                    parsed = json.loads(cleaned[s_idx:e_idx + 1]) if (s_idx != -1 and e_idx != -1) else {}
                elif isinstance(result, dict):
                    parsed = result
                else:
                    parsed = {}
            except Exception:
                parsed = {}

            verdict = str(parsed.get("verdict", "UNVERIFIABLE")).upper().strip()
            if verdict not in ["TRUE", "MISLEADING", "FALSE", "UNVERIFIABLE"]:
                verdict = "UNVERIFIABLE"

            try:
                confidence = float(parsed.get("confidence", 0.0))
                if not (0.0 <= confidence <= 1.0):
                    confidence = 0.0
            except Exception:
                confidence = 0.0

            return json.dumps({
                "verdict": verdict,
                "confidence": confidence,
                "reasoning": str(parsed.get("reasoning", "No detailed reasoning")),
                "key_evidence": str(parsed.get("key_evidence", "No evidence extracted"))
            }, sort_keys=True)

        consensus_result_str = gl.eq_principle.strict_eq(evaluate_consensus)
        res = json.loads(consensus_result_str)

        count = int(self.check_count) + 1
        self.check_count = str(count)
        cid = str(count)

        c = json.loads(self.checks) if self.checks else {}
        c[cid] = {
            "id": cid,
            "creator": str(gl.message.sender_address),
            "url": url,
            "claim": claim,
            "category": category,
            "verdict": res["verdict"],
            "confidence": str(res["confidence"]),
            "reasoning": res["reasoning"],
            "key_evidence": res["key_evidence"],
            "status": "resolved"
        }
        self.checks = json.dumps(c, sort_keys=True)
        gl.emit("NewsVerified", {"check_id": cid, "verdict": res["verdict"]})
        return cid

    @gl.public.view
    def getCheck(self, check_id: str) -> dict:
        c = json.loads(self.checks) if self.checks else {}
        if str(check_id) not in c:
            raise gl.vm.UserError("Check not found")
        return c[str(check_id)]

    @gl.public.view
    def getAllChecks(self) -> list:
        return list(json.loads(self.checks).values()) if self.checks else []

    @gl.public.view
    def getChecksByVerdict(self, verdict: str) -> list:
        c = json.loads(self.checks) if self.checks else {}
        return [x for x in c.values() if x["verdict"] == verdict]

    @gl.public.view
    def getChecksByCategory(self, category: str) -> list:
        c = json.loads(self.checks) if self.checks else {}
        return [x for x in c.values() if x["category"] == category]

    @gl.public.view
    def getStats(self) -> dict:
        c = json.loads(self.checks) if self.checks else {}
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
            "accuracy": str(round(true_count / total, 2)) if total > 0 else "0"
        }
