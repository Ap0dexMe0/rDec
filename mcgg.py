
from collections import Counter, defaultdict
from datetime import datetime

VERSION = "3.0"

# ============================================================
# HERO DATABASE
# Format: hero: (gold_cost, [synergies])
# Sahkan kos dan synergies dengan patch game semasa.
# ============================================================

HEROES = {
    # 1 GOLD
    "cici": (1, ["Bruiser", "Weapon Master"]),
    "dyrroth": (1, ["Bruiser", "Kishin"]),
    "eudora": (1, ["Dragoncaller", "Stargazer"]),
    "minotaur": (1, ["Astro Power", "Defender"]),
    "phoveus": (1, ["SPECTRE", "Scavenger"]),
    "uranus": (1, ["Dauntless", "Mistbender"]),
    "vale": (1, ["Echomancer", "Mage"]),
    "yi sun-shin": (1, ["Dragon Altar", "Swiftblade"]),

    # 2 GOLD
    "angela": (2, ["Kishin", "Scavenger"]),
    "balmond": (2, ["Dauntless", "Dragoncaller"]),
    "belerick": (2, ["Bruiser", "Enchanted Tales"]),
    "granger": (2, ["Marksman", "SPECTRE"]),
    "harley": (2, ["Echomancer", "Phasewarper"]),
    "hylos": (2, ["Defender", "Shadeweaver"]),
    "luo yi": (2, ["Dragon Altar", "Stargazer"]),
    "martis": (2, ["Astro Power", "Weapon Master"]),
    "miya": (2, ["Marksman", "Starbelle"]),
    "natalia": (2, ["Echomancer", "Swiftblade"]),
    "zhuxin": (2, ["Mage", "Starbelle"]),

    # 3 GOLD
    "aldous": (3, ["Bruiser", "Mistbender"]),
    "clint": (3, ["Dragoncaller", "Phasewarper"]),
    "edith": (3, ["Defender", "Starbelle"]),
    "franco": (3, ["Dauntless", "Kishin"]),
    "hilda": (3, ["Astro Power", "Dauntless"]),
    "kadita": (3, ["Mage", "Shadeweaver"]),
    "karina": (3, ["Astro Power", "Swiftblade"]),
    "mathilda": (3, ["Enchanted Tales", "Stargazer"]),
    "paquito": (3, ["Bruiser", "SPECTRE"]),
    "saber": (3, ["SPECTRE", "Swiftblade"]),
    "tigreal": (3, ["Defender", "Echomancer"]),
    "wanwan": (3, ["Dragon Altar", "Marksman"]),

    # 4 GOLD
    "atlas": (4, ["Defender", "Enchanted Tales"]),
    "gord": (4, ["Mage", "SPECTRE"]),
    "gusion": (4, ["Dragoncaller", "Swiftblade"]),
    "irithel": (4, ["Astro Power", "Marksman"]),
    "karrie": (4, ["Kishin", "Marksman"]),
    "lolita": (4, ["Dauntless", "Starbelle"]),
    "lunox": (4, ["Kishin", "Stargazer"]),
    "sora": (4, ["Echomancer", "Scavenger"]),
    "suyou": (4, ["Dragon Altar", "Weapon Master"]),
    "vexana": (4, ["Enchanted Tales", "Mage"]),
    "yin": (4, ["Bruiser", "Dragon Altar"]),
    "zilong": (4, ["Dragoncaller", "Weapon Master"]),

    # 5 GOLD
    "alice": (5, ["Dauntless", "SPECTRE"]),
    "badang": (5, ["Bruiser", "Dragoncaller"]),
    "baxia": (5, ["Defender", "Dragon Altar"]),
    "fanny": (5, ["Starbelle", "Swiftblade"]),
    "lancelot": (5, ["Kishin", "Phasewarper"]),
    "melissa": (5, ["Marksman", "Shadeweaver"]),
    "nana": (5, ["Mistbender", "Stargazer"]),
    "odette": (5, ["Astro Power", "Mage"]),
    "thamuz": (5, ["Echomancer", "Weapon Master"]),

    # 7 GOLD
    "alpha": (7, ["SPECTRE"]),
}

