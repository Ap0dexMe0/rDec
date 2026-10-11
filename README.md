# rDec - RYL Decompiler

One command decompiles every `.mcf` / `.gsf` script asset for a selected RYL game version.

## Features

- Single-command decompile per game version (`ROW`, `RYL1`, `RYL2`, …)
- Automatic version discovery - a new version is just a new folder under `script/`, no code changes
- Recursive file discovery with relative paths preserved
- `.mcf` handler: NPC scripts, quests, and world scripts to readable RYL script text
- `.gsf` handler: items, monsters, skills, chemical recipes, abuse filter, monster chat, and Lua bytecode (`SkillScriptEX`)
- Every output is `.txt`-only with the rDec banner on top - input binaries are only ever read, never overwritten
- Debug mode via `RDEC_LOG_LEVEL=DEBUG`

## Usage

```bash
python main.py -l
python main.py -v ROW -d
```

| Argument | Meaning |
|---|---|
| `-l`, `--list` | Print supported versions |
| `-v`, `--version` | Game version folder under `script/` (required with `-d`) |
| `-d`, `--decompile` | Decompile everything found |
| `-h`, `--help` | Show help and exit |

| Version | Label |
|---|---|
| `RYL2` | RYL2 V1600+ |
| `ROW` | Original ROW |

## Requirements & Installation

- Python 3.8+
- Java runtime for Lua bytecode (`SkillScriptEX.gsf`) only

```bash
python -m venv venv
pip install -r requirements.txt

```
## Demo
### Current Testing

- RYL2 (V1600+)

https://github.com/user-attachments/assets/a3564af6-7405-41b3-93f7-aa8b5170821b

- Origin ROW

https://github.com/user-attachments/assets/9f93b2f0-4bb1-4729-a714-7363e54a8bcf

### TODO
- Implement for another version