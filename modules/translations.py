

import os
import re

HANGUL = re.compile(r"[\uac00-\ud7a3\u3130-\u318f]")
CJK = re.compile(r"[\u3000-\u303f\u3130-\u318f\u3400-\u9fff"
                 r"\uff01-\uffee\uac00-\ud7a3]")
_PURE_KR = re.compile(r"[\uac00-\ud7a3\u3130-\u318f0-9 ()\[\]A-Za-z+.,%:_/-]+\Z")
_PK_COUNT = re.compile(r"\s*(\d+)개\s*\Z")
_PK_TAIL = re.compile(r"\s*/{2,}\s*(\d+)\s*\Z")
_PK_SIZE = re.compile(r"\s*\((S|M|L|Fine|Superior)\)\s*\Z")
_PK_XCOUNT = re.compile(r"\s*[xX]\s*(\d+)\s*\Z")
_COUNT_CHIP = re.compile(r"(\d+)개")
_STRING_ARG = re.compile(r'"([^"\r\n]*)"')

KOR_EN = {
    "이름": "Name",
    "모델링 파일명": "Model file name",

    "NPCDisplay(NPC ID, NPC가 출력될 클라이언트 국적(0=All, 1=Only Korea, "
    "2=Only Foreign), 테스트서버 표시여부, 정식서버 표시여부, 통합서버 표시여부);":
        "NPCDisplay(NPC ID, client nationality the NPC appears for "
        "(0=All, 1=Only Korea, 2=Only Foreign), show on test server, "
        "show on official server, show on merged server);",
    "SetNPC(존ID, NPC ID, 마을ID, 성속여부(true, false), GCMDS, Name);":
        "SetNPC(zone ID, NPC ID, town ID, sacred or profane (true, false), "
        "GCMDS, Name);",
    "SetNPC(존ID, NPC ID, 마을ID, 성속여부(true, false), GCMDS, 이름);":
        "SetNPC(zone ID, NPC ID, town ID, sacred or profane (true, false), "
        "GCMDS, Name);",
    "SetPosition(NPC ID, 방향, X, Y(높이), Z);":
        "SetPosition(NPC ID, facing, X, Y (height), Z);",
    "AddWords(NPC ID, NPC 클릭시 대화창에 표시되는 대화);":
        "AddWords(NPC ID, dialogue shown in the chat window when the NPC "
        "is clicked);",
    "AddDialog(NPC ID, Popup 기능으로 Dialog를 복수로 호출 했을 때 호출한 "
    "순서대로 정해지는 인자, 현재는 사용안함, Dialog에 들어가는 메시지);":
        "AddDialog(NPC ID, argument assigned in the order the Dialogs were "
        "called when several are invoked through the Popup feature, "
        "currently unused, message that goes into the Dialog);",
    "AddPopupFame(NPC ID, Popup Kind ID, NPC function ID , Popup String, "
    "Quest ID, 제한명성, 클래스 ID)\t\t// ROW2009_AbilitySystem":
        "AddPopupFame(NPC ID, Popup Kind ID, NPC function ID , Popup "
        "String, Quest ID, fame limit, class ID)\t\t// ROW2009_AbilitySystem",
    "AddPopupAbility(NPC ID, Popup Kind ID, NPC function ID , Popup String, "
    "Ability ID, Ability LV, 클래스 ID)\t\t// ROW2009_AbilitySystem":
        "AddPopupAbility(NPC ID, Popup Kind ID, NPC function ID , Popup "
        "String, Ability ID, Ability LV, class ID)\t\t// ROW2009_AbilitySystem",
    'AddQuestWords(NPC ID, Quest ID, "HelpMassege"); AddQuest(int,int)함수에 '
    "의해 등록된 Quest ID를 PC가 수락할 수 있을 때 NPC의 머리위에 뜨는 대사":
        'AddQuestWords(NPC ID, Quest ID, "HelpMassege"); words shown above '
        "the NPC's head when a PC can accept the Quest ID registered "
        "through the AddQuest(int,int) function",
    "AddZoneMove(NPC ID, 존 ID, X 좌표, Y좌표(높이), Z좌표); "
    "해당 좌표로 존이동 시켜줌":
        "AddZoneMove(NPC ID, zone ID, X coord, Y coord (height), Z coord); "
        "moves you to the zone at those coordinates",
    "AddQuest(NPC ID, Quest ID); Quest ID의 퀘스트를 NPC에 연결 시켜줌":
        "AddQuest(NPC ID, Quest ID); attaches the quest of Quest ID to "
        "the NPC",
    "); AddQuest(int,int)함수에 의해 등록된 Quest ID를 PC가 수락할 수 있을 "
    "때 NPC의 머리위에 뜨는 대사":
        "); words shown above the NPC's head when a PC can accept the "
        "Quest ID registered through the AddQuest(int,int) function",
    "SetDropGrade(NPCID, Item Type FGrade, DBase, CBase, BBase, ABase);  "
    "각 그레이드별 최소 (+)옵션 개수":
        "SetDropGrade(NPCID, Item Type FGrade, DBase, CBase, BBase, ABase);"
        "  minimum number of (+) options per grade",
    "(어빌리티 아이디, 어빌리티 레벨) - ROW2009_AbilitySystem":
        "(ability ID, ability level) - ROW2009_AbilitySystem",
    "(옵션타입, 아이템 ID, 그레이드, BASE 옵션 개수)":
        "(option type, item ID, grade, number of BASE options)",
    "(옵션타입, PC의 CLASS, PC의 LEVEL, 그레이드, BASE 옵션 개수)":
        "(option type, PC CLASS, PC LEVEL, grade, number of BASE options)",
    "(존 넘버, x좌표, y좌표, z좌표)":
        "(zone number, x coord, y coord, z coord)",
    "국가코드, 서버종류, 게임가드 스트링":
        "country code, server type, GameGuard string",
    "true = 목록저장  false = 저장안함":
        "true = save to list  false = do not save",
    "Name은 11자 이내로 하도록 주의를 할 것.":
        "Note that Name must be 11 characters or fewer.",
    "이름은 11자 이내로 하도록 주의를 할 것.":
        "Note that the name must be 11 characters or fewer.",
    "영문타이틀은 22자 이내로 하도록 주의를 할 것.":
        "Note that the English title must be 22 characters or fewer.",

    "238\t매찬용 접두사": "238\tprefix for the Lucky string",
    "239\t매직찬스": "239\tmagic chance",
    "4321 어빌리티 툴팁윈도우 하단 설명":
        "4321 ability tooltip window bottom note",
    "4361 액션 툴팁윈도우 하단 설명":
        "4361 action tooltip window bottom note",
    "4411\t아칸이 휴먼노점상 볼때":
        "4411\twhat an Ak'kan sees when viewing a Human stall",
    "4412\t휴먼이 아칸 노점상 볼때":
        "4412\twhat a Human sees when viewing an Ak'kan stall",
    "4413\t석상전쟁에 참여하기 위해선 41레벨 이상이 되어야 합니다.":
        "4413\tyou must be level 41 or higher to participate in Statue War.",
    "4607  Shatter 관련": "4607  relates to Shatter",
    "4608  하드히트 관련": "4608  relates to Hard Hit",
    "대만 정섭": "Taiwan official server",

    "어서오시게.": "Welcome.",
    "알벤트는 사이너 아일랜드에 있는 할아버지":
        "Albent is the grandfather on Scyna Island",
    "튜토리얼 퀘스트 걸어줄 것": "assign the tutorial quest",
    "퀘스트 걸어줄것": "assign the quest",
    "Blacksmith 튜토리얼 퀘스트 걸어줄 것":
        "assign the Blacksmith tutorial quest",
    "스페셜 메달상점": "Special medal shop",
    "캐릭터 Name 변경": "Character Name change",
    "캐릭터 이름 변경": "Character name change",
    "밸런스 붕괴에 치명적!!! 가급적 사용하지 말것(유료화 확정)":
        "FATAL to balance!!! Avoid using if at all possible "
        "(switch to a paid service confirmed)",
    "메인터넌스 챈트 스킬북 추가": "added Maintenance Chant skillbook",
    "엑셀레이션 챈트 스킬북 추가": "added Acceleration Chant skillbook",
    "라이프옵 가드암 - 2009. 01.16": "Life Armguard - 2009. 01.16",
    "Empty Cruet(2010.4.27 추가)": "Empty Cruet (added 2010.4.27)",
    "포리": "Pori",
    "가드 Arm": "Guard Arm",

    "퀘스트 보너스": "Quest bonus",
    "신전의 파편": "Temple fragment",
    "신전의 파편 제거": "Remove the temple fragment",
    "전직의 증표": "Class Change Certificate",
    "씨맨 비늘 10개 제거": "Remove 10 Seaman scales",
    "좀비도그 뼈 10개": "Zombie dog bone x10",
    "좀비도그 체인 3개": "Zombie dog chain x3",
    "가공된 늑대 발톱 5개 (이거 Drop/Sell 옵션 꺼야함)":
        "Processed wolf claw x5 (turn off the Drop/Sell options on this)",
    "고철덩어리 1개 (이거 Drop/Sell 옵션 꺼야함)":
        "Scrap iron x1 (turn off the Drop/Sell options on this)",
    "고철덩어리": "Scrap iron",
    "자이언트 스파이더링 10개 수집": "Collect 10 Giant Spiderlings",
    "Dire Boar 고기 10개 수집": "Collect 10 Dire Boar meat",
    "언데드 기생충 10개 수집": "Collect 10 Undead parasites",
    "트롤 대거 10개 수집": "Collect 10 Troll daggers",
    "Spis Thorn x 10개 수집": "Collect 10 Spis Thorn",
    "고블린 심장 5개": "Goblin heart x5",
    "고블린 심장": "Goblin heart",
    "킬러비틀 집게 10개": "Killer Beetle pincer x10",
    "킬러비틀 껍질 7개": "Killer Beetle shell x7",
    "쿠루민 스트랩 20개": "Korumin strap x20",
    "늑대 발톱 15개": "Wolf claw x15",
    "깃털 20개": "Feather x20",
    "거북이 껍질 10개": "Turtle shell x10",
    "엘로이 이빨 5개": "Eloyee tooth x5",
    "엘로이 심장 5개": "Eloyee heart x5",
    "엘로이 이빨 9개": "Eloyee tooth x9",
    "엘로이 심장 3개": "Eloyee heart x3",
    "리자드맨 비늘 10개": "Lizardman scale x10",
    "복어 지느러미 10개": "Pufferfish fin x10",
    "복어의 독 샘플 3개": "Pufferfish poison sample x3",
    "작은 진주": "Small pearl",
    "좀비 기생체": "Zombie parasite",
    "캐리온 라바 껍질 2개": "Carrion Larva skin x2",
    "시험관 3개": "Test tube x3",
    "젊은 여자": "Young woman",
    "해적마을 중앙 나무": "The pirate village central tree",
    "편지": "letter",
    "Tihon의 편지": "Tihon's letter",
    '이벤트 아이템 "금화': 'Event item "Gold coin',
    '이벤트 아이템 "Tihon의 편지': 'Event item "Tihon\'s letter',
    '이벤트 아이템 "편지': 'Event item "letter',
    "퀘스트 보상 ": "Quest reward ",
    "이벤트용 선물상자": "Event gift box",
    "이벤트용 사탕": "Event candy",
    "이벤트용 캔디 ": "Event candy ",
    "이벤트용 캔디": "Event candy",
    "이벤트용 파이": "Event pie",
    "이벤트용 술": "Event liquor",
    "불꽃놀이 셋트": "Fireworks set",
    "산타의 선물": "Santa's present",
    "가면 전용 상자": "Mask-only box",
    "할로윈 기프트": "Halloween gift",
    "황금열쇠": "Golden key",
    "동열쇠": "Bronze key",
    "은빛열쇠": "Silver key",
    "행운의 부적": "Lucky talisman",
    "알디아항구 스크롤": "Scroll to Aldia Harbor",
    "오피니 스크롤": "Scroll to Opeany",
    "미하엘의 가호": "Michael's blessing",
    "첫번째휴식": "First Rest",
    "첫번째 휴식": "First Rest",
    "알디아항구": "Aldia Harbor",
    "알디아 항구": "Aldia Harbor",
    "테시티오": "Tessetio",
    "감시자캠프": "Watch Camp",
    "베인 캠프": "Bein Camp",
    "베인": "Bein",
    "유니테": "Unite",
    "오페니": "Opeany",
    "시즈나": "Syzna",
    "뉴베린 항구": "New Berin Harbor",
    "파울린": "Paoulin",
    "하이레이크": "High Lake",
    "바르윈": "Varween",
    "오르티뉴": "Ortinue",
    "칼리오": "Carlio",
    "파르타인": "Partein",
    "미들캠프": "Middle Camp",
    "그린웨일즈": "Green Wales",
    "로슈캠프": "Roche Camp",
    "클라우츠": "Clauzhuz",
    "생명제단": "Sacrifice Shrine",
    "우익단체": "Righties Camp",
    "얼어붙은 초원 엘리오르": "Snowrimp Village",
    "귀환서": "Return Scroll",
    "스크롤": "scroll",
    "컴크러쉬": "Com Crush",
    "컴블레이드": "Com Blade",
    "오크러쉬": "Opp Crush",
    "오블레이드": "Opp Blade",
    "오해머": "Opp Hammer",
    "사이드": "Side",
    "클로우": "Claw",
    "어택암": "Attack Arm",
    "건암": "Gun Arm",
    "나이프암": "Knife Arm",
    "가드암": "Guard Arm",
    "컴상체": "Com Body",
    "오상체": "Opp Body",
    "컴투구": "Com Helm",
    "오투구": "Opp Helm",
    "컴하체": "Com Pelvis",
    "오하체": "Opp Pelvis",
    "컴암": "Com Arm",
    "오암": "Opp Arm",
    "컴배턴트 곡괭이": "Combatant Pickaxe",
    "오피세이터 곡괭이": "Officiator Pickaxe",
    "곡괭이": "Pickaxe",
    "단검": "Dagger",
    "한손검": "One-handed sword",
    "양손검": "Two-handed sword",
    "한손도끼": "One-handed axe",
    "양손도끼": "Two-handed axe",
    "한손둔기": "One-handed blunt",
    "양손둔기": "Two-handed blunt",
    "지팡이": "Staff",
    "석궁": "Crossbow",
    "중갑옷": "Heavy armor",
    "경갑옷(로그)": "Light armor (rogue)",
    "경갑옷(법사)": "Light armor (mage)",
    "경투구(공통)": "Light helmet (common)",
    "중투구": "Heavy helmet",
    "경투구": "Light helmet",
    "방패(공통)": "Shield (common)",
    "방패": "Shield",
    "중장갑": "Heavy gauntlet",
    "경장갑": "Light gauntlet",
    "중부츠": "Heavy boots",
    "경부츠": "Light boots",
    "농축": "concentrated",
    "셔츠": "Shirt",
    "튜닉": "Tunic",
    "빵": "Bread",
    "베이컨": "Bacon",
    "생고기": "Raw meat",
    "구운고기": "Roasted meat",
    "증류수": "Distilled Water",

    "MP회복 소": "MP recovery (S)",
    "MP회복 중": "MP recovery (M)",
    "MP회복 대": "MP recovery (L)",
    "MP회복 특대": "MP recovery (XL)",
    "HP/MP회복 소": "HP/MP recovery (S)",
    "HP/MP회복 중": "HP/MP recovery (M)",
    "HP/MP회복 대": "HP/MP recovery (L)",
    "HP/MP회복 특대": "HP/MP recovery (XL)",

    "레벨 10 D등급 장비": "Level 10 D-grade equipment",
    "레벨 1 B등급 장비": "Level 1 B-grade equipment",
    "레벨 30 B등급 장비": "Level 30 B-grade equipment",
    "레벨 35 D등급 장비": "Level 35 D-grade equipment",
    "D급 장비": "D-grade equipment",
    "(10렙 D+3 Master Sword)": "(Lv 10 D+3 Master Sword)",
    "(10렙 D+3 Pawn Stroke)": "(Lv 10 D+3 Pawn Stroke)",
    "(10렙 D+3 Wooden club)": "(Lv 10 D+3 Wooden club)",
    "(10렙 D+3 Dark Stick)": "(Lv 10 D+3 Dark Stick)",
    "(10렙 D+3 Latish Slusher)": "(Lv 10 D+3 Latish Slusher)",
    "중갑옷 60lv": "Heavy armor 60lv",
    "중갑옷 65lv": "Heavy armor 65lv",
    "중투구 60 로그": "Heavy helmet 60 rogue",
    "경투구 60 메이지": "Light helmet 60 mage",
    "중투구 60 워리어 계열": "Heavy helmet 60 warrior family",

    "소드마스터리1": "Sword Mastery 1",
    "소드마스터리2": "Sword Mastery 2",
    "하드히트": "Hard Hit",
    "윌파워1": "Willpower 1",
    "윌파워2": "Willpower 2",
    "임프루브드 크리티컬1": "Improved Critical 1",
    "임프루브드크리티컬2": "Improved Critical 2",
    "액스마스터리1": "Axe Mastery 1",
    "액스마스터리2": "Axe Mastery 2",
    "블런트마스터리1": "Blunt Mastery 1",
    "블런트마스터리2": "Blunt Mastery 2",
    "터프니스1": "Toughness 1",
    "터프니스2": "Toughness 2",
    "퍼스트 에이드": "First Aid",
    "니들 스핏": "Needle Spit",
    "이베이젼1": "Evasion 1",
    "이베이젼2": "Evasion 2",
    "인커리지": "Encourage",
    "블러디 마나": "Bloody Mana",
    "뱀파이어릭 터치": "Vampire Kiss",
    "마나셀": "Mana Cell",
    "그리스": "Grease",
    "서레너티1": "Serenity 1",
    "서레너티2": "Serenity 2",
    "슬러그": "Slug",
    "릴리프": "Relief",
    "블레스": "Bless",
    "페이먼트": "Blood Offering",
    "드레인라이프": "Drain Life",
    "프로텍션": "Protection",
    "홀드포지션": "Hold Position",
    "익스플로시브 니들": "Explosive Needle",

    "현재 등록되어 있는 서버군이 없기 때문에, 서버를 선택해야 됩니다.":
        "There is no registered server group at the moment, so a server "
        "must be selected.",
    r"안녕하세요. 릴(R.Y.L.)온라인입니다.\\":
        r"Hello. This is RYL (R.Y.L.) Online.\\",
    r"고객님께서는 현재 릴온라인 Part2 통합서버에 로그인하셨습니다.\\":
        r"You have logged into the RYL Online Part 2 merged server.\\",
    "릴 온라인은 Part2 가 업데이트되는 동시에 기존의 6개 서버에서 "
    "Part1 통합서버, Part2 통합서버, Part2 신규서버로 통합을 하여 "
    "새롭게 오픈하였습니다.":
        "When Part 2 was updated, RYL Online merged the previous 6 servers "
        "into the Part 1 merged server, the Part 2 merged server, and the "
        "Part 2 new server, and opened them anew.",
    "기존에 Part1 을 이용하고 계셨던 고객님께서는 아래의 유의 사항을 꼭 "
    r"참고하시어 이용에 착오 없으시길 바랍니다.\\ \\":
        "Customers who have been using Part 1, please make sure to read the "
        r"notes below so that there are no problems with your use.\\ \\",
    "1. Part2 통합서버에서는 서버 통합전 데이터에서 계정 내 캐릭터 최대 "
    r"5명, 창고 1개를 선택하실 수 있고 새로운 캐릭터 생성도 가능합니다. \\":
        "1. On the Part 2 merged server, you can choose up to 5 characters "
        "and 1 warehouse from the pre-merger data, and new character "
        r"creation is also possible. \\",
    "2. Part2 통합서버에서 미리 선택하시지 않은 캐릭터와 창고데이터들은 "
    "서버 통합전 데이터에서 삭제되지 않으며, Part2 통합서버에서 재차 "
    r"선택하실 수 있습니다. (Part2 신규서버 제외).\\":
        "2. Characters and warehouse data you did not pre-select on the "
        "Part 2 merged server are not deleted from the pre-merger data, and "
        "can be selected again on the Part 2 merged server (excluding the "
        r"Part 2 new server).\\",
    "3. Part1, Part2 통합서버에 같은 캐릭터와 같은 창고데이터를 중복적으로 "
    "선택하실 수 없습니다. 그리고 Part2 통합서버에서 선택하신 캐릭터는 "
    r"Part1 로의 이전이 불가능합니다.\\":
        "3. The same character and the same warehouse data cannot be "
        "selected on both the Part 1 and Part 2 merged servers. Also, a "
        "character selected on the Part 2 merged server cannot be moved "
        r"over to Part 1.\\",
    "4. Part1 통합서버나 Part2 통합서버에서 선택 혹은 이전하신 캐릭터를 "
    "'캐릭터 선택화면'에서 삭제하실 경우에 서버 통합전 데이터, Part1 "
    "통합서버, Part2 통합 서버에서 동시에 삭제되므로 신중히 결정해주시기 "
    r"바랍니다.\\":
        "4. If you delete a character you selected on or moved to the "
        "Part 1 or Part 2 merged server from the 'character selection "
        "screen', it is deleted at the same time from the pre-merger data, "
        "the Part 1 merged server, and the Part 2 merged server, so please "
        r"decide carefully.\\",
    r"캐릭터를 추가로 선택하실 수 있습니다.\\추가로 선택하시겠습니까?":
        r"You can select additional characters.\\Would you like to select "
        "more?",
    "추가선택": "Select more",
    "선택안함": "Do not select",
    r"안녕하십니까. 신화운영팀입니다.\\고객님은 현재 신화 파트투 통합서버에 "
    "접속중이십니다. 통합이전 서버군들 중에서 통합서버에서 플레이하실 서버를 "
    "골라주십시요. '빠른로그인'을 선택하실경우 가장 최근에 플레이하신 서버의 "
    "데이터로 접속하게 됩니다.":
        r"Hello. This is the Shinhwa operations team.\\You are currently "
        "connected to the Shinhwa Part Two merged server. Please choose "
        "which of the pre-merger server groups you will play on the merged "
        "server. Selecting 'Quick Login' connects you with the data of the "
        "server you played most recently.",

    r"Enjoy delicious Korean Chuseok food.\\HP 1100 recovery회복.\\":
        r"Enjoy delicious Korean Chuseok food.\\Restores 1100 HP.\\",
    r"Enjoy delicious Korean Chuseok food.\\HP 900 recovery.\\":
        r"Enjoy delicious Korean Chuseok food.\\Restores 900 HP.\\",

    "경험치": "EXP",
    "골드": "gold",
    "명성치": "fame",
    "명성": "fame",
    "레벨": "Level",
    "렙": "Lv",
    "등급 장비": "-grade equipment",
    "급 장비": "-grade equipment",
    "장비": "equipment",
    "회복약": "healing potions",
    "이터니움": "Iternium",
    "토파즈": "Topaz",
    "금화": "Gold coin",
    "고기": "meat",
    "가죽": "Pelt",
    "이빨": "Fang",
}

