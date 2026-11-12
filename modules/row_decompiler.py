import struct as _0x035e
from pathlib import Path as _0x035f
from collections import Counter as _0x0360
from modules.ryl_decompiler import _0x0100 as _0x0100, _0x0127 as _0x0127, _0x012e as _0x012e, _0x0101 as _0x0101, _0x014b as _0x014b, _0x0128 as _0x0128
from modules import output
_0x0036 = _0x035f(__file__).parent
_0x0037 = None

def _0x0038():
    global _0x0037
    if _0x0037 is None:
        from modules.xor_crypt import _0x017a as _0x017a, _0x0176 as _0x0176, _0x0014 as _0x0014
        _0x0361 = {}
        for _0x0362 in range(_0x0014):
            for _0x0364 in range(_0x0176):
                _0x0361[_0x0362, _0x0364] = bytes(_0x017a(_0x0362, _0x0364))
        _0x0037 = {}
        for _0x0362 in range(_0x0014):
            for _0x0364 in range(_0x0176):
                if _0x0362 in (2, 3):
                    _0x0037[_0x0362, _0x0364] = bytes((_0x0365 ^ _0x0366 for (_0x0365, _0x0366) in zip(_0x0361[_0x0362, _0x0364], _0x0361[0, _0x0364])))
                else:
                    _0x0037[_0x0362, _0x0364] = _0x0361[_0x0362, _0x0364]
    return _0x0037
_0x0039 = {'ItemScript.gsf': (3, 4), 'ItemScriptEx.gsf': (3, 4), 'Chemical.gsf': (3, 4), 'MonsterProtoType.gsf': (3, 2), 'SkillScript.gsf': (3, 3)}
_0x003a = 620
_0x003b = 616
_0x003c = 560
_0x003d = 552
_0x003e = 24
_0x003f = 304
_0x0040 = {'Itemscript.gsf': (3, 4), 'ItemScriptEx.gsf': (3, 4), 'Chemical.gsf': (3, 4), 'Monsterprototype.gsf': (3, 2), 'SkillScript.gsf': (3, 3), 'SkillScriptEx.gsf': None}
_0x0041 = {'Other': _0x0040}
_0x0042 = {'Other': _0x003b}
_0x0043 = 3806715111
_0x0044 = _0x0128 + ['Trailer']
_0x0045 = b'PickkingItem\t\t\tTargetItem\t\t\tResultItem\t\t\tExtra\t\t\t\t\t\r\nName\tID\tNum\tName\tID\tNum\tName\tID\tNum\tItemID\tAbilityID\tAbilityLevel\tQuestID\tPercent\r\n'
_0x0046 = {'AddPopupGuild': {7: (['i', 'i', 'i', 's', 'i', 'i', 'i'], 1, 0)}, 'AddPopupAbility': {7: (['i', 'i', 'i', 's', 'i', 'i', 'i'], 1, 0)}, 'AddPopupFame': {7: (['i', 'i', 'i', 's', 'i', 'i', 'i'], 1, 0)}, 'QuestStartLevel': {7: (['i', 'i', 'i', 'i', 'i', 'i', 'b'], 0, 0)}, 'QuestStartFame': {7: (['i', 'i', 'i', 'i', 'i', 'i', 'b'], 0, 0)}, 'QuestAbilityPoint': {1: (['i'], 1, 0)}, 'Event_AlarmBox': {1: (['s'], 3, 0)}, 'Event_AwardItemClass': {5: (['i'] * 5, 3, 0)}, 'Event_AwardItemID': {4: (['i'] * 4, 3, 0)}, 'Event_AwardAbility': {4: (['i'] * 4, 3, 0)}, 'Trigger_AbilityTalk': {3: (['i', 'i', 's'], 2, 0)}, 'Trigger_FameTalk': {3: (['i', 'i', 's'], 2, 0)}, 'Phase_Target': {3: (['i', 'i', 'i'], 2, 0)}, 'Event_Move': {4: (['i', 'f', 'f', 'f'], 3, 0)}}

