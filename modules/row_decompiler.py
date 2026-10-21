
import struct
from pathlib import Path
from collections import Counter

from modules.logging import get_logger
from modules.ryl_decompiler import (
    cstr,
    emit_item,
    emit_monster,
    field,
    with_banner,
    ITEM_HDR,
    SKILL_HDR,
    coerce_text,
)

log = get_logger()

HERE = Path(__file__).parent

_ROW_TABLES = None


def _row_tables():
    global _ROW_TABLES
    if _ROW_TABLES is None:
        from modules.xor_crypt import raw_page, PAGE_COUNT, VERSIONS
        _raw = {}
        for _v in range(VERSIONS):
            for _p in range(PAGE_COUNT):
                _raw[(_v, _p)] = bytes(raw_page(_v, _p))
        _ROW_TABLES = {}
        for _v in range(VERSIONS):
            for _p in range(PAGE_COUNT):
                if _v in (2, 3):
                    _ROW_TABLES[(_v, _p)] = bytes(
                        a ^ b for a, b in zip(_raw[(_v, _p)], _raw[(0, _p)]))
                else:
                    _ROW_TABLES[(_v, _p)] = _raw[(_v, _p)]
    return _ROW_TABLES


ROW_PAGES = {"ItemScript.gsf": (3, 4), "ItemScriptEx.gsf": (3, 4),
             "Chemical.gsf": (3, 4),
             "MonsterProtoType.gsf": (3, 2), "SkillScript.gsf": (3, 3)}

ROW_ITEM_ROW = 620
ROW_ITEM_CORE = 616
ROW_MONSTER_ROW = 560
ROW_MONSTER_CORE = 552
ROW_CHEM_ROW = 24
ROW_ITEMEX_ROW = 304

# Other ROW builds ship differently-cased file names and item rows
# without the 4-byte trailer (616-byte rows instead of 620).  The crypt
# pages match the original builds (verified by name-token decoding).
ROW_OTHER_PAGES = {"Itemscript.gsf": (3, 4), "ItemScriptEx.gsf": (3, 4),
                   "Chemical.gsf": (3, 4),
                   "Monsterprototype.gsf": (3, 2),
                   "SkillScript.gsf": (3, 3),
                   "SkillScriptEx.gsf": None}
ROW_VARIANT_PAGES = {"Other": ROW_OTHER_PAGES}
ROW_VARIANT_ITEM_STRIDE = {"Other": ROW_ITEM_CORE}

# NPC/quest/world-op scripts of the other ROW builds use the same MCF
# container but XOR every 4 bytes with this key (the classic RYL builds
# use MCF_KEY 0x425529AC in ryl_decompiler).
ROW_MCF_KEY = 0xE2E5DCE7

ROW_ITEM_HDR = ITEM_HDR + ["Trailer"]

ROW_CHEM_HDR = (b"PickkingItem\t\t\tTargetItem\t\t\tResultItem\t\t\t"
                b"Extra\t\t\t\t\t\r\n"
                b"Name\tID\tNum\tName\tID\tNum\tName\tID\tNum\t"
                b"ItemID\tAbilityID\tAbilityLevel\tQuestID\tPercent\r\n")

