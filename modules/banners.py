import os, time
from sys import stdout
try:
    from colorama import Fore, Style
except ImportError:
    class _NoColor:
        def __getattr__(self, _name):
            return ""
    Fore, Style = _NoColor(), _NoColor()


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def banners():
    stdout.write("                                                                                         \n")
    stdout.write(""+Fore.LIGHTRED_EX +"██████╗ ██████╗ ███████╗ ██████╗\n")
    stdout.write(""+Fore.LIGHTRED_EX +"██╔══██╗██╔══██╗██╔════╝██╔════╝\n")
    stdout.write(""+Fore.LIGHTRED_EX +"██████╔╝██║  ██║█████╗  ██║     \n")
    stdout.write(""+Fore.LIGHTRED_EX +"██╔══██╗██║  ██║██╔══╝  ██║     \n")
    stdout.write(""+Fore.LIGHTRED_EX +"██║  ██║██████╔╝███████╗╚██████╗\n")
    stdout.write(""+Fore.LIGHTRED_EX +"╚═╝  ╚═╝╚═════╝ ╚══════╝ ╚═════╝\n")
    stdout.write(""+Fore.YELLOW +"═════════════╦═════════════════════════════════╦══════════════════════════════\n")
    stdout.write(""+Fore.YELLOW   +"╔════════════╩═════════════════════════════════╩═════════════════════════════╗\n")
    stdout.write(""+Fore.YELLOW   +"║ \x1b[38;2;255;20;147m• "+Fore.GREEN+"AUTHOR             "+Fore.RED+"    |"+Fore.LIGHTWHITE_EX+"   Ap0dex Me0                                    "+Fore.YELLOW+"║\n")
    stdout.write(""+Fore.YELLOW   +"╔════════════════════════════════════════════════════════════════════════════╝\n")
    stdout.write(""+Fore.YELLOW   +"║ \x1b[38;2;255;20;147m• "+Fore.GREEN+"GITHUB             "+Fore.RED+"    |"+Fore.LIGHTWHITE_EX+"   GITHUB.COM/AP0DEXME0                          "+Fore.YELLOW+"║\n")
    stdout.write(""+Fore.YELLOW   +"╚════════════════════════════════════════════════════════════════════════════╝\n") 
    print(f"{Fore.YELLOW}[RDEC] - {Fore.GREEN}Decompiling Return Of Warrior (ROW) & Risk Your Life (RYL) MMORPG{Fore.RED} [V0.1] \n{Fore.RESET}")


def clear_and_print():
    time.sleep(1)
    clear_screen()
    banners()


def file_banner(stamp=None):
    from datetime import datetime
    import sys
    if stamp is None:
        stamp = datetime.now().strftime("%#m/%#d/%Y %#I:%M:%S %p") \
            if sys.platform == "win32" else datetime.now().strftime("%-m/%-d/%Y %-I:%M:%S %p")
    title = f"// rDecompiler By Ap0dexMe0 {stamp}   //"
    bar = "/" * max(52, len(title) + 1)
    return [bar, title, bar]
