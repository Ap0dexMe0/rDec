
from pathlib import Path

from modules.logging import get_logger

try:
    from colorama import Fore, Style
except ImportError:
    class _NoColor:
        def __getattr__(self, _name):
            return ""
    Fore, Style = _NoColor(), _NoColor()

try:
    from modules.banners import clear_and_print
except Exception:
    def clear_and_print():
        pass

log = get_logger()

SUPPORTED_SUFFIXES = (".mcf", ".gsf", ".ncf")
HANDLERS = {".mcf": "mcf", ".gsf": "gsf",
            ".ncf": "ncf"}

VERSIONS = {
    "ROW": "ROW - Original ROW",
    "RYL1": "RYL1 - Original RYL Online",
    "RYL2/V1700-V1900": "RYL2 V1700-V1900",
    "RYL2/V2000-V2240": "RYL2 V2000-V2240",
}

_MENU_WIDTH = 78
_EXIT_WORDS = {"0", "q", "quit", "exit", "back"}
_PROMPT = f"{Fore.GREEN}?{Fore.RESET} "


def project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def script_dir(root=None) -> Path:
    return (root or project_root()) / "script"


def list_versions(root=None) -> list:
    """Version IDs relative to script/ - e.g. 'ROW', 'RYL2/V1700-V1900'.

    A folder directly under script/ that contains only version folders
    (e.g. script/RYL2 with its era builds) is a group: each sub-folder
    becomes its own version ID as '<group>/<sub>'. A folder that holds
    files of its own - or neither files nor sub-folders - is a single
    version on its own.
    """
    base = script_dir(root)
    if not base.is_dir():
        return []
    ids = []
    for entry in sorted(base.iterdir()):
        if not entry.is_dir():
            continue
        subs = [p for p in sorted(entry.iterdir()) if p.is_dir()]
        if subs and not _has_files(entry):
            for sub in subs:
                ids.append(f"{entry.name}/{sub.name}")
        else:
            ids.append(entry.name)
    return ids


def _has_files(directory: Path) -> bool:
    return any(p.is_file() for p in directory.iterdir())


def _display_name(version_id: str) -> str:
    """'RYL2/V1700-V1900' -> 'RYL2 V1700-V1900'."""
    return version_id.replace("/", " ")


def version_row(version_id: str) -> str:
    """Display text for a version in menus, e.g. 'ROW - Original ROW'."""
    return VERSIONS.get(version_id) or f"{_display_name(version_id)} - unverified"


def resolve_version(version_id, root=None) -> Path:
    available = list_versions(root)
    if version_id not in available:
        names = ", ".join(version_row(v) for v in available) or "none"
        raise ValueError(
            f"Unknown version {version_id!r} "
            f"(available: {names}; "
            f"supported: {', '.join(VERSIONS)}; "
            f"script directory: {script_dir(root)})."
        )
    return script_dir(root) / Path(version_id)


def version_choices(root=None) -> list:
    """(version ID, label) pairs for every known/discovered version."""
    discovered = set(list_versions(root))
    return [(vid, VERSIONS.get(vid, "unverified"))
            for vid in sorted(set(VERSIONS) | discovered)]


def version_lines(root=None) -> list:
    lines = ["Supported versions:"]
    for vid, _label in version_choices(root):
        lines.append(f"  {version_row(vid)}")
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


def scan_summary(base: Path):
    """Count supported files per handler before decompiling a version."""
    supported, unsupported = discover_files(base)
    groups = {}
    for _path, key in supported:
        groups[key] = groups.get(key, 0) + 1
    breakdown = ", ".join(f"{c:,} .{key}"
                          for key, c in sorted(groups.items())) or "none"
    if unsupported:
        breakdown += f" (+{len(unsupported):,} unsupported)"
    return len(supported), breakdown


# ---------------------------------------------------------------------------
# Interactive prompt menu (replaces the old argparse CLI)
# ---------------------------------------------------------------------------

def _fmt(n: int) -> str:
    return f"{n:,}"


def _fresh() -> None:
    """Clear the screen and redraw the banner."""
    try:
        clear_and_print()
    except Exception:
        pass


