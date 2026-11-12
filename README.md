# rDec - RYL Decompiler

rDec is an interactive tool for decompiling game script files from different Risk Your Life (RYL) versions. Simply select a game, choose a version, and let rDec handle the rest.

## Features

- **Interactive Menu** - Select a game and version directly from the menu.
- **Directory Settings** - Configure and save your server-side and client-side directories.
- **Multiple Game Support** - Supports ROW, RYL1, and RYL2.
- **Automatic Version Detection** - Automatically detects available game versions.
- **Batch Decompilation** - Decompile all supported files in one operation.
- **Multiple File Support** - Supports `.mcf`, `.gsf`, and `.ncf` files.
- **Organized Output** - Decompiled files are saved as `.txt` files inside the `decompiled/` folder.
- **Language Support** - Supports Korean, Traditional Chinese, and Simplified Chinese text.
- **Compiler (TXT → GSF/MCF)** - Rebuild game script files from edited text files (RYL2 only).
- **Separate Workspace** - Keeps original game files and decompiled text files organized separately.
- **Original File Protection** - Original files are never modified during decompilation.

## Requirements & Installation

**Requirements:**
- Python 3.8 or newer
- Java Runtime (required only for Lua bytecode support)

**Installation:**

```bash
python -m venv venv
pip install -r requirements.txt
```

## Usage

Start rDec using:

```bash
python main.py
```

Select an option from the main menu:

| Option | Description |
|---|---|
| `1` Decompile | Select a game and version to decompile its script files. |
| `2` Compile | Rebuild script files from edited `.txt` files (RYL2 only). |
| `3` Directory Settings | Configure your server-side and client-side directories. |
| `0` Exit | Close rDec. |

### Directory Settings

Configure your server-side and client-side directories through the settings menu.

Your settings are saved automatically in `config.ini` and can be changed whenever needed.

## Workspace Structure

Each game version uses two separate folders:

| Folder | Description |
|---|---|
| `compiled/` | Original game script files. |
| `decompiled/` | Decompiled `.txt` files and editable scripts. |

**Decompilation:** Reads files from `compiled/` and saves the results in `decompiled/`.

**Compilation:** Reads edited `.txt` files from `decompiled/` and generates game files in `compiled/`.

## Compiler (RYL2 Only)

The compiler allows you to rebuild game script files after making changes to the decompiled text files.

Supported file types include:

- NPC scripts
- Quest scripts
- World scripts
- Item scripts
- Monster data
- Skill scripts
- Chemical recipes
- Abuse filter
- Monster chat
- Mineral vein data
- Special compensation data

**Note:** Keep a backup of your original files before compiling. Newly generated files may replace existing files in the `compiled/` folder.

## Supported Versions

| Game / Version | Directory | Status |
|---|---|---|
| ROW / Origin | `script/ROW/Origin` | Decompiled Only |
| ROW / Other | `script/ROW/Other` | Supported |
| RYL1 | `script/RYL1` | Supported |
| RYL2 V1700-V1900 | `script/RYL2/V1700-V1900` | Supported |
| RYL2 V2000-V2240 | `script/RYL2/V2000-V2240` | Supported |

### Preview

[View rDec in action](https://github.com/user-attachments/assets/98864fa3-6d12-48df-a4c2-7473397f825f)
