"""Case-report sourcing: the licence rule, the polite client, copy checks and the prefilter.

All XML and search replies here are synthetic; nothing calls Europe PMC.
"""

from __future__ import annotations

import csv
import email.message
import json
import urllib.error
from pathlib import Path

import pytest
import yaml

from clinical_env.sourcing import commands
from clinical_env.sourcing.europepmc import Candidate, Client, FetchError
from clinical_env.sourcing.licence import decide
from clinical_env.sourcing.overlap import shared_runs, source_text
from clinical_env.sourcing.screen import ages, prefilter


def article(licence: str, body: str = "<p>She fell twice.</p>") -> bytes:
    return (
        '<article xmlns:xlink="http://www.w3.org/1999/xlink" '
        'xmlns:ali="http://www.niso.org/schemas/ali/1.0/"><front><article-meta>'
        "<title-group><article-title>A case</article-title></title-group>"
        f"<permissions>{licence}</permissions></article-meta></front>"
        f"<body>{body}</body></article>"
    ).encode()


BY_LINK = '<license xlink:href="https://creativecommons.org/licenses/by/4.0/"><license-p>Open.</license-p></license>'
BY_TEXT_ONLY = (
    "<license><license-p>This is an open access article distributed under the terms of the "
    "Creative Commons Attribution License CC-BY 4.0., which permits unrestricted use."
    "</license-p></license>"
)
BY_ALI = (
    "<ali:license_ref>http://creativecommons.org/licenses/by/4.0/</ali:license_ref>"
    "<license><license-p>Reuse allowed.</license-p></license>"
)
NC_LINK = '<license xlink:href="https://creativecommons.org/licenses/by-nc/4.0/"><license-p>x</license-p></license>'
NC_TEXT = (
    "<license><license-p>Creative Commons Attribution-NonCommercial 4.0 International"
    "</license-p></license>"
)
SA_HIDDEN = (
    '<license xlink:href="https://creativecommons.org/licenses/by/4.0/"><license-p>Licensed '
    "under CC BY-SA.</license-p></license>"
)
CC0 = '<license xlink:href="https://creativecommons.org/publicdomain/zero/1.0/"><license-p>CC0</license-p></license>'
BMC_WITH_DATA_WAIVER = (
    "<license><license-p><bold>Open Access</bold> This article is licensed under a Creative "
    "Commons Attribution 4.0 International License. To view a copy of this licence, visit "
    '<ext-link xlink:href="http://creativecommons.org/licenses/by/4.0/">'
    "http://creativecommons.org/licenses/by/4.0/</ext-link>. The Creative Commons Public "
    "Domain Dedication waiver "
    '(<ext-link xlink:href="http://creativecommons.org/publicdomain/zero/1.0/">'
    "http://creativecommons.org/publicdomain/zero/1.0/</ext-link>) applies to the data made "
    "available in this article, unless otherwise stated.</license-p></license>"
)
OPEN_ONLY = "<license><license-p>This is an open access article.</license-p></license>"


@pytest.mark.parametrize(
    ("licence", "search", "accepted", "reason"),
    [
        (BY_LINK, "cc by", True, "full text says cc by"),
        (BY_TEXT_ONLY, "cc by", True, "full text says cc by"),
        (BY_ALI, "cc by", True, "full text says cc by"),
        (CC0, "cc0", True, "full text says cc0"),
        (BMC_WITH_DATA_WAIVER, "cc by", True, "full text says cc by"),
        (NC_LINK, "cc by", False, "restricted"),
        (NC_TEXT, "cc by", False, "restricted"),
        (SA_HIDDEN, "cc by", False, "restricted"),
        (OPEN_ONLY, "cc by", False, "does not name CC BY or CC0"),
        ("", "cc by", False, "no licence element"),
        (BY_LINK, "cc by-nc", False, "search metadata says"),
        (BY_LINK + CC0, "cc by", False, "both CC BY and CC0"),
    ],
    ids=[
        "by-link",
        "by-text-only",
        "by-ali",
        "cc0",
        "bmc-data-waiver",
        "nc-link",
        "nc-text",
        "sa-in-text",
        "open-access-only",
        "missing",
        "metadata-disagrees",
        "two-licences",
    ],
)
def test_licence_rule(licence: str, search: str, accepted: bool, reason: str) -> None:
    decision = decide(article(licence), search)
    assert decision.accepted is accepted
    assert reason in decision.reason
    if licence:
        assert decision.evidence


