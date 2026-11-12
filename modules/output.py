import os
from pathlib import Path as _Path
try:
    from colorama import Fore, Style
except ImportError:

    class _NoColor:

        def __getattr__(self, name):
            return ''
    (Fore, Style) = (_NoColor(), _NoColor())
_PROJECT_ROOT = _Path(__file__).resolve().parent.parent
RESET = Style.RESET_ALL
GREEN = Fore.GREEN
RED = Fore.RED
YELLOW = Fore.YELLOW
VERBOSE = os.environ.get('RDEC_VERBOSE', '').strip().lower() not in ('', '0', 'false', 'no', 'off')

def short(path) -> str:
    """Compact display path: project-relative when possible, else last 3 components."""
    p = path if isinstance(path, _Path) else _Path(str(path))
    try:
        return str(p.resolve().relative_to(_PROJECT_ROOT))
    except (ValueError, OSError):
        return str(_Path(*p.parts[-3:]))

def success(message: str) -> None:
    print(f'{GREEN}✔ {message}{RESET}')

def error(message: str) -> None:
    print(f'{RED}✖ {message}{RESET}')

def warn(message: str) -> None:
    print(f'{YELLOW}⚠ {message}{RESET}')

def detail(message: str = '') -> None:
    if VERBOSE:
        print(message)

def finish(message: str, failures: int) -> None:
    if failures:
        error(message)
    else:
        success(message)