THRESHOLDS = {
    "SPECTRE": [2, 4, 6, 10],
    "Starbelle": [2, 4, 6, 10],
    "Scavenger": [2, 3],
    "Marksman": [2, 4, 6],
    "Dauntless": [2, 4, 6],
    "Defender": [2, 4, 6],
    "Mage": [2, 4, 6],
    "Stargazer": [2, 4, 6],
    "Astro Power": [2, 4, 6, 10],
    "Mistbender": [2, 4],
    "Echomancer": [2, 4, 6],
    "Kishin": [2, 4, 6, 10],
    "Swift Blade": [2, 4],
    "Weapon Master": [2, 4, 6],
    "Shadeweaver": [2, 4],
    "Dragon Altar": [2, 4, 6, 10],
    "Dragoncaller": [2, 4, 6, 10],
    "Enchanted Tales": [2, 4],
    "Guardian": [2, 4, 6],
}

# ============================================================
# TERMINAL DISPLAY
# ============================================================

USE_COLOR = True

COLORS = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "cyan": "\033[96m",
    "magenta": "\033[95m",
}


def paint(text, color=None, bold=False):
    text = str(text)

    if not USE_COLOR:
        return text

    prefix = COLORS.get(color, "")
    if bold:
        prefix += COLORS["bold"]

    return f"{prefix}{text}{COLORS['reset']}"


def separator(char="─", width=78):
    print(char * width)


def section(title):
    print()
    separator("═")
    print(paint(title, "cyan", True))
    separator("═")


# ============================================================
# NUMBER-ONLY MENUS
# ============================================================

def menu_number(title, options, default=1):
    options = list(options)

    print(f"\n{title}")

    for index, option in enumerate(options, 1):
        print(f"  {index}. {option}")

    while True:
        raw = input(
            f"Pilih nombor [Enter = {default}]: "
        ).strip()

        if raw == "":
            return default - 1

        if raw.isdigit():
            number = int(raw)

            if 1 <= number <= len(options):
                return number - 1

        print(f"Pilih nombor 1 hingga {len(options)}.")


def number_input(prompt, minimum=0, maximum=999, default=0):
    while True:
        raw = input(
            f"{prompt} [Enter = {default}]: "
        ).strip()

        if raw == "":
            return default

        if raw.isdigit():
            value = int(raw)

            if minimum <= value <= maximum:
                return value

        print(f"Masukkan nombor {minimum} hingga {maximum}.")


# ============================================================
# HERO DATABASE MENU
# ============================================================

def show_hero_list():
    section("HERO DATABASE")

    by_cost = defaultdict(list)

    for name, (cost, synergies) in HEROES.items():
        by_cost[cost].append((name, synergies))

    for cost in sorted(by_cost):
        print(paint(f"\n{cost} GOLD", "yellow", True))

        for name, synergies in sorted(by_cost[cost]):
            print(
                f"  {name.title():14} | "
                f"{' + '.join(synergies)}"
            )


# ============================================================
# COLLECT PLAYER ROSTER
# ============================================================

def collect_roster():
    roster = {}
    hero_names = sorted(HEROES)

    while True:
        choices = [
            f"{name.title()} ({HEROES[name][0]} Gold)"
            for name in hero_names
        ]

        choices.append("Selesai masukkan hero")

        selected = menu_number(
            "PILIH HERO YANG KAU ADA",
            choices,
            default=len(choices),
        )

        if selected == len(hero_names):
            break

        name = hero_names[selected]

        if name in roster:
            print(
                paint(
                    f"{name.title()} sudah dimasukkan.",
                    "yellow",
                )
            )
            continue

        star = menu_number(
            f"Star level untuk {name.title()}",
            ["1 Star", "2 Star", "3 Star"],
            default=1,
        ) + 1

        copies = number_input(
            "Jumlah salinan hero",
            1,
            99,
            1,
        )

        deployed = (
            menu_number(
                "Lokasi hero",
                ["Board", "Bench"],
                default=1,
            ) == 0
        )

        roster[name] = {
            "star": star,
            "copies": copies,
            "deployed": deployed,
        }

    return roster


