

import re
import struct
import sys
from pathlib import Path

from modules.logging import get_logger

log = get_logger()

MCF_KEY = 0x425529AC
KB = struct.pack("<I", MCF_KEY)

SIGS = {
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


def output_name_for_mcf(filename: str) -> str:
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


_HANGUL = re.compile(r"[\uac00-\ud7a3\u3130-\u318f\u3018-\u301f\u3008-\u300b]")
_KS_SYMBOL = re.compile("[\u2014\u2018\u2019\u201c\u201d\u2025\u2030\u2032\u2033"
                        "\u2190-\u2193\u2200-\u22ff\u2460-\u2473"
                        "\u2500-\u257f\u25a0-\u25ff\u3010\u3011\u3000]")
_CTRL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


def smart_str(raw: bytes) -> str:
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        pass
    try:
        return _kr_evidence(raw)
    except UnicodeDecodeError:
        pass
    try:
        return raw.decode("cp1252")
    except UnicodeDecodeError:
        return raw.decode("latin-1")


def _kr_evidence(raw: bytes) -> str:
    s = raw.decode("euc-kr")
    non_ascii = [c for c in s if ord(c) > 127]
    if not non_ascii:
        raise UnicodeDecodeError("euc-kr", raw, 0, 1, "no Korean evidence")
    if all(_KS_SYMBOL.match(c) or _HANGUL.match(c) for c in non_ascii):
        return s
    raise UnicodeDecodeError("euc-kr", raw, 0, 1, "no Korean evidence")


def clean_text(s: str) -> str:
    s = _CTRL_RE.sub("", s)
    for a, b in (("\u2018", "'"), ("\u2019", "'"), ("\u201c", '"'),
                 ("\u201d", '"'), ("\u201e", '"'), ("\u2026", "..."),
                 ("\u2025", ".."), ("\u2014", "-"), ("\u2013", "-"),
                 ("\u201a", ","), ("\u2022", "*"), ("\u00a0", " "),
                 ("\u3000", " ")):
        s = s.replace(a, b)
    return s


def coerce_text(raw: bytes) -> bytes:
    return smart_str(raw).encode("utf-8", errors="replace")


def text_out(s: str) -> str:
    from modules.translations import translate_text
    text = translate_text(clean_text(s))
    return text.replace("\t", "    ").replace("\r\n", "\\n").replace("\n", "\\n")


def fmt_str(raw: bytes) -> bytes:
    text = text_out(smart_str(raw))
    return b'"' + text.encode("utf-8") + b'"'


def scan_calls(code: bytes, funcmap: dict, strbuf: bytes, srel: set):
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
        args = []
        q = i
        while q - 6 >= 0 and code[q - 1] == 0x51 and code[q - 6] == 0xB9 \
                and len(args) < 8:
            args.append(struct.unpack_from("<I", code, q - 5)[0])
            q -= 6
        args.reverse()
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
    while out and out[-1] == b"":
        out.pop()
    log.debug(f"{src.name}: recovered {len(calls):,} calls with "
              f"{len(anomalies)} call anomalies and "
              f"{len(arg_anom)} argument anomalies.")
    from modules.banners import file_banner
    L = [s.encode("ascii") for s in file_banner()]
    L.append(b"")
    L.extend(out)
    return b"\r\n".join(L), P, calls, anomalies, arg_anom


def mcf_main(argv):
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


import re
import struct
import sys
from pathlib import Path
from collections import Counter

from modules.logging import get_logger

log = get_logger()

HERE = Path(__file__).parent
_TABLES = None


def _tables():
    global _TABLES
    if _TABLES is None:
        from modules.xor_crypt import raw_page, PAGE_COUNT, VERSIONS
        _TABLES = {(_v, _p): list(raw_page(_v, _p))
                   for _v in range(VERSIONS) for _p in range(PAGE_COUNT)}
    return _TABLES


PAGES = {"ItemScript.gsf": (0, 2), "Chemical.gsf": (0, 2),
         "MonsterProtoType.gsf": (0, 3), "SkillScript.gsf": (0, 1),
         "Script1.gsf": (0, 1)}
OUTNAME = {"Script1.gsf": "Abuse.txt"}
PENDING_PAGES = {
    "SpeacialCompensation.gsf":
        "crypt page (3, 4) of the RYL2 V2000+ XORCryptoCodeList "}


def output_name_for_gsf(filename: str) -> str:
    return OUTNAME.get(filename, Path(filename).stem + ".txt")


def build_namemap(files, version=None) -> dict:
    for src in files:
        if Path(src).name == "ItemScript.gsf":
            if version == "RYL1":
                return ryl1_item_namemap(load_gsf(Path(src)))
            return item_namemap(load_gsf(Path(src)))
    return {}


_MC_DECO = b"??Monster Chat Script ??"
_MC_RYL1_SIGN = b"void MonsterChat(int, int, int, int, int, string); // KID, ?????"
_MC_DOC = (
    "void MonsterChat(int, int, int, int, int, string); // KID, MonsterAction, "
    "Monster SkillsID, Chattingtypes, Probability, ChattingMessage",
    "",
    "//////\tChattingtypes ID\t//////////",
    "//\t\t\t\t\t//",
    "//\tGeneral attack\t\t\t\t=0\t//",
    "//\tWhen getting attacked by general attack\t=1\t//",
    "//\tWhen attacking with skill attack\t\t=2\t//",
    "//\tWhen getting attacked by skill attack\t=3\t//",
    "//\tWhen attacking with crit attack\t\t=4\t//",
    "//\tWhen getting attacked by crit attack\t=5\t//",
    "//\tLisphone\t\t\t\t\t=6\t//",
    "//\tDeath\t\t\t\t\t\t=7\t//",
    "//\t\t\t\t\t//",
    "//////////////////////////",
    "",
    "//////\tChattingtypes ID\t//////",
    "//\t\t\t\t//",
    "//\tCommon Knowledge\t=255\t//",
    "//\tGeneral\t\t\t\t=0\t\t//",
    "//\tScreaming\t\t\t=7\t\t//",
    "//\t\t\t\t//",
    "///////////////////////",
    "",
    "////\tSkill ID\t//////",
    "//\t\t\t\t\t//",
    "//\tAll Skill\t=0xFFFF\t//",
    "//\t\t\t\t\t//",
    "//////////////////////////",
    "",
    "// $KILLERNAME$\tSubstitute with killer(player) name. It's only possible "
    "when Action ID matches number 7 (death).",
    "// $ATTNAME$\t\tSubstitute with hitter(player) name. It's only possible "
    "when Action ID matches number 1, 3, 5 (when the monster got hit).",
    "// $DEFNAME$\t\tSubstitute with the player name who got hit by the "
    "monster. It's only possible when Action ID matches number 0, 2, 4 "
    "(when the monster hits) (When two or more exist, chosen at random).",
    "",
    "// KID, Monster Action, Monster skill ID. When the chatting kinds are "
    "the same kind, the probability is calculated by adding them together.",
    "",
    "// ex ",
    '//MonsterChat(4001, 2, 0xFFFF, 0, 20, "Monster chat example text 1");',
    '//MonsterChat(4001, 2, 0xFFFF, 0, 20, "Monster chat example text 2");',
    "// (A random number is chosen from 1~100: the first message is covered "
    "by 1~20, the second by 21~40. Other numbers say nothing.) ",
    "",
    "// Note: this header was reconstructed in English - the original notes "
    "were lost to text corruption in the source binary.",
)


def repair_monsterchat(body: bytes) -> bytes:
    if _MC_DECO in body:
        body = body.replace(_MC_DECO, b"Monster Chat Script")
    if not body.startswith(_MC_RYL1_SIGN):
        return body
    lines = body.split(b"\r\n")
    idx = None
    for i, line in enumerate(lines):
        if b"Named Monster-Boss" in line:
            idx = i - 1
            break
    if idx is None:
        return body
    out = [s.encode("utf-8") for s in _MC_DOC]
    out += [b"", b""]
    return b"\r\n".join(out) + b"\r\n".join(lines[idx:])


def decompile_gsf(src: Path, namemap: dict, version=None) -> bytes:
    src = Path(src)
    lowered = src.name.lower()
    if lowered == "monsterchat.gsf":
        body = src.read_bytes()
        log.debug(f"MonsterChat.gsf: passing through {len(body):,} "
                  f"plaintext bytes.")
        return with_banner(repair_monsterchat(body), _eol_of(body))
    if lowered == "skillscriptex.gsf":
        import shutil
        import subprocess
        import tempfile
        jar = HERE / "unluac.jar"
        if not (shutil.which("java") and jar.exists()):
            raise RuntimeError("SKIP: needs java + modules/unluac.jar")
        log.debug("SkillScriptEX.gsf: decompiling Lua bytecode with unluac.")
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "SkillScriptEx.txt"
            r = subprocess.run(["java", "-jar", str(jar), str(src),
                                "-o", str(dest)],
                               capture_output=True, text=True)
            if r.returncode != 0 or not dest.exists():
                raise RuntimeError(f"unluac failed: {(r.stderr or '')[:200]}")
            body = dest.read_bytes()
            log.debug(f"SkillScriptEX.gsf: unluac returned {len(body):,} "
                      f"bytes.")
            return with_banner(body, _eol_of(body))
    dec = load_gsf(src)
    if version == "RYL1":
        if src.name == "ItemScript.gsf":
            return with_banner(decompile_ryl1_item(dec), b"\n")
        if src.name == "MonsterProtoType.gsf":
            return with_banner(decompile_ryl1_monster(dec), b"\n")
        if src.name == "Chemical.gsf":
            return with_banner(decompile_chemical(dec, namemap))
        if src.name == "SpeacialCompensation.gsf":
            return with_banner(decompile_compensation(dec, namemap))
        raise ValueError(f"{src.name}: no RYL1 GSF handler registered")
    if src.name == "ItemScript.gsf":
        S, N = 616, len(dec) // 616
        log.debug(f"ItemScript.gsf: {N:,} item rows.")
        lines = ["\t".join(ITEM_HDR)]
        for i in range(N):
            lines.append("\t".join(emit_item(dec[i * S:(i + 1) * S])))
        return with_banner(("\n".join(lines) + "\n").encode("utf-8"), b"\n")
    if src.name == "MonsterProtoType.gsf":
        S, N = 552, len(dec) // 552
        log.debug(f"MonsterProtoType.gsf: {N:,} monster rows.")
        return with_banner(("\r\n".join(
            "\t".join(emit_monster(dec[i * S:(i + 1) * S]))
            for i in range(N)) + "\r\n").encode("utf-8"))
    if src.name == "SkillScript.gsf":
        return with_banner(decompile_skill(dec))
    if src.name == "Chemical.gsf":
        return with_banner(decompile_chemical(dec, namemap))
    if src.name == "Script1.gsf":
        return with_banner(decompile_abuse(dec))
    if src.name == "SpeacialCompensation.gsf":
        return with_banner(decompile_compensation(dec, namemap))
    raise ValueError(f"{src.name}: no GSF handler registered")


def _eol_of(body: bytes) -> bytes:
    return b"\r\n" if b"\r\n" in body else b"\n"


def ror1(b):
    return ((b << 7) & 0xFF) | (b >> 1)


def load_gsf(path: Path):
    try:
        import lzo
    except ImportError as e:
        raise RuntimeError(f"{path.name}: needs the 'lzo' package ({e})")
    raw = path.read_bytes()
    trash = struct.unpack_from("<I", raw, 0)[0]
    if trash > len(raw):
        raise ValueError(f"{path.name} is not a GSF envelope "
                         f"(trash size {trash:,} exceeds "
                         f"file size {len(raw):,}).")
    orig = struct.unpack_from("<I", raw, 4 + trash)[0]
    body = lzo.decompress(bytes(raw[4 + trash + 4:]), False, orig)
    assert len(body) == orig, (f"LZO payload is {len(body):,} bytes; "
                               f"{orig:,} were expected.")
    log.debug(f"{path.name}: decompressed {orig:,} payload bytes "
              f"({len(raw):,} on disk, {trash:,} trash bytes skipped).")
    try:
        ver, page = PAGES[path.name]
    except KeyError:
        if path.name in PENDING_PAGES:
            raise RuntimeError(f"SKIP: {PENDING_PAGES[path.name]} is "
                               f"missing from the bundled XORCryptoCodeList.")
        raise ValueError(f"No crypt page is registered for {path.name} "
                         f"(known: {sorted(PAGES)}).")
    row = _tables()[(ver, page)]
    return bytes((ror1(c) ^ row[i % 40]) for i, c in enumerate(body))


def f32short(bits: int) -> str:
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


def cstr(b: bytes) -> bytes:
    return b.split(b"\x00")[0]


def field(raw: bytes) -> str:
    return text_out(smart_str(raw))


def ox(v: int) -> str:
    return "O" if v else "X"


ITEMTYPE = {0: "NONE", 1: "SHIRT", 2: "TUNIC", 3: "CON_ARMOUR", 4: "CON_HELM",
            5: "CON_GLOVE", 6: "CON_BOOTS", 7: "DEX_ARMOUR", 8: "DEX_HELM",
            9: "DEX_GLOVE", 10: "DEX_BOOTS", 11: "ONEHANDED_SWORD",
            12: "TWOHANDED_SWORD", 13: "ONEHANDED_AXE", 14: "TWOHANDED_AXE",
            15: "ONEHANDED_BLUNT", 16: "TWOHANDED_BLUNT", 17: "BOW",
            18: "CROSSBOW", 19: "STAFF", 20: "DAGGER", 21: "SHIELD",
            22: "CON_BODY", 23: "CON_HEAD", 24: "CON_PELVIS",
            25: "CON_PROTECT_A", 26: "DEX_BODY", 27: "DEX_HEAD",
            28: "DEX_PELVIS", 29: "DEX_PROTECT_A", 30: "COM_BLUNT",
            31: "COM_SWORD", 32: "OPP_HAMMER", 33: "OPP_AXE",
            34: "OPP_SLUSHER", 35: "OPP_TALON", 36: "OPP_SYTHE",
            37: "SKILL_A_GUARD", 38: "SKILL_A_ATTACK", 39: "SKILL_A_GUN",
            40: "SKILL_A_KNIFE", 41: "ARROW", 42: "BOLT", 43: "AMMO",
            44: "POTION", 45: "EXPBOOK", 46: "CASHBOOK", 47: "EVENT_LOTTERY",
            48: "PORTAL", 49: "FIRE_CRACKER", 50: "SKILLBOOK",
            51: "FIXED_PORTAL", 52: "SKILL_ITEM", 53: "CASH_ITEM", 54: "GEM",
            55: "ORE", 56: "ETC", 57: "CAMP_KIT", 58: "SHORT_RANGE_ARMS_KIT",
            59: "LONG_RANGE_ARMS_KIT", 60: "AIRSHIP_KIT",
            61: "WORLDWEAPON_K_KIT", 62: "WORLDWEAPON_M_KIT",
            63: "MINERAL_KIT", 64: "QUEST_ITEM", 65: "NECKLACE", 66: "RING",
            67: "RUNE", 68: "GEM_SELL", 69: "RIDE", 70: "TRANSFORM"}
EQUIP = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
         20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36,
         37, 38, 39, 40, 41, 42}
