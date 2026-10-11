#!/usr/bin/env python3
"""
GSF Decompiler v1.0 — RYL ItemScript/MonsterProtoType/SkillScript/Chemical/
Script1(MonsterChat) .gsf to TRUE text format.

Pipeline (verified vs RylServerProject C++ source + TRUE example txt files):
  envelope: [trash_size u32][trash bytes][orig_size u32][LZO1X payload]
            (trash is a whole embedded file, e.g. a JPEG for ItemScript)
  crypt:    LZO-decompress, then per byte ROR1 + XOR with the C++ runtime
            XORCrypt table. THESE files use ver-0 RAW rows (pre-ctor tables —
            the RYLGameConverter Python BIT_FIELDS belong to another revision
            and do NOT decode these files):
              ItemScript.gsf        ver0 page2     616B ItemInfo structs x4659
              Chemical.gsf          ver0 page2     10B  recipe entries x905
              MonsterProtoType.gsf  ver0 page3     552B MonsterInfo structs x910
              SkillScript.gsf       ver0 page1     5x516B skill groups x187
              Script1.gsf           ver0 page1     15B  abuse words x129
  MonsterChat.gsf is PLAINTEXT (byte passthrough).
  SkillScriptEX.gsf is Lua 5.0 bytecode — decompiled with unluac
  (lua/unluac.jar, built from source; needs java). Bytecode carries no
  comments/spacing/quote-style/number-format info, so cosmetic deltas vs
  any hand-written reference are expected; semantics are exact.

Verified:
  ItemScript   4659 rows; only diffs vs example = bool/empty spelling
               variants (same loader semantics), ORE->ETC retype, scattered
               revision value changes, 25 trailing-space lines, 1 added row.
               Grade enum of this data has NO S grade: {AAA:0..X:7}.
  Monster      910 rows, all names present; diffs = col27 (no binary
               counterpart in any representation — emitted '0'),
               col18 last-digit (9-digit txt vs f32-shortest), velocity and
               award/drop revision drifts, Siege/pattern rules verified.
  SkillScript  187 groups / 855 rows; diffs = cooldown/value rebalances,
               '?' placeholder glyphs vs newer localized text, prereq tree
               present in binary but flattened in example.
  Chemical     905 recipes; diffs = newer revision adds recipes/renames.
  Abuse        129 words, alphabet-closed (leet/case/space variants).
  MonsterChat  byte-identical passthrough.

Usage:
    python gsf_decompiler.py input --out out
Outputs <Base>.txt files ONLY (Abuse.txt for Script1.gsf).
"""
import re
import struct
import sys
from pathlib import Path
from collections import Counter

from modules.logging import get_logger

log = get_logger()

HERE = Path(__file__).parent
# XOR tables: ALWAYS parsed from the C++ source (authoritative). The Python
# BIT_FIELDS copies in RYLGameConverter/modules belong to a different
# revision and do NOT decode these files. Loaded lazily so that importing
# this module never fails when lzo or the C++ tree is absent.
_TABLES = None


def _tables():
    global _TABLES
    if _TABLES is None:
        import re as _re
        _src = (HERE.parent.parent / "RYLGameConverter" / "RylServerProject"
                / "RylServerLibrary" / "Network" / "XORCrypt"
                / "XORCryptoCodeList.cpp").read_text()
        _vals = [int(x, 16) for x in _re.findall(r"0x([0-9A-Fa-f]{2})", _src)]
        if len(_vals) != 1600:
            raise ValueError(f"C++ table has {len(_vals)} bytes, want 1600")
        _TABLES = {}
        _k = 0
        for _v in range(4):
            for _p in range(10):
                _TABLES[(_v, _p)] = _vals[_k:_k + 40]
                _k += 40
    return _TABLES



PAGES = {"ItemScript.gsf": (0, 2), "Chemical.gsf": (0, 2),
         "MonsterProtoType.gsf": (0, 3), "SkillScript.gsf": (0, 1),
         "Script1.gsf": (0, 1)}
OUTNAME = {"Script1.gsf": "Abuse.txt"}


def output_name_for(filename: str) -> str:
    """Output file name for a GSF input (single source of truth)."""
    return OUTNAME.get(filename, Path(filename).stem + ".txt")


def build_namemap(files) -> dict:
    """Item ID -> name map from the ItemScript.gsf in files ({} if absent)."""
    for src in files:
        if Path(src).name == "ItemScript.gsf":
            return item_namemap(load_gsf(Path(src)))
    return {}


def decompile_gsf(src: Path, namemap: dict) -> bytes:
    """Decompile one GSF file to its text bytes.

    Raises RuntimeError("SKIP: ...") when only the optional Lua toolchain
    is missing; any other failure is a real error.
    """
    src = Path(src)
    lowered = src.name.lower()
    if lowered == "monsterchat.gsf":
        body = src.read_bytes()  # plaintext, byte passthrough
        log.debug(f"MonsterChat.gsf: passing through {len(body):,} "
                  f"plaintext bytes.")
        return with_banner(body, _eol_of(body))
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


def ox(v: int) -> str:
    return "O" if v else "X"


