"""Offline unit tests: NewsGuard.py is loaded against a stubbed `gl` SDK object."""
import importlib.util
import pathlib
import re
import sys
import types

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = (ROOT / "NewsGuard.py").read_text()

PAGE = "This domain is for use in documentation examples without needing permission."
LLM_TRUE = '{"verdict":"TRUE","confidence":90,"key_evidence":"documentation examples"}'


class Result:
    pass


class Return(Result):
    def __init__(self, calldata):
        self.calldata = calldata


class UserError(Exception):
    pass


def _make_gl():
    gl = types.SimpleNamespace()
    gl.Contract = object
    gl.public = types.SimpleNamespace(write=lambda f: f, view=lambda f: f)
    gl.message = types.SimpleNamespace(sender_address="0xTEST")
    gl.nondet = types.SimpleNamespace(
        web=types.SimpleNamespace(render=lambda url, mode="text": ""),
        exec_prompt=lambda p: "{}",
    )
    gl.vm = types.SimpleNamespace(
        Result=Result, Return=Return, UserError=UserError,
        run_nondet_unsafe=lambda leader, validator: leader(),
    )
    return gl


@pytest.fixture
def mod():
    gl = _make_gl()
    stub = types.ModuleType("genlayer")
    stub.gl = gl
    sys.modules["genlayer"] = stub
    spec = importlib.util.spec_from_file_location("newsguard_contract", ROOT / "NewsGuard.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    m._gl = gl
    yield m
    sys.modules.pop("genlayer", None)


def _run(mod, page, llm):
    mod._gl.nondet.web.render = lambda url, mode="text": page
    mod._gl.nondet.exec_prompt = lambda p: llm
    captured = {}

    def fake_run(leader, validator):
        captured["validator"] = validator
        return leader()

    mod._gl.vm.run_nondet_unsafe = fake_run
    c = mod.NewsGuard()
    cid = c.verifyNews("https://x", "claim", "general")
    return c, cid, captured["validator"]


def test_runner_is_pinned_by_hash():
    first = SRC.splitlines()[0]
    assert re.fullmatch(r'# \{ "Depends": "py-genlayer:[0-9a-z]{40,}" \}', first), first


def test_uses_leader_validator_not_strict_eq():
    assert "run_nondet_unsafe" in SRC
    assert "strict_eq" not in SRC


def test_fetch_failure_returns_empty(mod):
    def boom(url, mode="text"):
        raise RuntimeError("net")
    mod._gl.nondet.web.render = boom
    assert mod._fetch_text("https://x") == ""


def test_empty_page_is_unverifiable(mod):
    assert mod._analyze("", "claim", "general")["verdict"] == "UNVERIFIABLE"


@pytest.mark.parametrize("raw", ["not json", '{"verdict":"MAYBE"}', "{}"])
def test_bad_llm_output_is_unverifiable(mod, raw):
    mod._gl.nondet.exec_prompt = lambda p: raw
    assert mod._analyze("page", "claim", "general")["verdict"] == "UNVERIFIABLE"


def test_llm_exception_is_unverifiable(mod):
    def boom(p):
        raise RuntimeError("llm")
    mod._gl.nondet.exec_prompt = boom
    assert mod._analyze("page", "claim", "general")["verdict"] == "UNVERIFIABLE"


def test_valid_output_is_normalized_and_confidence_clamped(mod):
    mod._gl.nondet.exec_prompt = lambda p: '```json\n{"verdict":"true","confidence":250,"key_evidence":"quote"}\n```'
    assert mod._analyze("page quote", "claim", "general") == {
        "verdict": "TRUE", "confidence": 100, "key_evidence": "quote"}


def test_verify_stores_result_and_stats(mod):
    c, cid, _ = _run(mod, PAGE, LLM_TRUE)
    rec = c.getCheck(cid)
    assert rec["verdict"] == "TRUE" and rec["key_evidence"] == "documentation examples"
    assert c.getStats()["true"] == "1"


def test_fetch_failure_is_recorded_as_unverifiable(mod):
    def boom(url, mode="text"):
        raise RuntimeError("net")
    mod._gl.nondet.web.render = boom
    c = mod.NewsGuard()
    cid = c.verifyNews("https://bad.invalid", "claim", "general")
    rec = c.getCheck(cid)
    assert rec["verdict"] == "UNVERIFIABLE" and rec["confidence"] == "0" and rec["key_evidence"] == ""


def test_invalid_category_rejected(mod):
    with pytest.raises(UserError):
        mod.NewsGuard().verifyNews("https://x", "claim", "nonsense")


def test_validator_accepts_matching_verdict_and_evidence(mod):
    _, _, v = _run(mod, PAGE, LLM_TRUE)
    assert v(Return({"verdict": "TRUE", "confidence": 50, "key_evidence": "documentation examples"})) is True


def test_validator_rejects_different_verdict(mod):
    _, _, v = _run(mod, PAGE, LLM_TRUE)
    assert v(Return({"verdict": "FALSE", "confidence": 90, "key_evidence": "documentation examples"})) is False


def test_validator_rejects_fabricated_evidence(mod):
    _, _, v = _run(mod, PAGE, LLM_TRUE)
    assert v(Return({"verdict": "TRUE", "confidence": 90, "key_evidence": "invented quote"})) is False


def test_validator_rejects_non_return_result(mod):
    _, _, v = _run(mod, PAGE, LLM_TRUE)
    assert v(Result()) is False
