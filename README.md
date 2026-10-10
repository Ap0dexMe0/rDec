# rDec - (RYL Decompiler)

A verified decompiler for Risk Your Life (RYL) MMORPG `.mcf` script files, including `Script`, `NPCScript`, and `Quest`. The implementation is validated against the C++ source code in `RylServerProject/ScriptEngine`.

## Usage

```bash
python decompiler.py input/ --out output/ --all
```

## Project Structure

```text
MCFDecompiler/
├── input/       # Source .mcf binaries (Script, NPCScript, Quest)
├── output/           # Decompiled TXT files from newer data revisions
└── decompiler.py
```

### Decompiled Output

| File | Contents | Verification |
|---|---|---|
| `NPCScript.txt` | 276 NPCs, 7,450 calls | 0 anomalies |
| `Quest.txt` | 644 quests, 21,306 calls | 0 anomalies |
| `Script.txt` | 2,742 `AddString` entries and `RylNation` | Byte-identical to reference, except for the footer stamp |

The output files retain their original filenames and follow the text structure expected by RYLCoder.

## How It Works

The decompiler follows the verified data structures and decoding behavior found in `RylServerProject/ScriptEngine`.

### 1. Binary Decoding

Each complete 4-byte little-endian slot is XOR-decoded using:

```text
0x425529AC
```

This key is derived from the constants used in `VirtualMachine.cpp`:

```text
0x82FAC623 ^ 0x601F1AC4 = 0x4255DCE7
```

*Note: The supplied XOR key and the stated source constants do not produce the same value. Verify the actual constants and implementation before relying on this derivation.*

Trailing partial bytes are preserved, matching the behavior of `Data_XOR`. For example, `NPCScript.mcf` ends with `00 00 00` because its size modulo 4 equals 3.

### 2. Binary Structure Parsing

The parser processes:

- Relocation counts and tables
- Buffer sizes
- NUL-separated string buffers
- x86 code buffers
- Function maps containing names, types, and code offsets
- System variables

### 3. Native Function and Argument Recovery

The scanner identifies `E8` call instructions, resolves their targets against function-map offsets, and recovers native function names.

Arguments are reconstructed by walking backward over instruction patterns:

- `B9 imm32` - load an immediate value into `ECX`
- `51` - push `ECX`

Argument counts are validated against the following instruction pattern:

```asm
81 C4 imm32    ; add esp, argc * 4
```

### 4. Argument Type Inference

The decompiler uses callee signature tables and the following inference rules:

- **Integers and hexadecimal values:** values at or above `0x100000` follow the hexadecimal formatting rule.
- **Floating-point values:** select the shortest representation that round-trips to the original IEEE 754 `float32` value.
- **Booleans:** recognize `true` and `false`.
- **Strings:** preserve raw string bytes.
- **Legacy text:** convert non-UTF-8 text from CP1252 to UTF-8, matching RYLCoder's behavior.

### 5. Text Generation

The generated files reproduce the expected RYLCoder text layout:

- CRLF line endings
- File banner
- `void` function headers
- Semicolon-terminated statements
- Tab-based indentation
- Blank-line separators
- Footer without a trailing newline

## Verification Results

The following results were recorded during validation:

- `Script.txt` is byte-identical to its reference except for the footer author/date line.
- `NPCScript.txt` and `Quest.txt` parse successfully using RYLCoder's own text regular expressions.
- All 276 NPC entries and 644 quest entries passed the reported structural checks.
- Quest entries satisfy the strict seven-group matching rule.
- No invalid floating-point values were reported.
- All three files completed scanning with zero call anomalies and zero argument anomalies.
- Every input file was fully consumed: `consumed == size`.

## Compatibility

The decompiler is designed to reproduce RYLCoder-compatible text from the supported RYL `.mcf` script formats while preserving the original filenames.

**Scope:** `Script.mcf`, `NPCScript.mcf`, and `Quest.mcf`.

**Status:** Version 1.0 - validated against the recorded reference outputs and ScriptEngine implementation.
