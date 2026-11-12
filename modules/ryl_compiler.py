
import re as _0x03dd
import struct as _0x03de
from pathlib import Path as _0x03df
from modules.ryl_decompiler import _0x00bc as _0x00bc, _0x00be as _0x00be, _0x0105 as _0x0105, _0x010a as _0x010a, _0x010b as _0x010b, _0x0130 as _0x0130, _0x0131 as _0x0131, _0x0132 as _0x0132, _0x0133 as _0x0133, _0x012a as _0x012a, _0x012b as _0x012b, _0x00e2 as _0x00e2, _0x00e1 as _0x03e0
from modules import output
try:
    from modules import lzo as lzo_codec
except ImportError as import_error:
    lzo_codec = None
    lzo_import_error = str(import_error)
_0x0060 = {'ItemScript': 'ItemScript.gsf', 'MonsterProtoType': 'MonsterProtoType.gsf', 'SkillScript': 'SkillScript.gsf', 'Chemical': 'Chemical.gsf', 'Abuse': 'Script1.gsf', 'Script1': 'Script1.gsf', 'MonsterChat': 'MonsterChat.gsf', 'SpeacialCompensation': 'SpeacialCompensation.gsf'}
_0x0061 = {'NPCScript': 'NPCScript.mcf', 'Quest': 'Quest.mcf', 'Script': 'Script.mcf'}
_0x0062 = {'SkillScriptEX': 'SkillScriptEX.gsf'}
_0x0063 = dict(_0x00e2)
_0x0064 = {_0x03e1.lower(): _0x03e2 for (_0x03e1, _0x03e2) in _0x0063.items()}
_0x0065 = {_0x03e3.lower(): _0x03e4 for (_0x03e3, _0x03e4) in _0x0060.items()}
_0x0066 = {_0x03e5.lower(): _0x03e6 for (_0x03e5, _0x03e6) in _0x0061.items()}
_0x0067 = {_0x03e7.lower(): _0x03e8 for (_0x03e7, _0x03e8) in _0x0062.items()}

def _0x0068(_0x01d5: str):
    
    _0x03e9 = _0x03df(_0x01d5).name.lower()
    _0x03ea = _0x0064.get(_0x03e9)
    if _0x03ea is None:
        if _0x03e9.startswith('mineralvein') and _0x03e9.endswith('.gsf'):
            _0x03ea = (0, 3)
    return _0x03ea

def _0x0069(_0x01d6: int) -> int:
    return _0x01d6 << 1 & 255 | _0x01d6 >> 7
_0x006a = frozenset(('itemscript', 'monsterprototype', 'skillscript', 'chemical', 'abuse', 'monsterchat', 'speacialcompensation', 'mineralvein'))
_0x006b = _0x03dd.compile('^//\\s*rDec-([A-Za-z-]+):\\s*(.+?)\\s*$')

def _0x006c(_0x01d7) -> dict:
    
    _0x03eb = {}
    for _0x03ec in _0x01d7:
        if isinstance(_0x03ec, bytes):
            _0x03ec = _0x03ec.decode('utf-8', 'replace')
        _0x03ed = _0x006b.match(_0x03ec.strip())
        if _0x03ed:
            _0x03eb[_0x03ed.group(1).lower()] = _0x03ed.group(2)
    return _0x03eb

def _0x006d(_0x01d8, _0x01d9: int=12) -> list:
    _0x03ee = _0x03df(_0x01d8).read_bytes()
    return _0x03ee.decode('utf-8', 'replace').splitlines()[:_0x01d9]

def _0x006e(_0x01da: dict):
    
    _0x03ef = _0x01da.get('crypt')
    if not _0x03ef:
        return None
    try:
        (_0x03f0, _0x03f1) = _0x03ef.split(',')
        return (int(_0x03f0.strip()), int(_0x03f1.strip()))
    except ValueError:
        raise RuntimeError(f"unparsable rDec-Crypt tag: {_0x03ef!r} (want 'version,page', e.g. '0,2')")

def _0x006f(_0x01db: str) -> bytes:
    
    try:
        return _0x01db.encode('cp949')
    except UnicodeEncodeError:
        return _0x01db.encode('utf-8', 'replace')

def _0x0070(_0x01dc: str) -> int:
    
    _0x01dc = _0x01dc.strip()
    if not _0x01dc:
        return 0
    _0x03f2 = _0x03dd.match('[+-]?0[xX][0-9a-fA-F]+', _0x01dc)
    if _0x03f2:
        return int(_0x03f2.group(0), 16)
    _0x03f2 = _0x03dd.match('[+-]?\\d+', _0x01dc)
    if _0x03f2:
        return int(_0x03f2.group(0))
    return 0

def _0x0071(_0x01dd: str) -> float:
    _0x01dd = _0x01dd.strip()
    return float(_0x01dd) if _0x01dd else 0.0

def _0x0072(_0x01de: str) -> int:
    _0x01de = _0x01de.strip()
    return 1 if _0x01de in ('O', 'o', 'true', 'True', 'TRUE', '1') else 0

def _0x0073(_0x01df: str) -> int:
    _0x01df = _0x01df.strip()
    return 1 if _0x01df in ('true', 'True', 'TRUE', '1') else 0

def _0x0074(_0x01e0: str) -> int:
    
    _0x03f3 = int(_0x0071(_0x01e0))
    return _0x03f3 + 256 if _0x03f3 < 0 else _0x03f3

def _0x0075(_0x01e1: dict) -> dict:
    return {_0x03f5: _0x03f4 for (_0x03f4, _0x03f5) in _0x01e1.items()}
_0x0076 = _0x0075(_0x0105)
_0x0077 = _0x0075(_0x010a)
_0x0078 = _0x0075(_0x010b)
_0x0079 = _0x0075(_0x0130)
_0x007a = _0x0075(_0x0131)
_0x007b = _0x0075(_0x0132)
_0x007c = _0x0075(_0x0133)
_0x007d = _0x0075(_0x012a)
_0x007e = _0x0075(_0x012b)

def _0x007f(_0x01e2: str) -> int:
    
    _0x01e2 = _0x01e2.strip()
    if _0x01e2 in _0x0076:
        return _0x0076[_0x01e2]
    _0x03f6 = _0x01e2.upper().replace(' ', '_').replace('-', '')
    if _0x03f6 in _0x0076:
        return _0x0076[_0x03f6]
    try:
        return _0x0070(_0x01e2) & 255
    except ValueError:
        return 0

def _0x0080(_0x01e3: str, _0x01e4: dict) -> int:
    _0x01e3 = _0x01e3.strip()
    if _0x01e3 in _0x01e4:
        return _0x01e4[_0x01e3]
    try:
        return _0x0070(_0x01e3)
    except ValueError:
        return 0

def _0x0081(_0x01e5: str) -> int:
    
    return _0x0070(_0x01e5)

def _0x0082(_0x01e6: str, _0x01e7: int):
    
    _0x03f7 = _0x0091(_0x01e6)
    _0x03f8 = _0x006f(_0x03f7)
    if len(_0x03f8) > _0x01e7:
        output.warn(f'string too long for its field ({len(_0x03f8):,} > {_0x01e7}); truncating: {_0x03f7[:40]!r}')
        _0x03f8 = _0x03f8[:_0x01e7]
    return _0x03f8

def _0x0083(_0x01e8: str, _0x01e9: int) -> bytes:
    
    if '\\x' in _0x01e8:
        _0x03f9 = _0x0085(_0x01e8)
    else:
        _0x03f9 = _0x01e8
    _0x03f9 = _0x03f9.encode('latin-1', 'replace').rstrip(b' \t\r')
    if len(_0x03f9) > _0x01e9:
        output.warn(f'string too long for its field ({len(_0x03f9):,} > {_0x01e9}); truncating: {_0x01e8[:40]!r}')
        _0x03f9 = _0x03f9[:_0x01e9]
    return _0x03f9
_0x0084 = _0x03dd.compile('\\\\x([0-9A-Fa-f]{2})')

def _0x0085(_0x01ea: str) -> str:
    
    return _0x0084.sub(lambda _0x022c: chr(int(_0x022c.group(1), 16)), _0x01ea)

def _0x0086(_0x01eb: bytearray, _0x01ec: int, _0x01ed: int):
    _0x03de.pack_into('<H', _0x01eb, _0x01ec, _0x01ed & 65535)

def _0x0087(_0x01ee: bytearray, _0x01ef: int, _0x01f0: int):
    _0x03de.pack_into('<I', _0x01ee, _0x01ef, _0x01f0 & 4294967295)