def _0x0047(_0x01b2=None):
    
    _0x0367 = _0x01b2.split('/')[-1] if _0x01b2 and '/' in _0x01b2 else None
    if _0x0367 and _0x0367 in _0x0041:
        return (_0x0041[_0x0367], _0x0042.get(_0x0367, _0x003a))
    return (_0x0039, _0x003a)

def _0x0048(_0x01b3: str) -> str:
    return _0x035f(_0x01b3).stem + '.txt'

def _0x0049(_0x01b4, _0x01b5=None, _0x01b6=None) -> dict:
    for _0x0368 in _0x01b4:
        if _0x035f(_0x0368).name.lower() == 'itemscript.gsf':
            return _0x004c(_0x004b(_0x035f(_0x0368), _0x01b5), _0x01b6 or _0x003a)
    return {}

def _0x004a(_0x01b7):
    return _0x01b7 << 7 & 255 | _0x01b7 >> 1

def _0x004b(_0x01b8: _0x035f, _0x01b9=None):
    try:
        from modules import lzo as lzo_codec
    except ImportError as _0x0373:
        raise RuntimeError(f"{_0x01b8.name}: needs the 'lzo' package ({_0x0373})")
    _0x0369 = _0x01b8.read_bytes()
    _0x036a = _0x035e.unpack_from('<I', _0x0369, 0)[0]
    if _0x036a > len(_0x0369):
        raise ValueError(f'{_0x01b8.name} is not a GSF envelope (trash size {_0x036a:,} exceeds file size {len(_0x0369):,}).')
    _0x036b = _0x035e.unpack_from('<I', _0x0369, 4 + _0x036a)[0]
    _0x036c = lzo_codec.decompress_lzo(bytes(_0x0369[4 + _0x036a + 4:]), False, _0x036b)
    assert len(_0x036c) == _0x036b, f'LZO payload is {len(_0x036c):,} bytes; {_0x036b:,} were expected.'
    output.detail(f'{_0x01b8.name}: decompressed {_0x036b:,} payload bytes ({len(_0x0369):,} on disk, {_0x036a:,} trash bytes skipped).')
    _0x036d = _0x0039 if _0x01b9 is None else _0x01b9
    _0x036e = {_0x0374.lower(): _0x0375 for (_0x0374, _0x0375) in _0x036d.items()}
    if _0x01b8.name.lower() not in _0x036e:
        raise ValueError(f'No ROW crypt page is registered for {_0x01b8.name} (known: {sorted(_0x036d)}).')
    (_0x036f, _0x0370) = _0x036e[_0x01b8.name.lower()]
    _0x0371 = _0x0038()[_0x036f, _0x0370]
    return bytes((_0x004a(_0x0377) ^ _0x0371[_0x0376 % 40] for (_0x0376, _0x0377) in enumerate(_0x036c)))

