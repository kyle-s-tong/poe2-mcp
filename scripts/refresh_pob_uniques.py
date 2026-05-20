#!/usr/bin/env python3
"""
Refresh data/pob_uniques.json from PathOfBuilding-PoE2.

PoB stores uniques as heredoc-style text blocks ([[ ... ]]) rather than Lua
tables, so this parser is text-oriented rather than slpp-based.

Each block has:
    Line 1: unique name
    Line 2: base item type
    Optional metadata: Variant:, League:, Source:, Implicits:, Limited to:,
                       Has Alt Variant:, Requires Level
    Remaining lines: stat lines, optionally prefixed with {variant:N,M} or
                     {tags:foo,bar}

Run when PoE2 patches.
"""

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _pob_lua import REPO, BRANCH, fetch_lua

UNIQUE_FILES = [
    "amulet.lua", "axe.lua", "belt.lua", "body.lua", "boots.lua", "bow.lua",
    "claw.lua", "crossbow.lua", "dagger.lua", "fishing.lua", "flail.lua",
    "flask.lua", "focus.lua", "gloves.lua", "helmet.lua", "incursionlimb.lua",
    "jewel.lua", "mace.lua", "quiver.lua", "ring.lua", "sceptre.lua",
    "shield.lua", "soulcore.lua", "spear.lua", "staff.lua", "sword.lua",
    "talisman.lua", "tincture.lua", "traptool.lua", "wand.lua",
]

# Uniques defined in Special/Generated.lua. Each one's variants/stats are
# produced at PoB runtime by combining mod templates with passive-tree or
# mod data, so we can't statically extract their stats — but we record their
# existence so consumers know they exist.
PROGRAMMATIC_UNIQUES = [
    {"name": "Against the Darkness", "base": "Time-Lost Diamond",
     "slot": "jewel", "source": "Drops from unique{Zarokh, the Temporal}",
     "note": "Variants are generated per UniqueJewelRadius* mod."},
    {"name": "From Nothing", "base": "Diamond",
     "slot": "jewel", "source": "Drops from unique{The King in the Mists} in normal{Crux of Nothingness}",
     "note": "Variants are generated per keystone."},
    {"name": "Prism of Belief", "base": "Diamond",
     "slot": "jewel", "source": "Drops from unique{Arbiter of Ash} in normal{The Burning Monolith}",
     "note": "Variants are generated per skill gem."},
    {"name": "Megalomaniac", "base": "Diamond",
     "slot": "jewel", "source": "Drops from unique{Kosis, The Revelation}",
     "note": "Variants are generated per notable passive."},
    {"name": "Grip of Kulemak", "base": "Abyssal Signet",
     "slot": "ring", "league": "Rise of the Abyssal",
     "note": "Variants are generated per PassageUnique* mod."},
    {"name": "Heart of the Well", "base": "Diamond",
     "slot": "jewel", "league": "Rise of the Abyssal",
     "note": "Variants are generated per UniqueHeart* veiled mod."},
]

OUT_FILE = Path(__file__).resolve().parent.parent / "data" / "pob_uniques.json"

BLOCK_RE = re.compile(r"\[\[\s*\n(.*?)\n\s*\]\]", re.DOTALL)
PREFIX_RE = re.compile(r"^(\{[^}]+\})+")

METADATA_KEYS = {
    "Variant": "variants",          # multiple Variant: lines accumulate
    "League": "league",
    "Source": "source",
    "Implicits": "implicits_count",
    "Limited to": "limited_to",
    "Has Alt Variant": "has_alt_variant",
    "Requires Level": "requires_level",
    "Implicits Visible": "implicits_visible",
    "LevelReq": "level_req",
}


def parse_stat_line(line: str) -> dict:
    """Pull {variant:...} / {tags:...} prefixes off a stat line."""
    variants: list = []
    tags: list = []
    while True:
        m = re.match(r"\{([^}]+)\}", line)
        if not m:
            break
        body = m.group(1)
        if ":" in body:
            key, val = body.split(":", 1)
            vals = [v.strip() for v in val.split(",")]
            if key == "variant":
                variants.extend(int(v) for v in vals if v.isdigit())
            elif key == "tags":
                tags.extend(vals)
        line = line[m.end():]
    return {"text": line.strip(), "variants": variants, "tags": tags}


def parse_block(block: str, slot: str) -> dict | None:
    lines = [ln.rstrip() for ln in block.split("\n") if ln.strip()]
    if len(lines) < 2:
        return None

    unique: dict = {
        "name": lines[0].strip(),
        "base": lines[1].strip(),
        "slot": slot,
        "variants": [],
        "stats": [],
    }

    for line in lines[2:]:
        matched = False
        for key, out_key in METADATA_KEYS.items():
            if line.startswith(f"{key}:"):
                value = line[len(key) + 1:].strip()
                if out_key == "variants":
                    unique["variants"].append(value)
                elif out_key in ("implicits_count", "implicits_visible", "requires_level", "level_req"):
                    try:
                        unique[out_key] = int(value)
                    except ValueError:
                        unique[out_key] = value
                else:
                    unique[out_key] = value
                matched = True
                break
        if not matched:
            unique["stats"].append(parse_stat_line(line))

    return unique


def main():
    all_uniques: list = []
    by_slot: dict = {}

    for fn in UNIQUE_FILES:
        slot = fn.rsplit(".", 1)[0]
        print(f"Fetching {fn}...", file=sys.stderr)
        text = fetch_lua(fn, "Uniques")
        count = 0
        for m in BLOCK_RE.finditer(text):
            parsed = parse_block(m.group(1), slot)
            if parsed:
                all_uniques.append(parsed)
                count += 1
        by_slot[slot] = count
        print(f"  parsed {count} uniques", file=sys.stderr)

    for stub in PROGRAMMATIC_UNIQUES:
        entry = {
            "name": stub["name"],
            "base": stub["base"],
            "slot": stub["slot"],
            "variants": [],
            "stats": [],
            "programmatic": True,
            "programmatic_note": stub["note"],
        }
        if "source" in stub:
            entry["source"] = stub["source"]
        if "league" in stub:
            entry["league"] = stub["league"]
        all_uniques.append(entry)
        by_slot[stub["slot"]] = by_slot.get(stub["slot"], 0) + 1
    print(f"Added {len(PROGRAMMATIC_UNIQUES)} programmatic-unique stubs from Special/Generated.lua",
          file=sys.stderr)

    payload = {
        "metadata": {
            "source": f"{REPO}@{BRANCH}",
            "extraction_date": datetime.now(timezone.utc).isoformat(),
            "total_uniques": len(all_uniques),
            "programmatic_uniques": len(PROGRAMMATIC_UNIQUES),
            "by_slot": by_slot,
        },
        "uniques": all_uniques,
    }

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    print(f"\nWrote {len(all_uniques)} uniques to {OUT_FILE}", file=sys.stderr)


if __name__ == "__main__":
    main()