def _0x0088(_0x01f1: bytes, _0x01f2: str, _0x01f3=None) -> bytes:
    
    if _0x01f3 is None:
        _0x01f3 = _0x0068(_0x01f2)
    if _0x01f3 is None:
        raise RuntimeError(f"""no crypt page registered for {_0x01f2} - tag the txt with "// rDec-Crypt: <version>,<page>" or rename it to a known build name ({', '.join(sorted(_0x0063))})""")
    _0x03fa = _0x03e0()[_0x01f3]
    return bytes((_0x0069(_0x03fc ^ _0x03fa[_0x03fb % 40]) for (_0x03fb, _0x03fc) in enumerate(_0x01f1)))

def _0x0089(_0x01f4: bytes, _0x01f5: str, _0x01f6: bytes=b'', _0x01f7=None) -> bytes:
    
    if lzo_codec is None:
        raise RuntimeError(f"needs the 'lzo' package ({lzo_import_error})")
    _0x03fd = _0x0088(_0x01f4, _0x01f5, _0x01f7)
    _0x03fe = lzo_codec.compress_lzo(_0x03fd, 1, False)
    _0x03ff = _0x03de.pack('<I', len(_0x01f6)) + _0x01f6 + _0x03de.pack('<I', len(_0x01f4))
    return _0x03ff + _0x03fe

def _0x008a(_0x01f8) -> bytes:
    
    try:
        _0x0400 = _0x03df(_0x01f8).read_bytes()
    except OSError:
        return b''
    try:
        _0x0401 = _0x03de.unpack_from('<I', _0x0400, 0)[0]
    except _0x03de.error:
        return b''
    if _0x0401 and 4 + _0x0401 <= len(_0x0400):
        return _0x0400[4:4 + _0x0401]
    return b''
_0x008b = {'b': 1, 'i': 2, 'f': 3, 's': 4}
_0x008c = _0x03dd.compile('^\\s*([A-Za-z_][A-Za-z0-9_]*)\\s*\\((.*)\\)\\s*;\\s*$')

def _0x008d(_0x01f9: str):
    
    _0x01f9 = _0x01f9.strip()
    if not _0x01f9 or _0x01f9.startswith('//') or _0x01f9.startswith('#'):
        return None
    _0x0402 = _0x008c.match(_0x01f9)
    if not _0x0402:
        raise ValueError(f'unparsable script line: {_0x01f9[:80]!r}')
    _0x0403 = _0x0402.group(1)
    _0x0404 = _0x0402.group(2).strip()
    return (_0x0403, _0x008e(_0x0404) if _0x0404 else [])

def _0x008e(_0x01fa: str) -> list:
    
    (_0x0405, _0x0406) = ([], [])
    _0x0407 = False
    (_0x0408, _0x0409) = (0, len(_0x01fa))
    while _0x0408 < _0x0409:
        _0x040b = _0x01fa[_0x0408]
        if _0x0407:
            if _0x040b == '\\' and _0x0408 + 1 < _0x0409:
                _0x0406.append(_0x01fa[_0x0408:_0x0408 + 2])
                _0x0408 += 2
                continue
            if _0x040b == '"':
                _0x0407 = False
            _0x0406.append(_0x040b)
            _0x0408 += 1
            continue
        if _0x040b == '"':
            _0x0407 = True
            _0x0406.append(_0x040b)
            _0x0408 += 1
            continue
        if _0x040b == ',':
            _0x0405.append(''.join(_0x0406).strip())
            _0x0406 = []
            _0x0408 += 1
            continue
        _0x0406.append(_0x040b)
        _0x0408 += 1
    _0x040a = ''.join(_0x0406).strip()
    if _0x040a:
        _0x0405.append(_0x040a)
    return _0x0405

def _0x008f(_0x01fb: str) -> str:
    if len(_0x01fb) >= 2 and _0x01fb.startswith('"') and _0x01fb.endswith('"'):
        return _0x01fb[1:-1]
    raise ValueError(f'string argument must be quoted: {_0x01fb!r}')

def _0x0090(_0x01fc: str) -> bytes:
    
    _0x040c = bytearray()
    _0x040d = []

    def _0x040e():
        if _0x040d:
            try:
                _0x040c.extend(''.join(_0x040d).encode('cp949'))
            except UnicodeEncodeError as _0x0414:
                raise RuntimeError(f'string is not cp949-encodable after unescaping: {_0x01fc!r}: {_0x0414}') from _0x0414
            _0x040d.clear()
    (_0x040f, _0x0410) = (0, len(_0x01fc))
    while _0x040f < _0x0410:
        _0x0411 = _0x01fc[_0x040f]
        if _0x0411 == '\\' and _0x040f + 1 < _0x0410:
            _0x0412 = _0x01fc[_0x040f + 1]
            if _0x0412 == '\\':
                _0x040d.append('\\')
                _0x040f += 2
                continue
            if _0x0412 == 'x' and _0x040f + 3 < _0x0410:
                try:
                    _0x0413 = int(_0x01fc[_0x040f + 2:_0x040f + 4], 16)
                except ValueError:
                    pass
                else:
                    _0x040e()
                    _0x040c.append(_0x0413)
                    _0x040f += 4
                    continue
        _0x040d.append(_0x0411)
        _0x040f += 1
    _0x040e()
    return bytes(_0x040c)

def _0x0091(_0x01fd: str) -> str:
    
    return _0x01fd.replace('\\r\\n', '\\n').replace('\\n', '\n')

def _0x0092(_0x01fe: str, _0x01ff: str):
    
    _0x01fe = _0x01fe.strip()
    if _0x01ff == 's':
        return None
    if _0x01ff == 'b':
        return _0x0073(_0x01fe)
    if _0x01ff == 'f':
        return _0x03de.unpack_from('<I', _0x03de.pack('<f', _0x0071(_0x01fe)))[0]
    _0x0415 = _0x0070(_0x01fe)
    return _0x0415 & 4294967295

def _0x0093(_0x0200: bytes):
    
    _0x0416 = _0x0200.decode('utf-8', 'replace')
    (_0x0417, _0x0418, _0x0419) = ([], {}, [])
    for (_0x041a, _0x041b) in enumerate(_0x0416.splitlines(), 1):
        _0x041c = _0x041b.strip()
        if _0x041c.startswith(';Stub '):
            try:
                (_, _0x0429, _0x042a, _0x042b) = _0x041c.split()
                _0x0419.append((int(_0x042b), int(_0x042a), _0x0429))
            except ValueError:
                raise RuntimeError(f'line {_0x041a}: malformed ;Stub carry')
            continue
        try:
            _0x0426 = _0x008d(_0x041b)
        except ValueError as _0x0427:
            raise RuntimeError(f'line {_0x041a}: {_0x0427}')
        if _0x0426 is None:
            continue
        (_0x041d, _0x041e) = _0x0426
        _0x041f = _0x00be.get(_0x041d)
        if not _0x041f or len(_0x041e) not in _0x041f:
            raise RuntimeError(f'line {_0x041a}: {_0x041d} is not a known RYL2 script function that takes {len(_0x041e)} argument(s)')
        _0x0420 = _0x041f[len(_0x041e)][0]
        _0x0423 = []
        for (_0x0424, _0x0425) in zip(_0x0420, _0x041e):
            if _0x0424 == 's':
                _0x0423.append(_0x0090(_0x008f(_0x0425.strip())))
            else:
                _0x0423.append(_0x0092(_0x0425, _0x0424))
        _0x0417.append((_0x041d, _0x0423))
        _0x0418.setdefault(_0x041d, set()).add(len(_0x041e))
    return (_0x0417, _0x0418, _0x0419)

def _0x0094(_0x0201) -> int:
    _0x042c = 0
    for (_0x042d, _0x042e) in enumerate(_0x0201):
        _0x042c |= _0x008b[_0x042e] << 4 * _0x042d
    return _0x042c

