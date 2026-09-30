# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *
import json

VERDICTS = ("TRUE", "MISLEADING", "FALSE", "UNVERIFIABLE")
CATEGORIES = ("politics", "health", "technology", "finance", "sports", "science", "general")
UNVERIFIABLE = {"verdict": "UNVERIFIABLE", "confidence": 0, "key_evidence": ""}


def _norm(s: str) -> str:
    return " ".join(str(s).split()).lower()


def _fetch_text(url: str) -> str:
    try:
        r = gl.nondet.web.render(url, mode="text")
        text = r.body.decode("utf-8", "ignore") if hasattr(r, "body") else str(r)
        return " ".join(text.split())[:4000]
    except Exception:
        return ""


def _analyze(page: str, claim: str, category: str) -> dict:
    if not page:
        return dict(UNVERIFIABLE)
    prompt = (
        "You are a fact-checker. Compare the claim with the page text.\n"
        f"CLAIM: {claim}\nCATEGORY: {category}\nPAGE:\n{page[:2000]}\n\n"
        "Reply ONLY with JSON: "
        '{"verdict":"TRUE|MISLEADING|FALSE|UNVERIFIABLE","confidence":0-100,'
        '"key_evidence":"one VERBATIM quote from PAGE, max 200 chars"}'
    )
    try:
        raw = gl.nondet.exec_prompt(prompt)
        if isinstance(raw, dict):
            data = raw
        else:
            s = str(raw).replace("```json", "").replace("```", "")
            data = json.loads(s[s.find("{"): s.rfind("}") + 1])
        verdict = str(data.get("verdict", "")).upper().strip()
        if verdict not in VERDICTS:
            return dict(UNVERIFIABLE)
        conf = max(0, min(100, int(float(data.get("confidence", 0)))))
        return {"verdict": verdict, "confidence": conf,
                "key_evidence": str(data.get("key_evidence", ""))[:200]}
    except Exception:
        return dict(UNVERIFIABLE)


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
        if category not in CATEGORIES:
            raise gl.vm.UserError("Invalid category")

        def leader_fn():
            return _analyze(_fetch_text(url), claim, category)

        def validator_fn(leaders_res: gl.vm.Result) -> bool:
            if not isinstance(leaders_res, gl.vm.Return):
                return False
            leader = leaders_res.calldata
            if leader.get("verdict") not in VERDICTS:
                return False
            page = _fetch_text(url)
            mine = _analyze(page, claim, category)
            if mine["verdict"] != leader["verdict"]:
                return False
            if leader["verdict"] != "UNVERIFIABLE":
                ev = _norm(leader.get("key_evidence", ""))
                if not ev or ev not in _norm(page):
                    return False
            return True

        res = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)

        count = int(self.check_count) + 1
        self.check_count = str(count)
        cid = str(count)
        c = json.loads(self.checks) if self.checks else {}
        c[cid] = {
            "id": cid, "creator": str(gl.message.sender_address),
            "url": url, "claim": claim, "category": category,
            "verdict": res["verdict"], "confidence": str(res["confidence"]),
            "key_evidence": res["key_evidence"], "status": "resolved",
        }
        self.checks = json.dumps(c, sort_keys=True)
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
        cnt = lambda v: str(sum(1 for x in c.values() if x["verdict"] == v))
        true_n = sum(1 for x in c.values() if x["verdict"] == "TRUE")
        return {
            "total_checks": str(total), "true": cnt("TRUE"), "false": cnt("FALSE"),
            "misleading": cnt("MISLEADING"), "unverifiable": cnt("UNVERIFIABLE"),
            "accuracy": str(round(true_n / total, 2)) if total > 0 else "0",
        }