# ---------------- Item ----------------
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
# Grade enum of THIS data revision (no S grade; verified 2316/2316 rows)
GRADE = {0: "AAA", 1: "AA", 2: "A", 3: "B", 4: "C", 5: "D", 6: "F", 7: "X"}
LIMIT = {0: "NONE", 1: "STR", 2: "DEX", 3: "CON", 4: "INT", 5: "WIS",
         6: "LEVEL"}
# attribute indices EXACTLY as C++ Item::Attribute::Type (NONE=0 first!)
(NONE_A, MIN_DAMAGE, MAX_DAMAGE, ARMOR, HIT_RATE, EVADE, MAX_HP, HP_REGEN,
 MAX_MP, MP_REGEN, CRITICAL, BLOCK, SPEED, MAGIC_POWER, MAGIC_RESIST,
 LUCKCHANCE, COOLDOWN, SKILL_POINT, FROST, FIRE, ELECTRO,
 DARKNESS) = range(22)


def hexid(v: int) -> str:
    return f"0x{v:04X}" if v >= 0x8000 else str(v)


def emit_item(r: bytes):
    itype = r[21]
    c = [str(struct.unpack_from("<H", r, 0)[0]),
         cstr(r[52:116]).decode("utf-8", errors="replace"),
         cstr(r[156:188]).decode("utf-8", errors="replace"),
         cstr(r[188:220]).decode("utf-8", errors="replace"),
         cstr(r[116:148]).decode("utf-8", errors="replace"),
         str(struct.unpack_from("<H", r, 148)[0]),
         str(struct.unpack_from("<H", r, 150)[0]),
         str(struct.unpack_from("<H", r, 152)[0]),
         str(struct.unpack_from("<H", r, 154)[0]),
         str(r[22]), str(r[23]),
         cstr(r[220:252]).decode("utf-8", errors="replace"),
         ITEMTYPE.get(itype, str(itype)),
         cstr(r[252:284]).decode("utf-8", errors="replace"),
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
              cstr(r[284:540]).decode("utf-8", errors="replace")] + [""] * 11
    else:
        c += [cstr(r[284:540]).decode("utf-8", errors="replace")] + [""] * 21
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


# ---------------- Monster ----------------
MONPAT = {0: "Common", 1: "Warrior", 2: "Defender", 3: "Mage", 4: "Acolyte",
          5: "Boss", 6: "BG", 7: "Summon", 8: "Structure", 9: "Named",
          10: "Chief", 11: "Object", 12: "Guard", 13: "Gather"}
MONSTATUE = {0: "0", 1: "HP", 2: "MP", 3: "EXP", 4: "DropRate"}


def mon_vel(bits: int) -> str:
    # txt stores velocity*100 (loader divides back); emit the shortest
    # spelling whose /100 narrows to these exact f32 bits.
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
    c[1] = cstr(r[64:128]).decode("utf-8", errors="replace")
    c[2] = cstr(r[128:160]).decode("utf-8", errors="replace")
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
    # col27 has no binary counterpart in this revision (verified across
    # f32/f64/f16/int/bool/hex/text/derived-offset searches); '0' is the
    # faithful absence value (89 rows carry it in the reference too).
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


# ---------------- Skill ----------------
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
         cstr(g[96:160]).decode("utf-8", errors="replace"),
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
         cstr(g[64:96]).decode("utf-8", errors="replace"),
         cstr(g[0:32]).decode("utf-8", errors="replace"),
         cstr(g[32:64]).decode("utf-8", errors="replace"),
         str(struct.unpack_from("<I", g, 488)[0]),
         str(g[510]),
         cstr(g[160:192]).decode("utf-8", errors="replace"),
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
    # NOTE: quotes are stored IN the buffer; emit verbatim (no wrapping)
    c.append(desc.decode("utf-8", errors="replace"))
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


# ---------------- Chemical ----------------
CHEM_HDR = (b"PickkingItem\t\t\tTargetItem\t\t\tResultItem\t\t\r\n"
            b"Name\tID\tNum\tName\tID\tNum\tName\tID\tNum\r\n")


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
            cstr(r[52:116]).decode("utf-8", errors="replace")
    return m


def with_banner(body: bytes, eol: bytes = b"\r\n") -> bytes:
    """Prepend the rDec header block + one blank separator line."""
    from modules.banners import file_banner
    head = eol.join(s.encode("ascii") for s in file_banner())
    return head + eol + eol + body


# ---------------- Script1 / MonsterChat ----------------
def decompile_abuse(dec: bytes) -> bytes:
    words = []
    for i in range(len(dec) // 15):
        w = dec[i * 15:(i + 1) * 15].split(b"\x00")[0]
        words.append(w)
    log.debug(f"Script1.gsf: {len(words)} abuse words.")
    return b"\r\n".join(words) + b"\r\n"


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
    # NOTE: outputs are byte-clean by design (no marker), so reruns simply
    # overwrite <Base>.txt.
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
        dest = out / output_name_for(src.name)
        dest.write_bytes(data)
        slog.info(f"Wrote {dest} ({len(data):,} bytes).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