ACCESSORY = {65, 66, 67}
AVATA = {69, 70}
USEITEM = {43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 57, 58, 59, 60, 61,
           62, 63, 64}
GRADE = {0: "AAA", 1: "AA", 2: "A", 3: "B", 4: "C", 5: "D", 6: "F", 7: "X"}
LIMIT = {0: "NONE", 1: "STR", 2: "DEX", 3: "CON", 4: "INT", 5: "WIS",
         6: "LEVEL"}
(NONE_A, MIN_DAMAGE, MAX_DAMAGE, ARMOR, HIT_RATE, EVADE, MAX_HP, HP_REGEN,
 MAX_MP, MP_REGEN, CRITICAL, BLOCK, SPEED, MAGIC_POWER, MAGIC_RESIST,
 LUCKCHANCE, COOLDOWN, SKILL_POINT, FROST, FIRE, ELECTRO,
 DARKNESS) = range(22)


def _all_qmark(s: str) -> bool:
    return bool(s) and "?" in s and set(s) <= {"?"}


def _pretty_word(w: str) -> str:
    return w.replace("_", " ").title()


def pretty_itemtype(itype: int) -> str:
    base = ITEMTYPE.get(itype)
    if base is None:
        return "Unknown"
    if "HANDED" in base:
        return base.replace("ONEHANDED", "One-Handed")\
            .replace("TWOHANDED", "Two-Handed")\
            .replace("_", " ").title().replace("And", "and")
    return _pretty_word(base)


