#!/usr/bin/env python3
"""
Refresh data/pob_complete_skills.json from PathOfBuilding-PoE2.

Downloads the Lua skill data files from upstream and converts them into the
JSON shape consumed by the spell gem MCP tools. Re-run when PoE2 patches.

Usage:
    python scripts/refresh_pob_skills.py            # all skills
    python scripts/refresh_pob_skills.py --player-only
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from slpp import slpp as lua

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _pob_lua import REPO, BRANCH, fetch_lua, preprocess, find_blocks, set_table_to_list

SKILL_FILES = [
    "act_str.lua", "act_dex.lua", "act_int.lua",
    "sup_str.lua", "sup_dex.lua", "sup_int.lua",
    "minion.lua", "spectre.lua", "other.lua",
]
OUT_FILE = Path(__file__).resolve().parent.parent / "data" / "pob_complete_skills.json"


def normalize_skill(skill: dict) -> dict:
    out: dict = {}
    for k, v in skill.items():
        if k in ("skillTypes", "weaponTypes", "tags"):
            out[k] = set_table_to_list(v)
        elif k == "levels" and isinstance(v, dict):
            out[k] = {str(lvl): data for lvl, data in v.items()}
        elif k == "statSets" and isinstance(v, dict):
            out[k] = {str(idx): _normalize_stat_set(data) for idx, data in v.items()}
        else:
            out[k] = v
    return out


def _normalize_stat_set(s):
    if not isinstance(s, dict):
        return s
    fixed = {}
    for k, v in s.items():
        if k == "baseFlags":
            fixed[k] = set_table_to_list(v)
        elif k == "levels" and isinstance(v, dict):
            fixed[k] = {str(lvl): data for lvl, data in v.items()}
        else:
            fixed[k] = v
    return fixed


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--player-only", action="store_true",
                    help="keep only skill IDs ending in 'Player'")
    args = ap.parse_args()

    all_skills: dict = {}
    parse_failures: list = []

    for fn in SKILL_FILES:
        print(f"Fetching {fn}...", file=sys.stderr)
        text = preprocess(fetch_lua(fn, "Skills"))
        count = 0
        for skill_id, block in find_blocks(text, "skills"):
            try:
                parsed = lua.decode(block)
            except Exception as e:
                parse_failures.append((skill_id, str(e)[:80]))
                continue
            if not isinstance(parsed, dict):
                continue
            all_skills[skill_id] = normalize_skill(parsed)
            count += 1
        print(f"  parsed {count} skills", file=sys.stderr)

    if args.player_only:
        before = len(all_skills)
        all_skills = {k: v for k, v in all_skills.items() if k.endswith("Player")}
        print(f"Filtered to player-only: {before} -> {len(all_skills)}", file=sys.stderr)

    if parse_failures:
        print(f"\n{len(parse_failures)} skills failed to parse (sample):", file=sys.stderr)
        for sid, err in parse_failures[:5]:
            print(f"  {sid}: {err}", file=sys.stderr)

    payload = {
        "metadata": {
            "source": f"{REPO}@{BRANCH}",
            "extraction_date": datetime.now(timezone.utc).isoformat(),
            "total_skills": len(all_skills),
            "parse_failures": len(parse_failures),
        },
        "skills": all_skills,
    }

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    print(f"\nWrote {len(all_skills)} skills to {OUT_FILE}", file=sys.stderr)


if __name__ == "__main__":
    main()
