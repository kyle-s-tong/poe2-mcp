"""Shared helpers for the PoB-PoE2 Lua data refresh scripts."""

from __future__ import annotations

import re
import urllib.request
from typing import Iterator

REPO = "PathOfBuildingCommunity/PathOfBuilding-PoE2"
BRANCH = "dev"


def fetch_lua(filename: str, subdir: str) -> str:
    """Download a Lua data file from upstream PoB-PoE2."""
    url = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/src/Data/{subdir}/{filename}"
    with urllib.request.urlopen(url, timeout=30) as r:
        return r.read().decode("utf-8")


def preprocess(text: str) -> str:
    """Strip comments and rewrite PoB-specific constructs so slpp can parse."""
    text = re.sub(r"(?m)--[^\n]*$", "", text)
    text = re.sub(r"\[\s*([A-Z]\w*)\s*\.\s*(\w+)\s*\]", r'["\2"]', text)
    text = re.sub(
        r"\b(?:mod|flag|skill|SkillMod|SkillFlag)\s*\([^()]*(?:\([^()]*\)[^()]*)*\)",
        "nil",
        text,
    )
    return text


def find_blocks(text: str, var_name: str) -> Iterator[tuple[str, str]]:
    """Yield (key, '{...}') for each `<var_name>["key"] = { ... }` assignment."""
    pattern = re.compile(rf'{re.escape(var_name)}\[\s*"([^"]+)"\s*\]\s*=\s*')
    for m in pattern.finditer(text):
        start = m.end()
        if start >= len(text) or text[start] != "{":
            continue
        depth = 0
        in_string = False
        escape = False
        j = start
        while j < len(text):
            c = text[j]
            if escape:
                escape = False
            elif c == "\\":
                escape = True
            elif c == '"' and not escape:
                in_string = not in_string
            elif not in_string:
                if c == "{":
                    depth += 1
                elif c == "}":
                    depth -= 1
                    if depth == 0:
                        yield m.group(1), text[start:j + 1]
                        break
            j += 1


def set_table_to_list(value):
    """Convert PoB's `{ key = true, key = true }` set pattern to a list of keys."""
    if not isinstance(value, dict):
        return value
    return [k for k, v in value.items() if v]