def pretty_ryl1_type(itype: int) -> str:
    base = RYL1_ITEMTYPE.get(itype)
    if base is None:
        return "Unknown"
    return _pretty_word(base)


def hexid(v: int) -> str:
    return f"0x{v:04X}" if v >= 0x8000 else str(v)


def emit_item(r: bytes):
    itype = r[21]
    tn = field(cstr(r[252:284]))
    if "?" in tn:
        tn = pretty_itemtype(itype)
    c = [str(struct.unpack_from("<H", r, 0)[0]),
         field(cstr(r[52:116])),
         field(cstr(r[156:188])),
         field(cstr(r[188:220])),
         field(cstr(r[116:148])),
         str(struct.unpack_from("<H", r, 148)[0]),
         str(struct.unpack_from("<H", r, 150)[0]),
         str(struct.unpack_from("<H", r, 152)[0]),
         str(struct.unpack_from("<H", r, 154)[0]),
         str(r[22]), str(r[23]),
         field(cstr(r[220:252])),
         ITEMTYPE.get(itype, str(itype)),
         tn,
         ox(r[34]), ox(r[35]), str(r[27]), str(r[28]),
         str(struct.unpack_from("<I", r, 4)[0]), ox(r[36]),
         str(struct.unpack_from("<I", r, 8)[0]),
         str(struct.unpack_from("<I", r, 12)[0]),
         str(struct.unpack_from("<I", r, 44)[0]),
         LIMIT.get(r[48], str(r[48])),
         str(struct.unpack_from("<H", r, 50)[0]),
         str(struct.unpack_from("<H", r, 30)[0]),
         str(struct.unpack_from("<H", r, 32)[0]),
         str(r[25]), str(r[26])]
    A = [struct.unpack_from("<H", r, 540 + 2 * i)[0] for i in range(22)]
    if itype in EQUIP:
        c += [str(A[MIN_DAMAGE]), str(A[MAX_DAMAGE]), str(A[ARMOR]),
              str(A[BLOCK]), str(struct.unpack_from("<H", r, 16)[0]),
              GRADE.get(r[18], str(r[18])), str(r[19]), str(r[20]),
              str(r[24]), str(A[LUCKCHANCE]), "0", "0", "0", "0", "0", "0",
              "0", "0", "0", "0", "0", "0"]
    elif itype in ACCESSORY:
        c += [str(A[MIN_DAMAGE]), str(A[MAX_DAMAGE]), str(A[ARMOR]),
              str(A[BLOCK]), str(struct.unpack_from("<H", r, 16)[0]),
              GRADE.get(r[18], str(r[18])), str(A[CRITICAL]),
              str(A[HIT_RATE]), str(A[MAGIC_POWER]), str(A[MAGIC_RESIST]),
              str(A[EVADE]), str(A[COOLDOWN]), str(A[MAX_HP]),
              str(A[MAX_MP]), str(A[HP_REGEN]), str(A[MP_REGEN]),
              str(A[SPEED]), str(A[SKILL_POINT]), str(A[FROST]),
              str(A[FIRE]), str(A[ELECTRO]), str(A[DARKNESS])]
    elif itype in AVATA:
        c += [str(struct.unpack_from("<H", r, 16)[0]),
              GRADE.get(r[18], str(r[18])), str(A[SPEED])] + [""] * 19
    elif itype in USEITEM:
        pos = [f32short(struct.unpack_from("<I", r, o)[0]) for o in (588, 592, 596)]
        c += [ox(r[615]), str(r[614]),
              hexid(struct.unpack_from("<H", r, 608)[0]),
              str(struct.unpack_from("<H", r, 610)[0]),
              str(r[600]), pos[0], pos[1], pos[2],
              str(struct.unpack_from("<I", r, 604)[0]),
              hexid(struct.unpack_from("<H", r, 612)[0]),
              field(cstr(r[284:540]))] + [""] * 11
    else:
        c += [field(cstr(r[284:540]))] + [""] * 21
    return c


