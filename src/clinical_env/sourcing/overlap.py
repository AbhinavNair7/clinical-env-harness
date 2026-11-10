"""Copy checks between a drafted case and its source article.

`shared_runs` finds every run of 8 or more words the case shares with the source (lowercased,
punctuation ignored), so no sentence is carried over. `source_text` pulls the readable text
of a JATS full-text XML: article titles (including cited ones), abstract, body, and figures
and tables kept outside the body.
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from collections.abc import Iterable

RUN_WORDS = 8
_WORD = re.compile(r"[a-z0-9]+(?:'[a-z]+)?")


def words(text: str) -> list[str]:
    return _WORD.findall(text.lower())


def shared_runs(case_text: str, source: str, n: int = RUN_WORDS) -> list[str]:
    """Each maximal run of at least `n` consecutive case words that also appears in the source
    as `n`-word pieces, in case order."""
    src = words(source)
    grams = {tuple(src[i : i + n]) for i in range(len(src) - n + 1)}
    mine = words(case_text)
    hit = [False] * len(mine)
    for i in range(len(mine) - n + 1):
        if tuple(mine[i : i + n]) in grams:
            hit[i : i + n] = [True] * n
    runs: list[str] = []
    start: int | None = None
    for i, flag in enumerate([*hit, False]):
        if flag and start is None:
            start = i
        elif not flag and start is not None:
            runs.append(" ".join(mine[start:i]))
            start = None
    return runs


def source_text(xml: bytes) -> str:
    root = ET.fromstring(xml)
    parts: Iterable[ET.Element] = [
        *root.iter("article-title"),
        *root.iter("abstract"),
        *root.iter("body"),
        *root.iter("floats-group"),  # figures and tables some journals keep outside <body>
    ]
    return "\n".join(" ".join("".join(el.itertext()).split()) for el in parts)


def strings(value: object) -> Iterable[str]:
    """Every string in a loaded YAML or JSON value."""
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from strings(item)
