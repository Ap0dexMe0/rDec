import sys as _0x02c4
import time as _0x02c5
from pathlib import Path as _0x02c6
_0x02c4.path.insert(0, str(_0x02c6(__file__).resolve().parent))
from modules.cli import _0x0021 as _0x0021, _0x002b as _0x002b, _0x001f as _0x001f
from modules.row_decompiler import _0x0047 as _0x0047
from modules import output

def _0x0002(_0x017b: int, _0x017c: str, _0x017d: str='') -> str:
    _0x02c7 = _0x017c if _0x017b == 1 else _0x017d or _0x017c + 's'
    return f'{_0x017b:,} {_0x02c7}'

def _0x0003(_0x017e: _0x02c6, _0x017f: _0x02c6, _0x0180: _0x02c6, _0x0181: str) -> _0x02c6:
    if _0x0181 == 'mcf':
        from modules.ryl_decompiler import _0x00c1 as _0x02c8
    elif _0x0181 == 'ncf':
        from modules.row_decompiler import _0x0048 as _0x02c8
    else:
        from modules.ryl_decompiler import _0x00e3 as _0x02c8
    return _0x017f / _0x017e.relative_to(_0x0180).parent / _0x02c8(_0x017e.name)

def _0x0004(_0x0182: _0x02c6, _0x0183: dict) -> bytes:
    from modules.row_decompiler import _0x005c as _0x005c
    return _0x005c(_0x0182, _0x0183)

def _0x0005(_0x0184: _0x02c6):
    from modules.ryl_decompiler import _0x0159 as _0x0159
    return _0x0159(_0x0184)

def _0x0006(_0x0185: _0x02c6, _0x0186: dict, _0x0187=None) -> bytes:
    from modules.ryl_decompiler import _0x015a as _0x015a
    return _0x015a(_0x0185, _0x0186, _0x0187)

def _0x0007(_0x0188: _0x02c6, _0x0189: dict, _0x018a=None, _0x018b: int=None) -> bytes:
    from modules.row_decompiler import _0x004e as _0x004e
    return _0x004e(_0x0188, _0x0189, _0x018a, _0x018b)

def _0x0008(_0x018c: _0x02c6) -> bytes:
    from modules.row_decompiler import _0x005e as _0x005e
    return _0x005e(_0x018c)

