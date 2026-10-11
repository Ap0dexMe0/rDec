# rDec — RYL Decompiler

One command decompiles every `.mcf` / `.gsf` script asset for a selected RYL game version.

## Features

- Single-command decompile per game version (`ROW`, `RYL1`, `RYL2`, …)
- Automatic version discovery — a new version is just a new folder under `script/`, no code changes
- Recursive file discovery with relative paths preserved
- `.mcf` handler: NPC scripts, quests, and world scripts to readable RYL script text
- `.gsf` handler: items, monsters, skills, chemical recipes, abuse filter, monster chat, and Lua bytecode (`SkillScriptEX`)
- Every output is `.txt`-only with the rDec banner on top — input binaries are only ever read, never overwritten
- Pretty colored logging with plain-English messages and a final summary (`decompiled / skipped / untouched / failed`)
- Debug mode via `RDEC_LOG_LEVEL=DEBUG`
- One file failing never stops the rest, and unsupported files (e.g. `.ncf`) are reported, not guessed
- stdlib-only test suite

## Usage

```bash
python main.py --version RYL2 -d
```

| Argument | Meaning |
|---|---|
| `--version` | Game version folder under `script/` |
| `-d`, `--decompile` | Decompile everything found (without it, just lists files) |

## Requirements

- Python 3.8+
- `pip install lzo coloredlogs` (colored logs + `.gsf` support; both already in `venv/`)
- Java runtime for Lua bytecode (`SkillScriptEX.gsf`) only

## Tests

```bash
python -m unittest discover -s tests
```
