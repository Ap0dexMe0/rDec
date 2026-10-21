# rDec - RYL Decompiler

An interactive prompt menu decompiles every `.mcf` / `.gsf` / `.ncf` script asset for a selected RYL game version - no command-line arguments needed.

## Features

- Interactive prompt menu - pick a version with a number, confirm, done
- Single-key decompile per game version (`ROW`, `RYL1`, `RYL2`, …)
- Automatic version discovery - a new version is just a new folder under `script/`, no code changes. A folder holding nothing but version folders (e.g. `script/RYL2` with its era builds) is treated as a group and each sub-folder is offered as its own version
- Recursive file discovery with relative paths preserved
- `.mcf` handler: NPC scripts, quests, and world scripts to readable RYL script text
- `.gsf` handler: items, monsters, skills, chemical recipes, abuse filter, monster chat, and Lua bytecode (`SkillScriptEX`)
- Every output is `.txt`-only with the rDec banner on top - input binaries are only ever read, never overwritten
- Debug mode via `RDEC_LOG_LEVEL=DEBUG`

## Usage

Run rDec and pick from the prompt menu:

```bash
python main.py
```

| Option | Meaning |
|---|---|
| `1` Decompile a game version | Pick a version folder under `script/`, then confirm to decompile every supported file inside |
| `2` List supported versions | Show the detected version folders |
| `0` Exit | Close rDec |

Flow when decompiling: rDec scans the selected folder first and reports how many `.mcf`/`.gsf`/`.ncf` files it found, asks `Decompile all supported files? [Y/n]`, then writes each output as `.txt` next to the input.

## Requirements & Installation

- Python 3.8+
- Java runtime for Lua bytecode (`SkillScriptEX.gsf`) only

```bash
python -m venv venv
pip install -r requirements.txt

```
## Current Testing

- ROW
- RYL1
- RYL2 (V1700-V2240 build):

### Supported version folders

| Version ID | Folder | State |
|---|---|---|
| `ROW` | `script/ROW` | Original ROW - decompiles |
| `RYL1` | `script/RYL1` | decompiles (4 GSF + 2 MCF); `SpeacialCompensation.gsf` needs crypt page `(3, 4)` |
| `RYL2 V1700-V1900` | `script/RYL2/V1700-V1900` | decompiles |
| `RYL2 V2000-V2240` | `script/RYL2/V2000-V2240` | 9/10 files; `SpeacialCompensation.gsf` needs crypt page `(3, 4)` from the V2000+
