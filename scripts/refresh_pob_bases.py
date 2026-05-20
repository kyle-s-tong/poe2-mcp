#!/usr/bin/env python3
"""
Refresh data/complete_models/base_items.json from PathOfBuilding-PoE2.

Pulls every Bases/*.lua file from upstream PoB, parses the itemBases tables,
and writes a base_items.json that FreshDataProvider can load. Re-run when
PoE2 patches.

Usage:
    python scripts/refresh_pob_bases.py
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from slpp import slpp as lua

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _pob_lua import REPO, BRANCH, fetch_lua, preprocess, find_blocks, set_table_to_list

BASE_FILES = [
    "amulet.lua", "axe.lua", "belt.lua", "body.lua", "boots.lua", "bow.lua",
    "claw.lua", "crossbow.lua", "dagger.lua", "fishing.lua", "flail.lua",
    "flask.lua", "focus.lua", "gloves.lua", "helmet.lua", "incursionlimb.lua",
    "jewel.lua", "mace.lua", "quiver.lua", "ring.lua", "sceptre.lua",
    "shield.lua", "soulcore.lua", "spear.lua", "staff.lua", "sword.lua",
    "talisman.lua", "traptool.lua", "wand.lua",
]
OUT_FILE = (Path(__file__).resolve().parent.parent
            / "data" / "complete_models" / "base_items.json")


def normalize_base(item_id: str, raw: dict, slot: str) -> dict:
    """Flatten PoB base item table to the shape FreshDataProvider expects."""
    out = {
        "id": item_id,
        "name": item_id,
        "slot": slot,
        "type": raw.get("type"),
    }
    for k, v in raw.items():
        if k == "tags":
            out["tags"] = set_table_to_list(v)
        elif k == "implicitModTypes":
            out["implicit_mod_types"] = [list(row.values()) if isinstance(row, dict) else row
                                         for row in (v.values() if isinstance(v, dict) else v)]
        else:
            out[k] = v
    return out


def main():
    all_items: dict = {}
    parse_failures: list = []

    for fn in BASE_FILES:
        slot = fn.rsplit(".", 1)[0]
        print(f"Fetching {fn}...", file=sys.stderr)
        text = preprocess(fetch_lua(fn, "Bases"))
        count = 0
        for item_id, block in find_blocks(text, "itemBases"):
            try:
                parsed = lua.decode(block)
            except Exception as e:
                parse_failures.append((item_id, str(e)[:80]))
                continue
            if not isinstance(parsed, dict):
                continue
            all_items[item_id] = normalize_base(item_id, parsed, slot)
            count += 1
        print(f"  parsed {count} items", file=sys.stderr)

    if parse_failures:
        print(f"\n{len(parse_failures)} items failed to parse (sample):", file=sys.stderr)
        for iid, err in parse_failures[:5]:
            print(f"  {iid}: {err}", file=sys.stderr)

    payload = {
        "metadata": {
            "source": f"{REPO}@{BRANCH}",
            "extraction_date": datetime.now(timezone.utc).isoformat(),
            "total_items": len(all_items),
            "parse_failures": len(parse_failures),
        },
        "base_items": all_items,
    }

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    print(f"\nWrote {len(all_items)} base items to {OUT_FILE}", file=sys.stderr)


if __name__ == "__main__":
    main()
