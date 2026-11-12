import os as _0x0691
import re as _0x0692
_0x015b = _0x0692.compile('[\\uac00-\\ud7a3\\u3130-\\u318f]')
_0x015c = _0x0692.compile('[\\u3000-\\u303f\\u3130-\\u318f\\u3400-\\u9fff\\uff01-\\uffee\\uac00-\\ud7a3]')
_0x015d = _0x0692.compile('[\\uac00-\\ud7a3\\u3130-\\u318f0-9 ()\\[\\]A-Za-z+.,%:_/-]+\\Z')
_0x015e = _0x0692.compile('\\s*(\\d+)개\\s*\\Z')
_0x015f = _0x0692.compile('\\s*/{2,}\\s*(\\d+)\\s*\\Z')
_0x0160 = _0x0692.compile('\\s*\\((S|M|L|Fine|Superior)\\)\\s*\\Z')
_0x0161 = _0x0692.compile('\\s*[xX]\\s*(\\d+)\\s*\\Z')
_0x0162 = _0x0692.compile('(\\d+)개')
_0x0163 = _0x0692.compile('"([^"\\r\\n]*)"')
_0x0164_rev = {}
_0x0164_rev_bytes = {}
_0x0164 = {'이름': 'Name', '모델링 파일명': 'Model file name', 'NPCDisplay(NPC ID, NPC가 출력될 클라이언트 국적(0=All, 1=Only Korea, 2=Only Foreign), 테스트서버 표시여부, 정식서버 표시여부, 통합서버 표시여부);': 'NPCDisplay(NPC ID, client nationality the NPC appears for (0=All, 1=Only Korea, 2=Only Foreign), show on test server, show on official server, show on merged server);', 'SetNPC(존ID, NPC ID, 마을ID, 성속여부(true, false), GCMDS, Name);': 'SetNPC(zone ID, NPC ID, town ID, sacred or profane (true, false), GCMDS, Name);', 'SetNPC(존ID, NPC ID, 마을ID, 성속여부(true, false), GCMDS, 이름);': 'SetNPC(zone ID, NPC ID, town ID, sacred or profane (true, false), GCMDS, Name);', 'SetPosition(NPC ID, 방향, X, Y(높이), Z);': 'SetPosition(NPC ID, facing, X, Y (height), Z);', 'AddWords(NPC ID, NPC 클릭시 대화창에 표시되는 대화);': 'AddWords(NPC ID, dialogue shown in the chat window when the NPC is clicked);', 'AddDialog(NPC ID, Popup 기능으로 Dialog를 복수로 호출 했을 때 호출한 순서대로 정해지는 인자, 현재는 사용안함, Dialog에 들어가는 메시지);': 'AddDialog(NPC ID, argument assigned in the order the Dialogs were called when several are invoked through the Popup feature, currently unused, message that goes into the Dialog);', 'AddPopupFame(NPC ID, Popup Kind ID, NPC function ID , Popup String, Quest ID, 제한명성, 클래스 ID)\t\t// ROW2009_AbilitySystem': 'AddPopupFame(NPC ID, Popup Kind ID, NPC function ID , Popup String, Quest ID, fame limit, class ID)\t\t// ROW2009_AbilitySystem', 'AddPopupAbility(NPC ID, Popup Kind ID, NPC function ID , Popup String, Ability ID, Ability LV, 클래스 ID)\t\t// ROW2009_AbilitySystem': 'AddPopupAbility(NPC ID, Popup Kind ID, NPC function ID , Popup String, Ability ID, Ability LV, class ID)\t\t// ROW2009_AbilitySystem', 'AddQuestWords(NPC ID, Quest ID, "HelpMassege"); AddQuest(int,int)함수에 의해 등록된 Quest ID를 PC가 수락할 수 있을 때 NPC의 머리위에 뜨는 대사': 'AddQuestWords(NPC ID, Quest ID, "HelpMassege"); words shown above the NPC\'s head when a PC can accept the Quest ID registered through the AddQuest(int,int) function', 'AddZoneMove(NPC ID, 존 ID, X 좌표, Y좌표(높이), Z좌표); 해당 좌표로 존이동 시켜줌': 'AddZoneMove(NPC ID, zone ID, X coord, Y coord (height), Z coord); moves you to the zone at those coordinates', 'AddQuest(NPC ID, Quest ID); Quest ID의 퀘스트를 NPC에 연결 시켜줌': 'AddQuest(NPC ID, Quest ID); attaches the quest of Quest ID to the NPC', '); AddQuest(int,int)함수에 의해 등록된 Quest ID를 PC가 수락할 수 있을 때 NPC의 머리위에 뜨는 대사': "); words shown above the NPC's head when a PC can accept the Quest ID registered through the AddQuest(int,int) function", 'SetDropGrade(NPCID, Item Type FGrade, DBase, CBase, BBase, ABase);  각 그레이드별 최소 (+)옵션 개수': 'SetDropGrade(NPCID, Item Type FGrade, DBase, CBase, BBase, ABase);  minimum number of (+) options per grade', '(어빌리티 아이디, 어빌리티 레벨) - ROW2009_AbilitySystem': '(ability ID, ability level) - ROW2009_AbilitySystem', '(옵션타입, 아이템 ID, 그레이드, BASE 옵션 개수)': '(option type, item ID, grade, number of BASE options)', '(옵션타입, PC의 CLASS, PC의 LEVEL, 그레이드, BASE 옵션 개수)': '(option type, PC CLASS, PC LEVEL, grade, number of BASE options)', '(존 넘버, x좌표, y좌표, z좌표)': '(zone number, x coord, y coord, z coord)', '국가코드, 서버종류, 게임가드 스트링': 'country code, server type, GameGuard string', 'true = 목록저장  false = 저장안함': 'true = save to list  false = do not save', 'Name은 11자 이내로 하도록 주의를 할 것.': 'Note that Name must be 11 characters or fewer.', '이름은 11자 이내로 하도록 주의를 할 것.': 'Note that the name must be 11 characters or fewer.', '영문타이틀은 22자 이내로 하도록 주의를 할 것.': 'Note that the English title must be 22 characters or fewer.', '238\t매찬용 접두사': '238\tprefix for the Lucky string', '239\t매직찬스': '239\tmagic chance', '4321 어빌리티 툴팁윈도우 하단 설명': '4321 ability tooltip window bottom note', '4361 액션 툴팁윈도우 하단 설명': '4361 action tooltip window bottom note', '4411\t아칸이 휴먼노점상 볼때': "4411\twhat an Ak'kan sees when viewing a Human stall", '4412\t휴먼이 아칸 노점상 볼때': "4412\twhat a Human sees when viewing an Ak'kan stall", '4413\t석상전쟁에 참여하기 위해선 41레벨 이상이 되어야 합니다.': '4413\tyou must be level 41 or higher to participate in Statue War.', '4607  Shatter 관련': '4607  relates to Shatter', '4608  하드히트 관련': '4608  relates to Hard Hit', '대만 정섭': 'Taiwan official server', '어서오시게.': 'Welcome.', '알벤트는 사이너 아일랜드에 있는 할아버지': 'Albent is the grandfather on Scyna Island', '튜토리얼 퀘스트 걸어줄 것': 'assign the tutorial quest', '퀘스트 걸어줄것': 'assign the quest', 'Blacksmith 튜토리얼 퀘스트 걸어줄 것': 'assign the Blacksmith tutorial quest', '스페셜 메달상점': 'Special medal shop', '캐릭터 Name 변경': 'Character Name change', '캐릭터 이름 변경': 'Character name change', '밸런스 붕괴에 치명적!!! 가급적 사용하지 말것(유료화 확정)': 'FATAL to balance!!! Avoid using if at all possible (switch to a paid service confirmed)', '메인터넌스 챈트 스킬북 추가': 'added Maintenance Chant skillbook', '엑셀레이션 챈트 스킬북 추가': 'added Acceleration Chant skillbook', '라이프옵 가드암 - 2009. 01.16': 'Life Armguard - 2009. 01.16', 'Empty Cruet(2010.4.27 추가)': 'Empty Cruet (added 2010.4.27)', '포리': 'Pori', '가드 Arm': 'Guard Arm', '퀘스트 보너스': 'Quest bonus', '신전의 파편': 'Temple fragment', '신전의 파편 제거': 'Remove the temple fragment', '전직의 증표': 'Class Change Certificate', '씨맨 비늘 10개 제거': 'Remove 10 Seaman scales', '좀비도그 뼈 10개': 'Zombie dog bone x10', '좀비도그 체인 3개': 'Zombie dog chain x3', '가공된 늑대 발톱 5개 (이거 Drop/Sell 옵션 꺼야함)': 'Processed wolf claw x5 (turn off the Drop/Sell options on this)', '고철덩어리 1개 (이거 Drop/Sell 옵션 꺼야함)': 'Scrap iron x1 (turn off the Drop/Sell options on this)', '고철덩어리': 'Scrap iron', '자이언트 스파이더링 10개 수집': 'Collect 10 Giant Spiderlings', 'Dire Boar 고기 10개 수집': 'Collect 10 Dire Boar meat', '언데드 기생충 10개 수집': 'Collect 10 Undead parasites', '트롤 대거 10개 수집': 'Collect 10 Troll daggers', 'Spis Thorn x 10개 수집': 'Collect 10 Spis Thorn', '고블린 심장 5개': 'Goblin heart x5', '고블린 심장': 'Goblin heart', '킬러비틀 집게 10개': 'Killer Beetle pincer x10', '킬러비틀 껍질 7개': 'Killer Beetle shell x7', '쿠루민 스트랩 20개': 'Korumin strap x20', '늑대 발톱 15개': 'Wolf claw x15', '깃털 20개': 'Feather x20', '거북이 껍질 10개': 'Turtle shell x10', '엘로이 이빨 5개': 'Eloyee tooth x5', '엘로이 심장 5개': 'Eloyee heart x5', '엘로이 이빨 9개': 'Eloyee tooth x9', '엘로이 심장 3개': 'Eloyee heart x3', '리자드맨 비늘 10개': 'Lizardman scale x10', '복어 지느러미 10개': 'Pufferfish fin x10', '복어의 독 샘플 3개': 'Pufferfish poison sample x3', '작은 진주': 'Small pearl', '좀비 기생체': 'Zombie parasite', '캐리온 라바 껍질 2개': 'Carrion Larva skin x2', '시험관 3개': 'Test tube x3', '젊은 여자': 'Young woman', '해적마을 중앙 나무': 'The pirate village central tree', '편지': 'letter', 'Tihon의 편지': "Tihon's letter", '이벤트 아이템 "금화': 'Event item "Gold coin', '이벤트 아이템 "Tihon의 편지': 'Event item "Tihon\'s letter', '이벤트 아이템 "편지': 'Event item "letter', '퀘스트 보상 ': 'Quest reward ', '이벤트용 선물상자': 'Event gift box', '이벤트용 사탕': 'Event candy', '이벤트용 캔디 ': 'Event candy ', '이벤트용 캔디': 'Event candy', '이벤트용 파이': 'Event pie', '이벤트용 술': 'Event liquor', '불꽃놀이 셋트': 'Fireworks set', '산타의 선물': "Santa's present", '가면 전용 상자': 'Mask-only box', '할로윈 기프트': 'Halloween gift', '황금열쇠': 'Golden key', '동열쇠': 'Bronze key', '은빛열쇠': 'Silver key', '행운의 부적': 'Lucky talisman', '알디아항구 스크롤': 'Scroll to Aldia Harbor', '오피니 스크롤': 'Scroll to Opeany', '미하엘의 가호': "Michael's blessing", '첫번째휴식': 'First Rest', '첫번째 휴식': 'First Rest', '알디아항구': 'Aldia Harbor', '알디아 항구': 'Aldia Harbor', '테시티오': 'Tessetio', '감시자캠프': 'Watch Camp', '베인 캠프': 'Bein Camp', '베인': 'Bein', '유니테': 'Unite', '오페니': 'Opeany', '시즈나': 'Syzna', '뉴베린 항구': 'New Berin Harbor', '파울린': 'Paoulin', '하이레이크': 'High Lake', '바르윈': 'Varween', '오르티뉴': 'Ortinue', '칼리오': 'Carlio', '파르타인': 'Partein', '미들캠프': 'Middle Camp', '그린웨일즈': 'Green Wales', '로슈캠프': 'Roche Camp', '클라우츠': 'Clauzhuz', '생명제단': 'Sacrifice Shrine', '우익단체': 'Righties Camp', '얼어붙은 초원 엘리오르': 'Snowrimp Village', '귀환서': 'Return Scroll', '스크롤': 'scroll', '컴크러쉬': 'Com Crush', '컴블레이드': 'Com Blade', '오크러쉬': 'Opp Crush', '오블레이드': 'Opp Blade', '오해머': 'Opp Hammer', '사이드': 'Side', '클로우': 'Claw', '어택암': 'Attack Arm', '건암': 'Gun Arm', '나이프암': 'Knife Arm', '가드암': 'Guard Arm', '컴상체': 'Com Body', '오상체': 'Opp Body', '컴투구': 'Com Helm', '오투구': 'Opp Helm', '컴하체': 'Com Pelvis', '오하체': 'Opp Pelvis', '컴암': 'Com Arm', '오암': 'Opp Arm', '컴배턴트 곡괭이': 'Combatant Pickaxe', '오피세이터 곡괭이': 'Officiator Pickaxe', '곡괭이': 'Pickaxe', '단검': 'Dagger', '한손검': 'One-handed sword', '양손검': 'Two-handed sword', '한손도끼': 'One-handed axe', '양손도끼': 'Two-handed axe', '한손둔기': 'One-handed blunt', '양손둔기': 'Two-handed blunt', '지팡이': 'Staff', '석궁': 'Crossbow', '중갑옷': 'Heavy armor', '경갑옷(로그)': 'Light armor (rogue)', '경갑옷(법사)': 'Light armor (mage)', '경투구(공통)': 'Light helmet (common)', '중투구': 'Heavy helmet', '경투구': 'Light helmet', '방패(공통)': 'Shield (common)', '방패': 'Shield', '중장갑': 'Heavy gauntlet', '경장갑': 'Light gauntlet', '중부츠': 'Heavy boots', '경부츠': 'Light boots', '농축': 'concentrated', '셔츠': 'Shirt', '튜닉': 'Tunic', '빵': 'Bread', '베이컨': 'Bacon', '생고기': 'Raw meat', '구운고기': 'Roasted meat', '증류수': 'Distilled Water', 'MP회복 소': 'MP recovery (S)', 'MP회복 중': 'MP recovery (M)', 'MP회복 대': 'MP recovery (L)', 'MP회복 특대': 'MP recovery (XL)', 'HP/MP회복 소': 'HP/MP recovery (S)', 'HP/MP회복 중': 'HP/MP recovery (M)', 'HP/MP회복 대': 'HP/MP recovery (L)', 'HP/MP회복 특대': 'HP/MP recovery (XL)', '레벨 10 D등급 장비': 'Level 10 D-grade equipment', '레벨 1 B등급 장비': 'Level 1 B-grade equipment', '레벨 30 B등급 장비': 'Level 30 B-grade equipment', '레벨 35 D등급 장비': 'Level 35 D-grade equipment', 'D급 장비': 'D-grade equipment', '(10렙 D+3 Master Sword)': '(Lv 10 D+3 Master Sword)', '(10렙 D+3 Pawn Stroke)': '(Lv 10 D+3 Pawn Stroke)', '(10렙 D+3 Wooden club)': '(Lv 10 D+3 Wooden club)', '(10렙 D+3 Dark Stick)': '(Lv 10 D+3 Dark Stick)', '(10렙 D+3 Latish Slusher)': '(Lv 10 D+3 Latish Slusher)', '중갑옷 60lv': 'Heavy armor 60lv', '중갑옷 65lv': 'Heavy armor 65lv', '중투구 60 로그': 'Heavy helmet 60 rogue', '경투구 60 메이지': 'Light helmet 60 mage', '중투구 60 워리어 계열': 'Heavy helmet 60 warrior family', '소드마스터리1': 'Sword Mastery 1', '소드마스터리2': 'Sword Mastery 2', '하드히트': 'Hard Hit', '윌파워1': 'Willpower 1', '윌파워2': 'Willpower 2', '임프루브드 크리티컬1': 'Improved Critical 1', '임프루브드크리티컬2': 'Improved Critical 2', '액스마스터리1': 'Axe Mastery 1', '액스마스터리2': 'Axe Mastery 2', '블런트마스터리1': 'Blunt Mastery 1', '블런트마스터리2': 'Blunt Mastery 2', '터프니스1': 'Toughness 1', '터프니스2': 'Toughness 2', '퍼스트 에이드': 'First Aid', '니들 스핏': 'Needle Spit', '이베이젼1': 'Evasion 1', '이베이젼2': 'Evasion 2', '인커리지': 'Encourage', '블러디 마나': 'Bloody Mana', '뱀파이어릭 터치': 'Vampire Kiss', '마나셀': 'Mana Cell', '그리스': 'Grease', '서레너티1': 'Serenity 1', '서레너티2': 'Serenity 2', '슬러그': 'Slug', '릴리프': 'Relief', '블레스': 'Bless', '페이먼트': 'Blood Offering', '드레인라이프': 'Drain Life', '프로텍션': 'Protection', '홀드포지션': 'Hold Position', '익스플로시브 니들': 'Explosive Needle', '현재 등록되어 있는 서버군이 없기 때문에, 서버를 선택해야 됩니다.': 'There is no registered server group at the moment, so a server must be selected.', '안녕하세요. 릴(R.Y.L.)온라인입니다.\\\\': 'Hello. This is RYL (R.Y.L.) Online.\\\\', '고객님께서는 현재 릴온라인 Part2 통합서버에 로그인하셨습니다.\\\\': 'You have logged into the RYL Online Part 2 merged server.\\\\', '릴 온라인은 Part2 가 업데이트되는 동시에 기존의 6개 서버에서 Part1 통합서버, Part2 통합서버, Part2 신규서버로 통합을 하여 새롭게 오픈하였습니다.': 'When Part 2 was updated, RYL Online merged the previous 6 servers into the Part 1 merged server, the Part 2 merged server, and the Part 2 new server, and opened them anew.', '기존에 Part1 을 이용하고 계셨던 고객님께서는 아래의 유의 사항을 꼭 참고하시어 이용에 착오 없으시길 바랍니다.\\\\ \\\\': 'Customers who have been using Part 1, please make sure to read the notes below so that there are no problems with your use.\\\\ \\\\', '1. Part2 통합서버에서는 서버 통합전 데이터에서 계정 내 캐릭터 최대 5명, 창고 1개를 선택하실 수 있고 새로운 캐릭터 생성도 가능합니다. \\\\': '1. On the Part 2 merged server, you can choose up to 5 characters and 1 warehouse from the pre-merger data, and new character creation is also possible. \\\\', '2. Part2 통합서버에서 미리 선택하시지 않은 캐릭터와 창고데이터들은 서버 통합전 데이터에서 삭제되지 않으며, Part2 통합서버에서 재차 선택하실 수 있습니다. (Part2 신규서버 제외).\\\\': '2. Characters and warehouse data you did not pre-select on the Part 2 merged server are not deleted from the pre-merger data, and can be selected again on the Part 2 merged server (excluding the Part 2 new server).\\\\', '3. Part1, Part2 통합서버에 같은 캐릭터와 같은 창고데이터를 중복적으로 선택하실 수 없습니다. 그리고 Part2 통합서버에서 선택하신 캐릭터는 Part1 로의 이전이 불가능합니다.\\\\': '3. The same character and the same warehouse data cannot be selected on both the Part 1 and Part 2 merged servers. Also, a character selected on the Part 2 merged server cannot be moved over to Part 1.\\\\', "4. Part1 통합서버나 Part2 통합서버에서 선택 혹은 이전하신 캐릭터를 '캐릭터 선택화면'에서 삭제하실 경우에 서버 통합전 데이터, Part1 통합서버, Part2 통합 서버에서 동시에 삭제되므로 신중히 결정해주시기 바랍니다.\\\\": "4. If you delete a character you selected on or moved to the Part 1 or Part 2 merged server from the 'character selection screen', it is deleted at the same time from the pre-merger data, the Part 1 merged server, and the Part 2 merged server, so please decide carefully.\\\\", '캐릭터를 추가로 선택하실 수 있습니다.\\\\추가로 선택하시겠습니까?': 'You can select additional characters.\\\\Would you like to select more?', '추가선택': 'Select more', '선택안함': 'Do not select', "안녕하십니까. 신화운영팀입니다.\\\\고객님은 현재 신화 파트투 통합서버에 접속중이십니다. 통합이전 서버군들 중에서 통합서버에서 플레이하실 서버를 골라주십시요. '빠른로그인'을 선택하실경우 가장 최근에 플레이하신 서버의 데이터로 접속하게 됩니다.": "Hello. This is the Shinhwa operations team.\\\\You are currently connected to the Shinhwa Part Two merged server. Please choose which of the pre-merger server groups you will play on the merged server. Selecting 'Quick Login' connects you with the data of the server you played most recently.", 'Enjoy delicious Korean Chuseok food.\\\\HP 1100 recovery회복.\\\\': 'Enjoy delicious Korean Chuseok food.\\\\Restores 1100 HP.\\\\', 'Enjoy delicious Korean Chuseok food.\\\\HP 900 recovery.\\\\': 'Enjoy delicious Korean Chuseok food.\\\\Restores 900 HP.\\\\', '경험치': 'EXP', '골드': 'gold', '명성치': 'fame', '명성': 'fame', '레벨': 'Level', '렙': 'Lv', '등급 장비': '-grade equipment', '급 장비': '-grade equipment', '장비': 'equipment', '회복약': 'healing potions', '이터니움': 'Iternium', '토파즈': 'Topaz', '금화': 'Gold coin', '고기': 'meat', '가죽': 'Pelt', '이빨': 'Fang'}
_0x0165 = [('요리에 사용되는 기본 도구', 'Basic tool used for cooking'), ('HP를 300 회복\\\\고기를 말려서 만든 육포\\\\Dire Boar Meat와 Goblin Heart를 이용하거나\\\\Dire Boar Meat와 Killer Beetle Husk를 써서 요리할 수 있다.', 'Restores 300 HP\\\\Jerky made by drying meat\\\\Made using Dire Boar Meat and Goblin Heart, or\\\\Dire Boar Meat and Killer Beetle Husk.'), ('HP를 300 회복\\\\잘 구운 Ostopterix 구이요리\\\\Ostopterix Meat와 Monk Brain를 쓰거나\\\\Ostopterix Meat와 Korkebine Heart를 써서 요리할 수 있다', 'Restores 300 HP\\\\Well-roast Ostopterix dish\\\\Made using Ostopterix Meat and Monk Brain, or\\\\Ostopterix Meat and Korkebine Heart'), ('HP를 400 회복\\\\말린 고기로 만든 요리\\\\Gnoll Rib과 Tren Charcoal을 써서 요리할 수 있다.', 'Restores 400 HP\\\\Dish made from dried meat\\\\Made using Gnoll Rib and Tren Charcoal.'), ('HP를 400 회복\\\\육류에 오크라를 넣어 만든 수프\\\\Scyna Scorpion Tail와 Rhinoman Horn을 쓰거나\\\\Gorep Brain과 Wraith Eyeball을 사용해 요리할 수 있다.', 'Restores 400 HP\\\\Soup made by adding okra to meat\\\\Made using Scyna Scorpion Tail and Rhinoman Horn, or\\\\Gorep Brain and Wraith Eyeball.'), ('HP를 500 회복\\\\말린 고기를 훈제해서 만든 음식\\\\Roasted Meat와 Ceratop Skin를 써서 요리할 수 있다.', 'Restores 500 HP\\\\Food made by smoking dried meat\\\\Made using Roasted Meat and Ceratop Skin.'), ('HP를 500 회복\\\\고기의 우둔살을 고운 요리\\\\Stump Charcoal와 Giant Boar Meat를 써서 요리할 수 있다.', 'Restores 500 HP\\\\Dish of roasted meat rump\\\\Made using Stump Charcoal and Giant Boar Meat.'), ('HP를 500 회복\\\\양고기로 만든 소시지\\\\Roasted Meat와 Stump Branch를 써서 요리할 수 있다.', 'Restores 500 HP\\\\Sausage made from lamb\\\\Made using Roasted Meat and Stump Branch.'), ('HP를 600 회복\\\\고기를 곱게 갈아 동물의 창자에 채운 요리\\\\Flynd Meat와 Nohnuut Eyeball를 써서 요리할 수 있다.', "Restores 600 HP\\\\Dish of finely ground meat stuffed into an animal's intestine\\\\Made using Flynd Meat and Nohnuut Eyeball."), ('HP를 600 회복\\\\고기를 반죽해 숙성시킨 뒤 만든 소시지\\\\Roasted Meat와 Naga Fin을 써서 만들 수 있다.', 'Restores 600 HP\\\\Sausage made by kneading meat and letting it mature\\\\Made using Roasted Meat and Naga Fin.'), ('HP를 600 회복\\\\고기로 걸쭉하게 끓인 수프\\\\Snow Gorgon Tail과 Snow Boar Meat를 써서 만들 수 있다.', 'Restores 600 HP\\\\Soup boiled thick with meat\\\\Made using Snow Gorgon Tail and Snow Boar Meat.'), ('HP를 700 회복\\\\고기를 꼬치에 꿰어서 구운 요리\\\\Roasted Meat와 Clinzer Bone Wing을 써서 만들 수 있다.', 'Restores 700 HP\\\\Meat roasted on a skewer\\\\Made using Roasted Meat and Clinzer Bone Wing.'), ('"HP를 700 회복\\\\돼지장에 후추와 잣, 과일 열매를 넣고 구운 요리\\\\Bacon과 Infected Gorgon Tail을 써서 만들 수 있다."', '"Restores 700 HP\\\\Pork fatback roast with pepper, pine nuts, and fruit baked in\\\\Made using Bacon and Infected Gorgon Tail."'), ('HP를 700 회복\\\\안심부위를 구운 요리\\\\Bacon과 Caernarvon Boar Meat를 사용해 만들 수 있다.', 'Restores 700 HP\\\\Roast of the tenderloin cut\\\\Made using Bacon and Caernarvon Boar Meat.'), ('HP를 700 회복\\\\와이번 고기로 만든 스튜\\\\Death Wyvern Meat와 Reaper Skull을 써서 만들 수 있다.', 'Restores 700 HP\\\\Stew made from wyvern meat\\\\Made using Death Wyvern Meat and Reaper Skull.'), ('"HP를 800 회복\\\\고기, 채소 등을 다진 것을 속에 넣고 만든 파이\\\\Caliga Scorpion Meat과 Kappa Blood를 써서 만들 수 있다."', '"Restores 800 HP\\\\Pie made with minced meat, vegetables, and the like as filling\\\\Made using Caliga Scorpion Meat and Kappa Blood."'), ('MP를 700 회복\\\\고기와 피와 기름,곡류를 섞어 크게 만든 소시지\\\\Dullahan Blood와 Snow Nianshou Meat를 써서 만들 수 있다.', 'Restores 700 MP\\\\Large sausage mixed from meat, blood, oil, and grain\\\\Made using Dullahan Blood and Snow Nianshou Meat.'), ('HP를 800 회복\\\\고기를 기름에 튀겨낸 요리\\\\Bacon과 Ashen Ichman Scale를 써서 만들 수 있다.', 'Restores 800 HP\\\\Dish of meat deep-fried in oil\\\\Made using Bacon and Ashen Ichman Scale.'), ('HP를 800 회복\\\\고기의 엉덩이부위를 검게 그을릴 정도로 구운 요리\\\\Hellwolf Meat과 Gredor Heart를 써서 만들 수 있다.', "Restores 800 HP\\\\Dish with the meat's rump roasted until charred black\\\\Made using Hellwolf Meat and Gredor Heart."), ('HP를 800 회복\\\\먹기좋게 한입 사이즈로 만든 고기 요리\\\\Bacon과 Caliga Fungal Spore를 사용해 만들 수 있다.', 'Restores 800 HP\\\\Meat dish made bite-sized for easy eating\\\\Made using Bacon and Caliga Fungal Spore.'), ('MP를 800 회복\\\\감자, 야채, 고기를 섞어서 버무린 샐러드\\\\Blackbean Manna와 Horsebee Wing를 써서 만들 수 있다.', 'Restores 800 MP\\\\Salad tossed together with potato, vegetables, and meat\\\\Made using Blackbean Manna and Horsebee Wing.'), ('MP를 300 회복\\\\얇게 썬 빵 사이에 육류나 채소류를 끼워서 먹는 요리\\\\Raged Dire Wolf Meat과 Dire Bat Wing써서 만들거나\\\\Eloyee Heart와 Krumin Meat를 써서 만들 수 있다.', 'Restores 300 MP\\\\Dish eaten with meat or vegetables sandwiched between thin slices of bread\\\\Made using Raged Dire Wolf Meat and Dire Bat Wing, or\\\\Eloyee Heart and Krumin Meat.'), ('MP를 300 회복\\\\재료를 한데 섞어 장시간 푹 끓여 만든 요리\\\\Poison Spiderling와 Monk Meat를 써서 만들거나\\\\Turtlebeast Shell과 Lehan Scorpion Tail를 써서 만들 수 있다.', 'Restores 300 MP\\\\Dish made by mixing the ingredients together and simmering them for a long time\\\\Made using Poison Spiderling and Monk Meat, or\\\\Turtlebeast Shell and Lehan Scorpion Tail.'), ('MP를 400 회복\\\\고기에 튀김옷을 입혀 튀긴 것과 감자튀김을 함께 먹는 음식\\\\Flynd Meat와 Carrion Crawler Antennae를 써서 만들거나\\\\Gargoyle Wing과 Carrion Crawler Antennae를 써서 만들 수 있다.', 'Restores 400 MP\\\\Food eaten as battered deep-fried meat together with french fries\\\\Made using Flynd Meat and Carrion Crawler Antennae, or\\\\Gargoyle Wing and Carrion Crawler Antennae.'), ('"MP를 400 회복\\\\밀가루에 고기, 우유, 달걀을 넣어 반죽한 것을 구운 요리\\\\Murky Ichman Egg와 Shiny Bulte Leg를 써서 만들 수 있다."', '"Restores 400 MP\\\\Batter of flour with meat, milk, and eggs kneaded in and baked\\\\Made using Murky Ichman Egg and Shiny Bulte Leg."'), ('MP를 500 회복\\\\야채와 고기로 속을 채운 페스트리\\\\Carrot Manna와 Skullbat Wing를 써서 만들 수 있다.', 'Restores 500 MP\\\\Pastry filled with vegetables and meat\\\\Made using Carrot Manna and Skullbat Wing.'), ('MP를 500 회복\\\\Gorgon Tail을 매콤한 양념에 장시간 끊인 찜요리\\\\Dire Gorgon Tail와 Strider Eyeball을 써서 만들 수 있다.', 'Restores 500 MP\\\\Stewed Gorgon Tail simmered for a long time in spicy seasoning\\\\Made using Dire Gorgon Tail and Strider Eyeball.'), ('MP를 500 회복\\\\각종 야채와 고기를 끓여서 만드는 수프\\\\Carrot Manna와 Fungus Feeler를 써서 만들 수 있다.', 'Restores 500 MP\\\\Soup made by boiling assorted vegetables and meat\\\\Made using Carrot Manna and Fungus Feeler.'), ('MP를 600 회복\\\\고기을 잘게 다져서 향신료로 양념하여 동물의 위에 넣어 삶은 요리\\\\Gavial Food와 Cursed Bat Wing를 써서 만들 수 있다.', "Restores 600 MP\\\\Dish of meat minced fine, seasoned with spices, put into an animal's stomach, and boiled\\\\Made using Gavial Food and Cursed Bat Wing."), ('MP를 600 회복\\\\야채로 속을 채운 파스타\\\\Carrot Manna와 Cursed Spider Blood를 써서 만들 수 있다.', 'Restores 600 MP\\\\Pasta filled with vegetables\\\\Made using Carrot Manna and Cursed Spider Blood.'), ('"MP를 600 회복\\\\고기, 양파, 감자, 과일로 속으로 채워놓은 패이스트리\\\\Beholder Tentacle와 Winter Wolf Meat를 써서 만들 수 있다."', '"Restores 600 MP\\\\Pastry packed as filling with meat, onion, potato, and fruit\\\\Made using Beholder Tentacle and Winter Wolf Meat."'), ('MP를 700 회복\\\\고기와 채소를 잘게 썰어서 소스로 버무린 요리\\\\Carrot Manna와 Reaper Skull를 써서 만들 수 있다.', 'Restores 700 MP\\\\Dish of meat and vegetables finely chopped and tossed in sauce\\\\Made using Carrot Manna and Reaper Skull.'), ('MP를 700 회복\\\\다리부위 고기에 완두콩과 절인 양배추를 곁들인 음식\\\\Blackbean Manna와 Infected Wolf Meat를 써서 만들 수 있다.', 'Restores 700 MP\\\\Food with peas and pickled cabbage served alongside leg meat\\\\Made using Blackbean Manna and Infected Wolf Meat.'), ('MP를 700 회복\\\\고기를 마늘과 함께 오븐에 구운 요리\\\\Blackbean Manna와 Vagrant Lizardman Tail를 써서 만들 수 있다.', 'Restores 700 MP\\\\Dish of meat roasted in the oven with garlic\\\\Made using Blackbean Manna and Vagrant Lizardman Tail.'), ('MP를 800 회복\\\\휘저어 부친 계란 프라이\\\\Blackbean Manna와 Ashen Ichman Egg를 써서 만들 수 있다.', 'Restores 800 MP\\\\Whisked and pan-fried egg\\\\Made using Blackbean Manna and Ashen Ichman Egg.'), ('MP를 800 회복\\\\고기와 야채를 함께 끓인 수프\\\\Caliga Scorpion Stinger와 Caliga Spider Thorn를 써서 만들 수 있다.', 'Restores 800 MP\\\\Soup boiled with meat and vegetables together\\\\Made using Caliga Scorpion Stinger and Caliga Spider Thorn.'), ('MP를 800 회복\\\\감자와 고기로 속을 채워서 만든 팬케이크 요리\\\\Delomnas Tail과 Caliga Fungal Spore Sac를 써서 만들 수 있다.', 'Restores 800 MP\\\\Pancake dish made by filling it with potato and meat\\\\Made using Delomnas Tail and Caliga Fungal Spore Sac.'), ('HP와 MP를 225회복\\\\해산물을 레몬에 절여서 만든 요리\\\\Killer Beetle Pincer와 Lizardman Tail를 써서 만들 수 있다.', 'Restores 225 HP and MP\\\\Dish made by pickling seafood in lemon\\\\Made using Killer Beetle Pincer and Lizardman Tail.'), ('"HP와 MP를 225회복\\\\짭짤한 소스에 양파, 고기, 피망 등을 넣고 볶아낸 요리\\\\Forgotten Knight Blood와 Amber Bulte Leg를 써서 만들거나\\\\Turtlebeast Pincer와 Amber Bulte Leg를 써서 만들 수 있다."', '"Restores 225 HP and MP\\\\Dish stir-fried in a salty sauce with onion, meat, green pepper, and the like\\\\Made using Forgotten Knight Blood and Amber Bulte Leg, or\\\\Turtlebeast Pincer and Amber Bulte Leg."'), ('"HP와 MP를 300회복\\\\얇은 밀가루 피에 고기, 콩, 야채 등을 싸서 만든 요리\\\\Gnoll Heart와 Stridling Eyeball를 써서 만들 수 있다."', '"Restores 300 HP and MP\\\\Dish made by wrapping meat, beans, vegetables, and the like in thin flour dough\\\\Made using Gnoll Heart and Stridling Eyeball."'), ('HP와 MP를 300회복\\\\튀긴 토르티야를 펴서 그 위에 고기와 채소를 얹은 요리\\\\Vampire Spider Blood와 Leokin Heart를 써서 만들 수 있다.', 'Restores 300 HP and MP\\\\Dish of a fried tortilla opened out with meat and vegetables laid on top\\\\Made using Vampire Spider Blood and Leokin Heart.'), ('HP와 MP를 375회복\\\\빵으로 만든 차가운 수프\\\\Chunky Soup와 Gorgon Tail를 써서 만들거나\\\\Chunky Soup와 Spis Cyst를 써서 만들 수 있다.', 'Restores 375 HP and MP\\\\Cold soup made from bread\\\\Made using Chunky Soup and Gorgon Tail, or\\\\Chunky Soup and Spis Cyst.'), ('"HP와 MP를 375회복\\\\밀가루로 만든 또띠아 사이에 치즈, 고기, 야채 등을 넣고 오븐에 구운 요리\\\\Carrion Devourer Antennae와 Coctopod Cyst를 써서 만들 수 있다."', '"Restores 375 HP and MP\\\\Dish with cheese, meat, vegetables, and the like between flour tortillas, baked in the oven\\\\Made using Carrion Devourer Antennae and Coctopod Cyst."'), ('"HP와 MP를 450회복\\\\옥수수와 감자, 야채 등을 층층이 쌓아 올려 만든 요리\\\\Chunky Soup와 Gavial Food를 써서 만들 수 있다."', '"Restores 450 HP and MP\\\\Dish made by stacking corn, potato, vegetables, and the like layer upon layer\\\\Made using Chunky Soup and Gavial Food."'), ('"HP와 MP를 450회복\\\\크림소스에 쌀과 콩, 해산물을 버무린 요리\\\\Naga Fin과 Phibios Fin을 써서 만들 수 있다."', '"Restores 450 HP and MP\\\\Dish with rice, beans, and seafood tossed in cream sauce\\\\Made using Naga Fin and Phibios Fin."'), ('"HP와 MP를 450회복\\\\얇게 저민 고기 속에 야채, 치즈 등을 넣어 말아 오븐에 구운 요리\\\\Snow Tiger Meat와 Beholder Eyeball를 써서 만들 수 있다."', '"Restores 450 HP and MP\\\\Dish with vegetables, cheese, and the like inside thinly sliced meat, rolled and baked in the oven\\\\Made using Snow Tiger Meat and Beholder Eyeball."'), ('HP와 MP를 525회복\\\\햄과 레몬 등이 들어간 매콤새콤한 스프\\\\Chunky Soup와 Snow Nianshou Meat를 써서 만들 수 있다.', 'Restores 525 HP and MP\\\\Spicy and sour soup with ham, lemon, and the like in it\\\\Made using Chunky Soup and Snow Nianshou Meat.'), ('HP와 MP를 525회복\\\\바삭한 패스트리에 부드러운 달걀 크림을 넣은 요리\\\\Gourmet Soup와 Crimson Ichman Egg를 써서 만들 수 있다.', 'Restores 525 HP and MP\\\\Dish with smooth egg cream stuffed into a crisp pastry\\\\Made using Gourmet Soup and Crimson Ichman Egg.'), ('HP와 MP를 525회복\\\\익히지 않은 고기에 달걀을 얹어서 만든 요리\\\\Gourmet Soup와 Infected Leokin Heart를 써서 만들 수 있다.', 'Restores 525 HP and MP\\\\Dish made by topping uncooked meat with egg\\\\Made using Gourmet Soup and Infected Leokin Heart.'), ('HP와 MP를 525회복\\\\쌀과 고기를 볶아서 만든 요리\\\\Death Wyvern Heart와 Death Blood를 써서 만들 수 있다.', 'Restores 525 HP and MP\\\\Dish made by stir-frying rice and meat\\\\Made using Death Wyvern Heart and Death Blood.'), ('HP와 MP를 600회복\\\\삶은 감자와 고기를 으깨서 튀겨낸 크로켓\\\\Gredor Marrow와 Horsebee Wing를 써서 만들 수 있다.', 'Restores 600 HP and MP\\\\Croquette of mashed boiled potato and meat, deep-fried\\\\Made using Gredor Marrow and Horsebee Wing.'), ('HP와 MP를 600회복\\\\고기를 두들겨 부드럽게 한 뒤 튀겨낸 요리\\\\Gourmet Soup와 Delomnas Horn를 써서 만들 수 있다.', 'Restores 600 HP and MP\\\\Dish made by pounding the meat soft and deep-frying\\\\Made using Gourmet Soup and Delomnas Horn.'), ('"HP와 MP를 600회복\\\\신 양배추, 버섯, 고기를 넣고 삶은 요리\\\\Gourmet Soup와 Caliga Spider Leg를 써서 만들 수 있다."', '"Restores 600 HP and MP\\\\Boiled dish with sauerkraut, mushrooms, and meat\\\\Made using Gourmet Soup and Caliga Spider Leg."'), ('"HP와 MP를 600회복\\\\옥수수 가루로 만든 토르티야에 고기, 콩 등을 싼 음식\\\\Ashen Ichman Egg와 Caliga Spider Leg를 써서 만들 수 있다."', '"Restores 600 HP and MP\\\\Food with meat, beans, and the like wrapped in a corn-flour tortilla\\\\Made using Ashen Ichman Egg and Caliga Spider Leg."')]
_0x0166 = None
_0x0167 = False
_0x0168 = None


