
import re as _0x0400
from pathlib import Path as _0x0402
from modules import output
_0x0421 = b'\r\n'
_0x0423 = ('AAA', 'AA', 'A', 'B', 'C', 'D', 'F', 'X')
_0x0424 = ('AA', 'A', 'B', 'C', 'D', 'F')
_0x0425 = 150
_0x0426 = {'AAA': 'AAA', 'AA': 'AA', 'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'F': 'F', 'X': 'X', '': '', '0': 'AAA', '1': 'AA', '2': 'A', '3': 'B', '4': 'C', '5': 'D', '6': 'F', '7': 'X'}
_0x0427 = {'NECKLACE': 65, 'RING': 66, 'RUNE': 67}


def _0x0500(_0x0428):
    
    _0x0429 = _0x0402(_0x0428)
    if not _0x0429.is_file():
        raise FileNotFoundError(f'{_0x0428}')
    _0x042a = _0x0429.read_bytes()
    try:
        _0x042b = _0x042a.decode('utf-8')
    except UnicodeDecodeError:
        _0x042b = _0x042a.decode('cp949', 'replace')
    _0x042c = None
    _0x042d = []
    for _0x042e in _0x042b.splitlines():
        if not _0x042e or _0x042e.startswith('//'):
            continue
        _0x042f = _0x042e.split('\t')
        if _0x042c is None:
            if _0x042f[0].strip() == 'ID':
                _0x042c = [_0x0430.strip() for _0x0430 in _0x042f]
                continue
            _0x042c = [f'col{i}' for i in range(len(_0x042f))]
        if not any((_0x0430.strip() for _0x0430 in _0x042f)):
            continue
        _0x0431 = {}
        for _0x0432, _0x0433 in enumerate(_0x042f):
            if _0x0432 >= len(_0x042c):
                break
            _0x0434 = _0x042c[_0x0432]
            _0x0435 = 'id' if _0x0434 == 'ID' else _0x0434.lower().replace(' ', '').replace('(', '').replace(')', '')
            _0x0431[_0x0435] = _0x0433.strip() if _0x0433 else ''
        if 'id' not in _0x0431 or not _0x0431['id']:
            continue
        _0x0436 = _0x0400.match('[+-]?0[xX][0-9a-fA-F]+|[-+]?\\d+', _0x0431['id'])
        if not _0x0436:
            continue
        try:
            _0x0431['_id'] = int(_0x0436.group(0), 0)
        except ValueError:
            continue
        _0x042d.append(_0x0431)
    _0x042d.sort(key=lambda _0x0437: _0x0437['_id'])
    return _0x042d


def _0x0501(_0x0438):
    
    if not _0x0438:
        return ''
    _0x0439 = _0x0438.strip()
    return _0x0426.get(_0x0439, _0x0439)


def _0x0502(_0x043a, _0x043b):
    
    _0x043c = []
    for _0x043d in _0x043a:
        try:
            _0x043e = int(_0x043d.get('mindroplevel', '0') or '0')
            _0x043f = int(_0x043d.get('maxdroplevel', '0') or '0')
        except ValueError:
            continue
        if _0x043e == 0 and _0x043f == 0:
            continue
        if _0x043e <= _0x043b <= _0x043f:
            _0x043c.append(_0x043d)
    return _0x043c


def _0x0503(_0x0440, _0x0441, _0x0442):
    
    _0x0443 = str(_0x0427[_0x0442])
    _0x0444 = []
    for _0x0445 in _0x0440:
        try:
            _0x0446 = int(_0x0445.get('mindroplevel', '0') or '0')
            _0x0447 = int(_0x0445.get('maxdroplevel', '0') or '0')
        except ValueError:
            continue
        if _0x0446 == 0 and _0x0447 == 0:
            continue
        if not (_0x0446 <= _0x0441 <= _0x0447):
            continue
        _0x0448 = _0x0445.get('itemtype', '').strip()
        _0x0449 = _0x0445.get('typename', '').strip().upper()
        if _0x0448 == _0x0443 or _0x0449 == _0x0442:
            _0x0444.append(_0x0445)
    _0x0444.sort(key=lambda _0x044a: _0x044a['_id'])
    return _0x0444


def _0x0504(_0x044b):
    
    _0x044c = {g: [] for g in _0x0423}
    for _0x044d in _0x044b:
        _0x044e = _0x0501(_0x044d.get('grade', ''))
        _0x044c.setdefault(_0x044e, []).append(_0x044d)
    return _0x044c


def _0x0505(_0x044f, _0x0450):
    
    _0x0451 = bytearray()
    for _0x0452 in range(1, _0x0425 + 1):
        _0x0453 = _0x0502(_0x044f, _0x0452)
        _0x0454 = [str(_0x0456['_id']) for _0x0456 in _0x0453]
        _0x0455 = '\t'.join([f'Level {_0x0452}'] + _0x0454) + '\t'
        _0x0451 += _0x0455.encode('cp949', 'replace') + _0x0421
    _0x0450.write_bytes(bytes(_0x0451))


def _0x0506(_0x0457, _0x0458):
    
    _0x0459 = bytearray()
    for _0x045a in range(1, _0x0425 + 1):
        _0x045b = _0x0502(_0x0457, _0x045a)
        _0x045c = [(_0x045e.get('typename', '') or '') for _0x045e in _0x045b]
        _0x045d = '\t'.join([f'Level {_0x045a}'] + _0x045c) + '\t'
        _0x0459 += _0x045d.encode('cp949', 'replace') + _0x0421
    _0x0458.write_bytes(bytes(_0x0459))


def _0x0507(_0x045f, _0x0460, _0x0461):
    
    _0x0462 = bytearray()
    for _0x0463 in range(1, _0x0425 + 1):
        _0x0464 = _0x0503(_0x045f, _0x0463, _0x0460)
        _0x0465 = _0x0504(_0x0464)
        _0x0462 += f'Level {_0x0463}'.encode('cp949', 'replace') + _0x0421
        for _0x0466 in _0x0423:
            _0x0467 = _0x0465.get(_0x0466, [])
            _0x0468 = [str(_0x046a['_id']) for _0x046a in _0x0467]
            _0x0469 = '\t'.join([f'\t{_0x0466} Grade'] + _0x0468) + '\t'
            _0x0462 += _0x0469.encode('cp949', 'replace') + _0x0421
    _0x046b = b''.join((f'\t{_0x046c} Grade\t'.encode('cp949', 'replace') for _0x046c in _0x0423))
    for _ in range(_0x0425):
        _0x0462 += _0x046b
    _0x0461.write_bytes(bytes(_0x0462))


def _0x0508(_0x046b, _0x046c, _0x046d, _0x046e):
    
    _0x046f = bytearray()
    for _0x0470 in range(1, _0x0425 + 1):
        _0x0471 = _0x0503(_0x046b, _0x0470, _0x046c)
        _0x0472 = _0x0504(_0x0471)
        _0x046f += f'Level {_0x0470}'.encode('cp949', 'replace') + _0x0421
        _0x046f += _0x0421
        for _0x0473 in _0x0424:
            _0x0474 = _0x0472.get(_0x0473, [])
            if _0x0474:
                _0x0475 = _0x0474[0].get('typename', _0x046e) or _0x046e
                _0x046f += (_0x0475 + '\t').encode('cp949', 'replace') + _0x0421
            else:
                _0x046f += _0x0421
        _0x046f += _0x0421
    _0x046d.write_bytes(bytes(_0x046f))


def _0x0509(_0x0476, dest=None):
    
    _0x0477 = _0x0402(_0x0476)
    if not _0x0477.is_file():
        output.warn(f'ItemScript source not found at {_0x0476}; skipping DropList generation.')
        return {}
    _0x0478 = _0x0500(_0x0477)
    if not _0x0478:
        output.warn(f'No item rows parsed from {_0x0476}; skipping DropList generation.')
        return {}
    output.detail(f"Loaded {len(_0x0478):,} item rows from {_0x0477.name} for DropList generation.")
    if dest is None:
        _0x0479 = _0x0477.parent
    else:
        _0x0479 = _0x0402(dest)
        _0x0479.mkdir(parents=True, exist_ok=True)
    _0x047a = {'DropListByLevel(ItemID).txt': lambda p: _0x0505(_0x0478, p), 'DropListByLevel(TypeName).txt': lambda p: _0x0506(_0x0478, p), 'RingDropListByLevel(ItemID).txt': lambda p: _0x0507(_0x0478, 'RING', p), 'RingDropListByLevel(TypeName).txt': lambda p: _0x0508(_0x0478, 'RING', p, 'Ring'), 'NecklaceDropListByLevel(ItemID).txt': lambda p: _0x0507(_0x0478, 'NECKLACE', p), 'NecklaceDropListByLevel(TypeName).txt': lambda p: _0x0508(_0x0478, 'NECKLACE', p, 'Necklace'), 'RuneDropListByLevel(ItemID).txt': lambda p: _0x0507(_0x0478, 'RUNE', p), 'RuneDropListByLevel(TypeName).txt': lambda p: _0x0508(_0x0478, 'RUNE', p, 'Rune')}
    _0x047b = {}
    for _0x047c, _0x047d in _0x047a.items():
        _0x047e = _0x0479 / _0x047c
        _0x047d(_0x047e)
        _0x047b[str(_0x047e)] = _0x047e.stat().st_size
        output.success(f"Wrote {_0x0479.name}\\{_0x047c} ({_0x047b[str(_0x047e)]:,} bytes).")
    return _0x047b


def _0x050a(_0x047f):
    
    _0x0480 = {}
    for _0x0481 in _0x0500(_0x047f):
        _0x0480[_0x0481['_id']] = _0x0481
    return _0x0480


def _0x050b(_0x0482):
    
    if not _0x0482:
        return ''
    _0x0483 = _0x0482.get('dropoption', '')
    if not _0x0483 or _0x0483.strip() in ('X', 'x', '0'):
        return ''
    return _0x0483.strip()


def _0x050c(_0x0484, _0x0485=None):
    
    if _0x0485 is None:
        _0x0485 = input
    _0x0486 = 0
    while True:
        try:
            _0x0487 = _0x0485('Input Items ID. (0 - Quit) : ').strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not _0x0487:
            continue
        if not _0x0487.lstrip('+-').isdigit():
            print(f'{_0x0487!r} is not an item ID - pick a number (0 = quit).')
            continue
        _0x0488 = int(_0x0487, 10)
        if _0x0488 == 0:
            break
        _0x0486 += 1
        _0x0489 = _0x0484.get(_0x0488)
        if _0x0489 is None:
            output.warn(f"Can't find the Item which is ID No.{_0x0488}")
            continue
        _0x048a = _0x0489.get('itemname', '') or ''
        _0x048b = _0x050b(_0x0489)
        print(f'Item Name : {_0x048a}      Note : {_0x048b}')
    return _0x0486


def _0x050d(_0x048c, _0x048d=None):
    
    _0x048e = _0x0402(_0x048c)
    if not _0x048e.is_file():
        output.warn(f'No ItemScript source at {_0x048c}; verifier skipped.')
        return 0
    _0x048f = _0x050a(_0x048e)
    if not _0x048f:
        output.warn(f'No items in {_0x048e.name}; verifier skipped.')
        return 0
    _0x0509(_0x048e)
    return _0x050c(_0x048f, _0x048d)


_0x050e = _0x0509
_0x050f = _0x050c
_0x0510 = _0x050d