def _title(text: str) -> None:
    bar = "═" * _MENU_WIDTH
    pad = max(0, (_MENU_WIDTH - len(text)) // 2)
    right = " " * max(0, _MENU_WIDTH - len(text) - pad)
    body = " " * pad + f"{Style.BRIGHT}{Fore.LIGHTWHITE_EX}" \
        f"{text}{Style.RESET_ALL}" + right
    print(f"{Fore.YELLOW}╔{bar}╗")
    print(f"{Fore.YELLOW}║{body}║")
    print(f"{Fore.YELLOW}╚{bar}╝")


def _rows(values: list, zero_label: str) -> None:
    for i, value in enumerate(values, 1):
        print(f"  [{Fore.GREEN}{i}{Fore.RESET}] {value}")
    print(f"  [{Fore.RED}0{Fore.RESET}] {zero_label}")


def _input(prompt: str) -> str:
    return input(f"{_PROMPT}{prompt}: ").strip()


def _confirm(question: str, default: bool = True) -> bool:
    tail = "[Y/n]" if default else "[y/N]"
    while True:
        raw = input(f"{_PROMPT}{question} {Style.BRIGHT}{tail}"
                    f"{Style.RESET_ALL} ").strip().lower()
        if not raw:
            return default
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        log.warning("Please answer 'y' or 'n'.")


def _pick(prompt: str, high: int) -> int:
    """Ask for a number 0..high; 0 (or q/exit/back) means 'go back'."""
    while True:
        raw = _input(prompt)
        if raw.isdigit() and int(raw) <= high:
            return int(raw)
        if raw.lower() in _EXIT_WORDS:
            return 0
        if raw:
            log.warning(f"{raw!r} is not a valid option - "
                        f"pick a number between 0 and {high}.")
        else:
            log.warning("Type a number (0 = back).")


def _pause() -> None:
    input(f"{_PROMPT}Press Enter to continue")


def menu_loop(run) -> int:
    """Show the main menu until the user exits. `run(version)` decompiles."""
    while True:
        try:
            _fresh()  # clear terminal + banner on every menu render
            _title("MAIN MENU")
            _rows(["Decompile a game version",
                   "List supported versions"], "Exit")
            picked = _pick("Select an option", 2)
            if picked == 0:
                log.info("Goodbye!")
                return 0
            if picked == 1:
                _flow_decompile(run)
            else:
                _flow_versions()
        except (KeyboardInterrupt, EOFError):
            log.info("Session ended. Goodbye!")
            return 0


def _flow_versions() -> None:
    _fresh()  # clear terminal + banner before the listing
    for line in version_lines():
        log.info(line)
    _pause()


def _flow_decompile(run) -> None:
    choices = version_choices()
    if not choices:
        log.error(f"No version folders found under {script_dir()}.")
        log.info("A version is any sub-folder of script/ "
                 "(e.g. script/RYL2).")
        _pause()
        return
    _fresh()  # clear terminal + banner for the version picker
    _title("SELECT A GAME VERSION")
    _rows([version_row(name) for name, _ in choices], "Back")
    picked = _pick("Select a version", len(choices))
    if picked == 0:
        log.info("Back to the menu - nothing was decompiled.")
        return
    name, _label = choices[picked - 1]
    _fresh()  # clear terminal + banner for the scan/confirm screen
    try:
        base = resolve_version(name)
    except ValueError as e:
        log.error(str(e))
        _pause()
        return
    log.info(f"Scanning {_display_name(name)} ({base}) ...")
    count, breakdown = scan_summary(base)
    if not count:
        log.warning(f"No supported files found in {name} ({breakdown}).")
        _pause()
        return
    log.info(f"Found {_fmt(count)} supported file"
             f"{'s' if count != 1 else ''} in {_display_name(name)}"
             f" ({base}): {breakdown}.")
    if not _confirm(f"Decompile all supported files in "
                    f"{version_row(name)}?"):
        log.info("Cancelled - nothing was decompiled.")
        return
    try:
        rc = run(name)
    except (KeyboardInterrupt, EOFError):
        log.warning("Decompilation cancelled.")
        return
    if rc != 0:
        log.warning(f"rDec finished with errors (exit code {rc}).")
    _pause()