_VN_TBL = {
    0xA7: 'đ',
    0xA8: 'ă',
    0xA9: 'â',
    0xAA: 'ê',
    0xAB: 'ô',
    0xAC: 'ơ',
    0xAD: 'ư',
    0xAE: 'đ',
    0xB5: 'à',
    0xB6: 'ả',
    0xB7: 'ã',
    0xB8: 'á',
    0xB9: 'ạ',
    0xBB: 'ằ',
    0xBC: 'ẳ',
    0xBD: 'ẵ',
    0xBE: 'ắ',
    0xBF: 'ặ',
    0xC6: 'ặ',
    0xC7: 'ầ',
    0xC8: 'ẩ',
    0xC9: 'ẫ',
    0xCA: 'ấ',
    0xCB: 'ậ',
    0xCD: 'è',
    0xCE: 'ẻ',
    0xCF: 'ẽ',
    0xD0: 'é',
    0xD1: 'ẹ',
    0xD2: 'ề',
    0xD3: 'ể',
    0xD4: 'ễ',
    0xD5: 'ế',
    0xD6: 'ệ',
    0xD7: 'ì',
    0xD8: 'ỉ',
    0xDD: 'í',
    0xDE: 'ị',
    0xDF: 'ò',
    0xE1: 'ỏ',
    0xE3: 'ó',
    0xE4: 'ọ',
    0xE5: 'ồ',
    0xE6: 'ố',
    0xE8: 'ố',
    0xE9: 'ộ',
    0xEA: 'ờ',
    0xEB: 'ơ',
    0xEC: 'ỡ',
    0xED: 'ớ',
    0xEE: 'ợ',
    0xEF: 'ù',
    0xF1: 'ủ',
    0xF2: 'ũ',
    0xF3: 'ú',
    0xF5: 'ừ',
    0xF6: 'ử',
    0xF7: 'ữ',
    0xF8: 'ứ',
    0xF9: 'ự',
    0xFC: 'ỹ',
}
def _vn_decode(data):
    return "".join(chr(b) if b < 0x80 else _VN_TBL.get(b, chr(b)) for b in data)

