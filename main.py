#!/usr/bin/env python3

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    from modules.banners import clear_and_print
except Exception:
    def clear_and_print():
        pass
from modules.cli import (build_parser, discover_files, resolve_version,
                         version_lines)
from modules.logging import setup

log = setup()


def _count(n: int, singular: str, plural: str = "") -> str:
    noun = singular if n == 1 else (plural or singular + "s")
    return f"{n:,} {noun}"


def _output_for(src: Path, base: Path, handler: str) -> Path:
    if handler == "mcf":
        from modules.ryl_decompiler import output_name_for_mcf \
            as output_name_for
    elif handler == "ncf":
        from modules.row_decompiler import output_name_for_ncf \
            as output_name_for
    else:
        from modules.ryl_decompiler import output_name_for_gsf \
            as output_name_for
    return base / src.relative_to(base).parent / output_name_for(src.name)


def _decompile_mcf(src: Path):
    from modules.ryl_decompiler import decompile_ryl_mcf
    return decompile_ryl_mcf(src)


def _decompile_gsf(src: Path, namemap: dict) -> bytes:
    from modules.ryl_decompiler import decompile_ryl_gsf
    return decompile_ryl_gsf(src, namemap)


def _decompile_row_gsf(src: Path, namemap: dict) -> bytes:
    from modules.row_decompiler import decompile_row_gsf
    return decompile_row_gsf(src, namemap)


def _decompile_ncf(src: Path) -> bytes:
    from modules.row_decompiler import decompile_ncf
    return decompile_ncf(src)


def run(version: str, base_dir=None) -> int:
    started = time.monotonic()
    try:
        version_dir = resolve_version(version)
    except ValueError as e:
        log.error(str(e))
        return 2
    base = Path(base_dir).resolve() if base_dir else version_dir
    if not base.is_dir():
        log.error(f"Input directory not found: {base}.")
        return 2
    is_row = (version == "ROW")

    supported, unsupported = discover_files(base)
    log.info(f"Decompiling version '{version}' from {base}.")
    log.info(f"Found {_count(len(supported), 'supported file')} "
             f"and {_count(len(unsupported), 'unsupported file')}.")

    namemap = {}
    if any(key == "gsf" for _, key in supported):
        if is_row:
            try:
                from modules.row_decompiler import build_row_namemap
                namemap = build_row_namemap([p for p, _ in supported])
                if namemap:
                    log.info(f"Loaded {len(namemap):,} item names "
                             f"for Chemical lookups.")
            except Exception as e:
                log.warning(f"Could not load item names ({e}); "
                            f"continuing without them.")
        else:
            try:
                from modules.ryl_decompiler import build_ryl_namemap
                namemap = build_ryl_namemap([p for p, _ in supported])
                if namemap:
                    log.info(f"Loaded {len(namemap):,} item names "
                             f"for Chemical lookups.")
            except Exception as e:
                log.warning(f"Could not load item names ({e}); "
                            f"continuing without them.")

    counts = {"ok": 0, "skipped": 0, "unsupported": len(unsupported),
              "failed": 0}
    for path, handler in supported:
        rel = path.relative_to(base)
        dest = _output_for(path, base, handler)
        if dest.suffix.lower() != ".txt":
            log.warning(f"Skipped {path.name}: the output would not be "
                        f"a .txt file.")
            counts["skipped"] += 1
            continue
        if dest.resolve() == path.resolve():
            log.warning(f"Skipped {path.name}: the output path matches "
                        f"the input path.")
            counts["skipped"] += 1
            continue
        try:
            if handler == "mcf":
                data, n_calls, n_anom = _decompile_mcf(path)
                if n_anom == 0:
                    detail = f"{n_calls:,} calls, no anomalies"
                else:
                    detail = (f"{n_calls:,} calls, "
                              f"{_count(n_anom, 'anomaly', 'anomalies')}")
            elif handler == "ncf":
                try:
                    data = _decompile_ncf(path)
                except RuntimeError as e:
                    if str(e).startswith("SKIP:"):
                        reason = str(e)[len("SKIP:"):].strip()
                        log.warning(f"Skipped {path.name}: {reason}.")
                        counts["skipped"] += 1
                        continue
                    raise
                detail = f"{len(data):,} bytes"
            elif is_row:
                try:
                    data = _decompile_row_gsf(path, namemap)
                except RuntimeError as e:
                    if str(e).startswith("SKIP:"):
                        reason = str(e)[len("SKIP:"):].strip()
                        log.warning(f"Skipped {path.name}: {reason}.")
                        counts["skipped"] += 1
                        continue
                    raise
                detail = f"{len(data):,} bytes"
            else:
                try:
                    data = _decompile_gsf(path, namemap)
                except RuntimeError as e:
                    if str(e).startswith("SKIP:"):
                        reason = str(e)[len("SKIP:"):].strip()
                        log.warning(f"Skipped {path.name}: {reason}.")
                        counts["skipped"] += 1
                        continue
                    raise
                detail = f"{len(data):,} bytes"
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
            log.info(f"Decompiled {rel} to {dest.relative_to(base)} "
                     f"({detail}).")
            counts["ok"] += 1
        except Exception as e:
            log.error(f"Could not decompile {rel} "
                      f"({type(e).__name__}: {e}).")
            counts["failed"] += 1

    if unsupported:
        groups = {}
        for path in unsupported:
            ext = path.suffix.lower() or "<no extension>"
            groups[ext] = groups.get(ext, 0) + 1
        breakdown = ", ".join(
            _count(c, f"{ext} file") for ext, c in sorted(groups.items()))
        log.info(f"Ignored {_count(len(unsupported), 'unsupported file')}: "
                 f"{breakdown}.")
    elapsed = time.monotonic() - started
    log.info(f"Finished in {elapsed:.1f} seconds: "
             f"{_count(counts['ok'], 'file')} decompiled, "
             f"{_count(counts['skipped'], 'file')} skipped, "
             f"{_count(counts['unsupported'], 'file')} left untouched, "
             f"{_count(counts['failed'], 'failure')}.")
    return 1 if counts["failed"] else 0


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.list or not args.decompile:
        for line in version_lines():
            log.info(line)
        if not args.decompile:
            return 0
    if not args.version:
        parser.error("-v/--version is required with -d/--decompile")
    return run(args.version)


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass
    try:
        clear_and_print()
    except Exception:
        pass
    sys.exit(main())