LONG_TEXT = [
    (r"요리에 사용되는 기본 도구", "Basic tool used for cooking"),
    (r"HP를 300 회복\\고기를 말려서 만든 육포\\Dire Boar Meat와 Goblin "
     r"Heart를 이용하거나\\Dire Boar Meat와 Killer Beetle Husk를 써서 "
     r"요리할 수 있다.",
     r"Restores 300 HP\\Jerky made by drying meat\\Made using Dire Boar "
     r"Meat and Goblin Heart, or\\Dire Boar Meat and Killer Beetle Husk."),
    (r"HP를 300 회복\\잘 구운 Ostopterix 구이요리\\Ostopterix Meat와 Monk "
     r"Brain를 쓰거나\\Ostopterix Meat와 Korkebine Heart를 써서 요리할 수 "
     r"있다",
     r"Restores 300 HP\\Well-roast Ostopterix dish\\Made using Ostopterix "
     r"Meat and Monk Brain, or\\Ostopterix Meat and Korkebine Heart"),
    (r"HP를 400 회복\\말린 고기로 만든 요리\\Gnoll Rib과 Tren Charcoal을 "
     r"써서 요리할 수 있다.",
     r"Restores 400 HP\\Dish made from dried meat\\Made using Gnoll Rib "
     r"and Tren Charcoal."),
    (r"HP를 400 회복\\육류에 오크라를 넣어 만든 수프\\Scyna Scorpion "
     r"Tail와 Rhinoman Horn을 쓰거나\\Gorep Brain과 Wraith Eyeball을 "
     r"사용해 요리할 수 있다.",
     r"Restores 400 HP\\Soup made by adding okra to meat\\Made using "
     r"Scyna Scorpion Tail and Rhinoman Horn, or\\Gorep Brain and Wraith "
     r"Eyeball."),
    (r"HP를 500 회복\\말린 고기를 훈제해서 만든 음식\\Roasted Meat와 "
     r"Ceratop Skin를 써서 요리할 수 있다.",
     r"Restores 500 HP\\Food made by smoking dried meat\\Made using "
     r"Roasted Meat and Ceratop Skin."),
    (r"HP를 500 회복\\고기의 우둔살을 고운 요리\\Stump Charcoal와 Giant "
     r"Boar Meat를 써서 요리할 수 있다.",
     r"Restores 500 HP\\Dish of roasted meat rump\\Made using Stump "
     r"Charcoal and Giant Boar Meat."),
    (r"HP를 500 회복\\양고기로 만든 소시지\\Roasted Meat와 Stump Branch를 "
     r"써서 요리할 수 있다.",
     r"Restores 500 HP\\Sausage made from lamb\\Made using Roasted Meat "
     r"and Stump Branch."),
    (r"HP를 600 회복\\고기를 곱게 갈아 동물의 창자에 채운 요리\\Flynd "
     r"Meat와 Nohnuut Eyeball를 써서 요리할 수 있다.",
     r"Restores 600 HP\\Dish of finely ground meat stuffed into an "
     r"animal's intestine\\Made using Flynd Meat and Nohnuut Eyeball."),
    (r"HP를 600 회복\\고기를 반죽해 숙성시킨 뒤 만든 소시지\\Roasted "
     r"Meat와 Naga Fin을 써서 만들 수 있다.",
     r"Restores 600 HP\\Sausage made by kneading meat and letting it "
     r"mature\\Made using Roasted Meat and Naga Fin."),
    (r"HP를 600 회복\\고기로 걸쭉하게 끓인 수프\\Snow Gorgon Tail과 Snow "
     r"Boar Meat를 써서 만들 수 있다.",
     r"Restores 600 HP\\Soup boiled thick with meat\\Made using Snow "
     r"Gorgon Tail and Snow Boar Meat."),
    (r"HP를 700 회복\\고기를 꼬치에 꿰어서 구운 요리\\Roasted Meat와 "
     r"Clinzer Bone Wing을 써서 만들 수 있다.",
     r"Restores 700 HP\\Meat roasted on a skewer\\Made using Roasted Meat "
     r"and Clinzer Bone Wing."),
    (r'"HP를 700 회복\\돼지장에 후추와 잣, 과일 열매를 넣고 구운 요리\\'
     r'Bacon과 Infected Gorgon Tail을 써서 만들 수 있다."',
     r'"Restores 700 HP\\Pork fatback roast with pepper, pine nuts, and '
     r'fruit baked in\\Made using Bacon and Infected Gorgon Tail."'),
    (r"HP를 700 회복\\안심부위를 구운 요리\\Bacon과 Caernarvon Boar "
     r"Meat를 사용해 만들 수 있다.",
     r"Restores 700 HP\\Roast of the tenderloin cut\\Made using Bacon and "
     r"Caernarvon Boar Meat."),
    (r"HP를 700 회복\\와이번 고기로 만든 스튜\\Death Wyvern Meat와 Reaper "
     r"Skull을 써서 만들 수 있다.",
     r"Restores 700 HP\\Stew made from wyvern meat\\Made using Death "
     r"Wyvern Meat and Reaper Skull."),
    (r'"HP를 800 회복\\고기, 채소 등을 다진 것을 속에 넣고 만든 파이\\'
     r'Caliga Scorpion Meat과 Kappa Blood를 써서 만들 수 있다."',
     r'"Restores 800 HP\\Pie made with minced meat, vegetables, and the '
     r'like as filling\\Made using Caliga Scorpion Meat and Kappa Blood."'),
    (r"MP를 700 회복\\고기와 피와 기름,곡류를 섞어 크게 만든 소시지\\"
     r"Dullahan Blood와 Snow Nianshou Meat를 써서 만들 수 있다.",
     r"Restores 700 MP\\Large sausage mixed from meat, blood, oil, and "
     r"grain\\Made using Dullahan Blood and Snow Nianshou Meat."),
    (r"HP를 800 회복\\고기를 기름에 튀겨낸 요리\\Bacon과 Ashen Ichman "
     r"Scale를 써서 만들 수 있다.",
     r"Restores 800 HP\\Dish of meat deep-fried in oil\\Made using Bacon "
     r"and Ashen Ichman Scale."),
    (r"HP를 800 회복\\고기의 엉덩이부위를 검게 그을릴 정도로 구운 요리\\"
     r"Hellwolf Meat과 Gredor Heart를 써서 만들 수 있다.",
     r"Restores 800 HP\\Dish with the meat's rump roasted until charred "
     r"black\\Made using Hellwolf Meat and Gredor Heart."),
    (r'HP를 800 회복\\먹기좋게 한입 사이즈로 만든 고기 요리\\Bacon과 '
     r'Caliga Fungal Spore를 사용해 만들 수 있다.',
     r"Restores 800 HP\\Meat dish made bite-sized for easy eating\\Made "
     r"using Bacon and Caliga Fungal Spore."),
    (r"MP를 800 회복\\감자, 야채, 고기를 섞어서 버무린 샐러드\\"
     r"Blackbean Manna와 Horsebee Wing를 써서 만들 수 있다.",
     r"Restores 800 MP\\Salad tossed together with potato, vegetables, "
     r"and meat\\Made using Blackbean Manna and Horsebee Wing."),
    (r"MP를 300 회복\\얇게 썬 빵 사이에 육류나 채소류를 끼워서 먹는 요리\\"
     r"Raged Dire Wolf Meat과 Dire Bat Wing써서 만들거나\\Eloyee Heart와 "
     r"Krumin Meat를 써서 만들 수 있다.",
     r"Restores 300 MP\\Dish eaten with meat or vegetables sandwiched "
     r"between thin slices of bread\\Made using Raged Dire Wolf Meat and "
     r"Dire Bat Wing, or\\Eloyee Heart and Krumin Meat."),
    (r"MP를 300 회복\\재료를 한데 섞어 장시간 푹 끓여 만든 요리\\Poison "
        r"Spiderling와 Monk Meat를 써서 만들거나\\Turtlebeast Shell과 Lehan "
        r"Scorpion Tail를 써서 만들 수 있다.",
        r"Restores 300 MP\\Dish made by mixing the ingredients together "
        r"and simmering them for a long time\\Made using Poison Spiderling "
        r"and Monk Meat, or\\Turtlebeast Shell and Lehan Scorpion Tail."),
    (r"MP를 400 회복\\고기에 튀김옷을 입혀 튀긴 것과 감자튀김을 함께 먹는 "
     r"음식\\Flynd Meat와 Carrion Crawler Antennae를 써서 만들거나\\"
     r"Gargoyle Wing과 Carrion Crawler Antennae를 써서 만들 수 있다.",
     r"Restores 400 MP\\Food eaten as battered deep-fried meat together "
     r"with french fries\\Made using Flynd Meat and Carrion Crawler "
     r"Antennae, or\\Gargoyle Wing and Carrion Crawler Antennae."),
    (r'"MP를 400 회복\\밀가루에 고기, 우유, 달걀을 넣어 반죽한 것을 구운 '
     r'요리\\Murky Ichman Egg와 Shiny Bulte Leg를 써서 만들 수 있다."',
     r'"Restores 400 MP\\Batter of flour with meat, milk, and eggs '
     r'kneaded in and baked\\Made using Murky Ichman Egg and Shiny Bulte '
     r'Leg."'),
    (r"MP를 500 회복\\야채와 고기로 속을 채운 페스트리\\Carrot Manna와 "
     r"Skullbat Wing를 써서 만들 수 있다.",
     r"Restores 500 MP\\Pastry filled with vegetables and meat\\Made "
     r"using Carrot Manna and Skullbat Wing."),
    (r"MP를 500 회복\\Gorgon Tail을 매콤한 양념에 장시간 끊인 찜요리\\"
     r"Dire Gorgon Tail와 Strider Eyeball을 써서 만들 수 있다.",
     r"Restores 500 MP\\Stewed Gorgon Tail simmered for a long time in "
     r"spicy seasoning\\Made using Dire Gorgon Tail and Strider Eyeball."),
    (r"MP를 500 회복\\각종 야채와 고기를 끓여서 만드는 수프\\Carrot "
     r"Manna와 Fungus Feeler를 써서 만들 수 있다.",
     r"Restores 500 MP\\Soup made by boiling assorted vegetables and "
     r"meat\\Made using Carrot Manna and Fungus Feeler."),
    (r"MP를 600 회복\\고기을 잘게 다져서 향신료로 양념하여 동물의 위에 "
     r"넣어 삶은 요리\\Gavial Food와 Cursed Bat Wing를 써서 만들 수 있다.",
     r"Restores 600 MP\\Dish of meat minced fine, seasoned with spices, "
     r"put into an animal's stomach, and boiled\\Made using Gavial Food "
     r"and Cursed Bat Wing."),
    (r"MP를 600 회복\\야채로 속을 채운 파스타\\Carrot Manna와 Cursed "
     r"Spider Blood를 써서 만들 수 있다.",
     r"Restores 600 MP\\Pasta filled with vegetables\\Made using Carrot "
     r"Manna and Cursed Spider Blood."),
    (r'"MP를 600 회복\\고기, 양파, 감자, 과일로 속으로 채워놓은 '
     r'패이스트리\\Beholder Tentacle와 Winter Wolf Meat를 써서 만들 수 '
     r'있다."',
     r'"Restores 600 MP\\Pastry packed as filling with meat, onion, '
     r'potato, and fruit\\Made using Beholder Tentacle and Winter Wolf '
     r'Meat."'),
    (r"MP를 700 회복\\고기와 채소를 잘게 썰어서 소스로 버무린 요리\\"
     r"Carrot Manna와 Reaper Skull를 써서 만들 수 있다.",
     r"Restores 700 MP\\Dish of meat and vegetables finely chopped and "
     r"tossed in sauce\\Made using Carrot Manna and Reaper Skull."),
    (r"MP를 700 회복\\다리부위 고기에 완두콩과 절인 양배추를 곁들인 "
     r"음식\\Blackbean Manna와 Infected Wolf Meat를 써서 만들 수 있다.",
     r"Restores 700 MP\\Food with peas and pickled cabbage served "
     r"alongside leg meat\\Made using Blackbean Manna and Infected Wolf "
     r"Meat."),
    (r"MP를 700 회복\\고기를 마늘과 함께 오븐에 구운 요리\\Blackbean "
     r"Manna와 Vagrant Lizardman Tail를 써서 만들 수 있다.",
     r"Restores 700 MP\\Dish of meat roasted in the oven with garlic\\"
     r"Made using Blackbean Manna and Vagrant Lizardman Tail."),
    (r"MP를 800 회복\\휘저어 부친 계란 프라이\\Blackbean Manna와 Ashen "
     r"Ichman Egg를 써서 만들 수 있다.",
     r"Restores 800 MP\\Whisked and pan-fried egg\\Made using Blackbean "
     r"Manna and Ashen Ichman Egg."),
    (r"MP를 800 회복\\고기와 야채를 함께 끓인 수프\\Caliga Scorpion "
     r"Stinger와 Caliga Spider Thorn를 써서 만들 수 있다.",
     r"Restores 800 MP\\Soup boiled with meat and vegetables together\\"
     r"Made using Caliga Scorpion Stinger and Caliga Spider Thorn."),
    (r"MP를 800 회복\\감자와 고기로 속을 채워서 만든 팬케이크 요리\\"
     r"Delomnas Tail과 Caliga Fungal Spore Sac를 써서 만들 수 있다.",
     r"Restores 800 MP\\Pancake dish made by filling it with potato and "
     r"meat\\Made using Delomnas Tail and Caliga Fungal Spore Sac."),
    (r"HP와 MP를 225회복\\해산물을 레몬에 절여서 만든 요리\\Killer Beetle "
     r"Pincer와 Lizardman Tail를 써서 만들 수 있다.",
     r"Restores 225 HP and MP\\Dish made by pickling seafood in lemon\\"
     r"Made using Killer Beetle Pincer and Lizardman Tail."),
    (r'"HP와 MP를 225회복\\짭짤한 소스에 양파, 고기, 피망 등을 넣고 '
     r'볶아낸 요리\\Forgotten Knight Blood와 Amber Bulte Leg를 써서 '
     r'만들거나\\Turtlebeast Pincer와 Amber Bulte Leg를 써서 만들 수 '
     r'있다."',
     r'"Restores 225 HP and MP\\Dish stir-fried in a salty sauce with '
     r'onion, meat, green pepper, and the like\\Made using Forgotten '
     r'Knight Blood and Amber Bulte Leg, or\\Turtlebeast Pincer and Amber '
     r'Bulte Leg."'),
    (r'"HP와 MP를 300회복\\얇은 밀가루 피에 고기, 콩, 야채 등을 싸서 만든 '
     r'요리\\Gnoll Heart와 Stridling Eyeball를 써서 만들 수 있다."',
     r'"Restores 300 HP and MP\\Dish made by wrapping meat, beans, '
     r'vegetables, and the like in thin flour dough\\Made using Gnoll '
     r'Heart and Stridling Eyeball."'),
    (r"HP와 MP를 300회복\\튀긴 토르티야를 펴서 그 위에 고기와 채소를 얹은 "
     r"요리\\Vampire Spider Blood와 Leokin Heart를 써서 만들 수 있다.",
     r"Restores 300 HP and MP\\Dish of a fried tortilla opened out with "
     r"meat and vegetables laid on top\\Made using Vampire Spider Blood "
     r"and Leokin Heart."),
    (r"HP와 MP를 375회복\\빵으로 만든 차가운 수프\\Chunky Soup와 Gorgon "
     r"Tail를 써서 만들거나\\Chunky Soup와 Spis Cyst를 써서 만들 수 있다.",
     r"Restores 375 HP and MP\\Cold soup made from bread\\Made using "
     r"Chunky Soup and Gorgon Tail, or\\Chunky Soup and Spis Cyst."),
    (r'"HP와 MP를 375회복\\밀가루로 만든 또띠아 사이에 치즈, 고기, 야채 '
     r'등을 넣고 오븐에 구운 요리\\Carrion Devourer Antennae와 Coctopod '
     r'Cyst를 써서 만들 수 있다."',
     r'"Restores 375 HP and MP\\Dish with cheese, meat, vegetables, and '
     r'the like between flour tortillas, baked in the oven\\Made using '
     r'Carrion Devourer Antennae and Coctopod Cyst."'),
    (r'"HP와 MP를 450회복\\옥수수와 감자, 야채 등을 층층이 쌓아 올려 만든 '
     r'요리\\Chunky Soup와 Gavial Food를 써서 만들 수 있다."',
     r'"Restores 450 HP and MP\\Dish made by stacking corn, potato, '
     r'vegetables, and the like layer upon layer\\Made using Chunky Soup '
     r'and Gavial Food."'),
    (r'"HP와 MP를 450회복\\크림소스에 쌀과 콩, 해산물을 버무린 요리\\'
     r'Naga Fin과 Phibios Fin을 써서 만들 수 있다."',
     r'"Restores 450 HP and MP\\Dish with rice, beans, and seafood '
     r'tossed in cream sauce\\Made using Naga Fin and Phibios Fin."'),
    (r'"HP와 MP를 450회복\\얇게 저민 고기 속에 야채, 치즈 등을 넣어 말아 '
     r'오븐에 구운 요리\\Snow Tiger Meat와 Beholder Eyeball를 써서 만들 '
     r'수 있다."',
     r'"Restores 450 HP and MP\\Dish with vegetables, cheese, and the '
     r'like inside thinly sliced meat, rolled and baked in the oven\\'
     r'Made using Snow Tiger Meat and Beholder Eyeball."'),
    (r"HP와 MP를 525회복\\햄과 레몬 등이 들어간 매콤새콤한 스프\\Chunky "
     r"Soup와 Snow Nianshou Meat를 써서 만들 수 있다.",
     r"Restores 525 HP and MP\\Spicy and sour soup with ham, lemon, and "
     r"the like in it\\Made using Chunky Soup and Snow Nianshou Meat."),
    (r"HP와 MP를 525회복\\바삭한 패스트리에 부드러운 달걀 크림을 넣은 "
     r"요리\\Gourmet Soup와 Crimson Ichman Egg를 써서 만들 수 있다.",
     r"Restores 525 HP and MP\\Dish with smooth egg cream stuffed into a "
     r"crisp pastry\\Made using Gourmet Soup and Crimson Ichman Egg."),
    (r"HP와 MP를 525회복\\익히지 않은 고기에 달걀을 얹어서 만든 요리\\"
     r"Gourmet Soup와 Infected Leokin Heart를 써서 만들 수 있다.",
     r"Restores 525 HP and MP\\Dish made by topping uncooked meat with "
     r"egg\\Made using Gourmet Soup and Infected Leokin Heart."),
    (r"HP와 MP를 525회복\\쌀과 고기를 볶아서 만든 요리\\Death Wyvern "
     r"Heart와 Death Blood를 써서 만들 수 있다.",
     r"Restores 525 HP and MP\\Dish made by stir-frying rice and meat\\"
     r"Made using Death Wyvern Heart and Death Blood."),
    (r"HP와 MP를 600회복\\삶은 감자와 고기를 으깨서 튀겨낸 크로켓\\Gredor "
     r"Marrow와 Horsebee Wing를 써서 만들 수 있다.",
     r"Restores 600 HP and MP\\Croquette of mashed boiled potato and "
     r"meat, deep-fried\\Made using Gredor Marrow and Horsebee Wing."),
    (r"HP와 MP를 600회복\\고기를 두들겨 부드럽게 한 뒤 튀겨낸 요리\\"
     r"Gourmet Soup와 Delomnas Horn를 써서 만들 수 있다.",
     r"Restores 600 HP and MP\\Dish made by pounding the meat soft and "
     r"deep-frying\\Made using Gourmet Soup and Delomnas Horn."),
    (r'"HP와 MP를 600회복\\신 양배추, 버섯, 고기를 넣고 삶은 요리\\'
     r'Gourmet Soup와 Caliga Spider Leg를 써서 만들 수 있다."',
     r'"Restores 600 HP and MP\\Boiled dish with sauerkraut, mushrooms, '
     r'and meat\\Made using Gourmet Soup and Caliga Spider Leg."'),
    (r'"HP와 MP를 600회복\\옥수수 가루로 만든 토르티야에 고기, 콩 등을 '
     r'싼 음식\\Ashen Ichman Egg와 Caliga Spider Leg를 써서 만들 수 '
     r'있다."',
     r'"Restores 600 HP and MP\\Food with meat, beans, and the like '
     r'wrapped in a corn-flour tortilla\\Made using Ashen Ichman Egg and '
     r'Caliga Spider Leg."'),
]

