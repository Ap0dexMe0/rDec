
import argparse
from pathlib import Path

from modules.logging import get_logger

log = get_logger()

SUPPORTED_SUFFIXES = (".mcf", ".gsf", ".ncf")
HANDLERS = {".mcf": "mcf", ".gsf": "gsf",
            ".ncf": "ncf"}

VERSIONS = {
    "RYL2": "RYL2 V1600+",
    "ROW": "Original ROW",
}


def project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def script_dir(root=None) -> Path:
    return (root or project_root()) / "script"


def list_versions(root=None) -> list:
    base = script_dir(root)
    if not base.is_dir():
        return []
    return sorted(p.name for p in base.iterdir() if p.is_dir())


def resolve_version(version, root=None) -> Path:
    available = list_versions(root)
    if version not in available:
        supported = ", ".join(f"{k} ({v})" for k, v in VERSIONS.items())
        raise ValueError(
            f"Unknown version {version!r} "
            f"(available: {', '.join(available) if available else 'none'}; "
            f"supported: {supported}; "
            f"script directory: {script_dir(root)})."
        )
    return script_dir(root) / version


def version_lines(root=None) -> list:
    lines = ["Supported versions:"]
    discovered = set(list_versions(root))
    for name in sorted(set(VERSIONS) | discovered):
        lines.append(f"  {name} - {VERSIONS.get(name, 'unverified')}")
    return lines


def discover_files(base: Path):
    supported, unsupported = [], []
    for path in sorted(base.rglob("*")):
        if not path.is_file():
            continue
        key = HANDLERS.get(path.suffix.lower())
        if key is None:
            unsupported.append(path)
        else:
            supported.append((path, key))
    return supported, unsupported


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="main.py",
        allow_abbrev=False,
        description="Decompile RYL .mcf/.gsf/.ncf script assets "
                    "for a game version.",
    )
    parser.add_argument("-v", "--version",
                        help="game version subdirectory of script/ "
                             "(required with -d)")
    parser.add_argument("-l", "--list", action="store_true",
                        help="list supported files without decompiling")
    parser.add_argument("-d", "--decompile", action="store_true",
                        help="decompile every supported file found")
    return parser