def _0x0095(_0x0202, _0x0203, _0x0204=None) -> bytes:
    
    _0x042f = bytearray()
    _0x0430 = {}
    for (_, _0x0432) in _0x0202:
        for _0x043e in _0x0432:
            if isinstance(_0x043e, bytes) and _0x043e not in _0x0430:
                _0x0430[_0x043e] = len(_0x042f)
                _0x042f += _0x043e + b'\x00'
    _0x0433 = bytearray()
    _0x0433 += b'\x90\x90\x90'
    _0x0433 += b'U\x89\xe5'
    _0x0434 = []
    _0x0435 = []
    for (_0x0436, _0x0432) in _0x0202:
        _0x0438 = len(_0x0432)
        for _0x043e in _0x0432:
            if isinstance(_0x043e, bytes):
                _0x0435.append(len(_0x0433) + 1)
            _0x0444 = _0x0430[_0x043e] if isinstance(_0x043e, bytes) else _0x043e or 0
            _0x0433 += b'\xb9' + _0x03de.pack('<I', _0x0444 & 4294967295)
            _0x0433 += b'Q'
        _0x0434.append((len(_0x0433) + 1, _0x0436, _0x0438))
        _0x0433 += b'\xe8' + b'\x00\x00\x00\x00'
        _0x0433 += b'\x81\xc4' + _0x03de.pack('<I', 4 * _0x0438)
    _0x0433 += b'\x89\xec]\xc3'
    _0x0433 += b'\xcc\xcc\xcc'
    if _0x0204:
        _0x043f = sorted(_0x0204)
        _0x0440 = {}
        for (_0x043a, _0x043b, _0x043c) in _0x043f:
            _0x0438 = len(f'{_0x043b:x}') if _0x043b else 0
            if len(_0x0433) != _0x043a:
                output.warn(f'{_0x043c}: stub carry offset {_0x043a} but code built to {len(_0x0433)}; replaying carry')
            _0x0440[_0x043c, _0x0438] = len(_0x0433)
            _0x0433 += b'U\x89\xe5'
            _0x0433 += b'\x90' * (5 + 3 * _0x0438)
            _0x0433 += b'\x89\xec]\xc3'
        _0x0441 = {}
        for (_0x0436, _0x0442) in _0x0202:
            _0x0441.setdefault(_0x0436, set()).add(len(_0x0442))
        for (_0x043a, _0x043b, _0x043c) in _0x043f:
            _0x0438 = len(f'{_0x043b:x}') if _0x043b else 0
            if _0x0438 in _0x0441.get(_0x043c, ()):
                _0x0445 = _0x0094(_0x00be[_0x043c][_0x0438][0])
                if _0x0445 != _0x043b:
                    output.warn(f'{_0x043c}({_0x0438}): carry typestamp {_0x043b:x} differs from SIGS {_0x0445:x}')
    else:
        _0x0443 = [(_0x0446, _0x0447) for _0x0446 in sorted(_0x0203) for _0x0447 in sorted(_0x0203[_0x0446])]
        _0x0440 = {}
        for (_0x0436, _0x0438) in _0x0443:
            _0x0440[_0x0436, _0x0438] = len(_0x0433)
            _0x0433 += b'U\x89\xe5'
            _0x0433 += b'\x90' * (5 + 3 * _0x0438)
            _0x0433 += b'\x89\xec]\xc3'
        _0x043f = sorted(((_0x044a, _0x0094(_0x00be[_0x0448][_0x0449][0]), _0x0448, _0x0449) for ((_0x0448, _0x0449), _0x044a) in _0x0440.items()), key=lambda _0x022e: _0x022e[0])
    for (_0x0437, _0x0436, _0x0438) in _0x0434:
        _0x03de.pack_into('<i', _0x0433, _0x0437, _0x0440[_0x0436, _0x0438] - (_0x0437 + 4))
    _0x0439 = bytearray()
    _0x0439 += _0x03de.pack('<I', len(_0x043f))
    for (_0x043a, _0x043b, _0x043c) in _0x0204 if _0x0204 else [(_0x0440[_0x044d, _0x044e], _0x044c, _0x044d) for (_, _0x044c, _0x044d, _0x044e) in _0x043f]:
        _0x0439 += _0x043c.encode('ascii') + b'\n'
        _0x0439 += _0x03de.pack('<II', _0x043b & 4294967295, _0x043a & 4294967295)
    _0x043d = bytearray()
    _0x043d += _0x03de.pack('<iii', 0, len(_0x0435), 0)
    _0x043d += b''.join((_0x03de.pack('<I', _0x044f) for _0x044f in _0x0435))
    _0x043d += _0x03de.pack('<iii', 28, len(_0x042f), len(_0x0433))
    _0x043d += _0x042f
    _0x043d += _0x0433
    _0x043d += _0x0439
    _0x043d += _0x03de.pack('<iiii', 4, 16, 20, 24)
    return bytes(_0x043d)

def _0x0096(_0x0205: bytes, _0x0206: int=_0x00bc) -> bytes:
    
    _0x0450 = _0x03de.pack('<I', _0x0206)
    _0x0451 = bytearray(len(_0x0205))
    for _0x0452 in range(4):
        _0x0451[_0x0452::4] = bytes((_0x0453 ^ _0x0450[_0x0452] for _0x0453 in _0x0205[_0x0452::4]))
    return bytes(_0x0451)

def _0x0097(_0x0207) -> bytes:
    (_0x0454, _0x0455, _0x0456) = _0x0093(_0x03df(_0x0207).read_bytes())
    _0x0457 = bytearray(_0x0095(_0x0454, _0x0455, _0x0456))
    _0x0458 = _0x03de.pack('<I', _0x00bc)
    _0x0459 = len(_0x0457) % 4
    if _0x0459:
        _0x0457[-_0x0459:] = _0x0458[:_0x0459]
    return _0x0096(bytes(_0x0457))
_0x0098 = lambda _0x0229: 540 + 2 * _0x0229
_0x0099 = {1: 1, 2: 1, 5: 1, 6: 1, 9: 1, 10: 1, 24: 1, 25: 1, 28: 1, 29: 1, 3: 33, 7: 33, 22: 33, 26: 33, 4: 17, 8: 17, 23: 17, 27: 17, 11: 129, 13: 129, 15: 129, 30: 129, 31: 129, 32: 129, 33: 129, 34: 129, 38: 129, 39: 129, 12: 1, 14: 1, 16: 1, 17: 1, 18: 1, 19: 1, 21: 1, 36: 1, 37: 1, 20: 65, 35: 65, 40: 65, 41: 9, 42: 9, 65: 1, 66: 1}
_0x009a = {43: 2, 44: 6, 45: 2, 46: 2, 47: 2, 48: 6, 49: 6, 50: 2, 52: 6, 53: 0, 54: 0, 55: 0, 56: 0, 57: 2, 58: 2, 59: 2, 60: 2, 61: 2, 62: 2, 63: 2, 64: 2, 51: 6}

def _0x009b(_0x0208, _0x0209: str) -> int:
    
    try:
        _0x045a = int(str(_0x0209).strip())
    except ValueError:
        _0x045a = 0
    return _0x009a.get(_0x0208, 0) + (8 if _0x045a > 1 else 0) & 255
_0x009c = {12: 2, 14: 2, 16: 2, 17: 1, 18: 1, 19: 4, 36: 4, 21: 8, 37: 8, 65: 16, 66: 32}
_0x009d = dict.fromkeys((1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42), 4)
_0x009d[65] = 20
_0x009d[66] = 20
_0x009e = set(range(1, 43)) | {69, 70}

def _0x009f(_0x020a) -> dict:
    
    try:
        _0x045d = _0x03df(_0x020a).read_bytes()
    except OSError:
        return {}
    _0x045b = {}
    for _0x045c in _0x045d.split(b'\n'):
        _0x045e = _0x045c.strip()
        if not _0x045e or _0x045e.lstrip().startswith(b'//'):
            continue
        _0x045f = _0x045e.split()
        if len(_0x045f) != 2:
            output.warn(f'{_0x03df(_0x020a).name}: skipping junk line {_0x045c[:60]!r}')
            continue
        try:
            _0x0460 = _0x0070(_0x045f[0].decode('latin-1'))
            _0x0461 = bytes.fromhex(_0x045f[1].decode('ascii'))
        except ValueError:
            output.warn(f'{_0x03df(_0x020a).name}: unparsable junk line {_0x045c[:60]!r}')
            continue
        if len(_0x0461) not in (22, 23):
            output.warn(f'{_0x03df(_0x020a).name}: junk window for id {_0x0460} is {len(_0x0461):,} bytes; 22/23 expected')
            continue
        _0x045b[_0x0460] = _0x0461
    return _0x045b

def _0x00a0(_0x020b: bytearray, _0x020c: dict):
    
    _0x0462 = _0x020c.get(_0x03de.unpack_from('<H', _0x020b, 0)[0])
    if not _0x0462:
        return
    _0x020b[2:4] = _0x0462[0:2]
    _0x020b[584:604] = _0x0462[2:22]
    if len(_0x0462) > 22 and _0x020b[21] not in _0x009e:
        _0x020b[18] = _0x0462[22]