_LOG = None
_BUILT = False
_SORTED_ITEMS = None


def _build() -> None:
    global _BUILT, _SORTED_ITEMS
    if _BUILT:
        return
    for kor, eng in LONG_TEXT:
        KOR_EN.setdefault(kor, eng)
    _SORTED_ITEMS = sorted(KOR_EN.items(), key=lambda kv: -len(kv[0]))
    _BUILT = True


def _log_miss(s: str) -> None:
    global _LOG
    path = os.environ.get("RDEC_COLLECT")
    if not path:
        return
    if _LOG is None:
        try:
            _LOG = open(path, "a", encoding="utf-8", errors="replace")
        except OSError:
            return
    try:
        _LOG.write(s.replace("\r", "\\r").replace("\n", "\\n") + "\n")
    except Exception:
        pass


def _replace(s: str) -> str:
    for kor, eng in _SORTED_ITEMS:
        if kor in s:
            s = s.replace(kor, eng)
            if not CJK.search(s):
                return s
    return s


def _generic(s: str) -> str:
    if not CJK.search(s):
        return s
    s = _COUNT_CHIP.sub(r"x\1", s)
    return _replace(s)


_HOOKS = (
    ("AddItem", re.compile(r"\A\s*AddItem\(\s*0x[0-9A-Fa-f]+\s*,\s*-?\d+"
                           r"\s*,\s*-?\d+\s*,\s*-?\d+\s*,\s*(\d+)\s*\)")),
    ("Event_Get", re.compile(r"\A\s*Event_Get\(\s*-?\d+\s*,\s*(-?\d+)\s*\)")),
    ("Event_Disappear", re.compile(
        r"\A\s*Event_Disappear\(\s*-?\d+\s*,\s*(-?\d+)(?:\s*,\s*-?\d+\s*)?\)")),
)

