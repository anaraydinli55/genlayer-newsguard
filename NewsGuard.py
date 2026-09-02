# { "Depends": "py-genlayer:15qfivjvy80800rh998pcxmd2m8va1wq2qzqhz850n8ggcr4i9q0" }
from genlayer import *
import json

class NewsGuard(gl.Contract):
    owner: str = ""
    check_count: str = "0"
    checks: str = "{}"

    def __init__(self):
        self.owner = str(gl.message.sender_address)
        self.check_count = "0"
        self.checks = "{}"

    @gl.public.view
    def getOwner(self):
        return self.owner

    @gl.public.view
    def checkNews(self, url, claim, category="general"):
        """View method: fetches web content and runs LLM analysis. No state change, no consensus needed."""
        cats = ["politics", "health", "technology", "finance", "sports", "science", "general"]
        if category not in cats:
            raise ValueError("Invalid category")
        
        # Fetch content — failures return UNVERIFIABLE
        try:
            response = gl.nondet.web.get(url)
            if hasattr(response, "body"):
                content = response.body.decode("utf-8")[:4000]
            else:
                content = str(response)[:4000]
        except Exception:
            return {
                "verdict": "UNVERIFIABLE",
                "confidence": "0",
                "reasoning": "Failed to fetch URL content",
                "key_evidence": "",
                "content_snippet": ""
            }
        
        # LLM analysis — parse failures return UNVERIFIABLE
        try:
            prompt = (
                "You are an expert fact-checker. Analyze the following webpage content against a specific claim.\n\n"
                "CLAIM: " + claim + "\n"
                "CATEGORY: " + category + "\n"
                "WEBPAGE CONTENT:\n" + content[:2000] + "\n\n"
                "Respond ONLY with valid JSON in this exact format:\n"
                '{"verdict":"TRUE"|"MISLEADING"|"FALSE"|"UNVERIFIABLE","confidence":0.0-1.0,"reasoning":"...","key_evidence":"..."}'
            )
            result = gl.nondet.exec_prompt(prompt)
            
            if isinstance(result, dict):
                parsed = result
            elif isinstance(result, str):
                cleaned = result.replace("```json", "").replace("```", "").strip()
                parsed = json.loads(cleaned)
            else:
                return {"verdict": "UNVERIFIABLE", "confidence": "0", "reasoning": "Invalid LLM response format", "key_evidence": "", "content_snippet": content[:500]}
            
            verdict = str(parsed.get("verdict", "UNVERIFIABLE")).upper().strip()
            if verdict not in ["TRUE", "MISLEADING", "FALSE", "UNVERIFIABLE"]:
                verdict = "UNVERIFIABLE"
            
            confidence = float(parsed.get("confidence", 0.0))
            if not (0.0 <= confidence <= 1.0):
                confidence = 0.0
            
            return {
                "verdict": verdict,
                "confidence": str(confidence),  # STRING! not float
                "reasoning": str(parsed.get("reasoning", "")),
                "key_evidence": str(parsed.get("key_evidence", "")),
                "content_snippet": content[:500]
            }
        except Exception:
            return {
                "verdict": "UNVERIFIABLE",
                "confidence": "0",
                "reasoning": "Failed to parse LLM response",
                "key_evidence": "",
                "content_snippet": content[:500]
            }

    @gl.public.write
    def verifyNews(self, url, claim, category, verdict, confidence_pct, reasoning, key_evidence):
        """Write method: validator logic checks meaningful verdict before storing."""
        # Validator logic: check meaningful verdict
        v = str(verdict).upper().strip()
        if v not in ["TRUE", "MISLEADING", "FALSE", "UNVERIFIABLE"]:
            raise ValueError("Invalid verdict: must be TRUE, MISLEADING, FALSE, or UNVERIFIABLE")
        
        # Validator logic: check confidence range
        conf_pct = int(confidence_pct)
        if not (0 <= conf_pct <= 100):
            raise ValueError("Invalid confidence: must be 0-100")
        
        # Validator logic: check reasoning quality
        if not reasoning or len(str(reasoning).strip()) < 10:
            raise ValueError("Reasoning required: minimum 10 characters")
        
        # Validator logic: check key evidence
        if not key_evidence or len(str(key_evidence).strip()) < 5:
            raise ValueError("Key evidence required: minimum 5 characters")
        
        # Validator logic: check category
        cats = ["politics", "health", "technology", "finance", "sports", "science", "general"]
        if category not in cats:
            raise ValueError("Invalid category")
        
        count = int(self.check_count) + 1
        self.check_count = str(count)
        check_id = str(count)
        
        conf = conf_pct / 100.0
        
        c = json.loads(self.checks) if self.checks else {}
        c[check_id] = {
            "id": check_id,
            "creator": str(gl.message.sender_address),
            "url": url,
            "claim": claim,
            "category": category,
            "verdict": v,
            "confidence": str(conf),
            "reasoning": str(reasoning),
            "key_evidence": str(key_evidence),
            "status": "resolved"
        }
        self.checks = json.dumps(c, sort_keys=True)
        return check_id

    @gl.public.view
    def getCheck(self, check_id):
        c = json.loads(self.checks) if self.checks else {}
        cid = str(check_id)
        if cid not in c:
            raise ValueError("Check not found")
        return c[cid]

    @gl.public.view
    def getChecksByVerdict(self, verdict):
        c = json.loads(self.checks) if self.checks else {}
        return [x for x in c.values() if x["verdict"] == verdict]

    @gl.public.view
    def getChecksByCategory(self, category):
        c = json.loads(self.checks) if self.checks else {}
        return [x for x in c.values() if x["category"] == category]

    @gl.public.view
    def getAllChecks(self):
        return list(json.loads(self.checks).values()) if self.checks else []

    @gl.public.view
    def getStats(self):
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
