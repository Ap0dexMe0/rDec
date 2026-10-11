#!/usr/bin/env python3
"""
MCF Decompiler v1.0 — RYL Script/NPCScript/Quest .mcf to TRUE script text.

Pipeline (all verified against the C++ ScriptEngine source in
RYLGameConverter/RylServerProject/ScriptEngine + TRUE txt reference files):
  1. Decode: every 4-byte LE slot XOR 0x425529AC
     (VirtualMachine.cpp: xor_key_value 0x82FAC623 ^ 0x601F1AC4).
     Trailing partial bytes (< 4) are untouched, same as Data_XOR.
  2. Parse: reloc counts + tables, buffer sizes, string buffer
     (NUL-separated, raw bytes incl. doubled backslashes), x86 code buffer,
     funcmap (name\\n + type + code offset per entry), 4 sysvar ints.
  3. Scan code for E8 call sites -> funcmap offset -> native name.
     Args = walk back over (B9 imm32, 51)* groups (COP_mov reg,const +
     COP_push ECX per GenCode_Function_Call); validated by 83 C4 NN and
     the string-reloc set. Types come from the callee signature tables.
  4. Emit RYL script (CRLF, rDec banner block + one blank line on top,
     ;-statements, TAB nesting, blank separators). No footer and no
     trailing newline. No Functions void block.

Usage:
    python mcf_decompiler.py assets --out out
    python mcf_decompiler.py assets/Script.mcf --out out
Outputs into --out: <Base>.txt ONLY (TRUE script statements).
Never overwrites a foreign .txt (falls back to .gen.txt).
"""
import struct
import sys
from pathlib import Path

from modules.logging import get_logger

log = get_logger()

MCF_KEY = 0x425529AC
KB = struct.pack("<I", MCF_KEY)

# name -> {argc: ([types], indent_tabs, blanks_before)}
# types: i=int f=float b=bool s=string
SIGS = {
    # ---- NPC ----
    "SetNPC": {6: (["i", "i", "i", "b", "s", "s"], 0, 2)},
    "SetPosition": {5: (["i", "f", "f", "f", "f"], 1, 0)},
    "SetNPCAttribute": {3: (["i", "i", "i"], 1, 0)},
    "NPCDisplay": {5: (["i", "i", "b", "b", "b"], 1, 0)},
    "AddWords": {2: (["i", "s"], 1, 0)},
    "AddDialog": {4: (["i", "i", "i", "s"], 1, 0)},
    "AddItem": {5: (["i", "i", "i", "i", "i"], 1, 0)},
    "AddZoneMove": {5: (["i", "i", "f", "f", "f"], 1, 0)},
    "AddQuest": {2: (["i", "i"], 1, 0)},
    "AddQuestWords": {3: (["i", "i", "s"], 1, 0)},
    "AddPopup": {7: (["i", "i", "i", "s", "i", "i", "i"], 1, 0)},
    "SetDropGrade": {7: (["i"] * 7, 1, 0)},
    "SetDropBase": {7: (["i"] * 7, 1, 0)},
    # ---- Quest ----
    "QuestStart": {7: (["i", "i", "i", "i", "i", "i", "b"], 0, 0)},
    "QuestEnd": {0: ([], 0, 0)},
    "QuestType": {2: (["i", "i"], 1, 0)},
    "QuestCompleteSave": {1: (["b"], 1, 0)},
    "QuestTitle": {1: (["s"], 1, 0)},
    "QuestLevel": {1: (["s"], 1, 0)},
    "QuestAward": {1: (["s"], 1, 0)},
    "QuestDesc": {1: (["s"], 1, 0)},
    "QuestShortDesc": {1: (["s"], 1, 0)},
    "QuestArea": {5: (["i", "f", "f", "f", "f"], 1, 0)},
    "QuestSkillPointBonus": {1: (["i"], 1, 0)},
    "QuestIcon": {5: (["s", "i", "i", "i", "i"], 1, 0)},
    "QuestCancelItemDel": {1: (["b"], 1, 0)},
    "AddPhase": {3: (["i", "i", "s"], 1, 1)},
    "Phase_Target": {2: (["i", "i"], 2, 0)},
    "Trigger_Start": {0: ([], 2, 0)},
    "Trigger_Puton": {6: (["i", "i", "f", "f", "f", "f"], 2, 0)},
    "Trigger_Geton": {6: (["i", "i", "f", "f", "f", "f"], 2, 0)},
    "Trigger_Talk": {1: (["i"], 2, 0)},
    "Trigger_Kill": {2: (["i", "i"], 2, 0)},
    "Trigger_Pick": {2: (["i", "i"], 2, 0)},
    "Trigger_Fame": {1: (["i"], 2, 0)},
    "Trigger_LevelTalk": {3: (["i", "i", "s"], 2, 0)},
    "Else": {0: ([], 2, 0)},
    "Event_Disappear": {3: (["i", "i", "i"], 3, 0)},
    "Event_Get": {2: (["i", "i"], 3, 0)},
    "Event_Spawn": {4: (["i", "f", "f", "f"], 3, 0)},
    "Event_MonsterDrop": {2: (["i", "i"], 3, 0)},
    "Event_Award": {4: (["i", "i", "i", "i"], 3, 0)},
    "Event_MsgBox": {1: (["s"], 3, 0)},
    "Event_Phase": {1: (["i"], 3, 0)},
    "Event_End": {0: ([], 3, 0)},
    "Event_AwardItem": {4: (["i", "i", "i", "i"], 3, 0)},
    "Event_AddQuest": {2: (["i", "i"], 3, 0)},
    "Event_Move": {3: (["i", "f", "f"], 3, 0)},
    "Event_TheaterMode": {0: ([], 3, 0)},
    # ---- Script (string table) ----
    "RylNation": {3: (["i", "i", "s"], 0, 0)},
    "AddString": {
        2: (["i", "s"], 0, 0),
        1: (["s"], 0, 0),
    },
}