# ============================================================
# SYNERGY ENGINE
# ============================================================

def active_hero_count(roster):
    return sum(
        1 for data in roster.values()
        if data["deployed"]
    )


def calculate_synergies(roster):
    counts = Counter()

    for name, data in roster.items():
        if not data["deployed"]:
            continue

        _, synergies = HEROES[name]
        counts.update(synergies)

    return counts


def next_breakpoint(synergy, count):
    for threshold in THRESHOLDS.get(synergy, []):
        if threshold > count:
            return threshold

    return None


def progress_bar(value, target, width=20):
    if target <= 0:
        return "·" * width

    filled = int(width * min(value / target, 1))

    return "█" * filled + "·" * (width - filled)


# ============================================================
# BOARD REPORT
# ============================================================

def print_board(roster, level):
    section("BOARD SEMASA")

    deployed = [
        (name, data)
        for name, data in roster.items()
        if data["deployed"]
    ]

    bench = [
        (name, data)
        for name, data in roster.items()
        if not data["deployed"]
    ]

    for title, heroes in [
        ("DI BOARD", deployed),
        ("DI BENCH", bench),
    ]:
        print(paint(f"\n{title}", "yellow", True))

        if not heroes:
            print("  Tiada hero.")
            continue

        for index, (name, data) in enumerate(heroes, 1):
            cost, synergies = HEROES[name]
            stars = "★" * data["star"] + "☆" * (3 - data["star"])

            print(
                f"{index:02}. {name.title():14} "
                f"{stars} | {cost} Gold | "
                f"{', '.join(synergies)} | "
                f"{data['copies']} salinan"
            )

    used = len(deployed)

    print(f"\nLevel: {level}")
    print(f"Hero di board: {used}")
    print(f"Slot kosong anggaran: {max(0, level - used)}")


# ============================================================
# SYNERGY DASHBOARD
# ============================================================

def print_synergy_report(counts):
    section("SYNERGY DASHBOARD")

    if not counts:
        print("Belum ada sinergi aktif.")
        return

    for synergy, count in counts.most_common():
        target = next_breakpoint(synergy, count)

        if target is None:
            target = max(count, 1)
            status = "Semak breakpoint dalam game"
            color = "cyan"
        else:
            missing = target - count
            status = f"Kurang {missing} untuk {target}"
            color = "green" if missing == 1 else "yellow"

        bar = progress_bar(count, target)

        print(
            f"{synergy:16} [{bar}] "
            f"{count:>2} | {paint(status, color)}"
        )


# ============================================================
# HERO-SYNERGY PAIRING DIAGRAM
# ============================================================

def print_pairing_map(roster, counts):
    section("PAIRING MAP: HERO ↔ SYNERGY")

    deployed_names = {
        name
        for name, data in roster.items()
        if data["deployed"]
    }

    if not deployed_names:
        print("Tiada hero di board.")
        return

    by_synergy = defaultdict(list)

    for name in deployed_names:
        for synergy in HEROES[name][1]:
            by_synergy[synergy].append(name)

    for synergy, names in sorted(
        by_synergy.items(),
        key=lambda item: (-counts[item[0]], item[0]),
    ):
        count = counts[synergy]
        target = next_breakpoint(synergy, count)

        if target:
            status = f"{count}/{target}, kurang {target - count}"
        else:
            status = f"{count} kiraan, semak breakpoint"

        print()
        print(paint(f"[{synergy}] {status}", "magenta", True))

        names = sorted(names)

        for index, name in enumerate(names):
            cost = HEROES[name][0]
            stars = "★" * roster[name]["star"]
            branch = "└─" if index == len(names) - 1 else "├─"

            print(
                f"  {branch} {name.title():14} "
                f"{stars:3} {cost} Gold"
            )

        candidates = []

        for name, (cost, traits) in HEROES.items():
            if name in deployed_names:
                continue

            if synergy in traits:
                candidates.append((cost, name))

        candidates.sort()

        if candidates:
            print(paint("  Calon pairing:", "yellow"))

            for cost, name in candidates[:5]:
                status = "boleh beli" if cost <= 999 else "mahal"
                print(f"    + {name.title():14} {cost} Gold")