def run(_0x018d: str, _0x018e=None) -> int:
    _0x02c9 = _0x02c5.monotonic()
    try:
        _0x02d7 = _0x001f(_0x018d)
    except ValueError as _0x02d8:
        output.error(str(_0x02d8))
        return 2
    _0x02ca = _0x02c6(_0x018e).resolve() if _0x018e else _0x02d7
    if not _0x02ca.is_dir():
        output.error(f'Input directory not found: {output.short(_0x02ca)}.')
        return 2
    _0x02cb = _0x018d == 'ROW' or _0x018d.startswith('ROW/')
    (_0x02cc, _0x02cd) = _0x0047(_0x018d) if _0x02cb else (None, None)
    _0x02ce = _0x02ca / 'compiled'
    if _0x02ce.is_dir():
        (_0x02d9, _) = _0x0021(_0x02ce)
        if not _0x02d9:
            _0x02ce = _0x02ca
    else:
        _0x02ce = _0x02ca
    _0x02cf = _0x02ca / 'decompiled'
    (_0x02d0, _0x02d1) = _0x0021(_0x02ce)
    print(f"Decompiling version '{_0x018d}' from {output.short(_0x02ce)} into {output.short(_0x02cf)}.")
    print(f"Found {_0x0002(len(_0x02d0), 'supported file')} and {_0x0002(len(_0x02d1), 'unsupported file')}.\n")
    _0x02d2 = {}
    if any((_0x02e7 == 'gsf' for (_, _0x02e7) in _0x02d0)):
        if _0x02cb:
            try:
                from modules.row_decompiler import _0x0049 as _0x0049
                _0x02d2 = _0x0049([_0x02e8 for (_0x02e8, _) in _0x02d0], _0x02cc, _0x02cd)
                if _0x02d2:
                    output.detail(f'Loaded {len(_0x02d2):,} item names for Chemical lookups.')
            except Exception as _0x02d8:
                output.warn(f'Could not load item names ({_0x02d8}); continuing without them.')
        else:
            try:
                from modules.ryl_decompiler import _0x0158 as _0x0158
                _0x02d2 = _0x0158([_0x02ea for (_0x02ea, _) in _0x02d0], _0x018d)
                if _0x02d2:
                    output.detail(f'Loaded {len(_0x02d2):,} item names for Chemical lookups.')
            except Exception as _0x02d8:
                output.warn(f'Could not load item names ({_0x02d8}); continuing without them.')
    _0x02d3 = {'ok': 0, 'skipped': 0, 'unsupported': len(_0x02d1), 'failed': 0}
    for (_0x02d4, _0x02d5) in _0x02d0:
        _0x02db = _0x02d4.relative_to(_0x02ce)
        _0x02dc = _0x0003(_0x02d4, _0x02cf, _0x02ce, _0x02d5)
        if _0x02dc.suffix.lower() != '.txt':
            output.warn(f'Skipped {_0x02d4.name}: the output would not be a .txt file.')
            _0x02d3['skipped'] += 1
            continue
        if _0x02dc.resolve() == _0x02d4.resolve():
            output.warn(f'Skipped {_0x02d4.name}: the output path matches the input path.')
            _0x02d3['skipped'] += 1
            continue
        try:
            if _0x02d5 == 'mcf':
                if _0x02cb:
                    _0x02e3 = _0x0008
                else:
                    _0x02e3 = _0x0005
                (_0x02e0, _0x02e1, _0x02e2) = _0x02e3(_0x02d4)
                if _0x02e2 == 0:
                    _0x02e4 = f'{_0x02e1:,} calls, no anomalies'
                else:
                    _0x02e4 = f"{_0x02e1:,} calls, {_0x0002(_0x02e2, 'anomaly', 'anomalies')}"
            elif _0x02d5 == 'ncf':
                try:
                    _0x02e0 = _0x0004(_0x02d4, _0x02d2)
                except RuntimeError as _0x02d8:
                    if str(_0x02d8).startswith('SKIP:'):
                        _0x02e5 = str(_0x02d8)[len('SKIP:'):].strip()
                        output.warn(f'Skipped {_0x02d4.name}: {_0x02e5}.')
                        _0x02d3['skipped'] += 1
                        continue
                    raise
                _0x02e4 = f'{len(_0x02e0):,} bytes'
            elif _0x02cb:
                try:
                    _0x02e0 = _0x0007(_0x02d4, _0x02d2, _0x02cc, _0x02cd)
                except RuntimeError as _0x02d8:
                    if str(_0x02d8).startswith('SKIP:'):
                        _0x02e5 = str(_0x02d8)[len('SKIP:'):].strip()
                        output.warn(f'Skipped {_0x02d4.name}: {_0x02e5}.')
                        _0x02d3['skipped'] += 1
                        continue
                    raise
                _0x02e4 = f'{len(_0x02e0):,} bytes'
            else:
                try:
                    _0x02e0 = _0x0006(_0x02d4, _0x02d2, _0x018d)
                except RuntimeError as _0x02d8:
                    if str(_0x02d8).startswith('SKIP:'):
                        _0x02e5 = str(_0x02d8)[len('SKIP:'):].strip()
                        output.warn(f'Skipped {_0x02d4.name}: {_0x02e5}.')
                        _0x02d3['skipped'] += 1
                        continue
                    raise
                _0x02e4 = f'{len(_0x02e0):,} bytes'
            _0x02dc.parent.mkdir(parents=True, exist_ok=True)
            _0x02dc.write_bytes(_0x02e0)
            from modules.ryl_decompiler import _0x0155 as _0x0155
            if not _0x02cb and _0x02d5 == 'gsf':
                _0x0155(_0x02d4, _0x02dc)
            output.success(f'Decompiled {_0x02db} to {_0x02dc.relative_to(_0x02ca)} ({_0x02e4}).')
            _0x02d3['ok'] += 1
        except Exception as _0x02d8:
            output.error(f'Could not decompile {_0x02db} ({type(_0x02d8).__name__}: {_0x02d8}).')
            _0x02d3['failed'] += 1
    if _0x02d1:
        _0x02dd = {}
        for _0x02d4 in _0x02d1:
            _0x02df = _0x02d4.suffix.lower() or '<no extension>'
            _0x02dd[_0x02df] = _0x02dd.get(_0x02df, 0) + 1
        _0x02de = ', '.join((_0x0002(_0x02ed, f'{_0x02ec} file') for (_0x02ec, _0x02ed) in sorted(_0x02dd.items())))
        output.warn(f"Ignored {_0x0002(len(_0x02d1), 'unsupported file')}: {_0x02de}.")
    _0x02d6 = _0x02c5.monotonic() - _0x02c9
    output.finish(f"Finished in {_0x02d6:.1f} seconds: {_0x0002(_0x02d3['ok'], 'file')} decompiled, {_0x0002(_0x02d3['skipped'], 'file')} skipped, {_0x0002(_0x02d3['unsupported'], 'file')} left untouched, {_0x0002(_0x02d3['failed'], 'failure')}.", _0x02d3['failed'])
    return 1 if _0x02d3['failed'] else 0

