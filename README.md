# rDec - RYL Decompiler

An interactive prompt menu decompiles every `.mcf` / `.gsf` / `.ncf` script asset for a selected RYL game version - no command-line arguments needed.

## Features

- Interactive prompt menu - pick a game, pick a version, confirm, done
- Single-key decompile per game version (`ROW/Origin`, `ROW/Other`, `RYL1`, `RYL2/…`)
- Automatic version discovery - a new version sub-folder under `script/ROW` or `script/RYL2` shows up in that game's submenu automatically, no code changes. A folder holding nothing but version folders (e.g. `script/RYL2` with its era builds) is treated as a group and each sub-folder is offered as its own version
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
| `1` Return of Warriors (ROW) | Pick `Original ROW (Rowplayon)` or `Other ROW Versions`, then confirm to decompile every supported file inside |
| `2` Risk Your Life 1 (RYL1) | Decompiles directly - RYL1 has no sub-versions |
| `3` Risk Your Life 2 (RYL2) | Pick `V1700–V1900` or `V2000–V2240`, then confirm to decompile every supported file inside |
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

https://github.com/user-attachments/assets/98864fa3-6d12-48df-a4c2-7473397f825f

### Supported version folders

| Version ID | Folder | State |
|---|---|---|
| `ROW/Origin` | `script/ROW/Origin` | Original ROW - decompiles |
| `ROW/Other` | `script/ROW/Other` | Other ROW builds - decompiles (9/9 files; item rows are 616 bytes without the trailer, `.mcf` op scripts use MCF key `0xE2E5DCE7`) |
| `RYL1` | `script/RYL1` | decompiles (4 GSF + 2 MCF); `SpeacialCompensation.gsf` needs crypt page `(3, 4)` |
| `RYL2 V1700-V1900` | `script/RYL2/V1700-V1900` | decompiles |
| `RYL2 V2000-V2240` | `script/RYL2/V2000-V2240` | 9/10 files; `SpeacialCompensation.gsf` needs crypt page `(3, 4)` from the V2000+