ITEM_HDR = ["ID", "ItemName", "FieldModelName", "AttachedModelName", "SpriteDDS",
            "MinX", "MinY", "MaxX", "MaxY", "SizeX", "SizeY", "EffectSound",
            "ItemType", "TypeName", "AbleExchangeNDrop", "AbleSell",
            "MinDropLevel", "MaxDropLevel", "Price", "OptionPrice",
            "BlackPrice", "MedalPrice", "ClassLimit", "LimitStat", "Limit",
            "LowLevel", "HighLevel", "Durability", "MaxDurability",
            "MinDamage", "MaxDamage", "Defence", "Block", "DropOption",
            "Grade", "CriticalType", "AttackRange", "MaxSocketNum",
            "MagicResist", "Evade", "CoolDown", "MaxHP", "MaxMP", "HPRegen",
            "MPRegen", "Speed", "SkillPoint", "Frost", "Fire", "Electro",
            "Darkness"]


def decompile_item(dec: bytes) -> bytes:
    S, N = 616, len(dec) // 616
    lines = ["\t".join(ITEM_HDR)]
    for i in range(N):
        lines.append("\t".join(emit_item(dec[i * S:(i + 1) * S])))
    return ("\n".join(lines) + "\n").encode("utf-8")


MONPAT = {0: "Common", 1: "Warrior", 2: "Defender", 3: "Mage", 4: "Acolyte",
          5: "Boss", 6: "BG", 7: "Summon", 8: "Structure", 9: "Named",
          10: "Chief", 11: "Object", 12: "Guard", 13: "Gather"}
MONSTATUE = {0: "0", 1: "HP", 2: "MP", 3: "EXP", 4: "DropRate"}


def mon_vel(bits: int) -> str:
    v = struct.unpack("<f", struct.pack("<I", bits))[0] * 100.0
    for prec in range(0, 12):
        cand = ("%.*f" % (prec, v)).rstrip("0").rstrip(".")
        if cand in ("-0", "", "-"):
            cand = "0"
        try:
            if struct.unpack("<I", struct.pack("<f", float(cand) / 100.0))[0] == bits:
                return cand
        except (OverflowError, ZeroDivisionError):
            pass
    return repr(v)


def emit_monster(r: bytes):
    c = [""] * 116
    c[0] = str(struct.unpack_from("<H", r, 348)[0])
    c[1] = field(cstr(r[64:128]))
    c[2] = field(cstr(r[128:160]))
    c[3] = ox(r[396])
    c[4] = str(r[370])
    c[5] = "Siege" if r[392] else MONPAT.get(r[366], str(r[366]))
    c[6] = ox(r[392])
    c[7] = str(r[12])
    c[8] = mon_vel(struct.unpack_from("<I", r, 4)[0])
    c[9] = str(r[28])
    c[10] = mon_vel(struct.unpack_from("<I", r, 20)[0])
    c[11] = str(r[44])
    c[12] = str(r[44])
    for i, o in enumerate((160, 164, 168, 172), start=13):
        c[i] = f32short(struct.unpack_from("<I", r, o)[0])
    c[17] = str(struct.unpack_from("<H", r, 364)[0])
    c[18] = f32short(struct.unpack_from("<I", r, 360)[0])
    c[19] = str(struct.unpack_from("<I", r, 456)[0])
    c[20] = str(r[464])
    for col, o in ((21, 472), (22, 474), (23, 478), (24, 476), (25, 480),
                   (26, 492), (28, 490), (30, 500), (31, 502)):
        c[col] = str(struct.unpack_from("<H", r, o)[0])
    c[27] = "0"
    c[27] = "0"
    c[29] = str(r[544])
    c[32] = str(r[494])
    for col, o in ((33, 482), (34, 486), (35, 484), (36, 488)):
        c[col] = str(struct.unpack_from("<H", r, o)[0])
    c[37] = f32short(struct.unpack_from("<I", r, 356)[0])
    c[38] = str(r[367])
    c[39] = ox(r[393])
    c[40] = ox(r[394])
    c[41] = ox(r[395])
    c[42] = ox(r[369])
    c[43] = str(r[368])
    c[44] = str(r[372])
    for col, o in ((45, 374), (46, 376), (47, 378), (48, 380), (49, 382)):
        c[col] = hexid(struct.unpack_from("<H", r, o)[0])
    c[50] = str(r[384])
    c[51] = str(r[385])
    c[52] = f32short(struct.unpack_from("<I", r, 388)[0])
    c[53] = str(struct.unpack_from("<I", r, 352)[0])
    for col, o in ((54, 176), (55, 178), (56, 180), (57, 182), (58, 184),
                   (59, 188), (60, 192), (61, 196), (62, 200), (63, 204)):
        c[col] = str(struct.unpack_from("<H", r, o)[0])
    c[64] = str(struct.unpack_from("<I", r, 208)[0])
    c[65] = str(r[216])
    c[66] = str(r[216])
    for col in range(67, 74):
        if col != 73:
            c[col] = "0"
    c[73] = str(r[244])
    for col in range(74, 98):
        c[col] = "0"
    c[98] = str(r[344])
    c[99] = str(r[344])
    c[100] = MONSTATUE.get(r[452], str(r[452]))
    c[101] = str(r[453])
    c[102] = str(r[400])
    c[103] = str(r[392])
    for col in range(104, 115):
        c[col] = "0"
    kid = struct.unpack_from("<H", r, 348)[0]
    c[115] = "0" if kid >= 40232 else ""
    return c


