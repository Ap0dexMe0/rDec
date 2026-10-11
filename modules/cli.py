"""CLI + dynamic resolution for MCFDECOMPILER (stdlib only).

Only two user-facing arguments: --version and -d/--decompile.
Game versions come from the real subdirectories of script/ — adding a new
version directory needs no code changes. The input directory is always
script/<version>/, resolved automatically.
"""

import argparse
from pathlib import Path

from modules.logging import get_logger

log = get_logger()

SUPPORTED_SUFFIXES = (".mcf", ".gsf")
HANDLERS = {".mcf": "mcf", ".gsf": "gsf"}  # suffix -> handler key


def project_root() -> Path:
    """Repository root, independent of the current working directory."""
    return Path(__file__).resolve().parent.parent


def script_dir(root=None) -> Path:
    return (root or project_root()) / "script"


def list_versions(root=None) -> list:
    """Available game versions = subdirectories of script/ (sorted)."""
    base = script_dir(root)
    if not base.is_dir():
        return []
    return sorted(p.name for p in base.iterdir() if p.is_dir())


def resolve_version(version, root=None) -> Path:
    """Validate a version against discovered versions; return its dir."""
    available = list_versions(root)
    if version not in available:
        raise ValueError(
            f"Unknown version {version!r} "
            f"(available: {', '.join(available) if available else 'none'}; "
            f"script directory: {script_dir(root)})."
        )
    return script_dir(root) / version


def discover_files(base: Path):
    """Recursively collect files under base.

    Returns (supported, unsupported) where supported is a sorted list of
    (path, handler_key) and unsupported a sorted list of other files.
    """
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
        # allow_abbrev=False: keeps `-d` usable next to `--decompile`
        # (otherwise `--d` is ambiguous) while exact flags still work.
        allow_abbrev=False,
        description="Decompile RYL .mcf/.gsf script assets for a game version.",
    )
    parser.add_argument("--version", required=True,
                        help="game version: a subdirectory of script/ "
                             "(ROW, RYL1, RYL2, ...)")
    parser.add_argument("-d", "--decompile", action="store_true",
                        help="decompile every supported .mcf/.gsf file found")
    return parser