def _0x00a1(_0x020d) -> bytes:
    _0x020d = [_0x046f.decode('latin-1') if isinstance(_0x046f, (bytes, bytearray)) else _0x046f for _0x046f in _0x020d]
    _0x020d = list(_0x020d) + [''] * (60 - len(_0x020d))
    _0x0463 = bytearray(616)
    _0x0464 = _0x007f(_0x020d[12])
    _0x0463[21] = _0x0464 & 255
    _0x0086(_0x0463, 0, _0x0070(_0x020d[0]))
    for (_0x0465, _0x0466, _0x0467) in ((52, 64, 1), (156, 32, 2), (188, 32, 3), (116, 32, 4), (220, 32, 11), (252, 32, 13)):
        _0x046d = _0x0083(_0x020d[_0x0467], _0x0466)
        _0x0463[_0x0465:_0x0465 + _0x0466] = _0x046d + b'\x00' * (_0x0466 - len(_0x046d))
    for (_0x0465, _0x0467) in ((148, 5), (150, 6), (152, 7), (154, 8)):
        _0x0086(_0x0463, _0x0465, _0x0070(_0x020d[_0x0467]))
    _0x0463[22] = _0x0070(_0x020d[9]) & 255
    _0x0463[23] = _0x0070(_0x020d[10]) & 255
    _0x0463[27] = _0x0070(_0x020d[16]) & 255
    _0x0463[28] = _0x0070(_0x020d[17]) & 255
    _0x0087(_0x0463, 4, _0x0070(_0x020d[18]))
    _0x0463[36] = _0x0072(_0x020d[19])
    _0x0087(_0x0463, 8, _0x0070(_0x020d[20]))
    _0x0087(_0x0463, 12, _0x0070(_0x020d[21]))
    _0x0087(_0x0463, 44, _0x0070(_0x020d[22]))
    _0x0463[48] = _0x0080(_0x020d[23], _0x0078)
    _0x0086(_0x0463, 50, _0x0070(_0x020d[24]))
    _0x0086(_0x0463, 30, _0x0070(_0x020d[25]))
    _0x0086(_0x0463, 32, _0x0070(_0x020d[26]))
    _0x0463[25] = _0x0070(_0x020d[27]) & 255
    _0x0463[26] = _0x0070(_0x020d[28]) & 255
    _0x0463[34] = _0x0072(_0x020d[14])
    _0x0463[35] = _0x0072(_0x020d[15])

    def _0x0468(_0x022a, _0x022b):
        _0x0470 = (_0x020d[_0x022a] or '').strip()
        if _0x0470 and _0x0470 != '0':
            _0x0086(_0x0463, _0x0098(_0x022b), _0x0070(_0x0470))
    _0x0469 = set(range(1, 43))
    _0x046a = {65, 66, 67}
    _0x046b = {69, 70}
    _0x046c = {43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 57, 58, 59, 60, 61, 62, 63, 64}
    if _0x0464 in _0x0469:
        _0x0086(_0x0463, _0x0098(1), _0x0070(_0x020d[29]))
        _0x0086(_0x0463, _0x0098(2), _0x0070(_0x020d[30]))
        _0x0086(_0x0463, _0x0098(3), _0x0070(_0x020d[31]))
        _0x0086(_0x0463, _0x0098(11), _0x0070(_0x020d[32]))
        _0x0086(_0x0463, 16, _0x0070(_0x020d[33]))
        _0x0463[18] = _0x0080(_0x020d[34], _0x0077)
        _0x0463[19] = _0x0070(_0x020d[35]) & 255
        _0x0463[20] = _0x0070(_0x020d[36]) & 255
        _0x0463[24] = _0x0070(_0x020d[37]) & 255
        _0x0463[40] = _0x0099.get(_0x0464, 1) & 255
        _0x0463[41] = _0x009c.get(_0x0464, 0) & 255
        _0x03de.pack_into('<H', _0x0463, 584, _0x009d.get(_0x0464, 4))
    elif _0x0464 in _0x046a:
        _0x0086(_0x0463, _0x0098(1), _0x0070(_0x020d[29]))
        _0x0086(_0x0463, _0x0098(2), _0x0070(_0x020d[30]))
        _0x0086(_0x0463, _0x0098(3), _0x0070(_0x020d[31]))
        _0x0086(_0x0463, _0x0098(11), _0x0070(_0x020d[32]))
        _0x0086(_0x0463, 16, _0x0070(_0x020d[33]))
        _0x0463[18] = _0x0080(_0x020d[34], _0x0077)
        _0x0463[40] = _0x0099.get(_0x0464, 1) & 255
        _0x0463[41] = _0x009c.get(_0x0464, 0) & 255
        _0x03de.pack_into('<H', _0x0463, 584, _0x009d.get(_0x0464, 20))
        for (_0x0467, _0x046e) in zip(range(35, 51), (10, 4, 13, 14, 5, 16, 6, 8, 7, 9, 12, 17, 18, 19, 20, 21)):
            _0x0468(_0x0467, _0x046e)
    elif _0x0464 in _0x046b:
        _0x0086(_0x0463, 16, _0x0070(_0x020d[29]))
        _0x0463[18] = _0x0080(_0x020d[30], _0x0077)
        _0x0086(_0x0463, _0x0098(12), _0x0070(_0x020d[31]))
    elif _0x0464 in _0x046c:
        _0x0463[615] = _0x0072(_0x020d[29])
        _0x0463[614] = _0x0070(_0x020d[30]) & 255
        _0x0086(_0x0463, 608, _0x0081(_0x020d[31]))
        _0x0086(_0x0463, 610, _0x0070(_0x020d[32]))
        _0x0463[600] = _0x0070(_0x020d[33]) & 255
        if _0x0464 in (48, 51):
            for (_0x0465, _0x0467) in ((588, 34), (592, 35), (596, 36)):
                _0x03de.pack_into('<f', _0x0463, _0x0465, _0x0071(_0x020d[_0x0467]))
            if _0x0463[588:600] != bytes(12) and _0x0463[18] == 0:
                _0x0463[18] = 7
        _0x0087(_0x0463, 604, _0x0070(_0x020d[37]))
        _0x0086(_0x0463, 612, _0x0081(_0x020d[38]))
        _0x046d = _0x0083(_0x020d[39], 256)
        _0x0463[284:284 + 256] = _0x046d + b'\x00' * (256 - len(_0x046d))
        _0x0463[40] = _0x009b(_0x0464, _0x020d[28])
    else:
        _0x046d = _0x0083(_0x020d[29], 256)
        _0x0463[284:284 + 256] = _0x046d + b'\x00' * (256 - len(_0x046d))
        _0x0463[40] = _0x009b(_0x0464, _0x020d[28])
    if _0x020d[51].strip():
        _0x0463[2] = _0x0070(_0x020d[51]) & 255
    if _0x020d[52].strip():
        _0x0463[3] = _0x0070(_0x020d[52]) & 255
    if _0x020d[53].strip():
        _0x0086(_0x0463, 584, _0x0070(_0x020d[53]))
    if _0x020d[54].strip():
        _0x0086(_0x0463, 586, _0x0070(_0x020d[54]))
    for (_0x0467, _0x0465) in ((55, 588), (56, 592), (57, 596)):
        if _0x020d[_0x0467].strip():
            _0x03de.pack_into('<f', _0x0463, _0x0465, _0x0071(_0x020d[_0x0467]))
    if _0x020d[58].strip():
        _0x0087(_0x0463, 600, _0x0070(_0x020d[58]))
    if _0x020d[59].strip():
        _0x0463[18] = _0x0070(_0x020d[59]) & 255
    return bytes(_0x0463)

def _0x00a2(_0x020e: str) -> int:
    return _0x03de.unpack('<I', _0x03de.pack('<f', _0x0071(_0x020e)))[0]

def _0x00a3(_0x020f: str) -> int:
    
    _0x0471 = _0x0071(_0x020f)
    _0x0472 = _0x03de.unpack('<f', _0x03de.pack('<f', _0x0471))[0]
    _0x0473 = _0x03de.unpack('<f', _0x03de.pack('<f', 0.01))[0]
    return _0x03de.unpack('<I', _0x03de.pack('<f', _0x0472 * _0x0473))[0]

