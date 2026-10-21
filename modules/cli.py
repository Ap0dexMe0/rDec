
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
    "ROW": "ROW",
    "ROW/Origin": "Original ROW (Rowplayon)",
    "ROW/Other": "Other ROW Versions",
    "RYL1": "Risk Your Life 1 (RYL1)",
    "RYL2/V1700-V1900": "RYL2 V1700–V1900",
    "RYL2/V2000-V2240": "RYL2 V2000–V2240",
}

# Fixed main-menu games.  Games with a `group` folder open a version
# submenu (configured entries first, then any newly discovered
# sub-folders); a game without `versions` decompiles directly.
GAMES = (
    {"id": "ROW", "title": "Return of Warriors (ROW)",
     "group": "ROW", "menu": "ROW VERSIONS",
     "versions": (("Origin", "Original ROW (Rowplayon)"),
                  ("Other", "Other ROW Versions"))},
    {"id": "RYL1", "title": "Risk Your Life 1 (RYL1)",
     "group": "RYL1", "menu": None, "versions": None},
    {"id": "RYL2", "title": "Risk Your Life 2 (RYL2)",
     "group": "RYL2", "menu": "RYL2 VERSIONS",
     "versions": (("V1700-V1900", "V1700–V1900"),
                  ("V2000-V2240", "V2000–V2240"))},
)

_MENU_WIDTH = 78
_EXIT_WORDS = {"0", "q", "quit", "exit", "back"}
_PROMPT = ""


def project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def script_dir(root=None) -> Path:
    return (root or project_root()) / "script"


def list_versions(root=None) -> list:
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
    return version_id.replace("/", " ")


def version_row(version_id: str) -> str:
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


def game_version_choices(game: dict, root=None) -> list:
    """(version_id, label) pairs for a game's submenu.

    Configured versions come first (in menu order, only when their
    folder exists), then any newly discovered sub-folders of the game
    group so auto-discovery keeps working without code changes.
    """
    group = game["group"]
    configured = [(f"{group}/{sub}", label)
                  for sub, label in (game["versions"] or ())]
    known = {vid for vid, _label in configured}
    existing = [(vid, label) for vid, label in configured
                if (script_dir(root) / vid).is_dir()]
    extras = []
    for vid in list_versions(root):
        if vid.startswith(f"{group}/") and vid not in known:
            extras.append((vid, version_row(vid)))
    return existing + sorted(extras)


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
    supported, unsupported = discover_files(base)
    groups = {}
    for _path, key in supported:
        groups[key] = groups.get(key, 0) + 1
    breakdown = ", ".join(f"{c:,} .{key}"
                          for key, c in sorted(groups.items())) or "none"
    if unsupported:
        breakdown += f" (+{len(unsupported):,} unsupported)"
    return len(supported), breakdown



def _fmt(n: int) -> str:
    return f"{n:,}"


def _fresh() -> None:
    try:
        clear_and_print()
    except Exception:
        pass


def _title(text: str) -> None:
    bar = "═" * _MENU_WIDTH
    pad = max(0, (_MENU_WIDTH - len(text)) // 2)
    right = " " * max(0, _MENU_WIDTH - len(text) - pad)
    body = " " * pad + f"{Style.BRIGHT}{Fore.LIGHTYELLOW_EX}" \
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
    while True:
        try:
            _fresh()
            _title("MAIN MENU")
            _rows([game["title"] for game in GAMES], "Exit")
            print()
            picked = _pick("Select a game", len(GAMES))
            if picked == 0:
                log.info("Goodbye!")
                return 0
            game = GAMES[picked - 1]
            if game["versions"] is None:
                _flow_game(run, game["id"])
            else:
                _flow_game_versions(run, game)
        except (KeyboardInterrupt, EOFError):
            log.info("Session ended. Goodbye!")
            return 0


def _flow_game_versions(run, game: dict) -> None:
    choices = game_version_choices(game)
    if not choices:
        log.error(f"No version folders found under "
                  f"{script_dir() / game['group']}.")
        _pause()
        return
    _fresh()
    _title(game["menu"])
    _rows([label for _vid, label in choices], "Back")
    print()
    picked = _pick("Select a version", len(choices))
    if picked == 0:
        log.info("Back to the main menu - nothing was decompiled.")
        return
    version_id, _label = choices[picked - 1]
    _flow_game(run, version_id)


def _flow_game(run, version_id: str) -> None:
    _fresh()
    try:
        base = resolve_version(version_id)
    except ValueError as e:
        log.error(str(e))
        _pause()
        return
    label = version_row(version_id)
    log.info(f"Scanning {label} ({base}) ...")
    count, breakdown = scan_summary(base)
    if not count:
        log.warning(f"No supported files found in {label} ({breakdown}).")
        _pause()
        return
    log.info(f"Found {_fmt(count)} supported file"
             f"{'s' if count != 1 else ''} in {label} ({base}): "
             f"{breakdown}.")
    if not _confirm(f"Decompile all supported files in {label}?"):
        log.info("Cancelled - nothing was decompiled.")
        return
    try:
        rc = run(version_id)
    except (KeyboardInterrupt, EOFError):
        log.warning("Decompilation cancelled.")
        return
    if rc != 0:
        log.warning(f"rDec finished with errors (exit code {rc}).")
    _pause()
