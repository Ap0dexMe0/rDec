from pathlib import Path as _0x0305
from modules.config import (
    get_directory_settings,
    set_directory_setting,
)
from modules import output
try:
    from colorama import Fore as _0x0010, Style as _0x0011
except ImportError:

    class _0x000f:

        def __getattr__(_0x0191, _0x0192):
            return ''
    (_0x0010, _0x0011) = (_0x000f(), _0x000f())
try:
    from modules.banners import _0x000d as _0x000d
except Exception:

    def _0x000d():
        pass
_0x0013 = {'.mcf': 'mcf', '.gsf': 'gsf', '.ncf': 'ncf'}
_0x0014 = {'ROW': 'ROW', 'ROW/Origin': 'Original ROW (Rowplayon)', 'ROW/Other': 'Other ROW Versions', 'RYL1': 'Risk Your Life 1 (RYL1)', 'RYL2/V1700-V1900': 'RYL2 V1700–V1900', 'RYL2/V2000-V2240': 'RYL2 V2000–V2240'}
_0x0015 = ({'id': 'ROW', 'title': 'Return of Warriors (ROW)', 'group': 'ROW', 'menu': 'ROW VERSIONS', 'versions': (('Origin', 'Original ROW (Rowplayon)'), ('Other', 'Other ROW Versions'))}, {'id': 'RYL1', 'title': 'Risk Your Life 1 (RYL1)', 'group': 'RYL1', 'menu': None, 'versions': None}, {'id': 'RYL2', 'title': 'Risk Your Life 2 (RYL2)', 'group': 'RYL2', 'menu': 'RYL2 VERSIONS', 'versions': (('V1700-V1900', 'V1700–V1900'), ('V2000-V2240', 'V2000–V2240'))})
_0x0016 = 78
_0x0017 = {'0', 'q', 'quit', 'exit', 'back'}
_0x0018 = ''

def _0x0019() -> _0x0305:
    return _0x0305(__file__).resolve().parent.parent

def _0x001a(_0x0193=None) -> _0x0305:
    return (_0x0193 or _0x0019()) / 'script'

def _0x001b(_0x0194=None) -> list:
    _0x0306 = _0x001a(_0x0194)
    if not _0x0306.is_dir():
        return []
    _0x0307 = []
    for _0x0308 in sorted(_0x0306.iterdir()):
        if not _0x0308.is_dir():
            continue
        _0x0309 = [_0x030b for _0x030b in sorted(_0x0308.iterdir()) if _0x030b.is_dir()]
        if _0x0309 and (not _0x001c(_0x0308)):
            for _0x030a in _0x0309:
                _0x0307.append(f'{_0x0308.name}/{_0x030a.name}')
        else:
            _0x0307.append(_0x0308.name)
    return _0x0307

def _0x001c(_0x0195: _0x0305) -> bool:
    return any((_0x030c.is_file() for _0x030c in _0x0195.iterdir()))

def _0x001d(_0x0196: str) -> str:
    return _0x0196.replace('/', ' ')

def _0x001e(_0x0197: str) -> str:
    return _0x0014.get(_0x0197) or f'{_0x001d(_0x0197)} - unverified'

def _0x001f(_0x0198, _0x0199=None) -> _0x0305:
    _0x030d = _0x001b(_0x0199)
    if _0x0198 not in _0x030d:
        _0x030e = ', '.join((_0x001e(_0x030f) for _0x030f in _0x030d)) or 'none'
        raise ValueError(f"Unknown version {_0x0198!r} (available: {_0x030e}; supported: {', '.join(_0x0014)}; script directory: {output.short(_0x001a(_0x0199))}).")
    return _0x001a(_0x0199) / _0x0305(_0x0198)

def _0x0020(_0x019a: dict, _0x019b=None) -> list:
    
    _0x0310 = _0x019a['group']
    _0x0311 = [(f'{_0x0310}/{_0x0316}', _0x0317) for (_0x0316, _0x0317) in _0x019a['versions'] or ()]
    _0x0312 = {_0x0318 for (_0x0318, _) in _0x0311}
    _0x0313 = [(_0x031a, _0x031b) for (_0x031a, _0x031b) in _0x0311 if (_0x001a(_0x019b) / _0x031a).is_dir()]
    _0x0314 = []
    for _0x0315 in _0x001b(_0x019b):
        if _0x0315.startswith(f'{_0x0310}/') and _0x0315 not in _0x0312:
            _0x0314.append((_0x0315, _0x001e(_0x0315)))
    return _0x0313 + sorted(_0x0314)