# ============================================================
# NEXT PICK RECOMMENDATIONS
# ============================================================

def recommend_targets(roster, counts, level):
    section("NEXT PICKS")

    for synergy, count in counts.most_common():
        target = next_breakpoint(synergy, count)

        if target is None:
            continue

        missing = target - count

        if missing <= 2:
            print(
                f"- {synergy}: cari {missing} hero lagi "
                f"untuk breakpoint {target}."
            )

    print("\nHero board yang boleh di-upgrade:")

    found = False

    for name, data in roster.items():
        if not data["deployed"]:
            continue

        if data["star"] < 3:
            found = True
            print(
                f"- {name.title()}: sekarang {data['star']}★; "
                f"nilai peluang naik star."
            )

    if not found:
        print("Semua hero board sudah 3★ dalam input.")

    print(f"\nSlot kosong pada level {level}: "
          f"{max(0, level - active_hero_count(roster))}")


# ============================================================
# GOLD PLANNER
# ============================================================

def print_gold_plan(level, gold, hp, roster):
    section("GOLD PLANNER")

    print(f"Level: {level} | Gold: {gold} | HP: {hp}")

    if hp <= 25:
        advice = (
            "HP kritikal: pertimbangkan menguatkan board."
        )
        color = "red"
    elif hp <= 45:
        advice = (
            "HP sederhana rendah: nilai kekuatan board dahulu."
        )
        color = "yellow"
    elif gold >= 50:
        advice = (
            "Gold tinggi: bandingkan level-up dengan upgrade hero."
        )
        color = "green"
    elif gold >= 30:
        advice = (
            "Ekonomi sederhana: elakkan reroll tanpa target jelas."
        )
        color = "cyan"
    elif gold >= 10:
        advice = (
            "Gold terhad: utamakan satu atau dua target."
        )
        color = "yellow"
    else:
        advice = (
            "Gold rendah: elakkan reroll berlebihan."
        )
        color = "red"

    print(paint(advice, color, True))

    print("\nKos hero dalam roster:")

    for name in sorted(roster, key=lambda item: HEROES[item][0]):
        data = roster[name]
        cost = HEROES[name][0]
        location = "BOARD" if data["deployed"] else "BENCH"

        print(
            f"  {cost} Gold | {name.title():14} | "
            f"{data['star']}★ | {location}"
        )

    print(
        "\nNota: ini panduan heuristik, bukan simulasi ekonomi "
        "atau win rate rasmi."
    )


# ============================================================
# FILTER CANDIDATE HEROES
# ============================================================

def recommend_next_picks(roster, counts, gold):
    section("FILTER & RANKING CALON HERO")

    filter_index = menu_number(
        "Pilih filter kos gold",
        [
            "Semua kos",
            "1–2 Gold",
            "3–4 Gold",
            "5+ Gold",
        ],
        default=1,
    )

    candidates = []

    for name, (cost, traits) in HEROES.items():
        if name in roster:
            continue

        if filter_index == 1 and not (1 <= cost <= 2):
            continue
        if filter_index == 2 and not (3 <= cost <= 4):
            continue
        if filter_index == 3 and cost < 5:
            continue

        matching = [
            trait for trait in traits
            if counts.get(trait, 0) > 0
        ]

        bonus = 0

        for trait in traits:
            current = counts.get(trait, 0)
            target = next_breakpoint(trait, current)

            if target is not None:
                missing = target - current

                if missing == 1:
                    bonus += 3
                elif missing == 2:
                    bonus += 1

        score = 2 * len(matching) + bonus - 0.35 * cost

        candidates.append(
            (score, cost, name, matching)
        )

    candidates.sort(
        key=lambda row: (-row[0], row[1], row[2])
    )

    if not candidates:
        print("Tiada calon untuk filter ini.")
        return

    print(
        f"\n{'Hero':14} {'Gold':>4} {'Score':>6} "
        f"{'Status':>12} | Pairing"
    )
    separator()

    for score, cost, name, matching in candidates[:10]:
        status = "MAMPU" if cost <= gold else "SIMPAN"
        pairing = ", ".join(matching) if matching else "Trait baru"

        print(
            f"{name.title():14} {cost:>4} "
            f"{score:>6.1f} {status:>12} | {pairing}"
        )

    print(
        "\nScore ialah ranking heuristik berdasarkan synergy "
        "dan breakpoint, bukan kebarangkalian hero muncul."
    )


