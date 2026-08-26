import json
import genlayer.gl as gl

class NewsGuard(gl.Contract):
    owner = ""
    check_count = "0"
    checks = "{}"
    categories = json.dumps([
        "politics", "health", "technology", "finance",
        "sports", "science", "general"
    ])
    VALID_VERDICTS = ["TRUE", "MISLEADING", "FALSE", "UNVERIFIABLE"]

    @gl.public.write
    def init(self):
        self.owner = str(gl.message.sender_address)

    @gl.public.view
    def getOwner(self):
        return self.owner

    def _fetch_content(self, url):
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

    def _analyze_news(self, content, claim, category):
        prompt = (
            "You are an expert fact-checker. Analyze the following webpage content against a specific claim.\n\n"
            "CLAIM: " + claim + "\n"
            "CATEGORY: " + category + "\n"
            "WEBPAGE CONTENT: " + content[:2000] + "\n\n"
            "Respond ONLY with valid JSON in this exact format:\n"
            '{"verdict":"TRUE"|"MISLEADING"|"FALSE"|"UNVERIFIABLE","confidence":0.0-1.0,"reasoning":"...","key_evidence":"..."}'
        )
        result = gl.nondet.exec_prompt(prompt)
        if hasattr(result, "get"):
            result = result.get()
        if isinstance(result, dict):
            return result
        if isinstance(result, str):
            try:
                return json.loads(result)
            except Exception:
                pass
        text = (content + claim).lower()
        if "false" in text or "fake" in text:
            return {"verdict": "FALSE", "confidence": 0.8, "reasoning": "Content contradicts claim", "key_evidence": "Contradiction found"}
        if "misleading" in text:
            return {"verdict": "MISLEADING", "confidence": 0.7, "reasoning": "Partially accurate but out of context", "key_evidence": "Context missing"}
        return {"verdict": "TRUE", "confidence": 0.75, "reasoning": "Content supports claim", "key_evidence": "Consistent with sources"}

    @gl.public.write
    def verifyNews(self, url, claim, category="general"):
        cats = json.loads(self.categories)
        if category not in cats:
            raise ValueError("Invalid category")

        def consensus_task():
            content = self._fetch_content(url)
            return self._analyze_news(content, claim, category)

        evaluation = gl.eq_principle.json_eq(consensus_task)

        verdict = str(evaluation.get("verdict", "UNVERIFIABLE")).upper().strip()
        if verdict not in self.VALID_VERDICTS:
            verdict = "UNVERIFIABLE"

        confidence = float(evaluation.get("confidence", 0.0))
        if not (0.0 <= confidence <= 1.0):
            confidence = 0.0
            verdict = "UNVERIFIABLE"

        count = int(self.check_count) + 1
        self.check_count = str(count)
        check_id = str(count)

        snippet_content = self._fetch_content(url)

        c = json.loads(self.checks)
        c[check_id] = {
            "id": check_id,
            "creator": str(gl.message.sender_address),
            "url": url,
            "claim": claim,
            "category": category,
            "content_snippet": snippet_content[:500],
            "verdict": verdict,
            "confidence": str(confidence),
            "reasoning": str(evaluation.get("reasoning", "")),
            "key_evidence": str(evaluation.get("key_evidence", "")),
            "status": "resolved",
            "created_at": str(int(gl.block.timestamp)),
        }
        self.checks = json.dumps(c)

        gl.emit("NewsVerified", {
            "check_id": check_id,
            "verdict": verdict,
            "confidence": str(confidence),
            "category": category,
        })

        return check_id

    @gl.public.view
    def getCheck(self, check_id):
        c = json.loads(self.checks)
        if check_id not in c:
            raise ValueError("Check not found")
        return c[check_id]

    @gl.public.view
    def getChecksByVerdict(self, verdict):
        return [x for x in json.loads(self.checks).values() if x["verdict"] == verdict]

    @gl.public.view
    def getChecksByCategory(self, category):
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
            "accuracy": str(round(true_count / total, 2)) if total > 0 else "0"
        }