def decompile_monster(dec: bytes) -> bytes:
    S, N = 552, len(dec) // 552
    lines = []
    for i in range(N):
        lines.append("\t".join(emit_monster(dec[i * S:(i + 1) * S])))
    return ("\r\n".join(lines) + "\r\n").encode("utf-8")


SKILLTYPES = {0: "NONE", 1: "PASSIVE", 2: "INSTANCE", 3: "CAST", 4: "CHANT",
              5: "ENCHANT", 6: "ITEM", 7: "SET", 8: "ACTION", 9: "ABILITY",
              10: "GATHER"}
USELIMITS = {0: "NONE", 1: "FORFIGHTER", 2: "WITHSHIELD",
             3: "FORFIGHTERTWOHAND", 4: "FORALLONEHAND", 5: "WITHDAGGER",
             6: "WITHTHROWINGDAGGER", 7: "RANGED", 8: "LEFTARM",
             9: "GUARDARM", 10: "WITHWEAPON", 11: "ATTACKARM", 12: "GUNARM",
             13: "KNIFEARM", 14: "WITHCLOW"}
STATLIMITS = {0: "NONE", 1: "STR", 2: "DEX", 3: "CON", 4: "INT", 5: "WIS",
              6: "LEVEL"}
TARGETS = {0: "NONE", 1: "MELEE", 2: "FRIEND", 3: "ENEMY", 4: "FRDEAD",
           5: "ENDEAD", 6: "FROBJ", 7: "ENOBJ", 8: "PARTY", 9: "FREXME",
           10: "ENLINE", 11: "SUMMON"}
SKILL_HDR = ["ID", "Type", "ClassSkill", "Name[5]", "Limit", "Stat[0]",
             "Value[0]", "Stat[1]", "Value[1]", "Target", "mRange", "Range",
             "Region", "StartMP", "LevelMP", "LockAdd", "Starttick",
             "LevelTick", "CastingFlag", "EffectFlag", "HitFlag",
             "CoolDownTime", "EndCoolDown", "dds", "MinX", "MinY", "MaxX",
             "MaxY", "Hit", "EndScript", "Protection", "Interrupt",
             "Counter", "Gauge", "Parent", "Child", "Text"]


def sval(b: int) -> int:
    return b - 256 if b >= 128 else b


def emit_skill(g: bytes):
    c = [f"0x{struct.unpack_from('<H', g, 472)[0]:04X}",
         SKILLTYPES.get(struct.unpack_from("<I", g, 456)[0], "?"),
         str(1 if g[506] else 0),
         field(cstr(g[96:160])),
         USELIMITS.get(struct.unpack_from("<I", g, 464)[0], "?"),
         STATLIMITS.get(g[468], str(g[468])),
         str(sval(g[470])),
         STATLIMITS.get(g[469], str(g[469])),
         str(sval(g[471])),
         TARGETS.get(struct.unpack_from("<I", g, 460)[0], "?"),
         f32short(struct.unpack_from("<I", g, 492)[0]),
         f32short(struct.unpack_from("<I", g, 496)[0]),
         f32short(struct.unpack_from("<I", g, 500)[0]),
         str(struct.unpack_from("<H", g, 474)[0]),
         str(struct.unpack_from("<H", g, 476)[0]),
         str(struct.unpack_from("<H", g, 478)[0]),
         str(struct.unpack_from("<H", g, 480)[0]),
         str(struct.unpack_from("<H", g, 482)[0]),
         field(cstr(g[64:96])),
         field(cstr(g[0:32])),
         field(cstr(g[32:64])),
         str(struct.unpack_from("<I", g, 488)[0]),
         str(g[510]),
         field(cstr(g[160:192])),
         str(struct.unpack_from("<H", g, 192)[0]),
         str(struct.unpack_from("<H", g, 194)[0]),
         str(struct.unpack_from("<H", g, 196)[0]),
         str(struct.unpack_from("<H", g, 198)[0]),
         str(g[511]), str(g[509]),
         str(1 if g[504] else 0), str(1 if g[507] else 0),
         str(1 if g[508] else 0), str(1 if g[505] else 0)]
    for o, w in ((484, 37), (486, 37)):
        v = struct.unpack_from("<H", g, o)[0]
        c.append(f"0x{v:04X}" if v else "0")
    desc = cstr(g[200:456])
    if desc.endswith(b"\n"):
        desc = desc[:-1]
    if desc.endswith(b"\r"):
        desc = desc[:-1]
    c.append(field(desc).strip().strip('"'))
    return c


