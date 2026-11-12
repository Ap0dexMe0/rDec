import os as _0x02fe
from sys import stdout as _0x0300
try:
    from colorama import Fore as _0x0010
except ImportError:

    class _0x000f:

        def __getattr__(_0x0191, _0x0192):
            return ''
    _0x0010 = _0x000f()

def _0x000b():
    _0x02fe.system('cls' if _0x02fe.name == 'nt' else 'clear')

def _0x000c():
    _0x0300.write('' + _0x0010.LIGHTRED_EX + '██████╗ ██████╗ ███████╗ ██████╗\n')
    _0x0300.write('' + _0x0010.LIGHTRED_EX + '██╔══██╗██╔══██╗██╔════╝██╔════╝\n')
    _0x0300.write('' + _0x0010.LIGHTRED_EX + '██████╔╝██║  ██║█████╗  ██║     \n')
    _0x0300.write('' + _0x0010.LIGHTRED_EX + '██╔══██╗██║  ██║██╔══╝  ██║     \n')
    _0x0300.write('' + _0x0010.LIGHTRED_EX + '██║  ██║██████╔╝███████╗╚██████╗\n')
    _0x0300.write('' + _0x0010.LIGHTRED_EX + '╚═╝  ╚═╝╚═════╝ ╚══════╝ ╚═════╝\n')
    _0x0300.write('' + _0x0010.YELLOW + '═════════════╦═════════════════════════════════╦══════════════════════════════\n')
    _0x0300.write('' + _0x0010.YELLOW + '╔════════════╩═════════════════════════════════╩═════════════════════════════╗\n')
    _0x0300.write('' + _0x0010.YELLOW + '║ ' + _0x0010.LIGHTRED_EX + '• ' + _0x0010.GREEN + 'AUTHOR             ' + _0x0010.YELLOW + '    |' + _0x0010.LIGHTWHITE_EX + '   Ap0dex Me0                                    ' + _0x0010.YELLOW + '║\n')
    _0x0300.write('' + _0x0010.YELLOW + '╠════════════════════════════════════════════════════════════════════════════╣\n')
    _0x0300.write('' + _0x0010.YELLOW + '║ ' + _0x0010.LIGHTRED_EX + '• ' + _0x0010.GREEN + 'GITHUB             ' + _0x0010.YELLOW + '    |' + _0x0010.LIGHTWHITE_EX + '   GITHUB.COM/AP0DEXME0                          ' + _0x0010.YELLOW + '║\n')
    _0x0300.write('' + _0x0010.YELLOW + '╚════════════════════════════════════════════════════════════════════════════╝\n')
    print(f'{_0x0010.YELLOW}[RDEC] - {_0x0010.GREEN}Return Of Warrior (ROW) & Risk Your Life (RYL) 1/2 MMORPG {_0x0010.YELLOW}[V0.5]{_0x0010.RESET}\n')

def _0x000d():
    _0x000b()
    _0x000c()

def _0x000e(_0x0190=None):
    from datetime import datetime as _0x0301
    import sys as _0x0302
    if _0x0190 is None:
        _0x0190 = _0x0301.now().strftime('%#m/%#d/%Y %#I:%M:%S %p') if _0x0302.platform == 'win32' else _0x0301.now().strftime('%-m/%-d/%Y %-I:%M:%S %p')
    _0x0303 = f'// rDecompiler By Ap0dexMe0 {_0x0190}   //'
    _0x0304 = '/' * max(52, len(_0x0303) + 1)
    return [_0x0304, _0x0303, _0x0304]