def _0x0009(_0x018f: str, _0x0490: bool=False) -> int:
    
    _0x02ee = _0x02c5.monotonic()
    try:
        _0x02f6 = _0x001f(_0x018f)
    except ValueError as _0x02f7:
        output.error(str(_0x02f7))
        return 2
    from modules.ryl_compiler import _0x00b8 as _0x00b8, _0x00b9 as _0x00b9
    _0x02ef = _0x02f6 / 'decompiled'
    if not _0x02ef.is_dir() or not any(_0x02ef.rglob('*.txt')):
        _0x02ef = _0x02f6
    _0x02f0 = _0x02f6 / 'compiled'
    _0x02f0.mkdir(parents=True, exist_ok=True)
    _0x02f1 = sorted(_0x02ef.rglob('*.txt'))
    _0x02f2 = {'ok': 0, 'skipped': 0, 'failed': 0}
    print(f"Compiling version '{_0x018f}' from {output.short(_0x02ef)} into {output.short(_0x02f0)}.\n")
    _0x02f3 = set()
    _0x0491 = None
    for _0x02f4 in _0x02f1:
        (_0x02f8, _0x02f9) = _0x00b8(_0x02f4)
        if _0x02f8 is None:
            _0x02f9 = _0x02f9[len('SKIP: '):] if _0x02f9.startswith('SKIP: ') else _0x02f9
            _0x02fc = f': {_0x02f9}' if _0x02f9 else '.'
            if _0x0490 and 'droplist' in _0x02f4.name.lower():
                output.detail(f'Skipped {_0x02f4.name}: no compile target (regenerated by the post-compile verifier).')
            else:
                output.warn(f'Not compilable: {_0x02f4.name}{_0x02fc}')
            _0x02f2['skipped'] += 1
            continue
        _0x02fa = _0x02f0 / _0x02f8
        if _0x02fa in _0x02f3:
            output.warn(f'Skipped {_0x02f4.relative_to(_0x02ef)}: {_0x02f8} was already produced from another .txt with the same stem.')
            _0x02f2['skipped'] += 1
            continue
        _0x02f3.add(_0x02fa)
        _0x02fb = _0x02f0 / _0x02f8
        if _0x02fa.exists():
            output.detail(f"{_0x02f8} already exists in 'compiled'; recompiling over it.")
        try:
            _0x02fd = _0x00b9(_0x02f4, _0x02fb if _0x02fb.exists() else None)
            _0x02fa.parent.mkdir(parents=True, exist_ok=True)
            _0x02fa.write_bytes(_0x02fd)
            output.success(f'Compiled {_0x02f4.relative_to(_0x02ef)} to {_0x02fa.relative_to(_0x02f6)} ({len(_0x02fd):,} bytes).')
            _0x02f2['ok'] += 1
            if _0x02f8.lower() == 'itemscript.gsf':
                _0x0491 = _0x02f4
        except RuntimeError as _0x02f7:
            if str(_0x02f7).startswith('SKIP:'):
                output.warn(f"Skipped {_0x02f4.name}: {str(_0x02f7)[len('SKIP:'):].strip()}.")
                _0x02f2['skipped'] += 1
            else:
                output.error(f'Could not compile {_0x02f4.name} ({type(_0x02f7).__name__}: {_0x02f7}).')
                _0x02f2['failed'] += 1
        except Exception as _0x02f7:
            output.error(f'Could not compile {_0x02f4.name} ({type(_0x02f7).__name__}: {_0x02f7}).')
            _0x02f2['failed'] += 1
    _0x02f5 = _0x02c5.monotonic() - _0x02ee
    output.finish(f"Finished in {_0x02f5:.1f} seconds: {_0x0002(_0x02f2['ok'], 'file')} compiled, {_0x0002(_0x02f2['skipped'], 'file')} skipped, {_0x0002(_0x02f2['failed'], 'failure')}.", _0x02f2['failed'])
    if _0x0491 is not None and _0x02f2['failed'] == 0:
        try:
            from modules.ryl_verifier import _0x050d as _0x050d, _0x0509 as _0x0509, _0x050a as _0x050a, _0x050c as _0x050c
            print(f"Post-compile verifier: regenerating DropList tables into {output.short(_0x02f0)}.")
            _0x0509(_0x0491, _0x02f0)
            if _0x0490:
                print('Post-compile verifier: entering interactive item-ID lookup (0 = quit).')
                _0x050c(_0x050a(_0x0491))
        except Exception as _0x02f7:
            output.warn(f'Verifier skipped ({type(_0x02f7).__name__}: {_0x02f7}).')
    return 1 if _0x02f2['failed'] else 0

def _0x000a() -> int:
    return _0x002b(run, _0x0009)
if __name__ == '__main__':
    try:
        _0x02c4.stdout.reconfigure(encoding='utf-8')
        _0x02c4.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass
    _0x02c4.exit(_0x000a())