def decompile_skill(dec: bytes) -> bytes:
    lines = ["\t".join(SKILL_HDR)]
    for gi in range(len(dec) // 2580):
        for j in range(5):
            g = dec[gi * 2580 + j * 516:(gi * 2580 + (j + 1) * 516)]
            if struct.unpack_from("<H", g, 472)[0] == 0:
                continue
            lines.append("\t".join(emit_skill(g)))
    log.debug(f"SkillScript.gsf: {len(lines) - 1:,} skill rows in "
              f"{len(dec) // 2580} groups.")
    return ("\r\n".join(lines) + "\r\n").encode("utf-8")


CHEM_HDR = (b"PickkingItem\t\t\tTargetItem\t\t\tResultItem\t\t\r\n"
            b"Name\tID\tNum\tName\tID\tNum\r\n")


RYL1_ITEM_ROW = 644

RYL1_ITEMTYPE = {
    0: "HELM", 1: "SHIRT", 2: "TUNIC", 3: "ARMOUR", 4: "GLOVE", 5: "BOOTS",
    6: "ONEHANDED_SWORD", 7: "ONEHANDED_BLUNT", 8: "ONEHANDED_AXE",
    9: "TWOHANDED_BLUNT", 10: "TWOHANDED_AXE", 11: "TWOHANDED_SWORD",
    12: "BOW", 13: "CROSSBOW", 14: "STAFF", 15: "DAGGER", 16: "SHIELD",
    17: "CLOAK", 18: "RING", 19: "NECKLACE", 20: "POTION", 21: "POISON",
    22: "TRAP", 23: "SKILLBOOK", 24: "GEM", 25: "RUNE", 26: "ORE",
    27: "AMMO", 28: "ETC", 29: "HEAD", 30: "BODY", 31: "PROTECT_A",
    32: "PELVIS", 33: "COM_BLUNT", 34: "COM_SWORD", 35: "OPP_HAMMER",
    36: "OPP_AXE", 37: "OPP_SLUSHER", 38: "OPP_TALON", 39: "OPP_SYTHE",
    40: "SKILL_A_GUARD", 41: "SKILL_A_ATTACK", 42: "SKILL_A_GUN",
    43: "SKILL_A_KNIFE", 44: "ACCESSORY", 45: "ARROW", 46: "BOLT",
    47: "PORTAL", 48: "EVENT_DROP", 49: "EVENT_LOTTERY", 50: "EXPBOOK",
    51: "CASHBOOK", 52: "FIRE_CRACKER", 53: "CAMP_KIT",
    54: "SHORT_RANGE_ARMS_KIT", 55: "LONG_RANGE_ARMS_KIT",
    56: "AIRSHIP_KIT",
}
RYL1_GRADE = {0: "ETC", 1: "NORMAL", 2: "ENHANCED", 3: "RARE"}
RYL1_EQUIP_TYPES = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                    17, 18, 19, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
                    41, 42, 43, 44, 45, 46}
RYL1_USE_TYPES = {20, 21, 22, 23, 27, 47, 49, 50, 51, 52, 53, 54, 55, 56}

RYL1_ITEM_HDR = ["ID", "ItemName", "FieldModelName", "AttachedModelName",
                 "SpriteDDS", "MinX", "MinY", "MaxX", "MaxY", "SizeX", "SizeY",
                 "EffectSound", "ItemLevel", "ItemType", "TypeName", "Price",
                 "BlackPrice", "MedalPrice", "OptionLimit", "Durability",
                 "MaxDurability", "ClassLimit", "SkillLimitType",
                 "SkillLimitLevel", "LevelLimit", "STRLimit", "DEXLimit",
                 "CONLimit", "INTLimit", "WISLimit", "CraftExp",
                 "CriticalType", "CriticalPercentage", "MinDamage", "MaxDamage",
                 "DRC", "OffenceRevision", "Defence", "DefenceRevision",
                 "Resistance", "BlockingPercentage", "AttackSpeed",
                 "MoveSpeed", "AttackRange", "LongRangeAttack", "HpMaxPlus",
                 "MpMaxPlus", "HPRegen", "MPRegen", "FireAttribute",
                 "LightingAttribute", "ColdAttribute", "DrainAttribute",
                 "PoisonAttribute", "FireResistance", "LightningResistance",
                 "ColdResistance", "DrainResistance", "PoisonResistance",
                 "STRAdd", "DEXAdd", "CONAdd", "INTAdd", "WISAdd",
                 "MaterialValue", "MaxSocketNum"]


def ryl1_text(r: bytes, off: int, size: int) -> str:
    return field(cstr(r[off:off + size]))


def emit_ryl1_item(r: bytes):
    itype = r[4]
    c = [str(struct.unpack_from("<H", r, 0)[0]),
         ryl1_text(r, 60, 64), ryl1_text(r, 164, 32), ryl1_text(r, 196, 32),
         ryl1_text(r, 124, 32),
         str(struct.unpack_from("<H", r, 156)[0]),
         str(struct.unpack_from("<H", r, 158)[0]),
         str(struct.unpack_from("<H", r, 160)[0]),
         str(struct.unpack_from("<H", r, 162)[0]),
         str(r[5]), str(r[6]), ryl1_text(r, 228, 32),
         RYL1_GRADE.get(struct.unpack_from("<I", r, 16)[0],
                        f"[{struct.unpack_from('<I', r, 16)[0]:,}]"),
         RYL1_ITEMTYPE.get(itype, f"[{itype}]"),
         (ryl1_text(r, 260, 32)
          if not _all_qmark(ryl1_text(r, 260, 32))
          else pretty_ryl1_type(itype)),
         str(struct.unpack_from("<I", r, 20)[0]),
         str(struct.unpack_from("<I", r, 24)[0]),
         str(struct.unpack_from("<I", r, 28)[0]),
         str(r[7]), str(r[8]), str(r[9]),
         str(struct.unpack_from("<I", r, 56)[0]),
         str(struct.unpack_from("<H", r, 50)[0]),
         str(r[52]), str(r[53]),
         str(struct.unpack_from("<H", r, 40)[0]),
         str(struct.unpack_from("<H", r, 42)[0]),
         str(struct.unpack_from("<H", r, 44)[0]),
         str(struct.unpack_from("<H", r, 46)[0]),
         str(struct.unpack_from("<H", r, 48)[0]),
         str(struct.unpack_from("<I", r, 12)[0])]
    if itype in RYL1_EQUIP_TYPES:
        a = [struct.unpack_from("<H", r, 548 + 2 * k)[0] for k in range(1, 34)]
        c += [str(v) for v in a]
        c += [str(r[10]), str(r[11])]
    elif itype in RYL1_USE_TYPES:
        c += [hexid(struct.unpack_from("<H", r, 620)[0]),
              str(r[52]),
              str(r[624]),
              f32short(struct.unpack_from("<I", r, 628)[0]),
              f32short(struct.unpack_from("<I", r, 632)[0]),
              f32short(struct.unpack_from("<I", r, 636)[0]),
              str(struct.unpack_from("<I", r, 640)[0]),
              ryl1_text(r, 292, 256)]
        c += [""] * 27
    else:
        c += [ryl1_text(r, 292, 256)]
        c += [""] * 34
    return c