_0x0165b = [
    ('MonsterChat(4001, 6, 0, 255, 100, "Dòng máu trong người bạn như đông cứng lại khi Ancient Guardian bước chân lên vùng Woods of Death.");', 'MonsterChat(4001, 6, 0, 255, 100, "The blood in your body hardens as Ancient Guardian enters the Woods of Death.");', b'MonsterChat(4001, 6, 0, 255, 100, "D\xdfng m\xb8u trong ng\xad\xeai b\xb9n nh\xad \xae\xabng c\xf8ng l\xb9i khi Ancient Guardian b\xad\xedc ch\xa9n l\xaan v\xefng Woods of Death.");'),
    ('MonsterChat(4001, 2, 0xFFFF, 0, 10, "$DEFNAME$ không thể .. tiến lên.. thêm chút nào..");', 'MonsterChat(4001, 2, 0xFFFF, 0, 10, "$DEFNAME$ cannot advance any further..");', b'MonsterChat(4001, 2, 0xFFFF, 0, 10, "$DEFNAME$ kh\xabng th\xd3 .. ti\xd5n l\xaan.. th\xaam ch\xf3t n\xb5o..");'),
    ('MonsterChat(4001, 2, 0xFFFF, 0, 10, "$DEFNAME$ trên đầu gối... Chào ta đi, đồ ngốc!");', 'MonsterChat(4001, 2, 0xFFFF, 0, 10, "$DEFNAME$ on the knee... Greet me, you fool!");', b'MonsterChat(4001, 2, 0xFFFF, 0, 10, "$DEFNAME$ tr\xaan \xae\xc7u g\xe8i... Ch\xb5o ta \xaei, \xae\xe5 ng\xe8c!");'),
    ('MonsterChat(4001, 4, 0, 0, 50, "Ngươi sẽ không qua được.");', 'MonsterChat(4001, 4, 0, 0, 50, "You will not pass.");', b'MonsterChat(4001, 4, 0, 0, 50, "Ng\xad\xaci s\xcf kh\xabng qua \xae\xad\xeec.");'),
    ('MonsterChat(4001, 4, 0, 0, 50, "Chính ta là người canh gác mảnh đất này.");\t\t\t\t\t\t\t\t\t', 'MonsterChat(4001, 4, 0, 0, 50, "I am the one guarding this land.");', b'MonsterChat(4001, 4, 0, 0, 50, "Ch\xddnh ta l\xb5 ng\xad\xeai canh g\xb8c m\xb6nh \xae\xcat n\xb5y.");\t\t\t\t\t\t\t\t\t'),
    ('MonsterChat(4001, 7, 0, 0, 100, "Ta sẽ không chết, không phải lúc này.");\t\t\t\t\t\t\t\t\t\t', 'MonsterChat(4001, 7, 0, 0, 100, "I will not die, not now.");', b'MonsterChat(4001, 7, 0, 0, 100, "Ta s\xcf kh\xabng ch\xd5t, kh\xabng ph\xb6i l\xf3c n\xb5y.");\t\t\t\t\t\t\t\t\t\t'),
    ('MonsterChat(4001, 7, 0, 255, 100, "[$KILLERNAME$] đã đánh bại Ancient Guardian trên vùng Woods of Death.");\t\t', 'MonsterChat(4001, 7, 0, 255, 100, "[$KILLERNAME$] has defeated Ancient Guardian in the Woods of Death.");', b'MonsterChat(4001, 7, 0, 255, 100, "[$KILLERNAME$] \xae\xb7 \xae\xb8nh b\xb9i Ancient Guardian tr\xaan v\xefng Woods of Death.");\t\t'),
    ('MonsterChat(4004, 6, 0, 255, 100, "Death Bringer vừa vào vùng Woods of Death.");', 'MonsterChat(4004, 6, 0, 255, 100, "Death Bringer has just entered the Woods of Death.");', b'MonsterChat(4004, 6, 0, 255, 100, "Death Bringer v\xf5a v\xb5o v\xefng Woods of Death.");'),
    ('MonsterChat(4004, 2, 0xFFFF, 0, 10, "$DEFNAME$ tại sao ngươi không tự nộp mạng?");', 'MonsterChat(4004, 2, 0xFFFF, 0, 10, "$DEFNAME$ why don\'t you submit your life?");', b'MonsterChat(4004, 2, 0xFFFF, 0, 10, "$DEFNAME$ t\xb9i sao ng\xad\xaci kh\xabng t\xf9 n\xe9p m\xb9ng?");'),
    ('MonsterChat(4004, 2, 0xFFFF, 0, 10, "$DEFNAME$ cái chết đang đến rất gần. Hãy để ta giúp.");', 'MonsterChat(4004, 2, 0xFFFF, 0, 10, "$DEFNAME$ death is coming very near. Let me help you.");', b'MonsterChat(4004, 2, 0xFFFF, 0, 10, "$DEFNAME$ c\xb8i ch\xd5t \xaeang \xae\xd5n r\xcat g\xc7n. H\xb7y \xae\xd3 ta gi\xf3p.");'),
    ('MonsterChat(4004, 4, 0, 0, 50, "Dimensional Portal đang bị phá hủy.");', 'MonsterChat(4004, 4, 0, 0, 50, "The Dimensional Portal is being destroyed.");', b'MonsterChat(4004, 4, 0, 0, 50, "Dimensional Portal \xaeang b\xde ph\xb8 h\xf1y.");'),
    ('MonsterChat(4004, 4, 0, 0, 50, "Ngươi có muốn đi cùng ta tới vùng Dimension of Death?");', 'MonsterChat(4004, 4, 0, 0, 50, "Do you want to come with me to the Dimension of Death?");', b'MonsterChat(4004, 4, 0, 0, 50, "Ng\xad\xaci c\xe3 mu\xe8n \xaei c\xefng ta t\xedi v\xefng Dimension of Death?");'),
    ('MonsterChat(4004, 7, 0, 0, 100, "$KILLERNAME$ ngươi đi trước và đợi ta.");', 'MonsterChat(4004, 7, 0, 0, 100, "$KILLERNAME$ go ahead and wait for me.");', b'MonsterChat(4004, 7, 0, 0, 100, "$KILLERNAME$ ng\xad\xaci \xaei tr\xad\xedc v\xb5 \xae\xeei ta.");'),
    ('MonsterChat(4004, 7, 0, 255, 100, "[$KILLERNAME$] đã đánh bại Death Bringer.");', 'MonsterChat(4004, 7, 0, 255, 100, "[$KILLERNAME$] has defeated Death Bringer.");', b'MonsterChat(4004, 7, 0, 255, 100, "[$KILLERNAME$] \xae\xb7 \xae\xb8nh b\xb9i Death Bringer.");'),
    ('MonsterChat(4005, 6, 0, 255, 100, "Bree nhìn một cách lạnh lùng về hướng bạn.");', 'MonsterChat(4005, 6, 0, 255, 100, "Bree looked at you coldly.");', b'MonsterChat(4005, 6, 0, 255, 100, "Bree nh\xd7n m\xe9t c\xb8ch l\xb9nh l\xefng v\xd2 h\xad\xedng b\xb9n.");'),
    ('MonsterChat(4005, 2, 0xFFFF, 0, 10, "$DEFNAME$ ngươi có một cơ thể thật mềm mại, hãy cho ta cắn một miếng.");', 'MonsterChat(4005, 2, 0xFFFF, 0, 10, "$DEFNAME$ you have a soft body, let me take a bite.");', b'MonsterChat(4005, 2, 0xFFFF, 0, 10, "$DEFNAME$ ng\xad\xaci c\xe3 m\xe9t c\xac th\xd3 th\xcbt m\xd2m m\xb9i, h\xb7y cho ta c\xben m\xe9t mi\xd5ng.");'),
    ('MonsterChat(4005, 2, 0xFFFF, 0, 10, "$DEFNAME$ ta sẽ gửi ngươi tới vùng Dimension of Death?");', 'MonsterChat(4005, 2, 0xFFFF, 0, 10, "$DEFNAME$ shall I send you to the Dimension of Death?");', b'MonsterChat(4005, 2, 0xFFFF, 0, 10, "$DEFNAME$ ta s\xcf g\xf6i ng\xad\xaci t\xedi v\xefng Dimension of Death?");'),
    ('MonsterChat(4005, 4, 0, 0, 50, "Ngươi không làm ta hài lòng như ta mong đợi... Ngươi làm ta chán.");', 'MonsterChat(4005, 4, 0, 0, 50, "You don\'t satisfy me as I expected... You bore me.");', b'MonsterChat(4005, 4, 0, 0, 50, "Ng\xad\xaci kh\xabng l\xb5m ta h\xb5i l\xdfng nh\xad ta mong \xae\xeei... Ng\xad\xaci l\xb5m ta ch\xb8n.");'),
    ('MonsterChat(4005, 4, 0, 0, 50, "Ngươi chỉ có như vậy sao?");', 'MonsterChat(4005, 4, 0, 0, 50, "Is that all you\'ve got?");', b'MonsterChat(4005, 4, 0, 0, 50, "Ng\xad\xaci ch\xd8 c\xe3 nh\xad v\xcby sao?");'),
    ('MonsterChat(4005, 7, 0, 0, 100, "$KILLERNAME$ Ta luôn mong muốn đón nhận cảm giác này...");', 'MonsterChat(4005, 7, 0, 0, 100, "$KILLERNAME$ I always wish to receive this feeling...");', b'MonsterChat(4005, 7, 0, 0, 100, "$KILLERNAME$ Ta lu\xabn mong mu\xe8n \xae\xe3n nh\xcbn c\xb6m gi\xb8c n\xb5y...");'),
    ('MonsterChat(4005, 7, 0, 255, 100, "[$KILLERNAME$] đã đánh bại Bree.");', 'MonsterChat(4005, 7, 0, 255, 100, "[$KILLERNAME$] has defeated Bree.");', b'MonsterChat(4005, 7, 0, 255, 100, "[$KILLERNAME$] \xae\xb7 \xae\xb8nh b\xb9i Bree.");'),
    ('MonsterChat(4006, 6, 0, 255, 100, "Smoldering Death tự lộ diện tại Caernarvon.");', 'MonsterChat(4006, 6, 0, 255, 100, "Smoldering Death has revealed itself at Caernarvon.");', b'MonsterChat(4006, 6, 0, 255, 100, "Smoldering Death t\xf9 l\xe9 di\xd6n t\xb9i Caernarvon.");'),
    ('MonsterChat(4006, 2, 0xFFFF, 0, 10, " $DEFNAME$ đừng có bỏ chạy, Ta sẽ sớm kết thúc ngươi.");', 'MonsterChat(4006, 2, 0xFFFF, 0, 10, " $DEFNAME$ don\'t run away, I will finish you soon.");', b'MonsterChat(4006, 2, 0xFFFF, 0, 10, " $DEFNAME$ \xa7\xf5ng c\xe3 b\xe1 ch\xb9y, Ta s\xcf s\xedm k\xd5t th\xf3c ng\xad\xaci.");'),
    ('MonsterChat(4006, 2, 0xFFFF, 0, 10, "HAHAHA. $DEFNAME$ Ngươi vẫn chưa thực sự bỏ cuộc, phải không?");', 'MonsterChat(4006, 2, 0xFFFF, 0, 10, "HAHAHA. $DEFNAME$ You haven\'t really given up yet, have you?");', b'MonsterChat(4006, 2, 0xFFFF, 0, 10, "HAHAHA. $DEFNAME$ Ng\xad\xaci v\xc9n ch\xada th\xf9c s\xf9 b\xe1 cu\xe9c, ph\xb6i kh\xabng?");'),
    ('MonsterChat(4006, 4, 0, 0, 50, "HAHAHA. Ta thích những kẻ yếu đuối. Ta có thể đùa giỡn với ngươi chừng nào ta muốn!");', 'MonsterChat(4006, 4, 0, 0, 50, "HAHAHA. I like weak ones. I can play with you whenever I want!");', b'MonsterChat(4006, 4, 0, 0, 50, "HAHAHA. Ta th\xddch nh\xf7ng k\xce y\xd5u \xaeu\xe8i. Ta c\xe3 th\xd3 \xae\xefa gi\xecn v\xedi ng\xad\xaci ch\xf5ng n\xb5o ta mu\xe8n!");'),
    ('MonsterChat(4006, 4, 0, 0, 50, "HAHA. $DEFNAME$, Ngươi không đau chứ, phải không?");', 'MonsterChat(4006, 4, 0, 0, 50, "HAHA. $DEFNAME$, it doesn\'t hurt, does it?");', b'MonsterChat(4006, 4, 0, 0, 50, "HAHA. $DEFNAME$, Ng\xad\xaci kh\xabng \xaeau ch\xf8, ph\xb6i kh\xabng?");'),
    ('MonsterChat(4006, 7, 0, 0, 100, "$KILLERNAME$, Ta đã đặt lời nguyền cho dòng máu nhà ngươi!");', 'MonsterChat(4006, 7, 0, 0, 100, "$KILLERNAME$, I have placed a curse on your bloodline!");', b'MonsterChat(4006, 7, 0, 0, 100, "$KILLERNAME$, Ta \xae\xb7 \xae\xc6t l\xeai nguy\xd2n cho d\xdfng m\xb8u nh\xb5 ng\xad\xaci!");'),
    ('MonsterChat(4006, 7, 0, 255, 100, "[$KILLERNAME$] đã đánh bại Smoldering Death.");', 'MonsterChat(4006, 7, 0, 255, 100, "[$KILLERNAME$] has defeated Smoldering Death.");', b'MonsterChat(4006, 7, 0, 255, 100, "[$KILLERNAME$] \xae\xb7 \xae\xb8nh b\xb9i Smoldering Death.");'),
    ('MonsterChat(99, 6, 0, 255, 100, "Hydra thoát ra khỏi đống rác bẩn của vùng Gavial Swamp Valley.");', 'MonsterChat(99, 6, 0, 255, 100, "Hydra has escaped out of the pile of dirty trash of Gavial Swamp Valley.");', b'MonsterChat(99, 6, 0, 255, 100, "Hydra tho\xb8t ra kh\xe1i \xae\xe8ng r\xb8c b\xc8n c\xf1a v\xefng Gavial Swamp Valley.");'),
    ('MonsterChat(99, 7, 0, 255, 100, "[$KILLERNAME$] đã đánh bại Hydra.");', 'MonsterChat(99, 7, 0, 255, 100, "[$KILLERNAME$] has defeated Hydra.");', b'MonsterChat(99, 7, 0, 255, 100, "[$KILLERNAME$] \xae\xb7 \xae\xb8nh b\xb9i Hydra.");'),
    ('MonsterChat(166, 6, 0, 255, 100, "Quái vật kinh khủng Brute xuất hiện tại South Nohnuut Field!");', 'MonsterChat(166, 6, 0, 255, 100, "The terrifying monster Brute has appeared at South Nohnuut Field!");', b'MonsterChat(166, 6, 0, 255, 100, "Qu\xb8i v\xcbt kinh kh\xf1ng Brute xu\xcat hi\xd6n t\xb9i South Nohnuut Field!");'),
    ('MonsterChat(166, 2, 0xFFFF, 0, 10, "Bây giờ, những con kiến bé bỏng yếu ớt sẽ phải chạy chốn nếu chúng biết cái gì là tốt cho chúng.");', 'MonsterChat(166, 2, 0xFFFF, 0, 10, "Now, the tiny weak ants will have to run if they know what\'s good for them.");', b'MonsterChat(166, 2, 0xFFFF, 0, 10, "B\xa9y gi\xea, nh\xf7ng con ki\xd5n b\xd0 b\xe1ng y\xd5u \xedt s\xcf ph\xb6i ch\xb9y ch\xe8n n\xd5u ch\xf3ng bi\xd5t c\xb8i g\xd7 l\xb5 t\xe8t cho ch\xf3ng.");'),
    ('MonsterChat(166, 2, 0xFFFF, 0, 10, "đừng sợ hãi, lũ kiến. Chúng mày đang cảm thấy gì?. Ta sẽ làm chúng mày chết ngay lập tức!");', 'MonsterChat(166, 2, 0xFFFF, 0, 10, "Don\'t be afraid, ants. What are you feeling? I will make you die right now!");', b'MonsterChat(166, 2, 0xFFFF, 0, 10, "\xa7\xf5ng s\xee h\xb7i, l\xf2 ki\xd5n. Ch\xf3ng m\xb5y \xaeang c\xb6m th\xcay g\xd7?. Ta s\xcf l\xb5m ch\xf3ng m\xb5y ch\xd5t ngay l\xcbp t\xf8c!");'),
    ('MonsterChat(166, 4, 0, 0, 50, "Cái gì? Lũ kiến đang làm gì vậy?!");', 'MonsterChat(166, 4, 0, 0, 50, "What? What are the ants doing?!");', b'MonsterChat(166, 4, 0, 0, 50, "C\xb8i g\xd7? L\xf2 ki\xd5n \xaeang l\xb5m g\xd7 v\xcby?!");'),
    ('MonsterChat(166, 4, 0, 0, 50, "đừng có chọc giận Brute!");', 'MonsterChat(166, 4, 0, 0, 50, "Don\'t provoke Brute\'s anger!");', b'MonsterChat(166, 4, 0, 0, 50, "\xa7\xf5ng c\xe3 ch\xe4c gi\xcbn Brute!");'),
    ('MonsterChat(166, 7, 0, 0, 100, "AGH! đau quá! Ta đã bị thương bơi $KILLERNAME$... người có sức khỏe phi thường ...");', 'MonsterChat(166, 7, 0, 0, 100, "AGH! It hurts so much! I have been wounded by $KILLERNAME$... you have extraordinary health...");', b'MonsterChat(166, 7, 0, 0, 100, "AGH! \xa7au qu\xb8! Ta \xae\xb7 b\xde th\xad\xacng b\xebi $KILLERNAME$... ng\xad\xeai c\xe3 s\xf8c kh\xe1e phi th\xad\xeang ...");'),
    ('MonsterChat(166, 7, 0, 255, 100, "[$KILLERNAME$], đã đánh bại Brute kẻ khủng bố vùng South Nohnuut Field.");', 'MonsterChat(166, 7, 0, 255, 100, "[$KILLERNAME$], has defeated Brute, terrorist of South Nohnuut Field.");', b'MonsterChat(166, 7, 0, 255, 100, "[$KILLERNAME$], \xae\xb7 \xae\xb8nh b\xb9i Brute k\xce kh\xf1ng b\xe8 v\xefng South Nohnuut Field.");'),
    ('MonsterChat(4007, 6, 0, 255, 100, "Quái vật [Fallen Archfiend] xuất hiện tại vùng Collapsed Dimensional Gateway.");', 'MonsterChat(4007, 6, 0, 255, 100, "The monster [Fallen Archfiend] has appeared at Collapsed Dimensional Gateway.");', b'MonsterChat(4007, 6, 0, 255, 100, "Qu\xb8i v\xcbt [Fallen Archfiend] xu\xcat hi\xd6n t\xb9i v\xefng Collapsed Dimensional Gateway.");'),
    ('MonsterChat(4007, 2, 0xFFFF, 0, 10, "Một cơ thể không có linh hồn..");', 'MonsterChat(4007, 2, 0xFFFF, 0, 10, "A body without a soul..");', b'MonsterChat(4007, 2, 0xFFFF, 0, 10, "M\xe9t c\xac th\xd3 kh\xabng c\xe3 linh h\xe5n..");'),
    ('MonsterChat(4007, 2, 0xFFFF, 0, 10, "không có những cảm giác đau đớn!");', 'MonsterChat(4007, 2, 0xFFFF, 0, 10, "No pain at all!");', b'MonsterChat(4007, 2, 0xFFFF, 0, 10, "kh\xabng c\xe3 nh\xf7ng c\xb6m gi\xb8c \xaeau \xae\xedn!");'),
    ('MonsterChat(4007, 4, 0, 0, 50, "Ah, sinh vật yếu đuối. Nhà người đã uống phí thời gian của mình! và ta sẽ rât sung sướng nhìn ngươi quằn quại trong bàn tay của ta!");', 'MonsterChat(4007, 4, 0, 0, 50, "Ah, weak creature. You have wasted your own time! and I will be very happy to watch you writhe in my hand!");', b'MonsterChat(4007, 4, 0, 0, 50, "Ah, sinh v\xcbt y\xd5u \xaeu\xe8i. Nh\xb5 ng\xad\xeai \xae\xb7 u\xe6ng ph\xdd th\xeai gian c\xf1a m\xd7nh! v\xb5 ta s\xcf r\xa9t sung s\xad\xedng nh\xd7n ng\xad\xaci qu\xbbn qu\xb9i trong b\xb5n tay c\xf1a ta!");'),
    ('MonsterChat(4007, 4, 0, 0, 50, "Sự độc ác của ta đã mạnh hơn ta tương!");', 'MonsterChat(4007, 7, 0, 0, 100, "$KILLERNAME$ - The cruelty within me is stronger than I thought!");', b'MonsterChat(4007, 4, 0, 0, 50, "S\xf9 \xae\xe9c \xb8c c\xf1a ta \xae\xb7 m\xb9nh h\xacn ta t\xad\xebng!");'),
    ('MonsterChat(4007, 7, 0, 0, 100, "$KILLERNAME$ - Sự độc ác trong ta sẽ tồn tại mãi mãi cho dù hôm nay ta có thất bại!");', 'MonsterChat(4007, 7, 0, 0, 100, "$KILLERNAME$ - The cruelty within me will exist forever even if I fail today!");', b'MonsterChat(4007, 7, 0, 0, 100, "$KILLERNAME$ - S\xf9 \xae\xe9c \xb8c trong ta s\xcf t\xe5n t\xb9i m\xb7i m\xb7i cho d\xef h\xabm nay ta c\xe3 th\xcat b\xb9i!");'),
    ('MonsterChat(4007, 7, 0, 255, 100, "[$KILLERNAME$], đã đánh bại [Fallen Archfiend] tại vùng Collapsed Dimensional Gateway.");', 'MonsterChat(4007, 7, 0, 255, 100, "[$KILLERNAME$], has defeated [Fallen Archfiend] at Collapsed Dimensional Gateway.");', b'MonsterChat(4007, 7, 0, 255, 100, "[$KILLERNAME$], \xae\xb7 \xae\xb8nh b\xb9i [Fallen Archfiend] t\xb9i v\xefng Collapsed Dimensional Gateway.");'),
]
def _0x0169() -> None:
    global _0x0167, _0x0168
    if _0x0167:
        return
    for (_0x0693, _0x0694) in _0x0165:
        _0x0164.setdefault(_0x0693, _0x0694)
    for (_0x0693, _0x0694, _0x0695) in _0x0165b:
        _0x0164.setdefault(_0x0693, _0x0694)
        _0x0164_rev.setdefault(_0x0694, _0x0693)
        _0x0164_rev_bytes.setdefault(_0x0694, _0x0695)
    _0x0168 = sorted(_0x0164.items(), key=lambda _0x01d4: -len(_0x01d4[0]))
    _0x0167 = True