# ============================================================
# LEVEL ROADMAP
# ============================================================

def print_level_roadmap(current_level):
    section("LEVEL ROADMAP 1–10")

    roadmap = {
        1: "Gunakan unit terbaik yang tersedia.",
        2: "Bina pasangan synergy awal.",
        3: "Cari hero yang melengkapkan synergy.",
        4: "Pilih arah lineup berdasarkan hero diperoleh.",
        5: "Kuatkan frontline dan damage dealer.",
        6: "Semak board berbanding ekonomi.",
        7: "Kukuhkan core lineup.",
        8: "Tambah hero untuk breakpoint penting.",
        9: "Pertimbangkan unit late-game.",
        10: "Gunakan slot tambahan untuk synergy atau utility.",
    }

    for level in range(1, 11):
        marker = "▶" if level == current_level else " "
        color = "green" if level == current_level else None

        print(
            paint(
                f"{marker} Level {level}: {roadmap[level]}",
                color,
                level == current_level,
            )
        )

    print(
        "\nRoadmap ini umum; laraskan mengikut rules dan "
        "komposisi game semasa."
    )


# ============================================================
# 10-SYNERGY PLANNER
# ============================================================

def ultra_synergy_planner(counts):
    section("10-SYNERGY TARGET CHECK")

    names = sorted(THRESHOLDS)

    selected = menu_number(
        "Pilih sinergi sasaran",
        names,
        default=1,
    )

    synergy = names[selected]
    base = counts.get(synergy, 0)

    print(f"\nSynergy: {synergy}")
    print(f"Kiraan board semasa: {base}")

    blessing = number_input("Bonus Blessing", 0, 10, 0)
    crystals = number_input("Magic Crystal", 0, 10, 0)
    other = number_input("Bonus lain", 0, 10, 0)

    total = base + blessing + crystals + other

    print(f"\nJumlah anggaran: {total}/10")

    if total >= 10:
        print(
            paint(
                "Jumlah mencapai 10 berdasarkan input.",
                "green",
                True,
            )
        )
    else:
        print(
            paint(
                f"Masih kurang {10 - total} kiraan.",
                "yellow",
                True,
            )
        )

    print("Sahkan hasil sebenar dalam game.")


# ============================================================
# MAIN
# ============================================================

def main():
    global USE_COLOR

    print(
        paint(
            f"MAGIC CHESS: GO GO — LINEUP ANALYZER v{VERSION}",
            "cyan",
            True,
        )
    )

    USE_COLOR = (
        menu_number(
            "Aktifkan warna terminal?",
            ["Ya", "Tidak"],
            default=1,
        ) == 0
    )

    if menu_number(
        "Tunjukkan semua hero dalam database?",
        ["Ya", "Tidak"],
        default=2,
    ) == 0:
        show_hero_list()

    level = number_input("Level semasa", 1, 10, 7)
    gold = number_input("Gold semasa", 0, 999, 20)
    hp = number_input("HP semasa", 1, 100, 70)

    roster = collect_roster()

    if not roster:
        print("Tiada hero dimasukkan. Analisis dihentikan.")
        return

    counts = calculate_synergies(roster)

    print_board(roster, level)
    print_synergy_report(counts)
    print_pairing_map(roster, counts)
    recommend_targets(roster, counts, level)
    print_gold_plan(level, gold, hp, roster)
    recommend_next_picks(roster, counts, gold)
    print_level_roadmap(level)

    if menu_number(
        "Kira sasaran 10 sinergi?",
        ["Ya", "Tidak"],
        default=1,
    ) == 0:
        ultra_synergy_planner(counts)

    section("ANALISIS SELESAI")
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAnalisis dibatalkan.")