def decompile_ryl1_item(dec: bytes) -> bytes:
    n, rem = divmod(len(dec), RYL1_ITEM_ROW)
    if rem:
        raise ValueError(f"ItemScript.gsf payload is {len(dec):,} bytes; "
                         f"not a multiple of the RYL1 {RYL1_ITEM_ROW}-byte "
                         f"ItemInfo record.")
    lines = ["\t".join(RYL1_ITEM_HDR)]
    for i in range(n):
        lines.append("\t".join(emit_ryl1_item(dec[i * RYL1_ITEM_ROW:
                                              (i + 1) * RYL1_ITEM_ROW])))
    log.debug(f"ItemScript.gsf (RYL1): {n:,} item rows "
              f"({RYL1_ITEM_ROW}-byte ItemInfo).")
    return ("\n".join(lines) + "\n").encode("utf-8")


def ryl1_item_namemap(dec: bytes) -> dict:
    m = {}
    for i in range(len(dec) // RYL1_ITEM_ROW):
        r = dec[i * RYL1_ITEM_ROW:(i + 1) * RYL1_ITEM_ROW]
        m[struct.unpack_from("<H", r, 0)[0]] = \
            field(cstr(r[60:124]))
    return m


RYL1_MON_CLASS = {0: "Siege", 1: "Warrior", 2: "Defender", 3: "Mage",
                  4: "Acolyte", 5: "Rogue", 6: "BG", 7: "Summon",
                  8: "Structure", 9: "Named", 10: "Chief", 11: "Object",
                  12: "Guard"}

RYL1_MON_HDR = [
    "ID", "Name", "Model", "Nation", "Class", "Toggle",
    "RespawnArea1", "Speed1", "RespawnArea2", "Speed2",
    "Param1", "Param2", "Zone1", "Zone2", "Zone3", "Zone4", "Value334",
    "Velocity", "BaseXP", "Level", "MinDamage", "MaxDamage", "Defense",
    "HitRate", "Evade", "Unk25", "CriticalRate", "Unk27", "Unk28", "Skill29",
    "Skill30", "Unk31", "Unk32", "Unk33", "Unk34", "Unk35", "Unk36", "Unk37",
    "Unk38", "Unk39", "Unk40", "Skill41", "Skill42", "MP", "HP", "Unk45",
    "Unk46", "Scale", "SkillByte197", "Toggle229", "Unk50", "Toggle231",
    "Unk52", "Toggle232", "Toggle199", "Byte198", "Byte202", "Unk57", "Unk58",
    "Unk59", "Unk60", "Unk61", "Unk62", "Unk63", "Float224", "SpawnTime",
    "Unk66", "Unk67", "Unk68", "Unk69", "Unk70", "Unk71", "Unk72", "Unk73",
    "Unk74", "Unk75", "Weight164",
    "Unk77", "Unk78", "Unk79", "Unk80", "Unk81", "Unk82", "Unk83", "Unk84",
    "Unk85", "Unk86", "Unk87", "Unk88", "Unk89", "Unk90", "Unk91", "Unk92",
    "Unk93", "Unk94", "Unk95", "Unk96",
]


def speed100(bits: int) -> str:
    v = struct.unpack("<f", struct.pack("<I", bits))[0] * 100.0
    s = "%.6g" % v
    return s


def emit_ryl1_monster(r: bytes):
    c = [str(struct.unpack_from("<I", r, 180)[0]),
         field(cstr(r[64:96])),
         field(cstr(r[96:128])),
         str(r[200]),
         RYL1_MON_CLASS.get(r[196], str(r[196])),
         ox(struct.unpack_from("<I", r, 0)[0]),
         str(struct.unpack_from("<I", r, 12)[0]),
         speed100(struct.unpack_from("<I", r, 4)[0]),
         str(struct.unpack_from("<I", r, 28)[0]),
         speed100(struct.unpack_from("<I", r, 20)[0]),
         str(struct.unpack_from("<I", r, 44)[0]),
         str(struct.unpack_from("<I", r, 60)[0])]
    c += [f32short(struct.unpack_from("<I", r, 128 + 4 * k)[0])
          for k in range(4)]
    c += [str(struct.unpack_from("<H", r, 334)[0]),
          f32short(struct.unpack_from("<I", r, 192)[0])]
    c += [str(struct.unpack_from("<I", r, 288)[0]),
          str(struct.unpack_from("<I", r, 296)[0]),
          str(struct.unpack_from("<H", r, 308)[0]),
          str(struct.unpack_from("<H", r, 310)[0]),
          str(struct.unpack_from("<H", r, 312)[0]),
          str(struct.unpack_from("<H", r, 320)[0]),
          str(struct.unpack_from("<H", r, 322)[0]),
          "0",
          f32short(struct.unpack_from("<I", r, 316)[0]),
          str(struct.unpack_from("<H", r, 306)[0]),
          "0",
          str(struct.unpack_from("<H", r, 326)[0]),
          str(struct.unpack_from("<H", r, 328)[0])]
    c += ["0"] * 10
    c += [str(struct.unpack_from("<H", r, 330)[0]),
          str(struct.unpack_from("<H", r, 332)[0]),
          str(struct.unpack_from("<H", r, 338)[0]),
          str(struct.unpack_from("<H", r, 340)[0]),
          "0",
          "0"]
    c += [f32short(struct.unpack_from("<I", r, 188)[0]),
          str(r[197]),
          ox(r[229]),
          ox(0),
          ox(r[231]),
          ox(0),
          ox(r[232]),
          ox(r[199]),
          str(r[198]),
          str(r[202])]
    c += ["0"] * 5
    c += ["0",
          str(struct.unpack_from("<H", r, 220)[0]),
          f32short(struct.unpack_from("<I", r, 224)[0]),
          str(struct.unpack_from("<I", r, 184)[0])]
    c += ["0"] * 10
    c += [str(struct.unpack_from("<H", r, 164)[0])]
    c += ["0"] * 20
    while c and c[-1] in ("", "0"):
        c.pop()
    return c


def decompile_ryl1_monster(dec: bytes) -> bytes:
    S = 368
    n, rem = divmod(len(dec), S)
    if rem:
        raise ValueError(f"MonsterProtoType.gsf payload is {len(dec):,} bytes; "
                         f"not a multiple of the RYL1 368-byte record.")
    lines = ["\t".join(RYL1_MON_HDR)]
    for i in range(n):
        lines.append("\t".join(emit_ryl1_monster(dec[i * S:(i + 1) * S])))
    log.debug(f"MonsterProtoType.gsf (RYL1): {n:,} records "
              f"(368-byte MonsterProto).")
    return ("\n".join(lines) + "\n").encode("utf-8")


def decompile_ryl1(dec: bytes, name: str, namemap: dict) -> bytes:
    if name == "ItemScript.gsf":
        return decompile_ryl1_item(dec)
    if name == "MonsterProtoType.gsf":
        return decompile_ryl1_monster(dec)
    if name == "Chemical.gsf":
        return decompile_chemical(dec, namemap)
    if name == "SpeacialCompensation.gsf":
        return decompile_compensation(dec, namemap)
    raise ValueError(f"{name}: no RYL1 GSF handler registered")



def decompile_chemical(dec: bytes, namemap: dict) -> bytes:
    out = [CHEM_HDR.rstrip(b"\r\n")]
    missing = Counter()
    n = len(dec) // 10
    for i in range(n):
        r = dec[i * 10:(i + 1) * 10]
        pk, tg, rs = struct.unpack_from("<HHH", r, 0)
        cells = []
        for vid, num in ((pk, r[6]), (tg, r[7]), (rs, r[8])):
            nm = namemap.get(vid)
            if nm is None:
                missing[vid] += 1
                nm = f"ITEM_{vid}"
            cells += [nm, str(vid), str(num)]
        out.append("\t".join(cells).encode("utf-8"))
    if missing:
        cells = sum(missing.values())
        log.warning(f"Chemical.gsf references {len(missing)} unknown "
                    f"item IDs ({cells:,} cells); wrote ITEM_<id> "
                    f"placeholders instead.")
        log.debug(f"Chemical.gsf most-missed IDs: "
                  f"{missing.most_common(5)}.")
    log.debug(f"Chemical.gsf: {n:,} recipes.")
    return ("\r\n".join([]).encode() + b"\r\n".join(out) + b"\r\n")


def item_namemap(dec: bytes) -> dict:
    m = {}
    for i in range(len(dec) // 616):
        r = dec[i * 616:(i + 1) * 616]
        m[struct.unpack_from("<H", r, 0)[0]] = \
            field(cstr(r[52:116]))
    return m


def with_banner(body: bytes, eol: bytes = b"\r\n") -> bytes:
    from modules.banners import file_banner
    head = eol.join(s.encode("ascii") for s in file_banner())
    return head + eol + eol + body


def decompile_compensation(dec: bytes, namemap: dict) -> bytes:
    out = ["CASE\tSEQ\tID\tITEM"]
    case, seq, seen = 0, 0, 0
    missing = Counter()
    for offset in range(0, len(dec) - 1, 2):
        vid = struct.unpack_from("<H", dec, offset)[0]
        if vid == 0:
            case += 1
            seq = 0
            continue
        seq += 1
        seen += 1
        nm = namemap.get(vid)
        if nm is None:
            missing[vid] += 1
            nm = f"ITEM_{vid}"
        out.append(f"{case}\t{seq}\t{vid}\t{nm}")
    if missing:
        cells = sum(missing.values())
        log.warning(f"SpeacialCompensation.gsf references {len(missing)} "
                    f"unknown item IDs ({cells:,} cells); wrote ITEM_<id> "
                    f"placeholders instead.")
        log.debug(f"SpeacialCompensation.gsf most-missed IDs: "
                  f"{missing.most_common(5)}.")
    log.debug(f"SpeacialCompensation.gsf: {seen:,} item ids across "
              f"{case + 1:,} case group(s).")
    return with_banner(("\r\n".join(out) + "\r\n").encode("utf-8"))


def decompile_abuse(dec: bytes) -> bytes:
    words = []
    for i in range(len(dec) // 15):
        w = dec[i * 15:(i + 1) * 15].split(b"\x00")[0]
        words.append(w)
    log.debug(f"Script1.gsf: {len(words)} abuse words.")
    return b"\r\n".join(words) + b"\r\n"


def gsf_main(argv):
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
    if not rest or out is None:
        print(__doc__)
        print("usage: python gsf_decompiler.py input --out out")
        return 2
    srcs = []
    for a in rest:
        p = Path(a)
        if p.is_dir():
            srcs += sorted(p.glob("*.gsf"))
        elif p.exists():
            srcs.append(p)
    out.mkdir(parents=True, exist_ok=True)
    forbid = {Path("input").resolve(), Path("example").resolve()}
    if out.resolve() in forbid:
        slog.error(f"--out must not point at {out.resolve()}.")
        return 1
    namemap = {}
    try:
        namemap = build_namemap(srcs)
        if namemap:
            slog.info(f"Loaded {len(namemap):,} item names.")
    except Exception as e:
        slog.warning(f"Could not load item names ({e}).")
    for src in srcs:
        try:
            data = decompile_gsf(src, namemap)
        except RuntimeError as e:
            if str(e).startswith("SKIP:"):
                reason = str(e)[len("SKIP:"):].strip()
                slog.warning(f"Skipped {src.name}: {reason}.")
                continue
            raise
        dest = out / output_name_for_gsf(src.name)
        dest.write_bytes(data)
        slog.info(f"Wrote {dest} ({len(data):,} bytes).")
    return 0


def output_name_for_ryl(filename: str) -> str:
    if Path(filename).suffix.lower() == ".mcf":
        return output_name_for_mcf(filename)
    return output_name_for_gsf(filename)


def build_ryl_namemap(files, version=None) -> dict:
    return build_namemap(files, version)


def decompile_ryl_mcf(src: Path):
    txt, _parsed, calls, anomalies, arg_anomalies = decompile_file(src)
    return txt, len(calls), len(anomalies) + len(arg_anomalies)


def decompile_ryl_gsf(src: Path, namemap: dict, version=None) -> bytes:
    return decompile_gsf(src, namemap, version)


if __name__ == "__main__":
    import sys as _sys
    _sys.exit("run main.py instead "
              "(legacy entry points: mcf_main / gsf_main)")