def _0x016a(_0x02b2: str) -> None:
    global _0x0166
    _0x0697 = _0x0691.environ.get('RDEC_COLLECT')
    if not _0x0697:
        return
    if _0x0166 is None:
        try:
            _0x0166 = open(_0x0697, 'a', encoding='utf-8', errors='replace')
        except OSError:
            return
    try:
        _0x0166.write(_0x02b2.replace('\r', '\\r').replace('\n', '\\n') + '\n')
    except Exception:
        pass

def _0x016b(_0x02b3: str) -> str:
    for (_0x0699, _0x069a) in _0x0168:
        if _0x0699 in _0x02b3:
            _0x02b3 = _0x02b3.replace(_0x0699, _0x069a)
            if not _0x015c.search(_0x02b3):
                return _0x02b3
    return _0x02b3

def _0x016c(_0x02b4: str) -> str:
    if not _0x015c.search(_0x02b4):
        return _0x02b4
    _0x02b4 = _0x0162.sub('x\\1', _0x02b4)
    return _0x016b(_0x02b4)
_0x016d = (('AddItem', _0x0692.compile('\\A\\s*AddItem\\(\\s*0x[0-9A-Fa-f]+\\s*,\\s*-?\\d+\\s*,\\s*-?\\d+\\s*,\\s*-?\\d+\\s*,\\s*(\\d+)\\s*\\)')), ('Event_Get', _0x0692.compile('\\A\\s*Event_Get\\(\\s*-?\\d+\\s*,\\s*(-?\\d+)\\s*\\)')), ('Event_Disappear', _0x0692.compile('\\A\\s*Event_Disappear\\(\\s*-?\\d+\\s*,\\s*(-?\\d+)(?:\\s*,\\s*-?\\d+\\s*)?\\)')))
_0x016e = _0x0692.compile('//')