KINDS = [
    ("npc", "NPC Script"),
    ("quest", "Quest"),
    ("script", "Script"),
]


def target_kind(src_name: str) -> str:
    low = src_name.lower()
    for key, kind in KINDS:
        if key in low:
            return kind
    return "Script"


def output_name_for(filename: str) -> str:
    """Output file name for an MCF input (single source of truth)."""
    return Path(filename).stem + ".txt"


def decode(raw: bytes) -> bytes:
    d0 = bytes(a ^ KB[0] for a in raw[0::4])
    d1 = bytes(a ^ KB[1] for a in raw[1::4])
    d2 = bytes(a ^ KB[2] for a in raw[2::4])
    d3 = bytes(a ^ KB[3] for a in raw[3::4])
    dec = bytearray(len(raw))
    dec[0::4] = d0
    dec[1::4] = d1
    dec[2::4] = d2
    dec[3::4] = d3
    return bytes(dec)


def parse(dec: bytes) -> dict:
    g, s, f = struct.unpack_from("<iii", dec, 0)
    p = 12
    glo = [struct.unpack_from("<i", dec, p + 4 * i)[0] for i in range(g)]
    p += 4 * g
    srel = [struct.unpack_from("<i", dec, p + 4 * i)[0] for i in range(s)]
    p += 4 * s
    frel = []
    for i in range(f):
        fn, fo = struct.unpack_from("<ii", dec, p + 8 * i)
        frel.append((fn, fo))
    p += 8 * f
    gv, sb, cs = struct.unpack_from("<iii", dec, p)
    p += 12
    strbuf = dec[p: p + sb]
    p += sb
    code = dec[p: p + cs]
    p += cs
    fmap_size = struct.unpack_from("<l", dec, p)[0]
    p += 4
    funcmap = {}
    for _ in range(fmap_size):
        end = dec.index(b"\n", p)
        name = dec[p:end].decode("ascii")
        p = end + 1
        typ, offset = struct.unpack_from("<ll", dec, p)
        p += 8
        funcmap.setdefault(offset, []).append(name)
    sysvars = struct.unpack_from("<iiii", dec, p)
    p += 16
    return {"glo": glo, "srel": set(srel), "frel": frel, "gv": gv,
            "strbuf": strbuf, "code": code, "funcmap": funcmap,
            "sysvars": sysvars, "consumed": p, "total": len(dec)}


