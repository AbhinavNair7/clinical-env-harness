"""A small, polite Europe PMC REST client: paged search and full-text XML, cached on disk.

About one request a second, with backoff on 429 and 5xx (Europe PMC rate-limits bursts).
Endpoints: https://europepmc.org/RestfulWebService (search, /{PMCID}/fullTextXML).
"""

from __future__ import annotations

import http.client
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

BASE = "https://www.ebi.ac.uk/europepmc/webservices/rest"
USER_AGENT = "clinical-env/0.1 (case research; polite client)"
PAGE_SIZE = 100
RETRY_STATUSES = frozenset({429, 500, 502, 503, 504})
MAX_DELAY = 60.0  # seconds; a huge Retry-After never stalls a pull for hours
PMCID = r"^PMC\d+$"  # also the cache file name, so nothing else may reach the path

# The default candidate pull: open, full-text, CC BY or CC0 case reports about common
# problems of older adults. The licence filter here is only a first pass: licence.py decides
# from each article's own XML.
DEFAULT_QUERY = (
    'PUB_TYPE:"case reports" AND OPEN_ACCESS:y AND HAS_FT:y '
    'AND (LICENSE:"cc by" OR LICENSE:"cc0") '
    'AND (polypharmacy OR "adverse drug" OR deprescribing OR delirium OR falls OR fall '
    'OR hyponatremia OR hyponatraemia OR "acute kidney injury" OR anticholinergic '
    'OR "medication reconciliation" OR "medication error" OR "prescribing cascade" '
    'OR "drug interaction") '
    'AND ("older adult" OR elderly OR geriatric OR "older patient" OR octogenarian '
    "OR nonagenarian)"
)

Get = Callable[[str], bytes]


class FetchError(RuntimeError):
    pass


class Candidate(BaseModel):
    """One search hit, as Europe PMC describes it (metadata only, no full text)."""

    model_config = ConfigDict(extra="ignore")

    pmcid: str = Field(pattern=PMCID)
    pmid: str | None = None
    doi: str | None = None
    title: str = ""
    authors: str = ""
    journal: str = ""
    year: str = ""
    search_licence: str | None = None
    abstract: str = ""

    @property
    def url(self) -> str:
        return f"https://europepmc.org/article/PMC/{self.pmcid}"


def urllib_get(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        body: bytes = response.read()
        return body


class Client:
    def __init__(
        self,
        cache_dir: Path | None = None,
        *,
        get: Get = urllib_get,
        sleep: Callable[[float], None] = time.sleep,
        clock: Callable[[], float] = time.monotonic,
        min_interval: float = 1.0,
        retries: int = 4,
    ) -> None:
        self.cache_dir = cache_dir
        self._get = get
        self._sleep = sleep
        self._clock = clock
        self._min_interval = min_interval
        self._retries = retries
        self._last: float | None = None

    def fetch(self, url: str) -> bytes:
        """GET with rate limiting and exponential backoff on throttling or server errors."""
        for attempt in range(self._retries + 1):
            if self._last is not None:
                wait = self._min_interval - (self._clock() - self._last)
                if wait > 0:
                    self._sleep(wait)
            self._last = self._clock()
            try:
                return self._get(url)
            except urllib.error.HTTPError as exc:
                if exc.code not in RETRY_STATUSES or attempt == self._retries:
                    raise FetchError(f"{url}: HTTP {exc.code}") from exc
                retry_after = exc.headers.get("Retry-After") if exc.headers else None
                delay = float(retry_after) if retry_after and retry_after.isdigit() else 0.0
            except (OSError, http.client.HTTPException) as exc:
                # URLError, timeouts, resets and truncated reads are all transient here.
                if attempt == self._retries:
                    raise FetchError(f"{url}: {exc}") from exc
                delay = 0.0
            self._sleep(min(MAX_DELAY, max(delay, 2.0**attempt)))
        raise AssertionError("unreachable")

    def search(self, query: str, limit: int) -> list[Candidate]:
        """Up to `limit` hits in relevance order, paged with cursorMark."""
        found: list[Candidate] = []
        cursor = "*"
        while len(found) < limit:
            params = {
                "query": query,
                "format": "json",
                "resultType": "core",
                "pageSize": str(min(PAGE_SIZE, limit - len(found))),
                "cursorMark": cursor,
            }
            data = self._json(f"{BASE}/search?{urllib.parse.urlencode(params)}")
            results = data.get("resultList", {}).get("result", [])
            found += [_candidate(r) for r in results if re.match(PMCID, str(r.get("pmcid", "")))]
            next_cursor = data.get("nextCursorMark")
            if not results or not next_cursor or next_cursor == cursor:
                break
            cursor = next_cursor
        return found[:limit]

    def hit_ids(self, query: str, limit: int = 10) -> tuple[int, set[str]]:
        """(total hits, every PMCID, PMID and lowercased DOI in the top `limit`) for a query:
        the identifiability check. A PubMed-only record of the source has no PMCID."""
        params = {"query": query, "format": "json", "pageSize": str(limit)}
        data = self._json(f"{BASE}/search?{urllib.parse.urlencode(params)}")
        results = data.get("resultList", {}).get("result", [])[:limit]
        ids = {str(r[k]).lower() for r in results for k in ("pmcid", "pmid", "doi") if r.get(k)}
        return int(data.get("hitCount", 0)), ids

    def _json(self, url: str) -> dict[str, Any]:
        try:
            data = json.loads(self.fetch(url))
        except json.JSONDecodeError as exc:
            raise FetchError(f"{url}: not JSON ({exc})") from exc
        if not isinstance(data, dict):
            raise FetchError(f"{url}: not a JSON object")
        return data

    def full_text(self, pmcid: str) -> bytes:
        cached = self.cache_dir / f"{pmcid}.xml" if self.cache_dir else None
        if cached is not None and cached.exists():
            return cached.read_bytes()
        body = self.fetch(f"{BASE}/{urllib.parse.quote(pmcid)}/fullTextXML")
        if cached is not None:
            cached.parent.mkdir(parents=True, exist_ok=True)
            cached.write_bytes(body)
        return body


def _candidate(result: dict[str, object]) -> Candidate:
    journal_info = result.get("journalInfo")
    journal = ""
    if isinstance(journal_info, dict):
        inner = journal_info.get("journal")
        if isinstance(inner, dict):
            journal = str(inner.get("title") or "")
    return Candidate(
        pmcid=str(result["pmcid"]),
        pmid=_text(result.get("pmid")),
        doi=_text(result.get("doi")),
        title=str(result.get("title") or ""),
        authors=str(result.get("authorString") or ""),
        journal=journal,
        year=str(result.get("pubYear") or ""),
        search_licence=_text(result.get("license")),
        abstract=str(result.get("abstractText") or ""),
    )


def _text(value: object) -> str | None:
    return str(value) if value else None