def _0x016f(_0x02b5: str) -> int:
    _0x069b = [_0x069d.start() for _0x069d in _0x016e.finditer(_0x02b5)]
    for _0x069c in reversed(_0x069b):
        if _0x015b.search(_0x02b5[_0x069c + 2:]):
            return _0x069c
    return -1

def _0x0170(_0x02b6, _0x02b7):
    try:
        if _0x02b7 in _0x02b6:
            return _0x02b6[_0x02b7]
    except TypeError:
        pass
    try:
        if str(_0x02b7) in _0x02b6:
            return _0x02b6[str(_0x02b7)]
    except TypeError:
        pass
    return None

def _0x0171(_0x02b8: str):
    for (_, _0x069f) in _0x016d:
        _0x06a0 = _0x069f.match(_0x02b8)
        if _0x06a0:
            return int(_0x06a0.group(1))
    return None

def _0x0172(_0x02b9: str):
    _0x06a1 = None
    _0x06a2 = None
    _0x06a3 = None
    _0x06a4 = _0x02b9
    _0x06a5 = _0x015f.search(_0x06a4)
    if _0x06a5:
        _0x06a1 = '//' + _0x06a5.group(1)
        _0x06a4 = _0x06a4[:_0x06a5.start()]
    _0x06a5 = _0x0160.search(_0x06a4)
    if _0x06a5:
        _0x06a2 = _0x06a5.group(1)
        _0x06a4 = _0x06a4[:_0x06a5.start()]
    _0x06a5 = _0x015e.search(_0x06a4)
    if _0x06a5:
        _0x06a3 = _0x06a5.group(1)
        _0x06a4 = _0x06a4[:_0x06a5.start()]
    _0x06a5 = _0x0161.search(_0x06a4)
    if _0x06a5:
        _0x06a3 = _0x06a5.group(1)
        _0x06a4 = _0x06a4[:_0x06a5.start()]
    return (_0x06a4.strip(), _0x06a3, _0x06a2, _0x06a1)