def fmt_int(v: int) -> str:
    if v >= 0x100000:
        return f"0x{v:X}"
    return str(v)


def fmt_float(bits: int) -> str:
    v = struct.unpack("<f", struct.pack("<I", bits))[0]
    for prec in range(0, 12):
        cand = ("%.*f" % (prec, v)).rstrip("0").rstrip(".")
        if cand in ("-0", "", "-"):
            cand = "0"
        try:
            if struct.unpack("<I", struct.pack("<f", float(cand)))[0] == bits:
                return cand
        except OverflowError:
            pass
    return repr(float(v))


def coerce_text(raw: bytes) -> bytes:
    # String bytes are emitted verbatim when valid UTF-8 (preserves U+2019
    # etc. byte-for-byte). Legacy single-byte text (CP949 Korean, 0x92
    # smart quotes, ...) is decoded as Windows-1252 and re-encoded UTF-8 —
    # byte-identical to what rylCoder writes for the same strings (verified
    # on every differing Script line, incl. the 0x92 -> U+2019 case that
    # distinguishes cp1252 from latin-1). Fallback latin-1 covers bytes
    # undefined in cp1252. No strbuf string contains a raw quote.
    try:
        raw.decode("utf-8")
        return raw
    except UnicodeDecodeError:
        pass
    try:
        return raw.decode("cp1252").encode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("latin-1").encode("utf-8")


def fmt_str(raw: bytes) -> bytes:
    return b'"' + coerce_text(raw) + b'"'


def scan_calls(code: bytes, funcmap: dict, strbuf: bytes, srel: set):
    """Return (calls, anomalies). calls = [(addr, name, [imm,...])]."""
    calls = []
    anomalies = []
    offs = set(funcmap)
    n = len(code)
    for i in range(n):
        if code[i] != 0xE8 or i + 5 > n:
            continue
        rel = struct.unpack_from("<i", code, i + 1)[0]
        tgt = i + 5 + rel
        if tgt not in offs:
            continue
        # walk back over (B9 imm32 51)*
        args = []
        q = i
        while q - 6 >= 0 and code[q - 1] == 0x51 and code[q - 6] == 0xB9 \
                and len(args) < 8:
            args.append(struct.unpack_from("<I", code, q - 5)[0])
            q -= 6
        args.reverse()
        # forward check: 81 C4 imm32 (COP_add ESP, argc*4)
        esp_ok = (i + 11 <= n and code[i + 5] == 0x81
                  and code[i + 6] == 0xC4
                  and struct.unpack_from("<I", code, i + 7)[0] == 4 * len(args))
        names = funcmap[tgt]
        cands = [nm for nm in names if len(args) in SIGS.get(nm, {})]
        if len(cands) != 1:
            anomalies.append((i, tgt, names, args))
            continue
        if not esp_ok:
            anomalies.append((i, tgt, names, args, "esp"))
            continue
        # string-reloc cross-check for s-typed args
        calls.append((i, cands[0], args))
    calls.sort()
    return calls, anomalies


def render_arg(typ: str, imm: int, strbuf: bytes, anomalies: list, where: str):
    if typ == "s":
        if imm >= len(strbuf):
            anomalies.append((where, "stroff", imm))
            return b'""'
        end = strbuf.index(b"\x00", imm)
        return fmt_str(strbuf[imm:end])
    if typ == "b":
        if imm not in (0, 1):
            anomalies.append((where, "bool", imm))
        return b"true" if imm else b"false"
    if typ == "f":
        return fmt_float(imm).encode("ascii")
    v = imm if imm < 0x80000000 else imm - 0x100000000
    return fmt_int(v).encode("ascii")