def _0x00a4(_0x0210, _0x0211: bool=False) -> bytes:
    
    _0x0210 = list(_0x0210) + [''] * (121 - len(_0x0210))
    _0x0474 = bytearray(552)
    _0x0086(_0x0474, 348, _0x0070(_0x0210[0]))
    _0x03de.pack_into('<I', _0x0474, 8, 8)
    _0x03de.pack_into('<I', _0x0474, 24, 1)
    _0x03de.pack_into('<I', _0x0474, 40, 2)
    _0x03de.pack_into('<I', _0x0474, 56, 24)
    for (_0x0475, _0x0476, _0x0477) in ((64, 64, 1), (128, 32, 2)):
        _0x047a = _0x0082(_0x0210[_0x0477], _0x0476)
        _0x0474[_0x0475:_0x0475 + _0x0476] = _0x047a + b'\x00' * (_0x0476 - len(_0x047a))
    _0x0474[396] = _0x0072(_0x0210[3])
    _0x0474[370] = _0x0070(_0x0210[4]) & 255
    _0x0474[392] = _0x0072(_0x0210[6])
    if _0x0474[392]:
        _0x0474[366] = _0x0070(_0x0210[68]) & 255
    else:
        _0x0474[366] = _0x0080(_0x0210[5], _0x007d)
    _0x0474[12] = _0x0070(_0x0210[7]) & 255
    if _0x0211 and _0x0210[8].strip():
        _0x03de.pack_into('<I', _0x0474, 4, _0x00a2(_0x0210[8]))
    else:
        _0x03de.pack_into('<I', _0x0474, 4, _0x00a3(_0x0210[8]))
    _0x0474[28] = _0x0070(_0x0210[9]) & 255
    if _0x0211 and _0x0210[10].strip():
        _0x03de.pack_into('<I', _0x0474, 20, _0x00a2(_0x0210[10]))
    else:
        _0x03de.pack_into('<I', _0x0474, 20, _0x00a3(_0x0210[10]))
    (_0x0478, _0x0479) = (_0x0070(_0x0210[11]), _0x0070(_0x0210[12]))
    if _0x0478 != _0x0479:
        output.warn(f'monster row {_0x0210[0]}: columns 11/12 disagree ({_0x0478} vs {_0x0479}); using {_0x0478}')
    _0x0474[44] = _0x0478 & 255
    _0x03de.pack_into('<I', _0x0474, 60, _0x0478)
    _0x03de.pack_into('<I', _0x0474, 212, _0x0070(_0x0210[65]))
    _0x03de.pack_into('<I', _0x0474, 216, _0x0070(_0x0210[66]))
    for (_0x0475, _0x0477) in ((160, 13), (164, 14), (168, 15), (172, 16), (360, 18), (356, 37), (388, 52)):
        _0x03de.pack_into('<I', _0x0474, _0x0475, _0x00a2(_0x0210[_0x0477]))
    _0x0086(_0x0474, 364, _0x0070(_0x0210[17]))
    _0x0087(_0x0474, 456, _0x0070(_0x0210[19]))
    _0x0474[464] = _0x0070(_0x0210[20]) & 255
    for (_0x0475, _0x0477) in ((472, 21), (474, 22), (478, 23), (476, 24), (480, 25), (492, 26), (490, 28), (500, 30), (502, 31), (482, 33), (486, 34), (484, 35), (488, 36), (374, 45), (376, 46), (378, 47), (380, 48), (382, 49), (176, 54), (178, 55), (180, 56), (182, 57), (184, 58), (188, 59), (192, 60), (196, 61), (200, 62), (204, 63)):
        _0x0086(_0x0474, _0x0475, _0x0070(_0x0210[_0x0477]))
    _0x0474[544] = _0x0070(_0x0210[29]) & 255
    _0x0474[494] = _0x0070(_0x0210[32]) & 255
    _0x0474[367] = _0x0070(_0x0210[38]) & 255
    _0x0474[393] = _0x0072(_0x0210[39])
    _0x0474[394] = _0x0072(_0x0210[40])
    _0x0474[395] = _0x0072(_0x0210[41])
    _0x0474[369] = _0x0072(_0x0210[42])
    _0x0474[368] = _0x0070(_0x0210[43]) & 255
    _0x0474[372] = _0x0070(_0x0210[44]) & 255
    _0x0474[384] = _0x0070(_0x0210[50]) & 255
    _0x0474[385] = _0x0070(_0x0210[51]) & 255
    _0x0087(_0x0474, 352, _0x0070(_0x0210[53]))
    _0x0087(_0x0474, 208, _0x0070(_0x0210[64]))
    _0x0474[244] = _0x0070(_0x0210[73]) & 255
    _0x0474[344] = _0x0070(_0x0210[98]) & 255
    _0x0474[345] = _0x0070(_0x0210[98]) & 255
    _0x0474[452] = _0x0080(_0x0210[100], _0x007e) & 255
    _0x0474[453] = _0x0070(_0x0210[101]) & 255
    _0x03de.pack_into('<I', _0x0474, 400, _0x0070(_0x0210[102]))
    _0x03de.pack_into('<I', _0x0474, 404, _0x0070(_0x0210[103]))
    for (_0x0475, _0x0477) in ((220, 74), (224, 75), (228, 76), (232, 77), (236, 78)):
        _0x03de.pack_into('<I', _0x0474, _0x0475, _0x0070(_0x0210[_0x0477]))
    for (_0x0475, _0x0477) in ((240, 79), (242, 80), (246, 82), (248, 83), (250, 84), (252, 85), (260, 86), (264, 87), (268, 88), (454, 120)):
        _0x0086(_0x0474, _0x0475, _0x0070(_0x0210[_0x0477]))
    _0x0474[245] = _0x0070(_0x0210[81]) & 255
    _0x0086(_0x0474, 190, _0x0070(_0x0210[107]))
    for (_0x0475, _0x0477) in ((272, 89), (276, 90), (280, 91), (284, 92), (288, 93), (292, 94), (296, 95), (300, 96), (304, 97), (308, 104), (312, 105), (316, 106)):
        _0x03de.pack_into('<I', _0x0474, _0x0475, _0x0070(_0x0210[_0x0477]))
    for (_0x0475, _0x0477) in ((408, 108), (412, 109), (416, 110), (420, 111), (424, 112), (428, 113), (432, 114), (436, 116), (440, 117), (444, 118), (448, 119)):
        _0x03de.pack_into('<I', _0x0474, _0x0475, _0x0070(_0x0210[_0x0477]))
    return bytes(_0x0474)

def _0x00a5(_0x0212) -> bytes:
    _0x0212 = list(_0x0212) + [''] * (37 - len(_0x0212))
    _0x047b = bytearray(516)
    _0x0086(_0x047b, 472, _0x0081(_0x0212[0]))
    _0x03de.pack_into('<I', _0x047b, 456, _0x0080(_0x0212[1], _0x0079))
    _0x047b[506] = 1 if _0x0212[2].strip() not in ('', '0') else 0
    for (_0x047c, _0x047d, _0x047e) in ((96, 64, 3), (64, 32, 18), (0, 32, 19), (32, 32, 20), (160, 32, 23)):
        _0x0480 = _0x0082(_0x0212[_0x047e], _0x047d)
        _0x047b[_0x047c:_0x047c + _0x047d] = _0x0480 + b'\x00' * (_0x047d - len(_0x0480))
    _0x03de.pack_into('<I', _0x047b, 464, _0x0080(_0x0212[4], _0x007a))
    _0x047b[468] = _0x0080(_0x0212[5], _0x007b)
    _0x047b[470] = _0x0074(_0x0212[6]) & 255
    _0x047b[469] = _0x0080(_0x0212[7], _0x007b)
    _0x047b[471] = _0x0074(_0x0212[8]) & 255
    _0x03de.pack_into('<I', _0x047b, 460, _0x0080(_0x0212[9], _0x007c))
    for (_0x047c, _0x047e) in ((492, 10), (496, 11), (500, 12)):
        _0x03de.pack_into('<f', _0x047b, _0x047c, _0x0071(_0x0212[_0x047e]))
    for (_0x047c, _0x047e) in ((474, 13), (476, 14), (478, 15), (480, 16), (482, 17)):
        _0x0086(_0x047b, _0x047c, _0x0070(_0x0212[_0x047e]))
    _0x0087(_0x047b, 488, _0x0070(_0x0212[21]))
    _0x047b[510] = _0x0070(_0x0212[22]) & 255
    for (_0x047c, _0x047e) in ((192, 24), (194, 25), (196, 26), (198, 27)):
        _0x0086(_0x047b, _0x047c, _0x0070(_0x0212[_0x047e]))
    _0x047b[511] = _0x0070(_0x0212[28]) & 255
    _0x047b[509] = _0x0070(_0x0212[29]) & 255
    _0x047b[504] = _0x0073(_0x0212[30])
    _0x047b[507] = _0x0073(_0x0212[31])
    _0x047b[508] = _0x0073(_0x0212[32])
    _0x047b[505] = _0x0073(_0x0212[33])
    for (_0x047c, _0x047e) in ((484, 34), (486, 35)):
        _0x0481 = _0x0212[_0x047e].strip()
        _0x0086(_0x047b, _0x047c, _0x0081(_0x0481) if _0x0481 and _0x0481 != '0' else 0)
    _0x047f = _0x0090(_0x0212[36])
    if len(_0x047f) > 256:
        output.warn(f'skill description too long ({len(_0x047f)} > 256); truncating: {_0x0212[36][:40]!r}')
        _0x047f = _0x047f[:256]
    _0x047b[200:200 + len(_0x047f)] = _0x047f
    return bytes(_0x047b)

