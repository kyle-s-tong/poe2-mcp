# Path of Exile 2 Build Optimizer MCP

[![PyPI version](https://badge.fury.io/py/poe2-mcp.svg)](https://pypi.org/project/poe2-mcp/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Community Project Disclaimer**
>
> This is an independent, fan-made community project built out of love for Path of Exile 2. It is **not affiliated with, endorsed by, or officially connected to Grinding Gear Games** in any way. Path of Exile is a trademark of Grinding Gear Games. All game data and assets remain the property of their respective owners.

A Model Context Protocol (MCP) server for Path of Exile 2 character analysis and optimization. Provides 34 MCP tools for AI-powered build analysis, passive tree analysis, item mod validation, support gem validation, unique item lookups, and Path of Building integration.

## What is This?

This is an **MCP server** - a backend service that gives AI assistants (like Claude, ChatGPT, Cursor, etc.) the ability to analyze your Path of Exile 2 characters and provide optimization recommendations.

**What it does:**
- Fetches your character data from poe.ninja
- Analyzes defensive stats, skills, gear, and passive tree
- Validates support gem combinations (prevents invalid recommendations)
- Inspects spell, support gem, base item, and unique item data (sourced from Path of Building)
- Imports/exports Path of Building codes
- Compares your build to top ladder players
- Explains PoE2 game mechanics

**What you need:**
- An AI assistant that supports MCP (Claude Desktop, ChatGPT Desktop, Cursor, Windsurf, etc.)
- Python 3.9+ installed
- Your PoE2 character on poe.ninja (public profile)

## Quick Start

### 1. Install

**Option A: PyPI (Recommended)**
```bash
pip install poe2-mcp
```

**Option B: From Source**
```bash
git clone https://github.com/HivemindOverlord/poe2-mcp.git
cd poe2-mcp
pip install -e .
```

### 2. Connect to Your AI Assistant

Choose your platform below:

---

## Claude Desktop Integration

### Option A: Manual Configuration (Recommended for Development)

Edit your Claude Desktop config file:
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

Add this server (replace the path with your actual installation path):

**Windows:**
```json
{
  "mcpServers": {
    "poe2-optimizer": {
      "command": "python",
      "args": ["C:\\Users\\YourName\\poe2-mcp\\launch.py"],
      "env": {}
    }
  }
}
```

**macOS/Linux:**
```json
{
  "mcpServers": {
    "poe2-optimizer": {
      "command": "python3",
      "args": ["/Users/YourName/poe2-mcp/launch.py"],
      "env": {}
    }
  }
}
```

Restart Claude Desktop. The server will appear in your MCP tools.

### Option B: Download .mcpb Bundle (One-Click Install)

Pre-built MCP bundles are available for one-click installation in Claude Desktop:

1. Download `poe2-mcp-1.0.0.mcpb` from the [GitHub Releases](https://github.com/HivemindOverlord/poe2-mcp/releases/latest)
2. In Claude Desktop: Settings > Extensions > Install Extension
3. Select the downloaded `.mcpb` file

**Note:** The bundle is ~109MB as it includes all game data files. Python 3.9+ must be installed on your system.

> **Recommendation:** For development or if you want automatic updates, use Option A (manual configuration) with `pip install poe2-mcp`.

---

## Other AI Platforms

MCP is an open standard supported by multiple AI platforms:

### OpenAI ChatGPT Desktop
ChatGPT desktop app supports MCP servers. Configuration varies by version - check OpenAI's documentation for current setup instructions.

### Cursor AI
Cursor supports MCP via SSE protocol. Add to your Cursor settings:
```json
{
  "mcp": {
    "servers": {
      "poe2-optimizer": {
        "command": "python",
        "args": ["/path/to/poe2-mcp/launch.py"]
      }
    }
  }
}
```

### Windsurf
Windsurf has a built-in MCP Plugin Store. You can either:
- Search for "poe2" in the plugin store (if published)
- Manually add the server path in settings

### Claude Code (CLI)
```bash
# In your project directory
claude mcp add poe2-optimizer python /path/to/poe2-mcp/launch.py
```

### Other Compatible Clients
- Zed Editor
- Replit
- Codeium
- Sourcegraph
- Microsoft Semantic Kernel
- Salesforce Agentforce

Check each platform's documentation for MCP server configuration.

---

## Available Tools (34 Registered)

Once connected, you can ask your AI assistant to use these tools:

### Character Analysis
| Tool | Description |
|------|-------------|
| `analyze_character` | Full character analysis (defenses, skills, gear, passives) |
| `import_poe_ninja_url` | Import character from poe.ninja URL directly |
| `compare_to_top_players` | Compare your build to ladder leaders |
| `analyze_passive_tree` | Analyze allocated passive nodes |

### Validation & Inspection
| Tool | Description |
|------|-------------|
| `validate_support_combination` | Check if support gems work together |
| `validate_build_constraints` | Validate build against game rules |
| `inspect_support_gem` | View complete support gem data |
| `inspect_spell_gem` | View complete spell gem data |
| `list_all_supports` | List all available support gems |
| `list_all_spells` | List all available spell gems |

### Passive Tree Data
| Tool | Description |
|------|-------------|
| `list_all_keystones` | List all keystones with full stats |
| `inspect_keystone` | Get complete keystone details by name |
| `list_all_notables` | List all notable passives with stats |
| `inspect_passive_node` | Get details for any passive node |

### Base Item Data
| Tool | Description |
|------|-------------|
| `list_all_base_items` | List all base item types |
| `inspect_base_item` | Get details for a specific base item |

### Unique Items
| Tool | Description |
|------|-------------|
| `list_uniques` | List unique items with filters (slot, name substring, league) |
| `inspect_unique` | Get details for a unique by name; defaults to the Current variant |

### Item Mod Data
| Tool | Description |
|------|-------------|
| `inspect_mod` | Get complete details for a specific mod by ID |
| `list_all_mods` | List mods with filtering by type (PREFIX/SUFFIX/IMPLICIT) |
| `search_mods_by_stat` | Search for mods by keyword (e.g., "fire", "life") |
| `get_mod_tiers` | Show all tier variations of a mod family |
| `validate_item_mods` | Check if mods can legally exist together on an item |
| `get_available_mods` | List all mods available for a generation type |

### Path of Building
| Tool | Description |
|------|-------------|
| `import_pob` | Import Path of Building code |
| `export_pob` | Export build to PoB format |
| `get_pob_code` | Get PoB code for a character |

### Trade & Items
| Tool | Description |
|------|-------------|
| `search_items` | Search local item database |
| `search_trade_items` | Search official trade site (requires auth) |
| `setup_trade_auth` | Set up trade site authentication |

### Knowledge & Utility
| Tool | Description |
|------|-------------|
| `explain_mechanic` | Explain PoE2 game mechanics |
| `get_formula` | Get calculation formulas |
| `health_check` | Check server status |
| `clear_cache` | Clear cached data |

> **Note:** Additional tools (DPS calculator, EHP calculator, optimizers) have handlers implemented but are not yet registered. These may be enabled in future updates.

---

## Example Usage

Once configured, just talk to your AI naturally:

> "Analyze my character TomawarTheFourth from account Tomawar"

> "Import this poe.ninja URL: https://poe.ninja/poe2/builds/char/..."

> "Can I use Faster Projectiles and Slower Projectiles together?" (uses `validate_support_combination`)

> "Show me all support gems that work with projectiles" (uses `list_all_supports`)

> "What keystones are available for life builds?" (uses `list_all_keystones`)

> "Tell me about Chaos Inoculation" (uses `inspect_keystone`)

> "Compare my build to top Witchhunter players"

> "Explain how armor works in PoE2"

> "What prefixes can roll on items?" (uses `get_available_mods`)

> "Show me all tiers of the Strength mod" (uses `get_mod_tiers`)

> "Can Strength1 and Strength2 exist on the same item?" (uses `validate_item_mods`)

> "Search for fire resistance mods" (uses `search_mods_by_stat`)

> "Show me all unique amulets" (uses `list_uniques`)

> "What does Mjölner do in the current patch?" (uses `inspect_unique` — defaults to Current variant)

The AI will use the appropriate tools automatically.

---

## Trade API Authentication (Optional)

For `search_trade_items` to work, you need to authenticate with pathofexile.com:

```bash
pip install playwright
playwright install chromium
python scripts/setup_trade_auth.py
```

This opens a browser for you to log in, then saves your session cookie.

---

## Local Game Database

The server includes a local database with:
- 4,975+ passive tree nodes
- 335+ ascendancy nodes (99% coverage)
- 14,269 item modifiers (2,252 prefixes, 2,037 suffixes, 8,930 implicits)
- 1,249 skill gems (incl. spells and supports, with per-level stats from PoB)
- 1,122 base item types
- 388 unique items (382 statically defined + 6 programmatic from PoB)
- Support gem effects and interactions

Data is loaded from `data/` directory on startup. The skill, base, and unique data files are generated from upstream [Path of Building (PoE2)](https://github.com/PathOfBuildingCommunity/PathOfBuilding-PoE2) — see [Refreshing PoB Data](#refreshing-pob-data) for how to regenerate them when PoE2 patches.

---

## Architecture

```
poe2-mcp/
├── launch.py              # Entry point (MCP-stdio safe: chatter → stderr, JSON-RPC → stdout)
├── src/
│   ├── mcp_server.py      # Main MCP server (34 tools registered)
│   ├── api/               # External API clients
│   ├── analyzer/          # Analysis components
│   ├── calculator/        # Numeric calculations
│   ├── data/
│   │   ├── mod_data_provider.py
│   │   └── fresh_data_provider.py  # Loads complete_models/*.json (skills, supports, bases, tree, stats)
│   ├── optimizer/         # Optimization engines
│   ├── parsers/           # Datc64 binary parsers
│   ├── knowledge/         # Game mechanics knowledge base
│   └── database/          # SQLite database
├── data/
│   ├── complete_models/
│   │   ├── active_skills.json       # 6,454 skill IDs (incl. minions/monsters)
│   │   ├── support_gems.json
│   │   ├── passive_tree.json
│   │   ├── stats.json
│   │   └── base_items.json          # 1,122 bases (refreshed from PoB)
│   ├── pob_complete_skills.json     # 1,249 player skills with per-level stats (PoB)
│   ├── pob_uniques.json             # 388 uniques (PoB)
│   ├── poe2_mods_extracted.json     # → symlink to poe2_mods_corrected.json
│   ├── poe2_mods_corrected.json     # 14,269 item mods
│   └── psg_passive_nodes.json
├── scripts/
│   ├── refresh_pob_skills.py        # PoB Lua → data/pob_complete_skills.json
│   ├── refresh_pob_bases.py         # PoB Lua → data/complete_models/base_items.json
│   ├── refresh_pob_uniques.py       # PoB Lua → data/pob_uniques.json
│   └── _pob_lua.py                  # Shared fetch/parse helpers
└── tests/                  # Test suite
```

---

## Development

### Running Tests
```bash
pytest tests/ -v
```

### Running the Server Directly
```bash
# If installed via pip
poe2-mcp

# From source
python launch.py
```

### Refreshing PoB Data

Skill, base item, and unique item data is derived from upstream [PathOfBuilding-PoE2](https://github.com/PathOfBuildingCommunity/PathOfBuilding-PoE2). When PoE2 patches, regenerate the JSON snapshots:

```bash
pip install slpp                                 # Lua parser, used only by the refresh scripts
python scripts/refresh_pob_skills.py             # → data/pob_complete_skills.json (1,249 skills)
python scripts/refresh_pob_bases.py              # → data/complete_models/base_items.json (1,122 bases)
python scripts/refresh_pob_uniques.py            # → data/pob_uniques.json (388 uniques)
```

Each script pulls the relevant `src/Data/**/*.lua` files from the PoB `dev` branch over HTTPS and converts them into the JSON shape consumed by the MCP tools. No PoB checkout required.

### Key Files
- `src/mcp_server.py` - MCP server with 34 registered tools
- `src/data/fresh_data_provider.py` - Singleton loader for the `data/complete_models/` snapshot
- `src/data/mod_data_provider.py` - Item mod data access layer
- `src/calculator/ehp_calculator.py` - EHP calculations
- `src/optimizer/gem_synergy_calculator.py` - Support gem logic
- `data/psg_passive_nodes.json` - Passive tree database
- `data/poe2_mods_corrected.json` - Item modifier database (14,269 mods)

---

## Troubleshooting

### "Server not found" in Claude Desktop
- Check the path in config is absolute (not relative)
- Ensure Python is in your PATH
- Try running `python launch.py` manually to see errors

### "No character found"
- Your character must be on poe.ninja (public ladder)
- Character name is case-sensitive
- Try the full poe.ninja URL with `import_poe_ninja_url`

### Tools return empty results
- Database may need initialization: `python launch.py` handles this
- Check `data/` directory exists with JSON files
- If `inspect_spell_gem`, `inspect_base_item`, or `list_uniques` returns "not found" / empty, regenerate the PoB snapshots — see [Refreshing PoB Data](#refreshing-pob-data)

---

## Credits

Data sources:
- [poe.ninja](https://poe.ninja) - Character data and builds
- [Path of Building (PoE2)](https://github.com/PathOfBuildingCommunity/PathOfBuilding-PoE2) - Skill, base item, and unique item data (see [Refreshing PoB Data](#refreshing-pob-data))
- [Path of Grinding](https://pathofgrinding.com) - Passive tree data

MCP Protocol:
- [Model Context Protocol](https://modelcontextprotocol.io)
- [mcpb Bundle Format](https://github.com/modelcontextprotocol/mcpb)

---

## License

MIT License - See [LICENSE](LICENSE) for details.

This is a community project. Not affiliated with Grinding Gear Games.

---

**[Report Issues](https://github.com/HivemindOverlord/poe2-mcp/issues)**