_MARK = re.compile(r"//")


def _comment_marker(line: str) -> int:
    starts = [m.start() for m in _MARK.finditer(line)]
    for pos in reversed(starts):
        if HANGUL.search(line[pos + 2:]):
            return pos
    return -1


def _namemap_get(namemap, key):
    try:
        if key in namemap:
            return namemap[key]
    except TypeError:
        pass
    try:
        if str(key) in namemap:
            return namemap[str(key)]
    except TypeError:
        pass
    return None


def _hook_id(call: str):
    for _name, pat in _HOOKS:
        m = pat.match(call)
        if m:
            return int(m.group(1))
    return None


def _split_marks(body: str):
    tail = None
    size = None
    count = None
    s = body
    m = _PK_TAIL.search(s)
    if m:
        tail = "//" + m.group(1)
        s = s[:m.start()]
    m = _PK_SIZE.search(s)
    if m:
        size = m.group(1)
        s = s[:m.start()]
    m = _PK_COUNT.search(s)
    if m:
        count = m.group(1)
        s = s[:m.start()]
    m = _PK_XCOUNT.search(s)
    if m:
        count = m.group(1)
        s = s[:m.start()]
    return s.strip(), count, size, tail


def _render_label(name: str, count, size, tail) -> str:
    out = name
    if size:
        out += f"({size})"
    if count:
        out += f" x{count}"
    if tail:
        out += " " + tail
    return out