def _0x00a6(_0x0213) -> bytes:
    
    _0x0482 = {}
    for _0x0483 in _0x0213:
        _0x0485 = _0x0081(_0x0483[0])
        _0x0482.setdefault(_0x0485, []).append(_0x0483)
    _0x0484 = []
    for _0x0485 in sorted(_0x0482):
        _0x0486 = _0x0482[_0x0485][:5]
        if len(_0x0482[_0x0485]) > 5:
            output.warn(f'skill {_0x0485:#06x} has {len(_0x0482[_0x0485])} level rows; keeping the first 5')
        _0x0487 = [_0x00a5(_0x0488) for _0x0488 in _0x0486]
        _0x0487 += [b'\x00' * 516] * (5 - len(_0x0487))
        _0x0484.append(b''.join(_0x0487))
    return b''.join(_0x0484)

def _0x00a7(_0x0214) -> bytes:
    _0x0214 = list(_0x0214) + [''] * (9 - len(_0x0214))
    return _0x03de.pack('<3H4B', _0x0070(_0x0214[1]), _0x0070(_0x0214[4]), _0x0070(_0x0214[7]), _0x0070(_0x0214[2]), _0x0070(_0x0214[5]), _0x0070(_0x0214[8]), 0)

def _0x00a8(_0x0215: str) -> bytes:
    _0x0489 = _0x006f(_0x0215)
    if len(_0x0489) > 15:
        output.warn(f'abuse word longer than 15 bytes; truncating {_0x0489!r}')
        _0x0489 = _0x0489[:15]
    return _0x0489 + b'\x00' * (15 - len(_0x0489))
_0x00a9 = 1048576

def _0x00aa(_0x0216: _0x03df) -> bytes:
    _0x048a = _0x0216.read_bytes()
    if len(_0x048a) != 18 + _0x00a9:
        raise ValueError(f'{_0x0216.name}: {len(_0x048a):,} bytes; the zone map must be an 18-byte TGA + {_0x00a9:,} px bytes')
    if _0x048a[2] != 2:
        raise ValueError(f'{_0x0216.name}: TGA type {_0x048a[2]}, type 2 expected')
    (_0x048b, _0x048c, _0x048d, _0x048e) = _0x03de.unpack_from('<HHBB', _0x048a, 12)
    if (_0x048b, _0x048c, _0x048d) != (512, 512, 32):
        raise ValueError(f'{_0x0216.name}: {_0x048b}x{_0x048c}x{_0x048d} TGA; 512x512x32 expected')
    _0x048f = _0x048a[18:]
    if _0x048e & 32:
        return b''.join((_0x048f[_0x0490 * 2048:(_0x0490 + 1) * 2048] for _0x0490 in range(512)))
    return b''.join((_0x048f[_0x0491 * 2048:(_0x0491 + 1) * 2048] for _0x0491 in range(511, -1, -1)))

def _0x00ab(_0x0217: _0x03df) -> dict:
    
    if not _0x0217.exists():
        return {}
    _0x0492 = {}
    for _0x0493 in _0x0217.read_text(encoding='ascii').splitlines():
        _0x0493 = _0x0493.strip()
        if not _0x0493 or _0x0493.startswith('//'):
            continue
        _0x0494 = _0x0493.split()
        if len(_0x0494) != 6:
            raise ValueError(f'{_0x0217.name}: unparsable junk line {_0x0493[:60]!r}')
        (_, _0x0496, _0x0497, _0x0498, _0x0499, _0x049a) = _0x0494
        _0x049b = bytes.fromhex(_0x0497)
        if len(_0x049b) != 32:
            raise ValueError(f'{_0x0217.name}: junk name field {len(_0x049b)} bytes, 32 expected')
        _0x049c = int(_0x0496, 16)
        if _0x049c in _0x0492:
            raise ValueError(f'{_0x0217.name}: duplicate junk colour 0x{_0x049c:08X}')
        _0x0492[_0x049c] = (_0x049b, int(_0x0498, 16), int(_0x0499, 16), int(_0x049a, 16))
    return _0x0492

def _0x00ac(_0x0218: str, _0x0219=None) -> bytes:
    
    if _0x0219 is not None:
        return _0x0219
    _0x049d = (_0x0218.encode('latin-1', 'replace') + b'\n')[:31]
    return (_0x049d + b'\x00').ljust(32, b'\x00')

def _0x00ad(_0x021a: _0x03df, _0x021b) -> bytes:
    (_0x049e, _0x049f) = ([], None)
    for _0x04a0 in _0x021b:
        if not _0x04a0.strip():
            continue
        _0x04a7 = _0x04a0.split('\t')
        _0x04a8 = _0x04a7[0].strip()
        _0x04a9 = _0x04a7[1:]
        if _0x04a8 == 'VEIN_COLOR':
            _0x049f = {'color': _0x0070(_0x04a9[0]), 'name': '', 'fert': 0, 'minerals': []}
            _0x049e.append(_0x049f)
        elif _0x04a8 == 'VEIN_NAME':
            if _0x049f is None:
                raise ValueError('VEIN_NAME before any VEIN_COLOR')
            _0x049f['name'] = _0x04a9[0] if _0x04a9 else ''
        elif _0x04a8 == 'FERTILITY':
            if _0x049f is None:
                raise ValueError('FERTILITY before any VEIN_COLOR')
            _0x049f['fert'] = _0x0070(_0x04a9[0])
        elif _0x04a8 == 'VEIN_RAW':
            if _0x049f is None:
                raise ValueError('VEIN_RAW before any VEIN_COLOR')
            if len(_0x04a9) < 4:
                raise ValueError(f'VEIN_RAW wants 4 fields (name32 hex, +0x28, +0x2C, list-head): {_0x04a0[:60]!r}')
            if 'raw' in _0x049f:
                raise ValueError(f"duplicate VEIN_RAW for colour 0x{_0x049f['color']:08X}")
            _0x04b0 = bytes.fromhex(_0x04a9[0])
            if len(_0x04b0) != 32:
                raise ValueError(f'VEIN_RAW name field {len(_0x04b0)} bytes, 32 expected')
            _0x049f['raw'] = (_0x04b0, int(_0x04a9[1], 16), int(_0x04a9[2], 16), int(_0x04a9[3], 16))
        elif _0x04a8 == 'MINERAL':
            if _0x049f is None:
                raise ValueError('MINERAL before any VEIN_COLOR')
            _0x049f['minerals'].append((_0x0070(_0x04a9[0]), _0x0070(_0x04a9[1]), _0x0070(_0x04a9[2])))
        else:
            raise ValueError(f'unknown MineralVein token: {_0x04a8!r}')
    if not _0x049e:
        raise ValueError('no VEIN_COLOR directive found')
    _0x04a1 = [_0x04b1['color'] for _0x04b1 in _0x049e]
    _0x04a2 = sorted({_0x04b2 for _0x04b2 in _0x04a1 if _0x04a1.count(_0x04b2) > 1})
    if _0x04a2:
        raise ValueError(f"duplicate VEIN_COLOR entries (the converter's loader rejects them too): " + ', '.join((f'0x{_0x04b3:08X}' for _0x04b3 in _0x04a2)))
    _0x04a3 = _0x00aa(_0x021a.with_suffix('.tga'))
    _0x04a4 = _0x00ab(_0x021a.with_suffix('.junk'))
    if _0x04a4 and any((_0x04b4.get('raw') is None for _0x04b4 in _0x049e)):
        if set(_0x04a4) != set(_0x04a1):
            raise ValueError(f'{_0x021a.name}: the .junk sidecar covers ' + ', '.join((f'0x{_0x04b5:08X}' for _0x04b5 in sorted(_0x04a4))) + " which does not match the txt's vein colours")
    _0x04a5 = [_0x03de.pack('<I', len(_0x049e)), _0x04a3]
    for _0x04a6 in sorted(_0x049e, key=lambda _0x022d: _0x022d['color']):
        _0x04aa = len(_0x04a6['minerals'])
        (_0x04ab, _0x04ac, _0x04ad, _0x04ae) = (None, 0, 0, 0)
        _0x04af = _0x04a6.get('raw')
        if _0x04af is not None:
            (_0x04ab, _0x04ac, _0x04ad, _0x04ae) = _0x04af
        elif _0x04a4 and _0x04a6['color'] in _0x04a4:
            (_0x04ab, _0x04ac, _0x04ad, _0x04ae) = _0x04a4[_0x04a6['color']]
        _0x04a5.append(_0x03de.pack('<I', _0x04aa))
        _0x04a5.append(_0x00ac(_0x04a6['name'], _0x04ab) + _0x03de.pack('<6I', _0x04a6['color'], _0x04a6['fert'], _0x04ac, _0x04ad, _0x04ae, _0x04aa))
        _0x04a5 += [_0x03de.pack('<I', _0x04b6[0] & 65535 | (_0x04b6[1] & 255) << 16 | (_0x04b6[2] & 255) << 24) for _0x04b6 in _0x04a6['minerals']]
    output.detail(f"{_0x021a.name}: {len(_0x049e):,} veins, {sum((len(_0x04b7['minerals']) for _0x04b7 in _0x049e)):,} minerals, garbage slots {('inline' if all((_0x04b8.get('raw') is not None for _0x04b8 in _0x049e)) else 'sidecar' if _0x04a4 else 'zeroed')}.")
    return b''.join(_0x04a5)
