#!/usr/bin/env python3

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
        import re as _re
        _src = (HERE.parent.parent / "RYLGameConverter" / "RylServerProject"
                / "RylServerLibrary" / "Network" / "XORCrypt"
                / "XORCryptoCodeList.cpp").read_text()
        _vals = [int(x, 16) for x in _re.findall(r"0x([0-9A-Fa-f]{2})", _src)]
        if len(_vals) != 1600:
            raise ValueError(f"C++ table has {len(_vals)} bytes, want 1600")
        _raw = {}
        _k = 0
        for _v in range(4):
            for _p in range(10):
                _raw[(_v, _p)] = bytes(_vals[_k:_k + 40])
                _k += 40
        _ROW_TABLES = {}
        for _v in range(4):
            for _p in range(10):
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

ROW_ITEM_HDR = ITEM_HDR + ["Trailer"]

ROW_CHEM_HDR = (b"PickkingItem\t\t\tTargetItem\t\t\tResultItem\t\t\t"
                b"Extra\t\t\t\t\t\r\n"
                b"Name\tID\tNum\tName\tID\tNum\tName\tID\tNum\t"
                b"ItemID\tAbilityID\tAbilityLevel\tQuestID\tPercent\r\n")


def output_name_for_row(filename: str) -> str:
    return Path(filename).stem + ".txt"


def build_row_namemap(files) -> dict:
    for src in files:
        if Path(src).name == "ItemScript.gsf":
            return row_item_namemap(load_row_gsf(Path(src)))
    return {}


def ror1(b):
    return ((b << 7) & 0xFF) | (b >> 1)


def load_row_gsf(path: Path):
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
        ver, page = ROW_PAGES[path.name]
    except KeyError:
        raise ValueError(f"No ROW crypt page is registered for {path.name} "
                         f"(known: {sorted(ROW_PAGES)}).")
    row = _row_tables()[(ver, page)]
    return bytes((ror1(c) ^ row[i % 40]) for i, c in enumerate(body))


def row_item_namemap(dec: bytes) -> dict:
    m = {}
    for i in range(len(dec) // ROW_ITEM_ROW):
        r = dec[i * ROW_ITEM_ROW:(i + 1) * ROW_ITEM_ROW]
        m[struct.unpack_from("<H", r, 0)[0]] = \
            field(cstr(r[52:116]))
    return m


def _eol_of(body: bytes) -> bytes:
    return b"\r\n" if b"\r\n" in body else b"\n"


def decompile_row_gsf(src: Path, namemap: dict) -> bytes:
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
    dec = load_row_gsf(src)
    if src.name == "ItemScript.gsf":
        return with_banner(decompile_row_item(dec), b"\n")
    if src.name == "ItemScriptEx.gsf":
        return with_banner(decompile_row_itemex(dec), b"\n")
    if src.name == "MonsterProtoType.gsf":
        return with_banner(decompile_row_monster(dec))
    if src.name == "SkillScript.gsf":
        from modules.ryl_decompiler import decompile_skill
        return with_banner(decompile_skill(dec))
    if src.name == "Chemical.gsf":
        return with_banner(decompile_row_chemical(dec, namemap))
    raise ValueError(f"{src.name}: no ROW GSF handler registered")


def decompile_row_item(dec: bytes) -> bytes:
    if len(dec) % ROW_ITEM_ROW:
        raise ValueError(f"Item payload {len(dec):,} is not a multiple "
                         f"of {ROW_ITEM_ROW}.")
    n = len(dec) // ROW_ITEM_ROW
    log.debug(f"ItemScript.gsf (ROW): {n:,} item rows.")
    nonzero = 0
    lines = ["\t".join(ROW_ITEM_HDR)]
    for i in range(n):
        r = dec[i * ROW_ITEM_ROW:(i + 1) * ROW_ITEM_ROW]
        cells = list(emit_item(r[:ROW_ITEM_CORE]))
        trailer = struct.unpack_from("<I", r, ROW_ITEM_CORE)[0]
        nonzero += trailer != 0
        cells.append(str(trailer))
        lines.append("\t".join(cells))
    if nonzero:
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


def decompile_ncf(src: Path) -> bytes:
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
            text = translate_text(text)
            out.append(text)
        else:
            out.append("")
    log.debug(f"{src.name}: recovered {len(out):,} lines.")
    head = list(file_banner())
    head.append("")
    head.extend(out)
    return "\r\n".join(head).encode("utf-8")


def decompile_row(src: Path, namemap: dict) -> bytes:
    src = Path(src)
    if src.suffix.lower() == ".ncf":
        return decompile_ncf(src)
    return decompile_row_gsf(src, namemap)