@pytest.mark.parametrize(
    "wording",
    [
        "Creative Commons Attribution Non Commercial 4.0",
        "Creative Commons Attribution No Derivatives 4.0",
        "Creative Commons Attribution Share Alike 4.0",
        "Licensed under CC BY\u2013NC 4.0",
        "Licensed under CC BY\u2011NC\u2011ND 4.0",
        "Licensed under CCBY-NC 4.0",
    ],
)
def test_restricted_wording_variants_are_rejected(wording: str) -> None:
    licence = f"<license><license-p>{wording}</license-p></license>"
    decision = decide(article(licence), "cc by")
    assert not decision.accepted
    assert "restricted" in decision.reason


def test_a_licence_link_that_is_not_cc_is_rejected() -> None:
    licence = (
        "<ali:license_ref>https://www.elsevier.com/tdm/userlicense/1.0/</ali:license_ref>"
        "<license><license-p>Creative Commons Attribution</license-p></license>"
    )
    decision = decide(article(licence), "cc by")
    assert not decision.accepted
    assert "not CC" in decision.reason


def test_no_front_matter_is_rejected() -> None:
    xml = f"<article><body><fig><permissions>{BY_LINK}</permissions></fig></body></article>"
    xml = xml.replace("<article>", '<article xmlns:xlink="http://www.w3.org/1999/xlink">')
    assert not decide(xml.encode(), "cc by").accepted


def test_figure_licence_in_the_body_does_not_count() -> None:
    body = f"<fig><permissions>{NC_LINK}</permissions></fig><p>Text.</p>"
    assert decide(article(BY_LINK, body), "cc by").accepted


def test_unreadable_xml_is_rejected() -> None:
    assert not decide(b"<article><unclosed></article>", "cc by").accepted


class FakeClock:
    def __init__(self) -> None:
        self.now = 0.0
        self.sleeps: list[float] = []

    def sleep(self, seconds: float) -> None:
        self.sleeps.append(seconds)
        self.now += seconds

    def clock(self) -> float:
        return self.now


def http_error(code: int, retry_after: str | None = None) -> urllib.error.HTTPError:
    headers = email.message.Message()
    if retry_after:
        headers["Retry-After"] = retry_after
    return urllib.error.HTTPError("https://x", code, "err", headers, None)


def test_client_backs_off_on_throttling_then_succeeds() -> None:
    clock = FakeClock()
    replies: list[object] = [http_error(429, "5"), http_error(503), b"ok"]

    def get(url: str) -> bytes:
        reply = replies.pop(0)
        if isinstance(reply, Exception):
            raise reply
        assert isinstance(reply, bytes)
        return reply

    client = Client(get=get, sleep=clock.sleep, clock=clock.clock)
    assert client.fetch("https://x") == b"ok"
    assert clock.sleeps[0] == 5.0  # Retry-After honoured
    assert clock.sleeps[1] == 2.0  # then exponential backoff


def test_client_retries_timeouts_and_caps_retry_after() -> None:
    clock = FakeClock()
    replies: list[object] = [TimeoutError("read timed out"), http_error(429, "86400"), b"ok"]

    def get(url: str) -> bytes:
        reply = replies.pop(0)
        if isinstance(reply, Exception):
            raise reply
        assert isinstance(reply, bytes)
        return reply

    assert Client(get=get, sleep=clock.sleep, clock=clock.clock).fetch("https://x") == b"ok"
    assert clock.sleeps == [1.0, 60.0]


def test_a_timeout_on_every_try_becomes_a_fetch_error() -> None:
    clock = FakeClock()

    def get(url: str) -> bytes:
        raise ConnectionResetError("reset")

    with pytest.raises(FetchError, match="reset"):
        Client(get=get, sleep=clock.sleep, clock=clock.clock, retries=2).fetch("https://x")