def _translate_comment(line: str, namemap):
    pos = _comment_marker(line)
    if pos < 0:
        return None
    call = line[:pos]
    piece = line[pos + 2:]

    n = len(piece)
    i = 0
    while i < n and piece[i] in " \t":
        i += 1
    while i < n and piece[i] == "/":
        i += 1
    while i < n and piece[i] in " \t":
        i += 1
    lead_quote = i < n and piece[i] == '"'
    j = i + 1 if lead_quote else i
    end = n
    while end > j and piece[end - 1] in " \t":
        end -= 1
    trailing_quote = end > j and piece[end - 1] == '"'
    if trailing_quote:
        end -= 1
    body = piece[j:end]

    inline = KOR_EN.get(body)
    if inline is not None:
        new_body = inline
    else:
        label, count, size, tail = _split_marks(body)
        name = None
        if (namemap is not None and label and "/" not in label
                and _PURE_KR.fullmatch(label) and HANGUL.search(label)):
            item_id = _hook_id(call)
            if item_id is not None:
                name = _namemap_get(namemap, item_id)
        if name:
            new_body = _render_label(name, count, size, tail)
        else:
            g = _generic(body)
            if HANGUL.search(g):
                return None
            new_body = g

    out = '"' if lead_quote else ""
    out += new_body
    if trailing_quote:
        out += '"'
    return line[:pos] + "//" + piece[:i] + out


def translate_text(s: str, namemap=None) -> str:
    global _BUILT
    if not _BUILT:
        _build()
    if not CJK.search(s):
        return s
    if "//" in s:
        res = _translate_comment(s, namemap)
        if res is not None and not CJK.search(res):
            return res
    hit = KOR_EN.get(s)
    if hit is not None:
        return hit
    if '(' in s and s.rstrip().endswith(");"):
        m = _STRING_ARG.fullmatch(s.strip()) or _STRING_ARG.search(s)
        if m and HANGUL.search(m.group(1)) and not HANGUL.search(
                s[:m.start()] + s[m.end():]):
            hit = KOR_EN.get(m.group(1))
            if hit is not None:
                return s[:m.start()] + '"' + hit + '"' + s[m.end():]
    out = _generic(s)
    if HANGUL.search(out):
        _log_miss(out)
    return out