def _0x0021(_0x019c: _0x0305):
    (_0x031c, _0x031d) = ([], [])
    for _0x031e in sorted(_0x019c.rglob('*')):
        if not _0x031e.is_file():
            continue
        _0x031f = _0x0013.get(_0x031e.suffix.lower())
        if _0x031f is None:
            _0x031d.append(_0x031e)
        else:
            _0x031c.append((_0x031e, _0x031f))
    return (_0x031c, _0x031d)

def _0x0022(_0x019d: _0x0305):
    (_0x0320, _0x0321) = _0x0021(_0x019d)
    _0x0322 = {}
    for (_, _0x0324) in _0x0320:
        _0x0322[_0x0324] = _0x0322.get(_0x0324, 0) + 1
    _0x0325 = ', '.join((f'{_0x0327:,} .{_0x0326}' for (_0x0326, _0x0327) in sorted(_0x0322.items()))) or 'none'
    if _0x0321:
        _0x0325 += f' (+{len(_0x0321):,} unsupported)'
    return (len(_0x0320), _0x0325)

def _0x0023(_0x019e: int) -> str:
    return f'{_0x019e:,}'

def _0x0024() -> None:
    try:
        _0x000d()
    except Exception:
        pass

def _0x0025(_0x019f: str) -> None:
    _0x0328 = '═' * _0x0016
    _0x0329 = max(0, (_0x0016 - len(_0x019f)) // 2)
    _0x032a = ' ' * max(0, _0x0016 - len(_0x019f) - _0x0329)
    _0x032b = ' ' * _0x0329 + f'{_0x0011.BRIGHT}{_0x0010.LIGHTYELLOW_EX}{_0x019f}{_0x0011.RESET_ALL}' + _0x032a
    print(f'{_0x0010.YELLOW}╔{_0x0328}╗')
    print(f'{_0x0010.YELLOW}║{_0x032b}║')
    print(f'{_0x0010.YELLOW}╚{_0x0328}╝')

def _0x0026(_0x01a0: list, _0x01a1: str) -> None:
    for (_0x032c, _0x032d) in enumerate(_0x01a0, 1):
        print(f'  [{_0x0010.GREEN}{_0x032c}{_0x0010.RESET}] {_0x032d}')
    print(f'  [{_0x0010.RED}0{_0x0010.RESET}] {_0x01a1}')

def _0x0027(_0x01a2: str) -> str:
    return input(f'{_0x0018}{_0x01a2}: ').strip()

def _0x0028(_0x01a3: str, _0x01a4: bool=True) -> bool:
    _0x032e = '[Y/n]' if _0x01a4 else '[y/N]'
    while True:
        _0x032f = input(f'{_0x0018}{_0x01a3} {_0x0011.BRIGHT}{_0x032e}{_0x0011.RESET_ALL} ').strip().lower()
        if not _0x032f:
            return _0x01a4
        if _0x032f in ('y', 'yes'):
            return True
        if _0x032f in ('n', 'no'):
            return False
        print("Please answer 'y' or 'n'.")

def _0x0029(_0x01a5: str, _0x01a6: int) -> int:
    while True:
        _0x0330 = _0x0027(_0x01a5)
        if _0x0330.isdigit() and int(_0x0330) <= _0x01a6:
            return int(_0x0330)
        if _0x0330.lower() in _0x0017:
            return 0
        if _0x0330:
            print(f'{_0x0330!r} is not a valid option - pick a number between 0 and {_0x01a6}.')
        else:
            print('Type a number (0 = back).')

def _0x002a() -> None:
    input(f'\n{_0x0018}Success! Press Enter to continue')

def _0x0032() -> None:
    _0x033f = {'SERVER_SIDE': 'Server-side', 'CLIENT_SIDE': 'Client-side'}
    while True:
        _0x0024()
        _0x0025('DIRECTORY SETTINGS')
        _0x0340 = get_directory_settings()
        print()
        for _0x0341, _0x0342 in _0x033f.items():
            print(f'  {_0x0342}: {_0x0340[_0x0341] or "(not set)"}')
        print()
        _0x0026(['Set server-side directory', 'Set client-side directory'], 'Back\n')
        _0x0343 = _0x0029('Choose a directory to set', 2)
        if _0x0343 == 0:
            return

        _0x0344 = ('SERVER_SIDE', 'CLIENT_SIDE')[_0x0343 - 1]
        _0x0346 = _0x0027(f'Enter {_0x033f[_0x0344]} directory (blank to clear)')
        if not _0x0346:
            try:
                set_directory_setting(_0x0344, '')
            except (OSError, ValueError) as _0x0348:
                print(f'Could not clear directory setting ({type(_0x0348).__name__}: {_0x0348}).')
                _0x002a()
                continue
            print(f'{_0x033f[_0x0344]} directory cleared in config.ini.\n')
            _0x002a()
            continue
        if len(_0x0346) >= 2 and _0x0346[0] == _0x0346[-1] and _0x0346[0] in ('"', "'"):
            _0x0346 = _0x0346[1:-1]
        _0x0347 = _0x0305(_0x0346).expanduser()
        if not _0x0347.is_dir():
            print(f'Directory not found: {_0x0347}. The configured path was not changed.\n')
            _0x002a()
            continue
        try:
            set_directory_setting(_0x0344, str(_0x0347.resolve()))
        except (OSError, ValueError) as _0x0348:
            print(f'Could not save directory setting ({type(_0x0348).__name__}: {_0x0348}).')
            _0x002a()
            continue
        print(f'{_0x033f[_0x0344]} directory set to {_0x0347.resolve()}.\n')
        _0x002a()

def _0x002b(_0x01a7, _0x01a8=None) -> int:
    while True:
        try:
            _0x0024()
            _0x0025('MAIN MENU')
            print()
            _0x0331 = ['Decompile']
            if _0x01a8 is not None:
                _0x0331.append('Compile')
            _0x0331.append('Set Server & Client Side Directory')
            _0x0026(_0x0331, 'Exit\n')
            _0x0332 = _0x0029('Choose an option', len(_0x0331))
            if _0x0332 == 0:
                print('Goodbye!')
                return 0
            if _0x0332 == len(_0x0331):
                _0x0032()
                continue
            _0x0333 = 'compile' if _0x01a8 is not None and _0x0332 == 2 else 'decompile'
            _0x0334 = _0x0333.upper()
            _0x0024()
            _0x0025(_0x0334)
            print()
            _0x0026([_0x0339['title'] for _0x0339 in _0x0015], 'Back')
            print()
            _0x0332 = _0x0029('Select a game', len(_0x0015))
            if _0x0332 == 0:
                continue
            _0x0335 = _0x0015[_0x0332 - 1]
            if _0x0335['versions'] is None:
                if _0x0333 == 'compile':
                    _0x002e(_0x01a8, _0x0335['id'])
                else:
                    _0x002f(_0x01a7, _0x0335['id'])
            else:
                _0x0336 = _0x0020(_0x0335)
                if not _0x0336:
                    print(f"No version folders found under {_0x001a() / _0x0335['group']}.")
                    _0x002a()
                    continue
                _0x0337 = _0x0335['menu'] or _0x001d(_0x0335['group'])
                _0x0024()
                _0x0025(f'{_0x0337} - {_0x0334}')
                print()
                _0x0026([_0x033b for (_, _0x033b) in _0x0336], 'Back')
                print()
                _0x0332 = _0x0029('Select a version', len(_0x0336))
                if _0x0332 == 0:
                    print('Back to the main menu - nothing was done.')
                    continue
                _0x0338 = _0x0336[_0x0332 - 1][0]
                if _0x0333 == 'compile':
                    _0x002e(_0x01a8, _0x0338)
                else:
                    _0x002f(_0x01a7, _0x0338)
        except (KeyboardInterrupt, EOFError):
            print('Session ended. Goodbye!\n')
            return 0

def _0x002c(_0x01a9, _0x01aa=None) -> _0x0305:
    
    _0x033c = _0x001f(_0x01a9, _0x01aa)
    _0x033d = _0x033c / 'compiled'
    if _0x033d.is_dir():
        (_0x033e, _) = _0x0021(_0x033d)
        if _0x033e:
            return _0x033d
    return _0x033c

def _0x002d(_0x01ab: _0x0305):
    
    from modules.ryl_compiler import _0x00b8 as _0x00b8
    (_0x0340, _0x0341) = ([], 0)
    for _0x0342 in sorted(_0x01ab.rglob('*.txt')):
        (_0x0343, _) = _0x00b8(_0x0342)
        if _0x0343:
            _0x0340.append(_0x0342)
        else:
            _0x0341 += 1
    return (_0x0340, _0x0341)

def _0x002e(_0x01ac, _0x01ad: str) -> None:
    _0x0024()
    try:
        _0x034b = _0x001f(_0x01ad)
    except ValueError as _0x034c:
        print(str(_0x034c))
        _0x002a()
        return
    _0x0345 = _0x034b / 'decompiled'
    if not _0x0345.is_dir() or not any(_0x0345.rglob('*.txt')):
        _0x0345 = _0x034b
    _0x0346 = _0x034b / 'compiled'
    _0x0347 = _0x001e(_0x01ad)
    print(f'Scanning {_0x0347} ({output.short(_0x0345)}) ...')
    (_0x0348, _0x0349) = _0x002d(_0x0345)
    if not _0x0348:
        output.warn(f'No compilable .txt files found in {_0x0347} ({output.short(_0x0345)}).')
        _0x002a()
        return
    print(f"Found {len(_0x0348):,} compilable .txt file{('s' if _0x0348 != 1 else '')} in {_0x0347} ({output.short(_0x0345)}){(f'; {_0x0349:,} not compilable' if _0x0349 else '')}.")
    _0x0356 = any((_0x0357.name.lower() == 'itemscript.txt' or _0x0357.stem.lower() == 'itemscript' for _0x0357 in _0x0348))
    if _0x0356:
        print('ItemScript detected: post-compile verifier will regenerate DropList tables and drop into the ID-lookup prompt.')
    if not _0x0028(f"Compile all compilable .txt files in {_0x0347} into '{output.short(_0x0346)}'?"):
        output.warn('Cancelled - nothing was compiled.')
        return
    try:
        _0x034d = _0x01ac(_0x01ad, _0x0490=_0x0356)
    except (KeyboardInterrupt, EOFError):
        output.warn('Compilation cancelled.')
        return
    if _0x034d != 0:
        output.error(f'rDec finished with errors (exit code {_0x034d}).')
    _0x002a()

def _0x002f(_0x01ae, _0x01af: str) -> None:
    _0x0024()
    try:
        _0x0352 = _0x002c(_0x01af)
        _0x0353 = _0x001f(_0x01af) / 'decompiled'
    except ValueError as _0x0354:
        print(str(_0x0354))
        _0x002a()
        return
    _0x034f = _0x001e(_0x01af)
    print(f'Scanning {_0x034f} ({output.short(_0x0352)})')
    (_0x0350, _0x0351) = _0x0022(_0x0352)
    if not _0x0350:
        output.warn(f'No supported files found in {_0x034f} ({output.short(_0x0351)}).')
        _0x002a()
        return
    print(f"Found {_0x0023(_0x0350)} supported file{('s' if _0x0350 != 1 else '')} in {_0x034f} ({output.short(_0x0352)}): {_0x0351}.")
    if not _0x0028(f"Decompile all supported files in {_0x034f} into '{output.short(_0x0353)}'?"):
        output.warn('Cancelled - nothing was decompiled.')
        return
    try:
        _0x0355 = _0x01ae(_0x01af)
    except (KeyboardInterrupt, EOFError):
        output.warn('Decompilation cancelled.')
        return
    if _0x0355 != 0:
        output.error(f'rDec finished with errors (exit code {_0x0355}).')
    _0x002a()