# Extra op signatures used by the other ROW builds' quest/NPC .mcf files.
# Most mirror their closest known sibling (AddPopup, QuestStart,
# QuestSkillPointBonus, Event_MsgBox, Event_Award, Trigger_LevelTalk);
# QuestStartLevel, Event_AlarmBox, Event_AwardItemClass, Event_AwardItemID
# and QuestAbilityPoint are verified against the call sites they fired in
# (same mov/push arg transports, same `add esp` trailing argument counts,
# string arguments resolved as strbuf offsets like every known op).
ROW_SIGS_EXT = {
    "AddPopupGuild": {7: (["i", "i", "i", "s", "i", "i", "i"], 1, 0)},
    "AddPopupAbility": {7: (["i", "i", "i", "s", "i", "i", "i"], 1, 0)},
    "AddPopupFame": {7: (["i", "i", "i", "s", "i", "i", "i"], 1, 0)},
    "QuestStartLevel": {7: (["i", "i", "i", "i", "i", "i", "b"], 0, 0)},
    "QuestStartFame": {7: (["i", "i", "i", "i", "i", "i", "b"], 0, 0)},
    "QuestAbilityPoint": {1: (["i"], 1, 0)},
    "Event_AlarmBox": {1: (["s"], 3, 0)},
    "Event_AwardItemClass": {5: (["i"] * 5, 3, 0)},
    "Event_AwardItemID": {4: (["i"] * 4, 3, 0)},
    "Event_AwardAbility": {4: (["i"] * 4, 3, 0)},
    "Trigger_AbilityTalk": {3: (["i", "i", "s"], 2, 0)},
    "Trigger_FameTalk": {3: (["i", "i", "s"], 2, 0)},
    # extended arities of ops that already exist in the classic builds
    "Phase_Target": {3: (["i", "i", "i"], 2, 0)},
    "Event_Move": {4: (["i", "f", "f", "f"], 3, 0)},
}


def row_setup(version_id=None):
    """Version-aware ROW wiring: (crypt pages registry, item stride).

    `version_id` is the rDec menu value, e.g. 'ROW', 'ROW/Origin' or
    'ROW/Other'.  The original ROW builds keep the exact legacy registry
    and 620-byte rows; variant folders use their own page table.
    """
    leaf = version_id.split("/")[-1] if version_id and "/" in version_id \
        else None
    if leaf and leaf in ROW_VARIANT_PAGES:
        return (ROW_VARIANT_PAGES[leaf],
                ROW_VARIANT_ITEM_STRIDE.get(leaf, ROW_ITEM_ROW))
    return ROW_PAGES, ROW_ITEM_ROW


def output_name_for_row(filename: str) -> str:
    return Path(filename).stem + ".txt"


def build_row_namemap(files, pages=None, stride=None) -> dict:
    for src in files:
        if Path(src).name.lower() == "itemscript.gsf":
            return row_item_namemap(load_row_gsf(Path(src), pages),
                                    stride or ROW_ITEM_ROW)
    return {}


def ror1(b):
    return ((b << 7) & 0xFF) | (b >> 1)


def load_row_gsf(path: Path, pages=None):
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
    registry = ROW_PAGES if pages is None else pages
    try:
        ver, page = registry[path.name]
    except KeyError:
        raise ValueError(f"No ROW crypt page is registered for {path.name} "
                         f"(known: {sorted(registry)}).")
    row = _row_tables()[(ver, page)]
    return bytes((ror1(c) ^ row[i % 40]) for i, c in enumerate(body))