def test_client_gives_up_and_does_not_retry_a_404() -> None:
    clock = FakeClock()
    calls: list[str] = []

    def get(url: str) -> bytes:
        calls.append(url)
        raise http_error(404)

    with pytest.raises(FetchError, match="HTTP 404"):
        Client(get=get, sleep=clock.sleep, clock=clock.clock).fetch("https://x")
    assert len(calls) == 1


def test_client_waits_about_a_second_between_requests() -> None:
    clock = FakeClock()
    client = Client(get=lambda url: b"x", sleep=clock.sleep, clock=clock.clock)
    client.fetch("a")
    client.fetch("b")
    assert clock.sleeps == [1.0]


def search_page(results: list[dict[str, object]], cursor: str) -> bytes:
    return json.dumps(
        {"hitCount": 3, "nextCursorMark": cursor, "resultList": {"result": results}}
    ).encode()


def hit(pmcid: str, licence: str = "cc by") -> dict[str, object]:
    return {
        "pmcid": pmcid,
        "title": "Falls in an 84-year-old woman",
        "abstractText": "An 84-year-old woman on five medicines fell twice.",
        "license": licence,
        "pubYear": "2026",
        "authorString": "A B.",
        "journalInfo": {"journal": {"title": "Cureus"}},
    }


def test_pull_logs_every_decision_and_keeps_abstracts_only_when_open(tmp_path: Path) -> None:
    pages = {
        "*": search_page([hit("PMC1"), hit("PMC2", "cc by-nc")], "c2"),
        "c2": search_page([hit("PMC3")], "c2"),
    }
    texts = {"PMC1": article(BY_LINK), "PMC2": article(NC_LINK), "PMC3": article(OPEN_ONLY)}

    def get(url: str) -> bytes:
        if "/search?" in url:
            cursor = "c2" if "cursorMark=c2" in url else "*"
            return pages[cursor]
        return texts[url.split("/")[-2]]

    clock = FakeClock()
    client = Client(tmp_path / "fulltext", get=get, sleep=clock.sleep, clock=clock.clock)
    assert commands.pull(client, "q", 10, tmp_path) == 0
    rows = [json.loads(line) for line in (tmp_path / "candidates.jsonl").read_text().splitlines()]
    assert [(r["pmcid"], r["accepted"]) for r in rows] == [
        ("PMC1", True),
        ("PMC2", False),
        ("PMC3", False),
    ]
    assert "abstract" in rows[0] and "abstract" not in rows[1]
    assert rows[0]["prefilter_drop"] == []
    with (tmp_path / "licence_log.csv").open() as f:
        assert len(list(csv.DictReader(f))) == 3
    assert (tmp_path / "fulltext" / "PMC1.xml").exists()


def test_shared_runs_finds_copied_text_and_ignores_short_echoes() -> None:
    source = "The patient was found on the floor by her carer early in the morning."
    copied = "Note: she was found on the floor by her carer early in the morning, again."
    seven = "She was found on the floor by her son later."
    assert shared_runs(copied, source) == [
        "was found on the floor by her carer early in the morning"
    ]
    assert shared_runs(seven, source) == []


def test_source_text_reads_title_abstract_and_body() -> None:
    xml = article(BY_LINK, "<sec><p>Sodium was 118.</p></sec>")
    text = source_text(xml)
    assert "A case" in text and "Sodium was 118." in text


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("An 84-year-old woman", [84]),
        ("a man aged 91 presented", [91]),
        ("78 year old with falls", [78]),
        ("an 82-yo", [82]),
    ],
)
def test_ages(text: str, expected: list[int]) -> None:
    assert ages(text) == expected


def candidate(title: str, abstract: str = "") -> Candidate:
    return Candidate(pmcid="PMC1", title=title, abstract=abstract)


def test_prefilter() -> None:
    assert prefilter(candidate("Delirium in an 86-year-old man")) == []
    assert prefilter(candidate("An octogenarian with falls")) == []
    assert prefilter(candidate("Falls in a 64-year-old")) == ["no stated age of 70+"]
    assert prefilter(
        candidate("A 75-year-old woman", "Radiographs showed a fracture; her children helped.")
    ) == ["image-led"]
    assert "surgical technique" in prefilter(candidate("Laparoscopic repair in a 72-year-old"))


