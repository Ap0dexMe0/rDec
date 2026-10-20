#!/usr/bin/env python3

"""Korean -> English translation table for script data that RYL ships in
Korean (comment headers in .ncf/.mcf script sources, server chat strings,
scaffold label rows).

`translate_text()` is the single entry point used by the decoders. It never
guesses: only exact matches from this table are replaced, so any string the
game data receives outside this file stays untouched. Strings containing
Hangul that have no entry are recorded in the "collected" log while
RDEC_COLLECT=1 is set, so a full regeneration lists every still-untranslated
string once.
"""

import os
import re

HANGUL = re.compile(r"[\uac00-\ud7a3\u3130-\u318f]")
CJK = re.compile(r"[\u3000-\u3020\uac00-\ud7a3\u3130-\u318f]")

# Exact-string table. Keys are the strings exactly as they appear in the
# decoded game data (comment bodies after '//', quoted server strings,
# scaffold table cells). Exact whole-string keys only.
KOR_EN = {
    # MonsterProtoType.gsf scaffold row 0 (field labels, Korean game build)
    "이름": "Name",
    "모델링 파일명": "Model file name",
}

_LOG = None


def _log_miss(s: str) -> None:
    global _LOG
    if _LOG is None:
        path = os.environ.get("RDEC_COLLECT")
        if not path:
            return
        _LOG = open(path, "a", encoding="utf-8")  # noqa: SIM115 - process-wide sink
    try:
        _LOG.write(s.replace("\r", "\\r").replace("\n", "\\n") + "\n")
    except Exception:
        pass


def translate_text(s: str) -> str:
    """Replace known Korean strings with their English translations."""
    if not CJK.search(s):
        return s
    hit = KOR_EN.get(s)
    if hit is not None:
        return hit
    for kor, eng in KOR_EN.items():
        if kor in s:
            s = s.replace(kor, eng)
            if not CJK.search(s):
                return s
    if HANGUL.search(s):
        _log_miss(s)
    return s