_0x00ae = 69
_0x00af = {'SHIRT': 1, 'TUNIC': 2, 'CON_ARMOUR': 3, 'CON_HELM': 4, 'CON_GLOVE': 5, 'CON_BOOTS': 6, 'DEX_ARMOUR': 7, 'DEX_HELM': 8, 'DEX_GLOVE': 9, 'DEX_BOOTS': 10, 'ONEHANDED_SWORD': 11, 'TWOHANDED_SWORD': 12, 'ONEHANDED_AXE': 13, 'TWOHANDED_AXE': 14, 'ONEHANDED_BLUNT': 15, 'TWOHANDED_BLUNT': 16, 'BOW': 17, 'CROSSBOW': 18, 'STAFF': 19, 'DAGGER': 20, 'SHIELD': 21, 'CON_BODY': 22, 'CON_HEAD': 23, 'CON_PELVIS': 24, 'CON_PROTECT_A': 25, 'DEX_BODY': 26, 'DEX_HEAD': 27, 'DEX_PELVIS': 28, 'DEX_PROTECT_A': 29, 'COM_BLUNT': 30, 'COM_SWORD': 31, 'OPP_HAMMER': 32, 'OPP_AXE': 33, 'OPP_SLUSHER': 34, 'OPP_TALON': 35, 'OPP_SYTHE': 36, 'SKILL_A_GUARD': 37, 'SKILL_A_ATTACK': 38, 'SKILL_A_GUN': 39, 'SKILL_A_KNIFE': 40, 'ARROW': 41, 'BOLT': 42}

def _0x00b0(_0x021c: bytes) -> bool:
    return _0x021c.lstrip(b' \t').startswith(b'//')

def _0x00b1(_0x021d: bytes) -> list:
    
    _0x04b9 = [[] for _ in range(_0x00ae)]
    _0x04ba = None
    _0x04bb = _0x04bc = None
    for _0x04bd in _0x021d.split(b'\n'):
        if _0x00b0(_0x04bd):
            continue
        _0x04be = _0x04bd.rstrip(b'\r').split(b'\t')
        if _0x04ba is None:
            if _0x04be[0].strip() == b'ID':
                _0x04ba = {_0x04c3.strip().decode('latin-1'): _0x04c2 for (_0x04c2, _0x04c3) in enumerate(_0x04be) if _0x04c3.strip()}
                _0x04bb = _0x04ba.get('ItemType')
                _0x04bc = _0x04ba.get('DropOption')
            continue
        if not _0x04be or not _0x04be[0].strip().isdigit():
            continue
        if _0x04bb is None or _0x04bc is None or _0x04bc >= len(_0x04be):
            continue
        try:
            _0x04c0 = int(_0x04be[_0x04bc].strip().decode('latin-1'))
        except ValueError:
            continue
        if _0x04c0 == 0:
            continue
        _0x04bf = _0x00af.get(_0x04be[_0x04bb].strip().decode('latin-1'))
        if _0x04bf is None:
            continue
        _0x04b9[_0x04bf].append(int(_0x04be[0]) & 65535)
    return _0x04b9

def _0x00b2(_0x021e: bytes) -> list:
    
    _0x04c4 = []
    _0x04c5 = None
    for _0x04c6 in _0x021e.split(b'\n'):
        if _0x00b0(_0x04c6):
            continue
        _0x04c7 = _0x04c6.rstrip(b'\r').strip()
        if not _0x04c7:
            continue
        if _0x04c7.startswith(b';'):
            if _0x04c5 is not None:
                _0x04c4.append(_0x04c5)
            _0x04c5 = []
            continue
        if _0x04c5 is None:
            output.warn(f"SpeacialCompensation.txt: id line before the first '//'/{';'} marker dropped: {_0x04c6[:60]!r}")
            continue
        for _0x04c8 in _0x04c7.split(b'\t'):
            _0x04c9 = _0x04c8.strip()
            if not _0x04c9 or not _0x04c9.isdigit():
                continue
            _0x04c5.append(int(_0x04c9) & 65535)
    if _0x04c5 is not None:
        _0x04c4.append(_0x04c5)
    return _0x04c4

def _0x00b3(_0x021f) -> bytes:
    
    _0x04ca = _0x03df(_0x021f)
    _0x04cb = _0x04ca.read_bytes()
    _0x04cc = b'SpeacialLayout: case-only' in _0x04cb
    if not _0x04cc:
        _0x04d1 = _0x04ca.with_name('ItemScript.txt')
        if not _0x04d1.exists() and _0x04ca.parent.is_dir():
            for _0x04d4 in sorted(_0x04ca.parent.iterdir()):
                if _0x04d4.name.lower() == 'itemscript.txt':
                    _0x04d1 = _0x04d4
                    break
        if not _0x04d1.exists():
            raise RuntimeError(f'{_0x04ca.name}: the sibling ItemScript.txt is required - the converter derives the auto slot groups from the loaded item table (CItemMgr::LoadItemSpeacialCompensation)')
        _0x04d2 = _0x00b1(_0x04d1.read_bytes())
    else:
        _0x04d2 = []
    _0x04cd = _0x00b2(_0x04cb)
    _0x04ce = bytearray()
    for _0x04cf in range(len(_0x04d2)):
        for _0x04d3 in _0x04d2[_0x04cf]:
            _0x04ce += _0x03de.pack('<H', _0x04d3)
        _0x04ce += b'\x00\x00'
    for _0x04d0 in _0x04cd:
        for _0x04d3 in _0x04d0:
            _0x04ce += _0x03de.pack('<H', _0x04d3)
        _0x04ce += b'\x00\x00'
    return bytes(_0x04ce)

def _0x00b4(_0x0220) -> int:
    
    _0x04d5 = 0
    while _0x04d5 < len(_0x0220):
        _0x04d6 = _0x0220[_0x04d5]
        if isinstance(_0x04d6, bytes):
            _0x04d6 = _0x04d6.decode('utf-8', 'replace')
        if not _0x04d6.strip() or _0x04d6.lstrip().startswith('/'):
            _0x04d5 += 1
            continue
        break
    return _0x04d5

def _0x00b5(_0x0221: str) -> list:
    return _0x0221.split('\t')

def _0x00b6(_0x0222: str, _0x0223: str='ID') -> bool:
    if not _0x0222:
        return False
    return _0x0222.split('\t', 1)[0].strip() == _0x0223