def _0x0173(_0x02ba: str, _0x02bb, _0x02bc, _0x02bd) -> str:
    _0x06a6 = _0x02ba
    if _0x02bc:
        _0x06a6 += f'({_0x02bc})'
    if _0x02bb:
        _0x06a6 += f' x{_0x02bb}'
    if _0x02bd:
        _0x06a6 += ' ' + _0x02bd
    return _0x06a6

def _0x0174(_0x02be: str, _0x02bf):
    _0x06a7 = _0x016f(_0x02be)
    if _0x06a7 < 0:
        return None
    _0x06a8 = _0x02be[:_0x06a7]
    _0x06a9 = _0x02be[_0x06a7 + 2:]
    _0x06aa = len(_0x06a9)
    _0x06ab = 0
    while _0x06ab < _0x06aa and _0x06a9[_0x06ab] in ' \t':
        _0x06ab += 1
    while _0x06ab < _0x06aa and _0x06a9[_0x06ab] == '/':
        _0x06ab += 1
    while _0x06ab < _0x06aa and _0x06a9[_0x06ab] in ' \t':
        _0x06ab += 1
    _0x06ac = _0x06ab < _0x06aa and _0x06a9[_0x06ab] == '"'
    _0x06ad = _0x06ab + 1 if _0x06ac else _0x06ab
    _0x06ae = _0x06aa
    while _0x06ae > _0x06ad and _0x06a9[_0x06ae - 1] in ' \t':
        _0x06ae -= 1
    _0x06af = _0x06ae > _0x06ad and _0x06a9[_0x06ae - 1] == '"'
    if _0x06af:
        _0x06ae -= 1
    _0x06b0 = _0x06a9[_0x06ad:_0x06ae]
    _0x06b1 = _0x0164.get(_0x06b0)
    if _0x06b1 is not None:
        _0x06b3 = _0x06b1
    else:
        (_0x06b4, _0x06b5, _0x06b6, _0x06b7) = _0x0172(_0x06b0)
        _0x06b8 = None
        if _0x02bf is not None and _0x06b4 and ('/' not in _0x06b4) and _0x015d.fullmatch(_0x06b4) and _0x015b.search(_0x06b4):
            _0x06b9 = _0x0171(_0x06a8)
            if _0x06b9 is not None:
                _0x06b8 = _0x0170(_0x02bf, _0x06b9)
        if _0x06b8:
            _0x06b3 = _0x0173(_0x06b8, _0x06b5, _0x06b6, _0x06b7)
        else:
            _0x06ba = _0x016c(_0x06b0)
            if _0x015b.search(_0x06ba):
                return None
            _0x06b3 = _0x06ba
    _0x06b2 = '"' if _0x06ac else ''
    _0x06b2 += _0x06b3
    if _0x06af:
        _0x06b2 += '"'
    return _0x02be[:_0x06a7] + '//' + _0x06a9[:_0x06ab] + _0x06b2