def test_identifiability_queries() -> None:
    queries = dict(commands.identifiability_queries(["sertraline", "hyponatremia", "falls"]))
    assert queries["all details"] == (
        '(sertraline) AND (hyponatremia) AND (falls) AND PUB_TYPE:"case reports"'
    )
    assert queries["any detail, by relevance"].startswith("((sertraline) OR (hyponatremia)")
    assert queries["pair: sertraline + hyponatremia"] == (
        '(sertraline) AND (hyponatremia) AND PUB_TYPE:"case reports"'
    )
    assert len(queries) == 1 + 3 + 1


def test_theme_pairs_are_not_searched() -> None:
    queries = dict(
        commands.identifiability_queries(
            ["glipizide", "mirtazapine", "prednisone"], ["pancreatic cancer", "worsening diabetes"]
        )
    )
    assert "pair: pancreatic cancer + worsening diabetes" not in queries
    assert "pair: glipizide + pancreatic cancer" in queries
    assert "pancreatic cancer" not in queries["any detail, by relevance"]
    assert len(queries) == 1 + (3 + 3 * 2) + 1


def provenance(case_id: str) -> dict[str, object]:
    return {
        "case_id": case_id,
        "pmcid": "PMC1",
        "title": "A case",
        "authors": "A B.",
        "journal": "Cureus",
        "year": "2026",
        "licence": "cc by",
        "url": "https://europepmc.org/article/PMC/PMC1",
        "changes": ["drug", "timeline", "presentation"],
        "distinctive_details": ["a", "b", "c"],
    }


def check_with(tmp_path: Path, case_text: str, top: list[str]) -> int:
    case = tmp_path / "case_x.yaml"
    case.write_text(yaml.safe_dump({"id": "case_x", "summary": case_text}))
    (tmp_path / "provenance").mkdir()
    (tmp_path / "provenance" / "case_x.yaml").write_text(yaml.safe_dump(provenance("case_x")))
    body = "<p>The patient was found on the floor by her carer early in the morning.</p>"

    def get(url: str) -> bytes:
        if "/search?" in url:
            return json.dumps(
                {"hitCount": len(top), "resultList": {"result": [{"pmcid": p} for p in top]}}
            ).encode()
        return article(BY_LINK, body)

    clock = FakeClock()
    client = Client(tmp_path / "fulltext", get=get, sleep=clock.sleep, clock=clock.clock)
    return commands.check(client, case, tmp_path / "provenance")


def test_check_passes_a_rewritten_case(tmp_path: Path) -> None:
    assert check_with(tmp_path, "Her son says she was on the hall rug at dawn.", ["PMC9"]) == 0


def test_check_fails_copied_text(tmp_path: Path) -> None:
    copied = "She was found on the floor by her carer early in the morning."
    assert check_with(tmp_path, copied, ["PMC9"]) == 1


def test_check_fails_when_the_source_is_findable(tmp_path: Path) -> None:
    assert check_with(tmp_path, "Rewritten entirely.", ["PMC9", "PMC1"]) == 1


def test_check_fails_when_only_the_doi_is_found(tmp_path: Path) -> None:
    case = tmp_path / "case_x.yaml"
    case.write_text(yaml.safe_dump({"id": "case_x", "summary": "Rewritten entirely."}))
    (tmp_path / "provenance").mkdir()
    prov = provenance("case_x") | {"doi": "10.1/ABC"}
    (tmp_path / "provenance" / "case_x.yaml").write_text(yaml.safe_dump(prov))

    def get(url: str) -> bytes:
        if "/search?" in url:  # a PubMed-only record of the source: no PMCID
            return json.dumps(
                {"hitCount": 1, "resultList": {"result": [{"doi": "10.1/abc"}]}}
            ).encode()
        return article(BY_LINK)

    clock = FakeClock()
    client = Client(tmp_path / "fulltext", get=get, sleep=clock.sleep, clock=clock.clock)
    assert commands.check(client, case, tmp_path / "provenance") == 1