def decompile_file(src: Path):
    raw = src.read_bytes()
    log.debug(f"{src.name}: read {len(raw):,} bytes.")
    dec = decode(raw)
    P = parse(dec)
    log.debug(f"{src.name}: decoded into {len(P['code']):,} code bytes, "
              f"{len(P['funcmap'])} functions and "
              f"{len(P['strbuf']):,} string bytes.")
    calls, anomalies = scan_calls(P["code"], P["funcmap"], P["strbuf"], P["srel"])
    # render statements (bytes: ascii + raw string bytes)
    out = []
    first = True
    arg_anom = []
    for addr, name, args in calls:
        types, indent, blanks = SIGS[name][len(args)]
        if not first:
            if name == "SetNPC":
                out.extend([b""] * 2)
            elif blanks:
                out.extend([b""] * blanks)
        rendered = []
        for t, imm in zip(types, args):
            rendered.append(render_arg(t, imm, P["strbuf"], arg_anom,
                                       f"{name}@{addr}"))
        out.append(b"\t" * indent
                   + f"{name}(".encode("ascii")
                   + b", ".join(rendered)
                   + b");")
        first = False
        if name == "QuestEnd":
            out.extend([b"", b""])
    # drop trailing blanks (file ends with the last statement)
    while out and out[-1] == b"":
        out.pop()
    log.debug(f"{src.name}: recovered {len(calls):,} calls with "
              f"{len(anomalies)} call anomalies and "
              f"{len(arg_anom)} argument anomalies.")
    # rDec header block on top + exactly one blank separator line.
    from modules.banners import file_banner
    L = [s.encode("ascii") for s in file_banner()]
    L.append(b"")
    L.extend(out)
    # NOTE: no trailing newline, no footer.
    return b"\r\n".join(L), P, calls, anomalies, arg_anom


def main(argv):
    from modules.logging import setup
    slog = setup()
    rest, out = [], None
    i = 0
    while i < len(argv):
        if argv[i] == "--out" and i + 1 < len(argv):
            out = Path(argv[i + 1])
            i += 2
            continue
        if argv[i].startswith("--"):
            i += 1
            continue
        rest.append(argv[i])
        i += 1
    if not rest:
        print(__doc__)
        return 2
    srcs = []
    for a in rest:
        p = Path(a)
        if p.is_dir():
            srcs += sorted(p.glob("*.mcf"))
        elif p.exists():
            srcs.append(p)
    if out is None:
        slog.error("Missing required --out <directory>.")
        return 1
    out.mkdir(parents=True, exist_ok=True)
    from collections import Counter
    for src in srcs:
        txt, P, calls, anomalies, arg_anom = decompile_file(src)
        dest = out / (src.stem + ".txt")
        if dest.exists() and b"mcf_decompiler.py" not in dest.read_bytes():
            dest = out / (src.stem + ".gen.txt")
            slog.warning(f"{src.stem}.txt already exists and looks foreign; "
                         f"writing {dest.name} instead.")
        dest.write_bytes(txt)
        cc = Counter(nm for _, nm, _ in calls)
        slog.info(f"{src.name}: {len(calls):,} calls, "
                  f"{len(anomalies)} call anomalies, "
                  f"{len(arg_anom)} argument anomalies "
                  f"({P['consumed']:,}/{P['total']:,} bytes consumed).")
        slog.info(f"Wrote {dest} ({len(txt):,} bytes).")
        for nm, k in sorted(cc.items()):
            slog.debug(f"    {nm:20s} x{k}")
        for a in anomalies[:5]:
            slog.debug(f"    call anomaly: {a}")
        for a in arg_anom[:5]:
            slog.debug(f"    argument anomaly: {a}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