def row_item_namemap(dec: bytes, stride: int = ROW_ITEM_ROW) -> dict:
    m = {}
    for i in range(len(dec) // stride):
        r = dec[i * stride:(i + 1) * stride]
        m[struct.unpack_from("<H", r, 0)[0]] = \
            field(cstr(r[52:116]))
    return m


def _eol_of(body: bytes) -> bytes:
    return b"\r\n" if b"\r\n" in body else b"\n"


def decompile_row_gsf(src: Path, namemap: dict, pages=None,
                      item_stride: int = None) -> bytes:
    src = Path(src)
    if src.name.lower() == "skillscriptex.gsf":
        import shutil
        import subprocess
        import tempfile
        jar = HERE / "unluac.jar"
        if not (shutil.which("java") and jar.exists()):
            raise RuntimeError("SKIP: needs java + modules/unluac.jar")
        log.debug("SkillScriptEx.gsf: decompiling Lua bytecode with unluac.")
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "SkillScriptEx.txt"
            r = subprocess.run(["java", "-jar", str(jar), str(src),
                                "-o", str(dest)],
                               capture_output=True, text=True)
            if r.returncode != 0 or not dest.exists():
                raise RuntimeError(f"unluac failed: {(r.stderr or '')[:200]}")
            body = dest.read_bytes()
            log.debug(f"SkillScriptEx.gsf: unluac returned {len(body):,} "
                      f"bytes.")
            return with_banner(body, _eol_of(body))
    dec = load_row_gsf(src, pages)
    low = src.name.lower()
    if low == "itemscript.gsf":
        return with_banner(decompile_row_item(
            dec, item_stride or ROW_ITEM_ROW), b"\n")
    if low == "itemscriptex.gsf":
        return with_banner(decompile_row_itemex(dec), b"\n")
    if low == "monsterprototype.gsf":
        return with_banner(decompile_row_monster(dec))
    if low == "skillscript.gsf":
        from modules.ryl_decompiler import decompile_skill
        return with_banner(decompile_skill(dec))
    if low == "chemical.gsf":
        return with_banner(decompile_row_chemical(dec, namemap))
    raise ValueError(f"{src.name}: no ROW GSF handler registered")


def decompile_row_item(dec: bytes, stride: int = ROW_ITEM_ROW) -> bytes:
    trailer = stride == ROW_ITEM_ROW
    if len(dec) % stride:
        raise ValueError(f"Item payload {len(dec):,} is not a multiple "
                         f"of {stride}.")
    n = len(dec) // stride
    log.debug(f"ItemScript.gsf (ROW): {n:,} item rows of {stride} bytes.")
    hdr = ROW_ITEM_HDR if trailer else ITEM_HDR
    nonzero = 0
    lines = ["\t".join(hdr)]
    for i in range(n):
        r = dec[i * stride:(i + 1) * stride]
        cells = list(emit_item(r[:ROW_ITEM_CORE]))
        if trailer:
            cell = struct.unpack_from("<I", r, ROW_ITEM_CORE)[0]
            nonzero += cell != 0
            cells.append(str(cell))
        lines.append("\t".join(cells))
    if trailer and nonzero:
        log.info(f"ItemScript.gsf (ROW): {nonzero:,}/{n:,} rows carry a "
                 f"nonzero trailer value (kept in the Trailer column).")
    return ("\n".join(lines) + "\n").encode("utf-8")


def decompile_row_monster(dec: bytes) -> bytes:
    if len(dec) % ROW_MONSTER_ROW:
        raise ValueError(f"Monster payload {len(dec):,} is not a multiple "
                         f"of {ROW_MONSTER_ROW}.")
    n = len(dec) // ROW_MONSTER_ROW
    log.debug(f"MonsterProtoType.gsf (ROW): {n:,} monster rows.")
    bad = sum(dec[i * ROW_MONSTER_ROW + ROW_MONSTER_CORE:
                  (i + 1) * ROW_MONSTER_ROW] != b"\x00" * 8
              for i in range(n))
    if bad:
        log.warning(f"MonsterProtoType.gsf (ROW): {bad:,}/{n:,} rows have "
                    f"a nonzero 8B trailer (dropped).")
    return ("\r\n".join(
        "\t".join(emit_monster(dec[i * ROW_MONSTER_ROW:
                                   i * ROW_MONSTER_ROW + ROW_MONSTER_CORE]))
        for i in range(n)) + "\r\n").encode("utf-8")


def decompile_row_chemical(dec: bytes, namemap: dict) -> bytes:
    if len(dec) % ROW_CHEM_ROW:
        raise ValueError(f"Chemical payload {len(dec):,} is not a multiple "
                         f"of {ROW_CHEM_ROW}.")
    out = [ROW_CHEM_HDR.rstrip(b"\r\n")]
    missing = Counter()
    n = len(dec) // ROW_CHEM_ROW
    for i in range(n):
        r = dec[i * ROW_CHEM_ROW:(i + 1) * ROW_CHEM_ROW]
        pk, tg, rs = struct.unpack_from("<HHH", r, 0)
        cells = []
        for vid, num in ((pk, r[6]), (tg, r[7]), (rs, r[8])):
            nm = namemap.get(vid)
            if nm is None:
                missing[vid] += 1
                nm = f"ITEM_{vid}"
            cells += [nm, str(vid), str(num)]
        cells += [str(struct.unpack_from("<I", r, 12)[0]),
                  str(struct.unpack_from("<H", r, 16)[0]),
                  str(r[18]),
                  str(struct.unpack_from("<H", r, 20)[0]),
                  str(r[22])]
        out.append("\t".join(cells).encode("utf-8"))
    if missing:
        cells = sum(missing.values())
        log.warning(f"Chemical.gsf (ROW) references {len(missing)} unknown "
                    f"item IDs ({cells:,} cells); wrote ITEM_<id> "
                    f"placeholders instead.")
        log.debug(f"Chemical.gsf (ROW) most-missed IDs: "
                  f"{missing.most_common(5)}.")
    log.debug(f"Chemical.gsf (ROW): {n:,} recipes.")
    return b"\r\n".join(out) + b"\r\n"


def decompile_row_itemex(dec: bytes) -> bytes:
    if len(dec) % ROW_ITEMEX_ROW:
        raise ValueError(f"ItemEx payload {len(dec):,} is not a multiple "
                         f"of {ROW_ITEMEX_ROW}.")
    n = len(dec) // ROW_ITEMEX_ROW
    log.debug(f"ItemScriptEx.gsf (ROW): {n:,} set records.")
    lines = ["\t".join(["ID", "F1", "F2", "F3", "F4", "Name", "Desc"])]
    for i in range(n):
        r = dec[i * ROW_ITEMEX_ROW:(i + 1) * ROW_ITEMEX_ROW]
        sid, f1, f2, f3, f4 = struct.unpack_from("<IHHII", r, 0)
        name = field(cstr(r[16:]))
        p = 16 + len(cstr(r[16:])) + 1
        while p < len(r) and r[p] == 0:
            p += 1
        desc = field(cstr(r[p:]))
        desc = desc.strip("\r\n").replace("\r\n", "\\n").replace("\n", "\\n")
        lines.append("\t".join([str(sid), str(f1), str(f2), str(f3),
                                 str(f4), name, desc]))
    return ("\n".join(lines) + "\n").encode("utf-8")


NCF_HEADER_TAG = 0x11ECC666

NCF_STATE0 = 0x11045
NCF_MULT = 0x14A3E
NCF_ADD = 0x13257


def parse_blocks(data: bytes) -> list:
    blocks = []
    off = 0
    total = len(data)
    while off + 4 <= total:
        (n,) = struct.unpack_from("<I", data, off)
        if off + 4 + n > total:
            raise ValueError(f"NCF block at offset {off:,} claims length "
                             f"{n:,}, exceeding file size {total:,}.")
        blocks.append(data[off + 4:off + 4 + n])
        off += 4 + n
    if off != total:
        raise ValueError(f"NCF chain ends at {off:,}, file is {total:,} "
                         f"bytes (trailing {total - off:,} bytes).")
    return blocks


def autokey_decrypt(data: bytes, state: int = NCF_STATE0) -> bytes:
    out = bytearray(len(data))
    for i, cipher in enumerate(data):
        out[i] = cipher ^ ((state >> 8) & 0xFF)
        state = ((cipher + state) * NCF_MULT + NCF_ADD) & 0xFFFFFFFF
    return bytes(out)


def describe_blocks(blocks: list) -> dict:
    tags = Counter()
    groups = Counter()
    for b in blocks:
        tag = b[:4].hex() if len(b) >= 4 else f"short{len(b)}"
        tags[tag] += 1
        groups[(tag, len(b))] += 1
    top_tag, top_count = tags.most_common(1)[0]
    dup_groups = sum(1 for c in Counter(bytes(b) for b in blocks
                                        if b).values() if c > 1)
    return {"blocks": len(blocks), "top_tag": top_tag,
            "top_count": top_count,
            "zero_blocks": sum(1 for b in blocks if not b),
            "distinct_tags": len(tags),
            "tag_census": tags.most_common(10),
            "top_groups": sorted(groups.items(), key=lambda kv: -kv[1])[:10],
            "duplicate_groups": dup_groups}


def output_name_for_ncf(filename: str) -> str:
    return output_name_for_row(filename)


def _check_text(line: bytes, where: str):
    for c in line:
        if c < 9 or (13 < c < 32) or c == 127:
            raise ValueError(f"{where}: decrypted block is not text "
                             f"(byte 0x{c:02X} in {line[:48]!r}).")


def decompile_ncf(src: Path, namemap: dict = None) -> bytes:
    from modules.banners import file_banner
    from modules.ryl_decompiler import clean_text, smart_str
    from modules.translations import translate_text
    src = Path(src)
    raw = src.read_bytes()
    log.debug(f"{src.name}: read {len(raw):,} bytes.")
    blocks = parse_blocks(raw)
    info = describe_blocks(blocks)
    log.debug(f"{src.name}: {info['blocks']:,} blocks, "
              f"{info['zero_blocks']:,} blank, "
              f"dominant prefix {info['top_tag']} "
              f"x{info['top_count']:,}.")
    out = []
    for i, body in enumerate(blocks):
        line = autokey_decrypt(body)
        _check_text(line, f"{src.name} block {i}")
        if line:
            text = clean_text(smart_str(line))
            text = text.replace("\r\n", "\\n").replace("\n", "\\n")
            text = translate_text(text, namemap)
            out.append(text)
        else:
            out.append("")
    log.debug(f"{src.name}: recovered {len(out):,} lines.")
    head = list(file_banner())
    head.append("")
    head.extend(out)
    return "\r\n".join(head).encode("utf-8")


def _probe_mcf(dec: bytes) -> dict:
    """Strict MCF container validation; raises on a wrong-key decode."""
    from modules.ryl_decompiler import parse
    g, s, f = struct.unpack_from("<iii", dec, 0)
    for name, v in (("g", g), ("s", s), ("f", f)):
        if not 0 <= v <= (1 << 22):
            raise ValueError(f"{name}={v:,} out of range")
    P = parse(dec)
    code = len(P["code"])
    if not (P["strbuf"] and code):
        raise ValueError("empty string/code payload")
    for off in P["funcmap"]:
        if not 0 <= off < code:
            raise ValueError(f"funcmap offset {off:,} outside the "
                             f"{code:,}-byte code payload")
    return P


def decompile_row_mcf(src: Path) -> bytes:
    """Decompile a ROW .mcf op script (NPC / quest / world).

    The container matches the classic RYL MCF layout, but other ROW
    builds XOR every 4 bytes with ROW_MCF_KEY instead of MCF_KEY, so
    both keys are probed (the classic one first, so original builds
    keep their exact decode path).
    """
    from modules.ryl_decompiler import decompile_file, decode, MCF_KEY
    src = Path(src)
    raw = src.read_bytes()
    log.debug(f"{src.name}: read {len(raw):,} bytes.")
    row_key = struct.pack("<I", ROW_MCF_KEY)
    tries = ((None, f"0x{MCF_KEY:08X}"), (row_key, f"0x{ROW_MCF_KEY:08X}"))
    errors = []
    for key, label in tries:
        if key is None:
            dec = decode(raw)
        else:
            dec = bytes(b ^ key[i % 4] for i, b in enumerate(raw))
        try:
            _probe_mcf(dec)
        except Exception as e:
            errors.append(f"{label} -> {type(e).__name__}: {e}")
            continue
        log.debug(f"{src.name}: decoded with MCF key {label}.")
        txt, _P, calls, anomalies, arg_anom = decompile_file(
            src, dec=dec, sigs=ROW_SIGS_EXT)
        return txt, len(calls), len(anomalies) + len(arg_anom)
    raise RuntimeError(f"No ROW MCF key fits {src.name}: "
                       f"{'; '.join(errors)}")


def decompile_row(src: Path, namemap: dict) -> bytes:
    src = Path(src)
    if src.suffix.lower() == ".ncf":
        return decompile_ncf(src, namemap)
    return decompile_row_gsf(src, namemap)