def _0x00b7(_0x0224, _0x0225=None) -> bytes:
    
    _0x04d7 = _0x03df(_0x0224)
    _0x04d8 = _0x04d7.stem
    _0x04d9 = _0x04d8.lower()
    _0x04da = _0x04d7.read_bytes()
    _0x04db = _0x04da.decode('utf-8', 'replace')
    _0x04dc = _0x04db.splitlines()
    _0x04dd = _0x00b4(_0x04dc)
    _0x04de = _0x006c(_0x04dc[:_0x04dd + 2])
    _0x04df = _0x04de.get('schema')
    if _0x04df is None:
        if _0x04d9 == 'script1':
            _0x04d9 = 'abuse'
        elif _0x04d9.startswith('mineralvein'):
            _0x04d9 = 'mineralvein'
        _0x04df = _0x04d9
    if _0x04df != 'mineralvein' and _0x04df not in _0x006a:
        raise RuntimeError(f'no GSF encoder for schema {_0x04df!r} ({_0x04d7.name})')
    _0x04e0 = _0x006e(_0x04de)
    if _0x04e0 is None and _0x04de.get('schema') == 'mineralvein':
        _0x04e0 = (0, 3)
    _0x04e1 = f'{_0x04d8}.gsf' if _0x04de.get('schema') else _0x0065.get(_0x04df, f'{_0x04d8}.gsf')
    if _0x04df == 'monsterchat':
        _0x04e5 = b'\r\n' if b'\r\n' in _0x04da else b'\n'
        _0x04e6 = _0x04da.split(_0x04e5)
        if len(_0x04e6) >= 4 and b'rDecompiler' in _0x04e6[1]:
            _0x04e7 = 4
            while _0x04e7 < len(_0x04e6) and _0x04e6[_0x04e7].lstrip().startswith(b'// rDec-'):
                _0x04e7 += 1
            if _0x04e7 < len(_0x04e6) and (not _0x04e6[_0x04e7].strip(b' \t\r')):
                _0x04e7 += 1
        else:
            _0x04e7 = _0x00b4(_0x04e6)
        from modules.translations import _0x0177 as _0x0177
        _0x04e8 = []
        for _0x04e9 in _0x04e6[_0x04e7:]:
            try:
                _0x04ea = _0x04e9.decode('utf-8')
                _0x04eb = _0x0177(_0x04ea)
                if _0x04eb is not None:
                    _0x04e8.append(_0x04eb)
                else:
                    _0x04e8.append(_0x04e9)
            except Exception:
                _0x04e8.append(_0x04e9)
        return _0x04e5.join(_0x04e8)
    _0x04e2 = any((_0x04f2.lstrip().startswith('// MonsterVelocity: raw-f32') for _0x04f2 in _0x04dc[:_0x04dd + 2]))
    _0x04e3 = _0x04dc[_0x04dd:]
    while _0x04e3 and (not _0x04e3[-1].strip()):
        _0x04e3.pop()
    if _0x04df == 'itemscript':
        _0x04e6 = _0x04da.split(b'\n')
        _0x04e7 = 0
        for _0x04e8 in _0x04e6:
            if _0x04e8.lstrip(b' \t\r').startswith(b'/') or not _0x04e8.strip(b' \t\r'):
                _0x04e7 += 1
                continue
            break
        _0x04e6 = _0x04e6[_0x04e7:]
        if _0x04e6 and _0x04e6[0].split(b'\t', 1)[0].strip() == b'ID':
            _0x04e6 = _0x04e6[1:]
        _0x04e9 = [_0x04f3.split(b'\t') for _0x04f3 in _0x04e6]
        _0x04e9 = [_0x04f4 for _0x04f4 in _0x04e9 if any((_0x04f5.strip(b' \t\r') for _0x04f5 in _0x04f4))]
        _0x04e9.sort(key=lambda _0x022f: _0x0070(_0x022f[0].decode('latin-1')))
        _0x04ea = bytearray()
        _0x04eb = _0x009f(_0x04d7.with_suffix('.junk'))
        for _0x04ec in _0x04e9:
            _0x04ed = bytearray(_0x00a1(_0x04ec))
            _0x00a0(_0x04ed, _0x04eb)
            _0x04ea += _0x04ed
        _0x04ea = bytes(_0x04ea)
    elif _0x04df == 'monsterprototype':
        _0x04e9 = []
        _0x04ee = _0x04e2
        for _0x04ef in _0x04e3:
            _0x04f0 = _0x04ef.strip()
            if not _0x04f0:
                continue
            if _0x04f0.startswith('//'):
                if _0x04f0.startswith('// MonsterVelocity: raw-f32'):
                    _0x04ee = True
                continue
            _0x04e9.append(_0x00b5(_0x04ef))
        _0x04e9.sort(key=lambda _0x0230: _0x0070(_0x0230[0]))
        _0x04ea = b''.join((_0x00a4(_0x04f6, _0x04ee) for _0x04f6 in _0x04e9))
    elif _0x04df == 'skillscript':
        _0x04f1 = 1 if _0x04e3 and _0x00b6(_0x04e3[0]) else 0
        _0x04e9 = [_0x00b5(_0x04f7) for _0x04f7 in _0x04e3[_0x04f1:] if _0x04f7.strip()]
        _0x04ea = _0x00a6(_0x04e9)
    elif _0x04df == 'chemical':
        if _0x04e3 and 'Pickking' in _0x04e3[0]:
            _0x04e3 = _0x04e3[1:]
        if _0x04e3 and (lambda _0x0230: len(_0x0230) >= 6 and _0x0230[0].strip() == 'Name' and (_0x0230[1].strip() == 'ID') and (_0x0230[2].strip() == 'Num'))(_0x04e3[0].split('\t')):
            _0x04e3 = _0x04e3[1:]
        _0x04e9 = [_0x00b5(_0x04f8) for _0x04f8 in _0x04e3 if _0x04f8.strip()]
        _0x04ea = b''.join((_0x00a7(_0x04f9) for _0x04f9 in _0x04e9))
    elif _0x04df == 'abuse':
        _0x04ea = b''.join((_0x00a8(_0x04fa) for _0x04fa in _0x04dc[_0x04dd:]))
    elif _0x04df == 'speacialcompensation':
        _0x04ea = _0x00b3(_0x04d7)
    elif _0x04df == 'mineralvein':
        _0x04ea = _0x00ad(_0x04d7, _0x04e3)
    else:
        raise RuntimeError(f'no GSF row encoder for {_0x04df}')
    _0x04e4 = _0x008a(_0x0225) if _0x0225 else b''
    return _0x0089(_0x04ea, _0x04e1, _0x04e4, _0x01f7=_0x04e0)

def _0x00b8(_0x0226: str):
    
    _0x04fb = _0x03df(_0x0226)
    _0x04fc = {}
    if _0x04fb.suffix.lower() == '.txt' and _0x04fb.exists():
        try:
            _0x04fc = _0x006c(_0x006d(_0x04fb))
        except OSError:
            pass
    _0x04fd = _0x04fc.get('schema')
    if _0x04fd == 'mcf':
        return (_0x04fb.stem + '.mcf', None)
    if _0x04fd == 'skillscriptex':
        return (None, 'SKIP: ' + _0x0067['skillscriptex'] + ' needs a LuaJIT bytecode writer (not available in this build).')
    if _0x04fd is not None:
        if _0x04fd in _0x006a:
            return (_0x04fb.stem + '.gsf', None)
        return (None, f'no compile target for schema {_0x04fd!r} (RYL1 GSF schemas are not compilable in this build)')
    _0x04fe = _0x04fb.stem.lower()
    if _0x04fe in _0x0065:
        return (_0x0065[_0x04fe], None)
    if _0x04fe.startswith('mineralvein'):
        return (_0x04fb.stem + '.gsf', None)
    if _0x04fe in _0x0066:
        return (_0x0066[_0x04fe], None)
    if _0x04fe in _0x0067:
        return (None, 'SKIP: ' + _0x0067[_0x04fe] + ' needs a LuaJIT bytecode writer (not available in this build).')
    return (None, 'no compile target')

def _0x00b9(_0x0227, _0x0228=None) -> bytes:
    
    _0x04ff = _0x03df(_0x0227)
    _0x0500 = _0x006c(_0x006d(_0x04ff)).get('schema')
    if _0x0500 == 'mcf':
        return _0x0097(_0x04ff)
    if _0x0500 == 'skillscriptex':
        raise RuntimeError('SKIP: ' + _0x0067['skillscriptex'] + ' needs a LuaJIT bytecode writer (not available in this build).')
    if _0x0500 in ('ryl1-item', 'ryl1-monster'):
        raise RuntimeError(f'SKIP: RYL1 GSF schema {_0x0500!r} is not compilable in this build.')
    if _0x0500 is None:
        _0x0501 = _0x04ff.stem.lower()
        if _0x0501 in _0x0066:
            return _0x0097(_0x04ff)
        if _0x0501 in _0x0067:
            raise RuntimeError('SKIP: ' + _0x0067[_0x0501] + ' needs a LuaJIT bytecode writer (not available in this build).')
    return _0x00b7(_0x04ff, _0x0228)