def _0x004c(_0x01ba: bytes, _0x01bb: int=_0x003a) -> dict:
    _0x0378 = {}
    for _0x0379 in range(len(_0x01ba) // _0x01bb):
        _0x037a = _0x01ba[_0x0379 * _0x01bb:(_0x0379 + 1) * _0x01bb]
        _0x0378[_0x035e.unpack_from('<H', _0x037a, 0)[0]] = _0x0101(_0x0100(_0x037a[52:116]))
    return _0x0378

def _0x004d(_0x01bc: bytes) -> bytes:
    return b'\r\n' if b'\r\n' in _0x01bc else b'\n'

def _0x004e(_0x01bd: _0x035f, _0x01be: dict, _0x01bf=None, _0x01c0: int=None) -> bytes:
    _0x01bd = _0x035f(_0x01bd)
    if _0x01bd.name.lower() == 'skillscriptex.gsf':
        import shutil as _0x037d
        import subprocess as _0x037e
        import tempfile as _0x037f
        _0x0380 = _0x0036 / 'unluac.jar'
        if not (_0x037d.which('java') and _0x0380.exists()):
            raise RuntimeError('SKIP: needs java + modules/unluac.jar')
        output.detail('SkillScriptEx.gsf: decompiling Lua bytecode with unluac.')
        with _0x037f.TemporaryDirectory() as _0x0381:
            _0x0382 = _0x035f(_0x0381) / 'SkillScriptEx.txt'
            _0x0383 = _0x037e.run(['java', '-jar', str(_0x0380), str(_0x01bd), '-o', str(_0x0382)], capture_output=True, text=True)
            if _0x0383.returncode != 0 or not _0x0382.exists():
                raise RuntimeError(f"unluac failed: {(_0x0383.stderr or '')[:200]}")
            _0x0384 = _0x0382.read_bytes()
            output.detail(f'SkillScriptEx.gsf: unluac returned {len(_0x0384):,} bytes.')
            return _0x014b(_0x0384, _0x004d(_0x0384))
    _0x037b = _0x004b(_0x01bd, _0x01bf)
    _0x037c = _0x01bd.name.lower()
    if _0x037c == 'itemscript.gsf':
        return _0x014b(_0x004f(_0x037b, _0x01c0 or _0x003a), b'\n')
    if _0x037c == 'itemscriptex.gsf':
        return _0x014b(_0x0052(_0x037b), b'\n')
    if _0x037c == 'monsterprototype.gsf':
        return _0x014b(_0x0050(_0x037b))
    if _0x037c == 'skillscript.gsf':
        from modules.ryl_decompiler import _0x0137 as _0x0137
        return _0x014b(_0x0137(_0x037b))
    if _0x037c == 'chemical.gsf':
        return _0x014b(_0x0051(_0x037b, _0x01be))
    raise ValueError(f'{_0x01bd.name}: no ROW GSF handler registered')

def _0x004f(_0x01c1: bytes, _0x01c2: int=_0x003a) -> bytes:
    _0x0385 = _0x01c2 == _0x003a
    if len(_0x01c1) % _0x01c2:
        raise ValueError(f'Item payload {len(_0x01c1):,} is not a multiple of {_0x01c2}.')
    _0x0386 = len(_0x01c1) // _0x01c2
    output.detail(f'ItemScript.gsf (ROW): {_0x0386:,} item rows of {_0x01c2} bytes.')
    _0x0387 = _0x0044 if _0x0385 else _0x0128
    _0x0388 = 0
    _0x0389 = ['\t'.join(_0x0387)]
    for _0x038a in range(_0x0386):
        _0x038b = _0x01c1[_0x038a * _0x01c2:(_0x038a + 1) * _0x01c2]
        _0x038c = list(_0x0127(_0x038b[:_0x003b]))
        if _0x0385:
            _0x038d = _0x035e.unpack_from('<I', _0x038b, _0x003b)[0]
            _0x0388 += _0x038d != 0
            _0x038c.append(str(_0x038d))
        _0x0389.append('\t'.join(_0x038c))
    if _0x0385 and _0x0388:
        output.detail(f'ItemScript.gsf (ROW): {_0x0388:,}/{_0x0386:,} rows carry a nonzero trailer value (kept in the Trailer column).')
    return ('\n'.join(_0x0389) + '\n').encode('utf-8')

def _0x0050(_0x01c3: bytes) -> bytes:
    if len(_0x01c3) % _0x003c:
        raise ValueError(f'Monster payload {len(_0x01c3):,} is not a multiple of {_0x003c}.')
    _0x038e = len(_0x01c3) // _0x003c
    output.detail(f'MonsterProtoType.gsf (ROW): {_0x038e:,} monster rows.')
    _0x038f = sum((_0x01c3[_0x0390 * _0x003c + _0x003d:(_0x0390 + 1) * _0x003c] != b'\x00' * 8 for _0x0390 in range(_0x038e)))
    if _0x038f:
        output.detail(f'MonsterProtoType.gsf (ROW): {_0x038f:,}/{_0x038e:,} rows have a nonzero 8B trailer (dropped).')
    return ('\r\n'.join(('\t'.join(_0x012e(_0x01c3[_0x0391 * _0x003c:_0x0391 * _0x003c + _0x003d])) for _0x0391 in range(_0x038e))) + '\r\n').encode('utf-8')

def _0x0051(_0x01c4: bytes, _0x01c5: dict) -> bytes:
    if len(_0x01c4) % _0x003e:
        raise ValueError(f'Chemical payload {len(_0x01c4):,} is not a multiple of {_0x003e}.')
    _0x0392 = [_0x0045.rstrip(b'\r\n')]
    _0x0393 = _0x0360()
    _0x0394 = len(_0x01c4) // _0x003e
    for _0x0395 in range(_0x0394):
        _0x0396 = _0x01c4[_0x0395 * _0x003e:(_0x0395 + 1) * _0x003e]
        (_0x0397, _0x0398, _0x0399) = _0x035e.unpack_from('<HHH', _0x0396, 0)
        _0x039a = []
        for (_0x039b, _0x039c) in ((_0x0397, _0x0396[6]), (_0x0398, _0x0396[7]), (_0x0399, _0x0396[8])):
            _0x039d = _0x01c5.get(_0x039b)
            if _0x039d is None:
                _0x0393[_0x039b] += 1
                _0x039d = f'ITEM_{_0x039b}'
            _0x039a += [_0x039d, str(_0x039b), str(_0x039c)]
        _0x039a += [str(_0x035e.unpack_from('<I', _0x0396, 12)[0]), str(_0x035e.unpack_from('<H', _0x0396, 16)[0]), str(_0x0396[18]), str(_0x035e.unpack_from('<H', _0x0396, 20)[0]), str(_0x0396[22])]
        _0x0392.append('\t'.join(_0x039a).encode('utf-8'))
    if _0x0393:
        _0x039a = sum(_0x0393.values())
        output.warn(f'Chemical.gsf (ROW) references {len(_0x0393)} unknown item IDs ({_0x039a:,} cells); wrote ITEM_<id> placeholders instead.')
        output.warn(f'Chemical.gsf (ROW) most-missed IDs: {_0x0393.most_common(5)}.')
    output.detail(f'Chemical.gsf (ROW): {_0x0394:,} recipes.')
    return b'\r\n'.join(_0x0392) + b'\r\n'

def _0x0052(_0x01c6: bytes) -> bytes:
    if len(_0x01c6) % _0x003f:
        raise ValueError(f'ItemEx payload {len(_0x01c6):,} is not a multiple of {_0x003f}.')
    _0x039e = len(_0x01c6) // _0x003f
    output.detail(f'ItemScriptEx.gsf (ROW): {_0x039e:,} set records.')
    _0x039f = ['\t'.join(['ID', 'F1', 'F2', 'F3', 'F4', 'Name', 'Desc'])]
    for _0x03a0 in range(_0x039e):
        _0x03a1 = _0x01c6[_0x03a0 * _0x003f:(_0x03a0 + 1) * _0x003f]
        (_0x03a2, _0x03a3, _0x03a4, _0x03a5, _0x03a6) = _0x035e.unpack_from('<IHHII', _0x03a1, 0)
        _0x03a7 = _0x0101(_0x0100(_0x03a1[16:]))
        _0x03a8 = 16 + len(_0x0100(_0x03a1[16:])) + 1
        while _0x03a8 < len(_0x03a1) and _0x03a1[_0x03a8] == 0:
            _0x03a8 += 1
        _0x03a9 = _0x0101(_0x0100(_0x03a1[_0x03a8:]))
        _0x03a9 = _0x03a9.strip('\r\n').replace('\r\n', '\\n').replace('\n', '\\n')
        _0x039f.append('\t'.join([str(_0x03a2), str(_0x03a3), str(_0x03a4), str(_0x03a5), str(_0x03a6), _0x03a7, _0x03a9]))
    return ('\n'.join(_0x039f) + '\n').encode('utf-8')
_0x0054 = 69701
_0x0055 = 84542
_0x0056 = 78423

def _0x0057(_0x01c7: bytes) -> list:
    _0x03aa = []
    _0x03ab = 0
    _0x03ac = len(_0x01c7)
    while _0x03ab + 4 <= _0x03ac:
        (_0x03ad,) = _0x035e.unpack_from('<I', _0x01c7, _0x03ab)
        if _0x03ab + 4 + _0x03ad > _0x03ac:
            raise ValueError(f'NCF block at offset {_0x03ab:,} claims length {_0x03ad:,}, exceeding file size {_0x03ac:,}.')
        _0x03aa.append(_0x01c7[_0x03ab + 4:_0x03ab + 4 + _0x03ad])
        _0x03ab += 4 + _0x03ad
    if _0x03ab != _0x03ac:
        raise ValueError(f'NCF chain ends at {_0x03ab:,}, file is {_0x03ac:,} bytes (trailing {_0x03ac - _0x03ab:,} bytes).')
    return _0x03aa

def _0x0058(_0x01c8: bytes, _0x01c9: int=_0x0054) -> bytes:
    _0x03ae = bytearray(len(_0x01c8))
    for (_0x03af, _0x03b0) in enumerate(_0x01c8):
        _0x03ae[_0x03af] = _0x03b0 ^ _0x01c9 >> 8 & 255
        _0x01c9 = (_0x03b0 + _0x01c9) * _0x0055 + _0x0056 & 4294967295
    return bytes(_0x03ae)

def _0x0059(_0x01ca: list) -> dict:
    _0x03b1 = _0x0360()
    _0x03b2 = _0x0360()
    for _0x03b3 in _0x01ca:
        _0x03b7 = _0x03b3[:4].hex() if len(_0x03b3) >= 4 else f'short{len(_0x03b3)}'
        _0x03b1[_0x03b7] += 1
        _0x03b2[_0x03b7, len(_0x03b3)] += 1
    (_0x03b4, _0x03b5) = _0x03b1.most_common(1)[0]
    _0x03b6 = sum((1 for _0x03b8 in _0x0360((bytes(_0x03b9) for _0x03b9 in _0x01ca if _0x03b9)).values() if _0x03b8 > 1))
    return {'blocks': len(_0x01ca), 'top_tag': _0x03b4, 'top_count': _0x03b5, 'zero_blocks': sum((1 for _0x03ba in _0x01ca if not _0x03ba)), 'distinct_tags': len(_0x03b1), 'tag_census': _0x03b1.most_common(10), 'top_groups': sorted(_0x03b2.items(), key=lambda _0x01d4: -_0x01d4[1])[:10], 'duplicate_groups': _0x03b6}

def _0x005b(_0x01cc: bytes, _0x01cd: str):
    for _0x03bb in _0x01cc:
        if _0x03bb < 9 or 13 < _0x03bb < 32 or _0x03bb == 127:
            raise ValueError(f'{_0x01cd}: decrypted block is not text (byte 0x{_0x03bb:02X} in {_0x01cc[:48]!r}).')

def _0x005c(_0x01ce: _0x035f, _0x01cf: dict=None) -> bytes:
    from modules.banners import _0x000e as _0x000e
    from modules.ryl_decompiler import _0x00d7 as _0x00d7, _0x00d6 as _0x00d6
    from modules.translations import _0x0175 as _0x0175
    _0x01ce = _0x035f(_0x01ce)
    _0x03bc = _0x01ce.read_bytes()
    output.detail(f'{_0x01ce.name}: read {len(_0x03bc):,} bytes.')
    _0x03bd = _0x0057(_0x03bc)
    _0x03be = _0x0059(_0x03bd)
    output.detail(f"{_0x01ce.name}: {_0x03be['blocks']:,} blocks, {_0x03be['zero_blocks']:,} blank, dominant prefix {_0x03be['top_tag']} x{_0x03be['top_count']:,}.")
    _0x03bf = []
    for (_0x03c0, _0x03c1) in enumerate(_0x03bd):
        _0x03c3 = _0x0058(_0x03c1)
        _0x005b(_0x03c3, f'{_0x01ce.name} block {_0x03c0}')
        if _0x03c3:
            _0x03c4 = _0x00d7(_0x00d6(_0x03c3))
            _0x03c4 = _0x03c4.replace('\r\n', '\\n').replace('\n', '\\n')
            _0x03c4 = _0x0175(_0x03c4, _0x01cf)
            _0x03bf.append(_0x03c4)
        else:
            _0x03bf.append('')
    output.detail(f'{_0x01ce.name}: recovered {len(_0x03bf):,} lines.')
    _0x03c2 = list(_0x000e())
    _0x03c2.append('')
    _0x03c2.extend(_0x03bf)
    return '\r\n'.join(_0x03c2).encode('utf-8')

def _0x005d(_0x01d0: bytes) -> dict:
    
    from modules.ryl_decompiler import _0x00c2 as _0x00c2
    (_0x03c5, _0x03c6, _0x03c7) = _0x035e.unpack_from('<iii', _0x01d0, 0)
    for (_0x03c8, _0x03c9) in (('g', _0x03c5), ('s', _0x03c6), ('f', _0x03c7)):
        if not 0 <= _0x03c9 <= 1 << 22:
            raise ValueError(f'{_0x03c8}={_0x03c9:,} out of range')
    _0x03ca = _0x00c2(_0x01d0)
    _0x03cb = len(_0x03ca['code'])
    if not (_0x03ca['strbuf'] and _0x03cb):
        raise ValueError('empty string/code payload')
    for _0x03cc in _0x03ca['funcmap']:
        if not 0 <= _0x03cc < _0x03cb:
            raise ValueError(f'funcmap offset {_0x03cc:,} outside the {_0x03cb:,}-byte code payload')
    return _0x03ca

def _0x005e(_0x01d1: _0x035f) -> bytes:
    
    from modules.ryl_decompiler import _0x00de as _0x00de, decode as _0x03cd, _0x00bc as _0x00bc
    _0x01d1 = _0x035f(_0x01d1)
    _0x03ce = _0x01d1.read_bytes()
    output.detail(f'{_0x01d1.name}: read {len(_0x03ce):,} bytes.')
    _0x03cf = _0x035e.pack('<I', _0x0043)
    _0x03d0 = ((None, f'0x{_0x00bc:08X}'), (_0x03cf, f'0x{_0x0043:08X}'))
    _0x03d1 = []
    for (_0x03d2, _0x03d3) in _0x03d0:
        if _0x03d2 is None:
            _0x03d9 = _0x03cd(_0x03ce)
        else:
            _0x03d9 = bytes((_0x03dc ^ _0x03d2[_0x03db % 4] for (_0x03db, _0x03dc) in enumerate(_0x03ce)))
        try:
            _0x005d(_0x03d9)
        except Exception as _0x03da:
            _0x03d1.append(f'{_0x03d3} -> {type(_0x03da).__name__}: {_0x03da}')
            continue
        output.detail(f'{_0x01d1.name}: decoded with MCF key {_0x03d3}.')
        (_0x03d4, _, _0x03d6, _0x03d7, _0x03d8) = _0x00de(_0x01d1, _0x0254=_0x03d9, _0x0255=_0x0046)
        return (_0x03d4, len(_0x03d6), len(_0x03d7) + len(_0x03d8))
    raise RuntimeError(f"No ROW MCF key fits {_0x01d1.name}: {'; '.join(_0x03d1)}")