def _0x0175(_0x02c0: str, _0x02c1=None) -> str:
    global _0x0167
    if not _0x0167:
        _0x0169()
    if not _0x015c.search(_0x02c0):
        _0x06bb = _0x0164.get(_0x02c0)
        if _0x06bb is not None:
            return _0x06bb
        return _0x02c0
    if '//' in _0x02c0:
        _0x06bd = _0x0174(_0x02c0, _0x02c1)
        if _0x06bd is not None and (not _0x015c.search(_0x06bd)):
            return _0x06bd
    _0x06bb = _0x0164.get(_0x02c0)
    if _0x06bb is not None:
        return _0x06bb
    if '(' in _0x02c0 and _0x02c0.rstrip().endswith(');'):
        _0x06be = _0x0163.fullmatch(_0x02c0.strip()) or _0x0163.search(_0x02c0)
        if _0x06be and _0x015b.search(_0x06be.group(1)) and (not _0x015b.search(_0x02c0[:_0x06be.start()] + _0x02c0[_0x06be.end():])):
            _0x06bb = _0x0164.get(_0x06be.group(1))
            if _0x06bb is not None:
                return _0x02c0[:_0x06be.start()] + '"' + _0x06bb + '"' + _0x02c0[_0x06be.end():]
    _0x06bc = _0x016c(_0x02c0)
    if _0x015b.search(_0x06bc):
        _0x016a(_0x06bc)
    return _0x06bc


def _0x0176(_0x02c0: str) -> str:
    
    global _0x0167
    if not _0x0167:
        _0x0169()
    _0x06bb = _0x0164_rev.get(_0x02c0)
    if _0x06bb is not None:
        return _0x06bb
    return _0x02c0


def _0x0177(_0x02c0: str):
    
    global _0x0167
    if not _0x0167:
        _0x0169()
    return _0x0164_rev_bytes.get(_0x02c0)
