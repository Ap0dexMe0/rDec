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

- RYL2 (V1700-V1900 build):

https://github.com/user-attachments/assets/a3564af6-7405-41b3-93f7-aa8b5170821b

- Origin ROW:

https://github.com/user-attachments/assets/9f93b2f0-4bb1-4729-a714-7363e54a8bcf

### Supported version folders

| Version ID | Folder | State |
|---|---|---|
| `ROW` | `script/ROW` | Original ROW - decompiles |
| `RYL1` | `script/RYL1` | decompiles (4 GSF + 2 MCF); `SpeacialCompensation.gsf` needs crypt page `(3, 4)` |
| `RYL2 V1700-V1900` | `script/RYL2/V1700-V1900` | decompiles |
| `RYL2 V2000-V2240` | `script/RYL2/V2000-V2240` | 9/10 files; `SpeacialCompensation.gsf` needs crypt page `(3, 4)` from the V2000+ `XORCryptoCodeList` (decoder is ready, waits for the page) |

### RYL1 notes

The RYL1 folder is reverse engineered from the game's own server sources
(`RebalanceConvert/OldItemStructure.h`, `OldItemDataParser.cpp`, `OldItemMgr.cpp`)
and, for monsters, cross-checked against AlphA's authentic RYL1
`MonsterProtoType.txt` dump (`example/MonsterProtoType.txt` in the folder):
- `ItemScript.gsf` - 644-byte `OldItem::ItemInfo` records (`pragma pack(8)`),
  emitted in the authentic 66-column parser layout (31 default + 33 equip
  attribute columns + `MaterialValue` `MaxSocketNum`, no `Describe` column).
  Use-item rows carry the skill ID as `0x…` hex under `CriticalType` and the
  item description under `DefenceRevision`; ETC rows carry the description
  under `CriticalType`; untouched columns stay empty so `atoi("") == 0`.
- `MonsterProtoType.gsf` - 368-byte records (`u32` ID at `+0x0B4`), output
  mirrors the authentic dump's 97-column plan (Name/Model `char[32]`,
  Nation byte `+0xC8`, MonsterClass byte `+0xC4`, HP/MP/regs at `+0x154`
  onwards, spawn time `+0x0B8`); a few columns only exist in later builds and
  stay `0`.
- `Chemical.gsf`, `MonsterChat.gsf` (plaintext pass-through), plus the two
  `.mcf` scripts (npcscript, quest) decompile as in the other versions.
- `gsfStruct.xml` is AlphA's editor configuration that stays in the folder -
  it documents the era's cell sizes (ItemScript 1600=608/1700=616,
  MonsterProtoType 1600=548/1700=552) and is only a field-order reference; the
  actual RYL1 binaries differ (644-byte items, 368-byte monsters).

### TODO
- Implement for another version
