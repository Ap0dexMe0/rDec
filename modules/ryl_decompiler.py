import os as _0x0502
import re as _0x0503
import struct as _0x0504
from pathlib import Path as _0x0506
from modules import output
_0x00bc = 1112877484
_0x00bd = _0x0504.pack('<I', _0x00bc)
_0x00be = {'SetNPC': {6: (['i', 'i', 'i', 'b', 's', 's'], 0, 2)}, 'SetPosition': {5: (['i', 'f', 'f', 'f', 'f'], 1, 0)}, 'SetNPCAttribute': {3: (['i', 'i', 'i'], 1, 0)}, 'NPCDisplay': {5: (['i', 'i', 'b', 'b', 'b'], 1, 0)}, 'AddWords': {2: (['i', 's'], 1, 0)}, 'AddDialog': {4: (['i', 'i', 'i', 's'], 1, 0)}, 'AddItem': {5: (['i', 'i', 'i', 'i', 'i'], 1, 0)}, 'AddZoneMove': {5: (['i', 'i', 'f', 'f', 'f'], 1, 0)}, 'AddQuest': {2: (['i', 'i'], 1, 0)}, 'AddQuestWords': {3: (['i', 'i', 's'], 1, 0)}, 'AddPopup': {7: (['i', 'i', 'i', 's', 'i', 'i', 'i'], 1, 0)}, 'SetDropGrade': {7: (['i'] * 7, 1, 0)}, 'SetDropBase': {7: (['i'] * 7, 1, 0)}, 'QuestStart': {7: (['i', 'i', 'i', 'i', 'i', 'i', 'b'], 0, 0)}, 'QuestEnd': {0: ([], 0, 0)}, 'QuestType': {2: (['i', 'i'], 1, 0)}, 'QuestCompleteSave': {1: (['b'], 1, 0)}, 'QuestTitle': {1: (['s'], 1, 0)}, 'QuestLevel': {1: (['s'], 1, 0)}, 'QuestAward': {1: (['s'], 1, 0)}, 'QuestDesc': {1: (['s'], 1, 0)}, 'QuestShortDesc': {1: (['s'], 1, 0)}, 'QuestArea': {5: (['i', 'f', 'f', 'f', 'f'], 1, 0)}, 'QuestSkillPointBonus': {1: (['i'], 1, 0)}, 'QuestIcon': {5: (['s', 'i', 'i', 'i', 'i'], 1, 0)}, 'QuestCancelItemDel': {1: (['b'], 1, 0)}, 'AddPhase': {3: (['i', 'i', 's'], 1, 1)}, 'Phase_Target': {2: (['i', 'i'], 2, 0)}, 'Trigger_Start': {0: ([], 2, 0)}, 'Trigger_Puton': {6: (['i', 'i', 'f', 'f', 'f', 'f'], 2, 0)}, 'Trigger_Geton': {6: (['i', 'i', 'f', 'f', 'f', 'f'], 2, 0)}, 'Trigger_Talk': {1: (['i'], 2, 0)}, 'Trigger_Kill': {2: (['i', 'i'], 2, 0)}, 'Trigger_Pick': {2: (['i', 'i'], 2, 0)}, 'Trigger_Fame': {1: (['i'], 2, 0)}, 'Trigger_LevelTalk': {3: (['i', 'i', 's'], 2, 0)}, 'Else': {0: ([], 2, 0)}, 'Event_Disappear': {3: (['i', 'i', 'i'], 3, 0)}, 'Event_Get': {2: (['i', 'i'], 3, 0)}, 'Event_Spawn': {4: (['i', 'f', 'f', 'f'], 3, 0)}, 'Event_MonsterDrop': {2: (['i', 'i'], 3, 0)}, 'Event_Award': {4: (['i', 'i', 'i', 'i'], 3, 0)}, 'Event_MsgBox': {1: (['s'], 3, 0)}, 'Event_Phase': {1: (['i'], 3, 0)}, 'Event_End': {0: ([], 3, 0)}, 'Event_AwardItem': {4: (['i', 'i', 'i', 'i'], 3, 0)}, 'Event_AddQuest': {2: (['i', 'i'], 3, 0)}, 'Event_Move': {3: (['i', 'f', 'f'], 3, 0)}, 'Event_TheaterMode': {0: ([], 3, 0)}, 'RylNation': {3: (['i', 'i', 's'], 0, 0)}, 'AddString': {2: (['i', 's'], 0, 0), 1: (['s'], 0, 0)}}
def _0x00c1(_0x0232: str) -> str:
    return _0x0506(_0x0232).stem + '.txt'

def decode(_0x0233: bytes) -> bytes:
    _0x050a = bytes((_0x050f ^ _0x00bd[0] for _0x050f in _0x0233[0::4]))
    _0x050b = bytes((_0x0510 ^ _0x00bd[1] for _0x0510 in _0x0233[1::4]))
    _0x050c = bytes((_0x0511 ^ _0x00bd[2] for _0x0511 in _0x0233[2::4]))
    _0x050d = bytes((_0x0512 ^ _0x00bd[3] for _0x0512 in _0x0233[3::4]))
    _0x050e = bytearray(len(_0x0233))
    _0x050e[0::4] = _0x050a
    _0x050e[1::4] = _0x050b
    _0x050e[2::4] = _0x050c
    _0x050e[3::4] = _0x050d
    return bytes(_0x050e)

def _0x00c2(_0x0234: bytes) -> dict:
    (_0x0513, _0x0514, _0x0515) = _0x0504.unpack_from('<iii', _0x0234, 0)
    _0x0516 = 12
    _0x0517 = [_0x0504.unpack_from('<i', _0x0234, _0x0516 + 4 * _0x052b)[0] for _0x052b in range(_0x0513)]
    _0x0516 += 4 * _0x0513
    _0x0518 = [_0x0504.unpack_from('<i', _0x0234, _0x0516 + 4 * _0x052c)[0] for _0x052c in range(_0x0514)]
    _0x0516 += 4 * _0x0514
    _0x0519 = []
    for _0x051a in range(_0x0515):
        (_0x0525, _0x0526) = _0x0504.unpack_from('<ii', _0x0234, _0x0516 + 8 * _0x051a)
        _0x0519.append((_0x0525, _0x0526))
    _0x0516 += 8 * _0x0515
    (_0x051b, _0x051c, _0x051d) = _0x0504.unpack_from('<iii', _0x0234, _0x0516)
    _0x0516 += 12
    _0x051e = _0x0234[_0x0516:_0x0516 + _0x051c]
    _0x0516 += _0x051c
    _0x051f = _0x0234[_0x0516:_0x0516 + _0x051d]
    _0x0516 += _0x051d
    _0x0520 = _0x0504.unpack_from('<l', _0x0234, _0x0516)[0]
    _0x0516 += 4
    _0x0521 = {}
    _0x0522 = []
    for _ in range(_0x0520):
        _0x0527 = _0x0234.index(b'\n', _0x0516)
        _0x0528 = _0x0234[_0x0516:_0x0527].decode('ascii')
        _0x0516 = _0x0527 + 1
        (_0x0529, _0x052a) = _0x0504.unpack_from('<ll', _0x0234, _0x0516)
        _0x0516 += 8
        _0x0521.setdefault(_0x052a, []).append(_0x0528)
        _0x0522.append((_0x052a, _0x0529, _0x0528))
    _0x0524 = _0x0504.unpack_from('<iiii', _0x0234, _0x0516)
    _0x0516 += 16
    return {'glo': _0x0517, 'srel': set(_0x0518), 'frel': _0x0519, 'gv': _0x051b, 'strbuf': _0x051e, 'code': _0x051f, 'funcmap': _0x0521, 'fmap_entries': _0x0522, 'sysvars': _0x0524, 'consumed': _0x0516, 'total': len(_0x0234)}

def _0x00c3(_0x0235: int) -> str:
    if _0x0235 >= 1048576:
        return f'0x{_0x0235:X}'
    return str(_0x0235)

def _0x00c4(_0x0236: int) -> str:
    _0x052d = _0x0504.unpack('<f', _0x0504.pack('<I', _0x0236))[0]
    for _0x052e in range(0, 12):
        _0x052f = ('%.*f' % (_0x052e, _0x052d)).rstrip('0').rstrip('.')
        if _0x052f in ('-0', '', '-'):
            _0x052f = '0'
        try:
            if _0x0504.unpack('<I', _0x0504.pack('<f', float(_0x052f)))[0] == _0x0236:
                return _0x052f
        except OverflowError:
            pass
    return repr(float(_0x052d))
_0x00c5 = _0x0503.compile('[\\uac00-\\ud7a3\\u3130-\\u318f\\u3018-\\u301f\\u3008-\\u300b]')
_0x00c6 = _0x0503.compile('[—‘’“”‥‰′″←-↓∀-⋿①-⑳─-╿■-◿【】\u3000]')
_0x00c7 = _0x0503.compile('[\\x00-\\x08\\x0b\\x0c\\x0e-\\x1f\\x7f]')
_0x00c8 = frozenset('們個時這點實現動隊讓開說話對發問還沒過處應該為後辦買賣裝備經驗職業戰騎師會聖導錘項鍊藥遠視範圍頭體腳條記簽驗任務獲錄線連錯誤請輸帳號碼選取消確關閉視窗按指示伺服器登密創立角色姓別寶箱賞紀幫訊息物品介切換拖曳點擊憂餘效果持續耗損怒恢復速移穿負重修復率爆擊種類臺灣式長權驅除員樣已儲啟煉申組空間答藝都不膽怯勇婦如果穿梭蘑菇森林垂釣名從南訪遠維珂隆族譜所歷王國遷移民建立大陸特開拓基本活努力變種少始威脅擴領當耐磨久需智運迴致傷祈功廢鐵喔終堂正士雛鳥獨面目前雞為了要內忠誠兵槍砲冒歡離敗礦蘊藏發現挑戰學習調樓層隨機等級裝飾置態區域圖傳送檢查方形圓形三角條件結算是誰找尋劇情噢注哦快鬼魂覺警衝雙單軍弓榴彈藥火焰冰雷毒課益城鎮村莊巡荒野門研究界技命擋數能不丟落到地上道幾打提煉嗎電梯明深度寬高重間結單位量取捨最值以及將與使用可以透過力量敏捷幸運盾牌魔杖武器頭盔飾品叫賣收購通關獎勵擊殺目標得到經驗值與金錢求排列位置視野半徑生效場合無法其他怪物攻防具備強化附屬屬性死後重生週期十五秒半分鐘聚會會長幹部首領成員報名參現在開放開始把關卡四周傳遞送來源方向目標距離時麵佈告欄捕捉殺掉灰石精密寶石屬於函數釣魚')
_0x00c9 = frozenset('们个时点实现队让开说话对发问还没过处应该为后办买卖装备经验职业战骑师会圣导锤项链药远视范围头体脚条记签验任务获录线连错误请输帐号码选取消确认关闭视窗按指示服务器登密创立角色性别宝箱赏纪帮讯息物品界面切换拖曳点击忧余果持续耗损怒恢复速移动穿负重修复率爆击码种类台湾正式长权驱除员样已经话储启动炼申请组空间答艺都不胆怯勇妇如果穿梭蘑菇森林垂钓名从南访远维珂隆族谱所历史王国迁移民建立大陆特开拓基本生活努力变种少始威胁扩领土当耐磨久需智运回致伤祈祷功废铁喔终堂正战士雏鸟独面目前鸡为了要内忠诚兵枪炮冒欢离败矿蕴藏发现挑战学习调楼层随机等级装饰置态区域图传送检查方形圆形三角条件结算是谁找寻剧情噢注哦快鬼魂觉警冲双单军弓榴弹药火焰冰雷毒课益城镇村庄巡荒野门研究界技命挡数能不丢落到地上道具几打提炼吗电梯明深度宽高重间结单位量取舍最值以及将与使用可以透过力量敏捷幸运盾牌魔杖武器头盔饰叫收购通关奖励击杀目标得到经验值与金钱求排列位置视野半径生效场合无法其他怪物攻防具备强化附属属性死后重生周期十五秒半分钟聚会会长干部首领成员报名参现在开放开始把关卡四周递送来源方向目标距离时')
_0x00ca = frozenset('한다은을를에의와과이가로그리고있없않여서명면지한해주것니말함검계속제일위장물품상태템사용선택취소확동의거래작업완료실패성공회복경치증가감소시간단추속도이동공격방어력마력확률강화보정고블린거인위치좌표존아디이름몬스터엔피시퀘트트립대화상자팝업문자열포인트보상금명성아템개수등급제한밸직전사도적법사마성직칸휴먼종족국가버스데이직구매월드콘버튼클릭창온라인확인안녕환영감사합니다민국힘벨노가정작업완성체이닝먼응즈으금은동철광석보석종이가죽각귀집요')
_0x00cb = frozenset('…—‘’“”·‼‰℃ⓘ㉑㉒㉓㉔㉕¶†‡§℃')
_0x00cc = 0.18
_0x00cd = 0.1

def _0x00ce() -> str:
    _0x0530 = _0x0502.environ.get('RDEC_LANG', '').strip().lower()
    return _0x0530 if _0x0530 in ('kor', 'chs', 'cht') else 'auto'

def _0x00cf(_0x0237: str) -> bool:
    _0x0531 = ord(_0x0237)
    return 12288 <= _0x0531 <= 12351 or 13312 <= _0x0531 <= 40959 or 63744 <= _0x0531 <= 64255 or (65280 <= _0x0531 <= 65519) or (_0x0531 in (169, 174, 176, 215, 8226, 65533))

def _0x00d0(_0x0238: str) -> bool:
    return all((ord(_0x0532) <= 127 or _0x00cf(_0x0532) or _0x0532 in _0x00cb for _0x0532 in _0x0238))

def _0x00d1(_0x0239: str) -> bool:
    return all((ord(_0x0533) <= 127 or _0x00c5.match(_0x0533) or _0x00c6.match(_0x0533) or (_0x0533 == '�') for _0x0533 in _0x0239))

def _0x00d2(_0x023a: str, _0x023b) -> float:
    _0x0534 = [_0x0535 for _0x0535 in _0x023a if 13312 <= ord(_0x0535) <= 40959 or 63744 <= ord(_0x0535) <= 64255]
    if not _0x0534:
        return 0.0
    return sum((_0x0536 in _0x023b for _0x0536 in _0x0534)) / len(_0x0534)

def _0x00d3(_0x023c: str, _0x023d) -> float:
    _0x0537 = [_0x0538 for _0x0538 in _0x023c if _0x00c5.match(_0x0538)]
    if not _0x0537:
        return 0.0
    return sum((_0x0539 in _0x023d for _0x0539 in _0x0537)) / len(_0x0537)

def _0x00d4(_0x023e: bytes, _0x023f: str) -> list:
    
    _0x053a = []
    _0x053b = {'chs': ('cp936',), 'cht': ('big5',)}.get(_0x023f, ('big5', 'cp936'))
    if _0x023f != 'kor':
        for _0x053d in _0x053b:
            _0x0540 = _0x00c8 if _0x053d == 'big5' else _0x00c9
            _0x0541 = _0x00d5(_0x023e, _0x053d)
            if _0x0541 is None:
                continue
            (_0x053e, _0x053f) = _0x0541
            if _0x00d0(_0x053e):
                _0x053a.append((_0x053d, _0x053e, _0x00d2(_0x053e, _0x0540) * _0x053f))
    _0x053c = None
    for _0x053d in ('euc-kr', 'cp949'):
        (_0x053e, _0x053f) = _0x00d5(_0x023e, _0x053d, _0x0242=False)
        if _0x053e is None:
            continue
        if _0x00d1(_0x053e):
            _0x0542 = _0x00d3(_0x053e, _0x00ca)
            if len(_0x053a) == 0 or _0x023f == 'kor':
                _0x0542 = max(_0x0542, _0x00cd)
            _0x053c = (_0x053d, _0x053e, _0x0542 * _0x053f)
            break
        (_0x053e, _0x053f) = _0x00d5(_0x023e, _0x053d, _0x0242=True)
        if _0x053e is not None and _0x00d1(_0x053e):
            _0x0542 = _0x00d3(_0x053e, _0x00ca) * _0x053f
            if len(_0x053a) == 0 and _0x053d == 'euc-kr':
                _0x0542 = max(_0x0542, _0x00cd * _0x053f)
            _0x053c = (_0x053d, _0x053e, _0x0542)
            break
    if _0x053c is not None:
        _0x053a.append(_0x053c)
    return _0x053a

def _0x00d5(_0x0240: bytes, _0x0241: str, _0x0242: bool=True):
    
    try:
        return (_0x0240.decode(_0x0241), 1.0)
    except UnicodeDecodeError:
        if not _0x0242:
            return (None, 0.0)
    return (_0x0240.decode(_0x0241, errors='replace'), 0.4)

def _0x00d6(_0x0243: bytes) -> str:
    
    if _0x0243.isascii():
        return _0x0243.decode('ascii')
    try:
        return _0x0243.decode('utf-8')
    except UnicodeDecodeError:
        pass
    _0x0543 = _0x00ce()
    _0x0544 = _0x00d4(_0x0243, _0x0543)
    _0x0545 = max(_0x0544, key=lambda _0x0230: _0x0230[2], default=None)
    if _0x0545 is not None and _0x0545[2] >= _0x00cc:
        return _0x0545[1]
    if _0x0545 is not None and _0x0543 == 'kor':
        return _0x0545[1]
    _0x0546 = [_0x0547 for _0x0547 in _0x0544 if _0x0547[0] in ('big5', 'cp936')]
    if _0x0546:
        return max(_0x0546, key=lambda _0x0230: _0x0230[2])[1]
    try:
        return _0x0243.decode('cp1252')
    except UnicodeDecodeError:
        return _0x0243.decode('latin-1')

def _0x00d7(_0x0244: str) -> str:
    _0x0244 = _0x00c7.sub('', _0x0244)
    for (_0x0548, _0x0549) in (('‘', "'"), ('’', "'"), ('“', '"'), ('”', '"'), ('„', '"'), ('…', '...'), ('‥', '..'), ('—', '-'), ('–', '-'), ('‚', ','), ('•', '*'), ('\xa0', ' '), ('\u3000', ' ')):
        _0x0244 = _0x0244.replace(_0x0548, _0x0549)
    return _0x0244

def _0x00d9(_0x0246: str) -> str:
    from modules.translations import _0x0175 as _0x0175
    _0x054a = _0x0175(_0x00d7(_0x0246))
    return _0x054a.replace('\t', '    ').replace('\r\n', '\\n').replace('\n', '\\n')

def _0x00da(_0x0247: bytes) -> bytes:
    _0x054b = bytearray()
    (_0x054c, _0x054d) = (0, len(_0x0247))
    while _0x054c < _0x054d:
        _0x054e = _0x0247[_0x054c]
        if _0x054e >= 129 and _0x054c + 1 < _0x054d:
            try:
                _0x054f = _0x0247[_0x054c:_0x054c + 2].decode('cp949')
            except UnicodeDecodeError:
                _0x054f = None
            if _0x054f is not None and _0x054f.encode('cp949') == _0x0247[_0x054c:_0x054c + 2]:
                _0x054b += _0x054f.encode('utf-8')
                _0x054c += 2
                continue
        if 32 <= _0x054e < 127 and _0x054e not in (34, 92):
            _0x054b += bytes((_0x054e,))
        elif _0x054e == 92:
            _0x054b += b'\\\\'
        else:
            _0x054b += f'\\x{_0x054e:02X}'.encode('ascii')
        _0x054c += 1
    return b'"' + bytes(_0x054b) + b'"'

def _0x00db(_0x0248: dict=None) -> dict:
    
    _0x0550 = {**_0x00be}
    for (_0x0551, _0x0552) in (_0x0248 or {}).items():
        _0x0550[_0x0551] = {**_0x0550.get(_0x0551, {}), **_0x0552}
    return _0x0550

def _0x00dc(_0x0249: bytes, _0x024a: dict, _0x024b: bytes, _0x024c: set, _0x024d: dict=None):
    _0x0553 = _0x00db(_0x024d) if _0x024d else _0x00be
    _0x0554 = []
    _0x0555 = []
    _0x0556 = set(_0x024a)
    _0x0557 = len(_0x0249)
    for _0x0558 in range(_0x0557):
        if _0x0249[_0x0558] != 232 or _0x0558 + 5 > _0x0557:
            continue
        _0x0559 = _0x0504.unpack_from('<i', _0x0249, _0x0558 + 1)[0]
        _0x055a = _0x0558 + 5 + _0x0559
        if _0x055a not in _0x0556:
            continue
        _0x055b = []
        _0x055c = _0x0558
        while _0x055c - 6 >= 0 and _0x0249[_0x055c - 1] == 81 and (_0x0249[_0x055c - 6] == 185) and (len(_0x055b) < 8):
            _0x055b.append(_0x0504.unpack_from('<I', _0x0249, _0x055c - 5)[0])
            _0x055c -= 6
        _0x055b.reverse()
        _0x055d = _0x0558 + 11 <= _0x0557 and _0x0249[_0x0558 + 5] == 129 and (_0x0249[_0x0558 + 6] == 196) and (_0x0504.unpack_from('<I', _0x0249, _0x0558 + 7)[0] == 4 * len(_0x055b))
        _0x055e = _0x024a[_0x055a]
        _0x055f = [_0x0560 for _0x0560 in _0x055e if len(_0x055b) in _0x0553.get(_0x0560, {})]
        if len(_0x055f) != 1:
            _0x0555.append((_0x0558, _0x055a, _0x055e, _0x055b))
            continue
        if not _0x055d:
            _0x0555.append((_0x0558, _0x055a, _0x055e, _0x055b, 'esp'))
            continue
        _0x0554.append((_0x0558, _0x055f[0], _0x055b))
    _0x0554.sort()
    return (_0x0554, _0x0555)

def _0x00dd(_0x024e: str, _0x024f: int, _0x0250: bytes, _0x0251: list, _0x0252: str):
    if _0x024e == 's':
        if _0x024f >= len(_0x0250):
            _0x0251.append((_0x0252, 'stroff', _0x024f))
            return b'""'
        _0x0562 = _0x0250.index(b'\x00', _0x024f)
        return _0x00da(_0x0250[_0x024f:_0x0562])
    if _0x024e == 'b':
        if _0x024f not in (0, 1):
            _0x0251.append((_0x0252, 'bool', _0x024f))
        return b'true' if _0x024f else b'false'
    if _0x024e == 'f':
        return _0x00c4(_0x024f).encode('ascii')
    _0x0561 = _0x024f if _0x024f < 2147483648 else _0x024f - 4294967296
    return _0x00c3(_0x0561).encode('ascii')

def _0x00de(_0x0253: _0x0506, _0x0254: bytes=None, _0x0255: dict=None):
    _0x0563 = _0x0253.read_bytes()
    output.detail(f'{_0x0253.name}: read {len(_0x0563):,} bytes.')
    if _0x0254 is None:
        _0x0254 = decode(_0x0563)
    _0x0564 = _0x00c2(_0x0254)
    output.detail(f"{_0x0253.name}: decoded into {len(_0x0564['code']):,} code bytes, {len(_0x0564['funcmap'])} functions and {len(_0x0564['strbuf']):,} string bytes.")
    (_0x0565, _0x0566) = _0x00dc(_0x0564['code'], _0x0564['funcmap'], _0x0564['strbuf'], _0x0564['srel'], _0x0255)
    _0x0567 = _0x00db(_0x0255) if _0x0255 else _0x00be
    _0x0568 = []
    _0x0569 = True
    _0x056a = []
    for (_0x056b, _0x056c, _0x056d) in _0x0565:
        (_0x0572, _0x0573, _0x0574) = _0x0567[_0x056c][len(_0x056d)]
        if not _0x0569:
            if _0x056c == 'SetNPC':
                _0x0568.extend([b''] * 2)
            elif _0x0574:
                _0x0568.extend([b''] * _0x0574)
        _0x0575 = []
        for (_0x0576, _0x0577) in zip(_0x0572, _0x056d):
            _0x0575.append(_0x00dd(_0x0576, _0x0577, _0x0564['strbuf'], _0x056a, f'{_0x056c}@{_0x056b}'))
        _0x0568.append(b'\t' * _0x0573 + f'{_0x056c}('.encode('ascii') + b', '.join(_0x0575) + b');')
        _0x0569 = False
        if _0x056c == 'QuestEnd':
            _0x0568.extend([b'', b''])
    while _0x0568 and _0x0568[-1] == b'':
        _0x0568.pop()
    output.detail(f'{_0x0253.name}: recovered {len(_0x0565):,} calls with {len(_0x0566)} call anomalies and {len(_0x056a)} argument anomalies.')
    from modules.banners import _0x000e as _0x000e
    _0x056e = [_0x0578.encode('ascii') for _0x0578 in _0x000e()]
    _0x056e.append(b'// rDec-Schema: mcf')
    _0x056e.append(b'')
    for (_0x056f, _0x0570, _0x0571) in _0x0564['fmap_entries']:
        _0x056e.append(f';Stub {_0x0571} {_0x0570} {_0x056f}'.encode('ascii'))
    _0x056e.append(b'')
    _0x056e.extend(_0x0568)
    return (b'\r\n'.join(_0x056e), _0x0564, _0x0565, _0x0566, _0x056a)

from collections import Counter as _0x058d
_0x0036 = _0x0506(__file__).parent
_0x00e0 = None

def _0x00e1():
    global _0x00e0
    if _0x00e0 is None:
        from modules.xor_crypt import _0x017a as _0x017a, _0x0176 as _0x0176, _0x0014 as _0x0014
        _0x00e0 = {(_0x058f, _0x0590): list(_0x017a(_0x058f, _0x0590)) for _0x058f in range(_0x0014) for _0x0590 in range(_0x0176)}
    return _0x00e0
_0x00e2 = {'ItemScript.gsf': (0, 2), 'Chemical.gsf': (0, 2), 'MonsterProtoType.gsf': (0, 3), 'SkillScript.gsf': (0, 1), 'Script1.gsf': (0, 1), 'Abuse.gsf': (0, 1), 'SpeacialCompensation.gsf': (0, 2)}

def _0x00e3(_0x0257: str) -> str:
    return _0x0506(_0x0257).stem + '.txt'
_0x00e4 = {}

def _0x00e5(_0x0258: str):
    
    _0x0591 = _0x0506(_0x0258).name.lower()
    if _0x0591 == 'itemscript.gsf':
        _0x0592 = (0, 2)
    elif _0x0591 == 'chemical.gsf':
        _0x0592 = (0, 2)
    elif _0x0591 == 'monsterprototype.gsf':
        _0x0592 = (0, 3)
    elif _0x0591 == 'skillscript.gsf':
        _0x0592 = (0, 1)
    elif _0x0591 in ('script1.gsf', 'abuse.gsf'):
        _0x0592 = (0, 1)
    elif _0x0591 == 'speacialcompensation.gsf':
        _0x0592 = (0, 2)
    elif _0x0591.startswith('mineralvein') and _0x0591.endswith('.gsf'):
        _0x0592 = (0, 3)
    else:
        return None
    return _0x0592

def _0x00e6(_0x0259, _0x025a=None) -> dict:
    
    for _0x0593 in _0x0259:
        if _0x0506(_0x0593).name.lower() == 'itemscript.gsf':
            if _0x025a == 'RYL1':
                return _0x0142(_0x00fd(_0x0506(_0x0593)))
            return _0x014a(_0x00fd(_0x0506(_0x0593)))
    for _0x0593 in _0x0259:
        _0x0594 = _0x0506(_0x0593)
        try:
            _0x0596 = _0x00fc(_0x0594.read_bytes(), _0x0594.name)
        except Exception:
            continue
        for _0x0595 in _0x00fe(_0x0594.name):
            _0x0597 = _0x00fb(_0x0596, _0x0595)
            if _0x00ed(_0x0597):
                return _0x014a(_0x0597)
            if _0x025a == 'RYL1' and _0x00f3(_0x0597):
                return _0x0142(_0x0597)
    return {}
_0x00e7 = b'??Monster Chat Script ??'
_0x00e8 = b'void MonsterChat(int, int, int, int, int, string); // KID, ?????'
_0x00e9 = ('void MonsterChat(int, int, int, int, int, string); // KID, MonsterAction, Monster SkillsID, Chattingtypes, Probability, ChattingMessage', '', '//////\tChattingtypes ID\t//////////', '//\t\t\t\t\t//', '//\tGeneral attack\t\t\t\t=0\t//', '//\tWhen getting attacked by general attack\t=1\t//', '//\tWhen attacking with skill attack\t\t=2\t//', '//\tWhen getting attacked by skill attack\t=3\t//', '//\tWhen attacking with crit attack\t\t=4\t//', '//\tWhen getting attacked by crit attack\t=5\t//', '//\tLisphone\t\t\t\t\t=6\t//', '//\tDeath\t\t\t\t\t\t=7\t//', '//\t\t\t\t\t//', '//////////////////////////', '', '//////\tChattingtypes ID\t//////', '//\t\t\t\t//', '//\tCommon Knowledge\t=255\t//', '//\tGeneral\t\t\t\t=0\t\t//', '//\tScreaming\t\t\t=7\t\t//', '//\t\t\t\t//', '///////////////////////', '', '////\tSkill ID\t//////', '//\t\t\t\t\t//', '//\tAll Skill\t=0xFFFF\t//', '//\t\t\t\t\t//', '//////////////////////////', '', "// $KILLERNAME$\tSubstitute with killer(player) name. It's only possible when Action ID matches number 7 (death).", "// $ATTNAME$\t\tSubstitute with hitter(player) name. It's only possible when Action ID matches number 1, 3, 5 (when the monster got hit).", "// $DEFNAME$\t\tSubstitute with the player name who got hit by the monster. It's only possible when Action ID matches number 0, 2, 4 (when the monster hits) (When two or more exist, chosen at random).", '', '// KID, Monster Action, Monster skill ID. When the chatting kinds are the same kind, the probability is calculated by adding them together.', '', '// ex ', '//MonsterChat(4001, 2, 0xFFFF, 0, 20, "Monster chat example text 1");', '//MonsterChat(4001, 2, 0xFFFF, 0, 20, "Monster chat example text 2");', '// (A random number is chosen from 1~100: the first message is covered by 1~20, the second by 21~40. Other numbers say nothing.) ', '', '// Note: this header was reconstructed in English - the original notes were lost to text corruption in the source binary.')

def _0x00ea(_0x025b: bytes) -> bytes:
    if _0x00e7 in _0x025b:
        _0x025b = _0x025b.replace(_0x00e7, b'Monster Chat Script')
    if not _0x025b.startswith(_0x00e8):
        return _0x025b
    _0x0598 = _0x025b.split(b'\r\n')
    _0x0599 = None
    for (_0x059a, _0x059b) in enumerate(_0x0598):
        if b'Named Monster-Boss' in _0x059b:
            _0x0599 = _0x059a - 1
            break
    if _0x0599 is None:
        return _0x025b
    _0x059c = [_0x059d.encode('utf-8') for _0x059d in _0x00e9]
    _0x059c += [b'', b'']
    return b'\r\n'.join(_0x059c) + b'\r\n'.join(_0x0598[_0x0599:])
_0x009e = frozenset(range(1, 43)) | {69, 70}

def _0x00ec(_0x025c: bytes, _0x025d: bool=False) -> bool:
    
    _0x059e = _0x025c.split(b'\x00')[0]
    if len(_0x025c) > 1 and 0 not in _0x025c:
        return False
    if _0x025d and any((_0x059f < 32 or _0x059f == 127 for _0x059f in _0x059e)):
        return False
    return True

def _0x00ed(_0x025e: bytes) -> bool:
    _0x05a0 = 616
    if not _0x025e or len(_0x025e) % _0x05a0:
        return False
    for _0x05a1 in range(len(_0x025e) // _0x05a0):
        _0x05a2 = _0x025e[_0x05a1 * _0x05a0:(_0x05a1 + 1) * _0x05a0]
        if _0x05a2[21] > 127:
            return False
        for (_0x05a3, _0x05a4) in ((52, 116), (116, 148), (156, 188), (188, 220), (220, 252)):
            if not _0x00ec(_0x05a2[_0x05a3:_0x05a4]):
                return False
    return True

def _0x00ee(_0x025f: bytes) -> bool:
    _0x05a5 = 552
    if not _0x025f or len(_0x025f) % _0x05a5:
        return False
    _0x05a6 = set()
    for _0x05a7 in range(len(_0x025f) // _0x05a5):
        _0x05a8 = _0x025f[_0x05a7 * _0x05a5:(_0x05a7 + 1) * _0x05a5]
        if not _0x00ec(_0x05a8[64:128], _0x025d=True):
            return False
        if not _0x00ec(_0x05a8[128:160]):
            return False
        _0x05a9 = _0x0504.unpack_from('<H', _0x05a8, 348)[0]
        if _0x05a9 in _0x05a6:
            return False
        _0x05a6.add(_0x05a9)
    return True

def _0x00ef(_0x0260: bytes) -> bool:
    if not _0x0260 or len(_0x0260) % 2580:
        return False
    _0x05aa = {}
    for _0x05ab in range(len(_0x0260) // 2580):
        for _0x05ac in range(5):
            _0x05ad = _0x0260[_0x05ab * 2580 + _0x05ac * 516:_0x05ab * 2580 + (_0x05ac + 1) * 516]
            _0x05ae = _0x0504.unpack_from('<H', _0x05ad, 472)[0]
            if _0x05ae == 0:
                continue
            _0x05aa[_0x05ae] = _0x05aa.get(_0x05ae, 0) + 1
            if _0x05aa[_0x05ae] > 5:
                return False
            if not _0x00ec(_0x05ad[96:160], _0x025d=True):
                return False
            if _0x0504.unpack_from('<I', _0x05ad, 456)[0] > 65535:
                return False
    return bool(_0x05aa)

def _0x00f0(_0x0261: bytes) -> bool:
    if not _0x0261 or len(_0x0261) % 10:
        return False
    _0x05af = 0
    for _0x05b0 in range(0, len(_0x0261), 10):
        _0x05b1 = _0x0261[_0x05b0:_0x05b0 + 10]
        if _0x05b1[9]:
            return False
        if any(_0x05b1[0:6]):
            _0x05af += 1
    return _0x05af > 0

def _0x00f1(_0x0262: bytes) -> bool:
    if not _0x0262 or len(_0x0262) % 15:
        return False
    for _0x05b2 in range(0, len(_0x0262), 15):
        _0x05b3 = _0x0262[_0x05b2:_0x05b2 + 15].split(b'\x00')[0]
        if any((_0x05b4 < 32 or _0x05b4 == 127 for _0x05b4 in _0x05b3)):
            return False
    return True

def _0x00f2(_0x0263: bytes) -> bool:
    if len(_0x0263) < 4 or len(_0x0263) % 2 or _0x0263[-2:] != b'\x00\x00':
        return False
    _0x05b5 = 1
    for _0x05b6 in range(0, len(_0x0263) - 1, 2):
        if _0x0263[_0x05b6] == 0 and _0x0263[_0x05b6 + 1] == 0:
            _0x05b5 += 1
    return _0x05b5 >= 69

def _0x00f3(_0x0264: bytes) -> bool:
    _0x05b7 = 644
    if not _0x0264 or len(_0x0264) % _0x05b7:
        return False
    for _0x05b8 in range(len(_0x0264) // _0x05b7):
        _0x05b9 = _0x0264[_0x05b8 * _0x05b7:(_0x05b8 + 1) * _0x05b7]
        if _0x05b9[4] > 127:
            return False
        for (_0x05ba, _0x05bb) in ((60, 124), (124, 156), (164, 196), (196, 228)):
            if not _0x00ec(_0x05b9[_0x05ba:_0x05bb]):
                return False
    return True

def _0x00f4(_0x0265: bytes) -> bool:
    _0x05bc = 368
    if not _0x0265 or len(_0x0265) % _0x05bc:
        return False
    for _0x05bd in range(len(_0x0265) // _0x05bc):
        _0x05be = _0x0265[_0x05bd * _0x05bc:(_0x05bd + 1) * _0x05bc]
        if not _0x00ec(_0x05be[64:96], _0x025d=True):
            return False
        if not _0x00ec(_0x05be[96:128]):
            return False
    return True

def _0x00f5(_0x0266: bytes, _0x0267=None) -> str:
    
    if _0x0267 == 'RYL1':
        for (_0x05bf, _0x05c0) in (('ryl1-item', _0x00f3), ('ryl1-monster', _0x00f4), ('chemical', _0x00f0), ('speacialcompensation', _0x00f2), ('mineralvein', _0x0150)):
            try:
                if _0x05c0(_0x0266):
                    return _0x05bf
            except Exception:
                pass
        return None
    for (_0x05bf, _0x05c0) in (('mineralvein', _0x0150), ('itemscript', _0x00ed), ('monsterprototype', _0x00ee), ('skillscript', _0x00ef), ('chemical', _0x00f0), ('abuse', _0x00f1), ('speacialcompensation', _0x00f2)):
        try:
            if _0x05c0(_0x0266):
                return _0x05bf
        except Exception:
            pass
    return None

def _0x00f6(_0x0268: str, _0x0269: bytes, _0x026a=None):
    
    _0x05c1 = _0x00fc(_0x0269, _0x0268)
    for _0x05c2 in _0x00fe(_0x0268):
        _0x05c3 = _0x00fb(_0x05c1, _0x05c2)
        _0x05c4 = _0x00f5(_0x05c3, _0x026a)
        if _0x05c4:
            output.detail(f'{_0x0268}: schema {_0x05c4} on crypt page {_0x05c2[0]},{_0x05c2[1]}.')
            return (_0x05c2, _0x05c3, _0x05c4)
    raise ValueError(f"{_0x0268}: the GSF payload decrypted on no crypt page into a known schema (tried {', '.join((f'{_0x05c5},{_0x05c6}' for (_0x05c5, _0x05c6) in _0x00fe(_0x0268)))}).")

def _0x00f7(_0x026b: bytes, _0x026c: str) -> bool:
    try:
        _0x00fc(_0x026b, _0x026c)
        return True
    except Exception:
        return False

def _0x00f8(_0x026d: bytes) -> bool:
    
    return all((_0x05c7 >= 32 or _0x05c7 in (0, 9, 10, 13) for _0x05c7 in _0x026d))

def _0x00f9(_0x026e: _0x0506) -> bytes:
    
    import shutil as _0x05c8
    import subprocess as _0x05c9
    import tempfile as _0x05ca
    _0x05cb = _0x0036 / 'unluac.jar'
    if not (_0x05c8.which('java') and _0x05cb.exists()):
        raise RuntimeError('SKIP: needs java + modules/unluac.jar')
    output.detail(f'{_0x026e.name}: decompiling Lua bytecode with unluac.')
    with _0x05ca.TemporaryDirectory() as _0x05cc:
        _0x05cd = _0x0506(_0x05cc) / 'SkillScriptEx.txt'
        _0x05ce = _0x05c9.run(['java', '-jar', str(_0x05cb), str(_0x026e), '-o', str(_0x05cd)], capture_output=True, text=True)
        if _0x05ce.returncode != 0 or not _0x05cd.exists():
            raise RuntimeError(f"unluac failed: {(_0x05ce.stderr or '')[:200]}")
        _0x05cf = _0x05cd.read_bytes()
        output.detail(f'{_0x026e.name}: unluac returned {len(_0x05cf):,} bytes.')
        return _0x05cf

def _0x00fa(_0x026f: _0x0506, _0x0270: dict, _0x0271=None) -> bytes:
    
    _0x026f = _0x0506(_0x026f)
    _0x05d0 = _0x026f.read_bytes()
    if _0x05d0[:3] in (b'\x1bLu', b'\x1bLJ'):
        return _0x014b(_0x00f9(_0x026f), _0x004d(_0x05d0), _0x029e=['rDec-Schema: skillscriptex'])
    if not _0x00f7(_0x05d0, _0x026f.name):
        if _0x00f8(_0x05d0):
            _0x05da = _0x00ea(_0x05d0) if _0x0271 == 'RYL1' else _0x05d0
            output.detail(f'{_0x026f.name}: passing through {len(_0x05da):,} plaintext script bytes (monsterchat).')
            from modules.translations import _0x0175 as _0x0175, _vn_decode as _vn_decode
            _0x05db = _vn_decode(_0x05da)
            _0x05dc = _0x05db.split('\n')
            _0x05dd = []
            for _0x05de in _0x05dc:
                _0x05df = ''
                if _0x05de.endswith('\r'):
                    _0x05df = '\r'
                    _0x05de = _0x05de[:-1]
                _0x05dd.append(_0x0175(_0x05de) + _0x05df)
            _0x05da = '\n'.join(_0x05dd).encode('utf-8')
            return _0x014b(_0x05da, _0x004d(_0x05da), _0x029e=['rDec-Schema: monsterchat'])
        raise ValueError(f'{_0x026f.name}: unrecognized GSF payload (no envelope and not a plaintext script).')
    (_0x05d1, _0x05d2, _0x05d3) = _0x00f6(_0x026f.name, _0x05d0, _0x0271)
    _0x05d4 = [f'rDec-Schema: {_0x05d3}']
    if _0x05d1 is not None:
        _0x05d4.append(f'rDec-Crypt: {_0x05d1[0]},{_0x05d1[1]}')
    if _0x05d3 == 'ryl1-item':
        return _0x014b(_0x0141(_0x05d2), b'\n', _0x05d4)
    if _0x05d3 == 'ryl1-monster':
        return _0x014b(_0x0147(_0x05d2), b'\n', _0x05d4)
    if _0x05d3 == 'itemscript':
        (_0x05d5, _0x05d6) = (616, len(_0x05d2) // 616)
        output.detail(f'{_0x026f.name}: {_0x05d6:,} item rows.')
        _0x05d7 = ['\t'.join(_0x0128)]
        for _0x05d8 in range(_0x05d6):
            _0x05d7.append('\t'.join(_0x0127(_0x05d2[_0x05d8 * _0x05d5:(_0x05d8 + 1) * _0x05d5])))
        return _0x014b(('\n'.join(_0x05d7) + '\n').encode('utf-8'), b'\n', _0x05d4)
    if _0x05d3 == 'monsterprototype':
        (_0x05d5, _0x05d6) = (552, len(_0x05d2) // 552)
        output.detail(f'{_0x026f.name}: {_0x05d6:,} monster rows.')
        _0x05d9 = any((not _0x012d(_0x0504.unpack_from('<I', _0x05d2, _0x05db * _0x05d5 + _0x05dc)[0]) for _0x05db in range(_0x05d6) for _0x05dc in (4, 20)))
        if _0x05d9:
            output.detail(f'{_0x026f.name}: raw-f32 velocities (unreachable by the f32(x)*0.01f chain) - txt tagged raw.')
        _0x05d7 = ['// MonsterVelocity: raw-f32'] if _0x05d9 else []
        _0x05d7.extend(('\t'.join(_0x012e(_0x05d2[_0x05dd * _0x05d5:(_0x05dd + 1) * _0x05d5], _0x05d9)) for _0x05dd in range(_0x05d6)))
        return _0x014b(('\r\n'.join(_0x05d7) + '\r\n').encode('utf-8'), b'\r\n', _0x05d4)
    if _0x05d3 == 'skillscript':
        return _0x014b(_0x0137(_0x05d2), b'\r\n', _0x05d4)
    if _0x05d3 == 'chemical':
        return _0x014b(_0x0149(_0x05d2, _0x0270), b'\r\n', _0x05d4)
    if _0x05d3 == 'abuse':
        return _0x014b(_0x014d(_0x05d2), b'\r\n', _0x05d4)
    if _0x05d3 == 'speacialcompensation':
        return _0x014b(_0x014c(_0x05d2, _0x0270), b'\r\n', _0x05d4)
    if _0x05d3 == 'mineralvein':
        return _0x014b(_0x0153(_0x05d2), b'\n', _0x05d4)
    raise RuntimeError(f'{_0x026f.name}: detector returned unknown schema {_0x05d3!r}')

def _0x004d(_0x01bc: bytes) -> bytes:
    return b'\r\n' if b'\r\n' in _0x01bc else b'\n'

def _0x004a(_0x01b7):
    return _0x01b7 << 7 & 255 | _0x01b7 >> 1

def _0x00fb(_0x0272: bytes, _0x0273) -> bytes:
    
    _0x05de = _0x00e1()[_0x0273]
    return bytes((_0x004a(_0x05e0) ^ _0x05de[_0x05df % 40] for (_0x05df, _0x05e0) in enumerate(_0x0272)))

def _0x00fc(_0x0274: bytes, _0x0275: str) -> bytes:
    
    from modules import lzo as lzo_codec
    if len(_0x0274) < 8:
        raise ValueError(f'{_0x0275}: too small to be a GSF envelope.')
    _0x05e2 = _0x0504.unpack_from('<I', _0x0274, 0)[0]
    if _0x05e2 > len(_0x0274) or 4 + _0x05e2 + 4 > len(_0x0274):
        raise ValueError(f'{_0x0275} is not a GSF envelope (trash size {_0x05e2:,} exceeds file size {len(_0x0274):,}).')
    _0x05e3 = _0x0504.unpack_from('<I', _0x0274, 4 + _0x05e2)[0]
    try:
        _0x05e4 = lzo_codec.decompress_lzo(bytes(_0x0274[8 + _0x05e2:]), False, _0x05e3)
    except Exception as _0x05e5:
        raise ValueError(f'{_0x0275}: the LZO payload does not parse ({_0x05e5}); not a GSF envelope.')
    if len(_0x05e4) != _0x05e3:
        raise ValueError(f'{_0x0275}: LZO payload is {len(_0x05e4):,} bytes; {_0x05e3:,} were expected.')
    output.detail(f'{_0x0275}: decompressed {_0x05e3:,} payload bytes ({len(_0x0274):,} on disk, {_0x05e2:,} trash bytes skipped).')
    return _0x05e4

def _0x00fd(_0x0276: _0x0506):
    try:
        import modules.lzo
    except ImportError as _0x05e9:
        raise RuntimeError(f"{_0x0276.name}: needs the 'lzo' package ({_0x05e9})")
    _0x05e6 = _0x00fc(_0x0276.read_bytes(), _0x0276.name)
    _0x05e7 = _0x00e5(_0x0276.name)
    if _0x05e7 is None:
        _0x05ea = {_0x05eb.lower(): _0x05ec for (_0x05eb, _0x05ec) in _0x00e4.items()}
        if _0x0276.name.lower() in _0x05ea:
            raise RuntimeError(f'SKIP: {_0x05ea[_0x0276.name.lower()]} is missing from the bundled XORCryptoCodeList.')
        raise ValueError(f'No crypt page is registered for {_0x0276.name} (known: {sorted(_0x00e2)}).')
    return _0x00fb(_0x05e6, _0x05e7)

def _0x00fe(_0x0277: str) -> list:
    
    _0x05ed = _0x00e5(_0x0277)
    if _0x05ed is not None:
        return [_0x05ed] + [_0x05ee for _0x05ee in sorted(_0x00e1()) if _0x05ee != _0x05ed]
    return sorted(_0x00e1())

def _0x00ff(_0x0278: int) -> str:
    _0x05ef = _0x0504.unpack('<f', _0x0504.pack('<I', _0x0278))[0]
    for _0x05f0 in range(0, 12):
        _0x05f1 = ('%.*f' % (_0x05f0, _0x05ef)).rstrip('0').rstrip('.')
        if _0x05f1 in ('-0', '', '-'):
            _0x05f1 = '0'
        try:
            if _0x0504.unpack('<I', _0x0504.pack('<f', float(_0x05f1)))[0] == _0x0278:
                return _0x05f1
        except OverflowError:
            pass
    return repr(float(_0x05ef))

def _0x0100(_0x0279: bytes) -> bytes:
    return _0x0279.split(b'\x00')[0]

def _0x0101(_0x027a: bytes) -> str:
    return _0x00d9(_0x00d6(_0x027a))

def _0x0102(_0x027b: bytes) -> str:
    
    if not any((0 < _0x05f5 < 32 or _0x05f5 == 127 for _0x05f5 in _0x027b)):
        return _0x0101(_0x027b)
    _0x05f2 = ''
    for _0x05f3 in _0x00d6(_0x027b):
        _0x05f4 = ord(_0x05f3)
        _0x05f2 += f'\\x{_0x05f4:02X}' if 0 < _0x05f4 < 32 or _0x05f4 == 127 else _0x05f3
    return _0x00d9(_0x05f2)

def _0x0103(_0x027c: bytes) -> str:
    
    return _0x00da(_0x027c)[1:-1].decode('utf-8')

def _0x0104(_0x027d: int) -> str:
    return 'O' if _0x027d else 'X'
_0x0105 = {0: 'NONE', 1: 'SHIRT', 2: 'TUNIC', 3: 'CON_ARMOUR', 4: 'CON_HELM', 5: 'CON_GLOVE', 6: 'CON_BOOTS', 7: 'DEX_ARMOUR', 8: 'DEX_HELM', 9: 'DEX_GLOVE', 10: 'DEX_BOOTS', 11: 'ONEHANDED_SWORD', 12: 'TWOHANDED_SWORD', 13: 'ONEHANDED_AXE', 14: 'TWOHANDED_AXE', 15: 'ONEHANDED_BLUNT', 16: 'TWOHANDED_BLUNT', 17: 'BOW', 18: 'CROSSBOW', 19: 'STAFF', 20: 'DAGGER', 21: 'SHIELD', 22: 'CON_BODY', 23: 'CON_HEAD', 24: 'CON_PELVIS', 25: 'CON_PROTECT_A', 26: 'DEX_BODY', 27: 'DEX_HEAD', 28: 'DEX_PELVIS', 29: 'DEX_PROTECT_A', 30: 'COM_BLUNT', 31: 'COM_SWORD', 32: 'OPP_HAMMER', 33: 'OPP_AXE', 34: 'OPP_SLUSHER', 35: 'OPP_TALON', 36: 'OPP_SYTHE', 37: 'SKILL_A_GUARD', 38: 'SKILL_A_ATTACK', 39: 'SKILL_A_GUN', 40: 'SKILL_A_KNIFE', 41: 'ARROW', 42: 'BOLT', 43: 'AMMO', 44: 'POTION', 45: 'EXPBOOK', 46: 'CASHBOOK', 47: 'EVENT_LOTTERY', 48: 'PORTAL', 49: 'FIRE_CRACKER', 50: 'SKILLBOOK', 51: 'FIXED_PORTAL', 52: 'SKILL_ITEM', 53: 'GEM', 54: 'ORE', 55: 'ETC', 56: 'EVENT_DROP', 57: 'CAMP_KIT', 58: 'SHORT_RANGE_ARMS_KIT', 59: 'LONG_RANGE_ARMS_KIT', 60: 'AIRSHIP_KIT', 61: 'WORLDWEAPON_K_KIT', 62: 'WORLDWEAPON_M_KIT', 63: 'MINERAL_KIT', 64: 'QUEST_ITEM', 65: 'NECKLACE', 66: 'RING', 67: 'RUNE', 68: 'GEM_SELL', 69: 'RIDE', 70: 'TRANSFORM'}
_0x0106 = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42}
_0x0107 = {65, 66, 67}
_0x0108 = {69, 70}
_0x0109 = {43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 57, 58, 59, 60, 61, 62, 63, 64}
_0x010a = {0: 'AAA', 1: 'AA', 2: 'A', 3: 'B', 4: 'C', 5: 'D', 6: 'F', 7: 'X'}
_0x010b = {0: 'NONE', 1: 'STR', 2: 'DEX', 3: 'CON', 4: 'INT', 5: 'WIS', 6: 'LEVEL'}
(_0x010c, _0x010d, _0x010e, _0x010f, _0x0110, _0x0111, _0x0112, _0x0113, _0x0114, _0x0115, _0x0116, _0x0117, _0x0118, _0x0119, _0x011a, _0x011b, _0x011c, _0x011d, _0x011e, _0x011f, _0x0120, _0x0121) = range(22)

def _0x0122(_0x027e: str) -> bool:
    return bool(_0x027e) and '?' in _0x027e and (set(_0x027e) <= {'?'})

def _0x0123(_0x027f: str) -> str:
    return _0x027f.replace('_', ' ').title()

def _0x0125(_0x0281: int) -> str:
    _0x05f7 = _0x013a.get(_0x0281)
    if _0x05f7 is None:
        return 'Unknown'
    return _0x0123(_0x05f7)

def _0x0126(_0x0282: int) -> str:
    return f'0x{_0x0282:04X}' if _0x0282 >= 32768 else str(_0x0282)

def _0x0127(_0x0283: bytes):
    _0x05f8 = _0x0283[21]
    _0x05f9 = _0x0101(_0x0100(_0x0283[252:284]))
    _0x05fa = [str(_0x0504.unpack_from('<H', _0x0283, 0)[0]), _0x0102(_0x0100(_0x0283[52:116])), _0x0101(_0x0100(_0x0283[156:188])), _0x0101(_0x0100(_0x0283[188:220])), _0x0101(_0x0100(_0x0283[116:148])), str(_0x0504.unpack_from('<H', _0x0283, 148)[0]), str(_0x0504.unpack_from('<H', _0x0283, 150)[0]), str(_0x0504.unpack_from('<H', _0x0283, 152)[0]), str(_0x0504.unpack_from('<H', _0x0283, 154)[0]), str(_0x0283[22]), str(_0x0283[23]), _0x0101(_0x0100(_0x0283[220:252])), _0x0105.get(_0x05f8, str(_0x05f8)), _0x05f9, _0x0104(_0x0283[34]), _0x0104(_0x0283[35]), str(_0x0283[27]), str(_0x0283[28]), str(_0x0504.unpack_from('<I', _0x0283, 4)[0]), _0x0104(_0x0283[36]), str(_0x0504.unpack_from('<I', _0x0283, 8)[0]), str(_0x0504.unpack_from('<I', _0x0283, 12)[0]), str(_0x0504.unpack_from('<I', _0x0283, 44)[0]), _0x010b.get(_0x0283[48], str(_0x0283[48])), str(_0x0504.unpack_from('<H', _0x0283, 50)[0]), str(_0x0504.unpack_from('<H', _0x0283, 30)[0]), str(_0x0504.unpack_from('<H', _0x0283, 32)[0]), str(_0x0283[25]), str(_0x0283[26])]
    _0x05fb = [_0x0504.unpack_from('<H', _0x0283, 540 + 2 * _0x05fd)[0] for _0x05fd in range(22)]
    if _0x05f8 in _0x0106:
        _0x05fa += [str(_0x05fb[_0x010d]), str(_0x05fb[_0x010e]), str(_0x05fb[_0x010f]), str(_0x05fb[_0x0117]), str(_0x0504.unpack_from('<H', _0x0283, 16)[0]), _0x010a.get(_0x0283[18], str(_0x0283[18])), str(_0x0283[19]), str(_0x0283[20]), str(_0x0283[24]), str(_0x05fb[_0x011b]), '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
    elif _0x05f8 in _0x0107:
        _0x05fa += [str(_0x05fb[_0x010d]), str(_0x05fb[_0x010e]), str(_0x05fb[_0x010f]), str(_0x05fb[_0x0117]), str(_0x0504.unpack_from('<H', _0x0283, 16)[0]), _0x010a.get(_0x0283[18], str(_0x0283[18])), str(_0x05fb[_0x0116]), str(_0x05fb[_0x0110]), str(_0x05fb[_0x0119]), str(_0x05fb[_0x011a]), str(_0x05fb[_0x0111]), str(_0x05fb[_0x011c]), str(_0x05fb[_0x0112]), str(_0x05fb[_0x0114]), str(_0x05fb[_0x0113]), str(_0x05fb[_0x0115]), str(_0x05fb[_0x0118]), str(_0x05fb[_0x011d]), str(_0x05fb[_0x011e]), str(_0x05fb[_0x011f]), str(_0x05fb[_0x0120]), str(_0x05fb[_0x0121])]
    elif _0x05f8 in _0x0108:
        _0x05fa += [str(_0x0504.unpack_from('<H', _0x0283, 16)[0]), _0x010a.get(_0x0283[18], str(_0x0283[18])), str(_0x05fb[_0x0118])] + [''] * 19
    elif _0x05f8 in _0x0109:
        _0x05fc = [_0x00ff(_0x0504.unpack_from('<I', _0x0283, _0x05fe)[0]) for _0x05fe in (588, 592, 596)]
        _0x05fa += [_0x0104(_0x0283[615]), str(_0x0283[614]), _0x0126(_0x0504.unpack_from('<H', _0x0283, 608)[0]), str(_0x0504.unpack_from('<H', _0x0283, 610)[0]), str(_0x0283[600]), _0x05fc[0], _0x05fc[1], _0x05fc[2], str(_0x0504.unpack_from('<I', _0x0283, 604)[0]), _0x0126(_0x0504.unpack_from('<H', _0x0283, 612)[0]), _0x0101(_0x0100(_0x0283[284:540]))] + [''] * 11
    else:
        _0x05fa += [_0x0101(_0x0100(_0x0283[284:540]))] + [''] * 21
    _0x05fa += [str(_0x0283[2]), str(_0x0283[3]), str(_0x0504.unpack_from('<H', _0x0283, 584)[0]), str(_0x0504.unpack_from('<H', _0x0283, 586)[0]), _0x00ff(_0x0504.unpack_from('<I', _0x0283, 588)[0]), _0x00ff(_0x0504.unpack_from('<I', _0x0283, 592)[0]), _0x00ff(_0x0504.unpack_from('<I', _0x0283, 596)[0]), str(_0x0504.unpack_from('<I', _0x0283, 600)[0])]
    _0x05fa.append(str(_0x0283[18]) if _0x05f8 not in _0x009e else '')
    return _0x05fa
_0x0128 = ['ID', 'ItemName', 'FieldModelName', 'AttachedModelName', 'SpriteDDS', 'MinX', 'MinY', 'MaxX', 'MaxY', 'SizeX', 'SizeY', 'EffectSound', 'ItemType', 'TypeName', 'AbleExchangeNDrop', 'AbleSell', 'MinDropLevel', 'MaxDropLevel', 'Price', 'OptionPrice', 'BlackPrice', 'MedalPrice', 'ClassLimit', 'LimitStat', 'Limit', 'LowLevel', 'HighLevel', 'Durability', 'MaxDurability', 'MinDamage', 'MaxDamage', 'Defence', 'Block', 'DropOption', 'Grade', 'CriticalType', 'AttackRange', 'MaxSocketNum', 'MagicResist', 'Evade', 'CoolDown', 'MaxHP', 'MaxMP', 'HPRegen', 'MPRegen', 'Speed', 'SkillPoint', 'Frost', 'Fire', 'Electro', 'Darkness', 'Res2', 'Res3', 'Res584', 'Res586', 'Res588', 'Res592', 'Res596', 'Res600', 'Res18']

_0x012a = {0: 'Common', 1: 'Warrior', 2: 'Defender', 3: 'Mage', 4: 'Acolyte', 5: 'Boss', 6: 'BG', 7: 'Summon', 8: 'Structure', 9: 'Named', 10: 'Chief', 11: 'Object', 12: 'Guard', 13: 'Gather'}
_0x012b = {0: '0', 1: 'HP', 2: 'MP', 3: 'EXP', 4: 'DropRate'}

def _0x012c(_0x0285: int) -> str:
    from modules.ryl_compiler import _0x00a3 as _0x0603
    _0x0604 = _0x0504.unpack('<f', _0x0504.pack('<I', _0x0285))[0] * 100.0
    for _0x0605 in range(0, 12):
        _0x0607 = ('%.*f' % (_0x0605, _0x0604)).rstrip('0').rstrip('.')
        if _0x0607 in ('-0', '', '-'):
            _0x0607 = '0'
        try:
            if _0x0603(_0x0607) == _0x0285:
                return _0x0607
        except (OverflowError, ZeroDivisionError, ValueError):
            pass
    _0x0606 = _0x0504.unpack('<f', _0x0504.pack('<f', 0.01))[0]
    try:
        _0x0608 = _0x0504.unpack('<f', _0x0504.pack('<I', _0x0285 & 4294967295))[0]
        _0x0609 = _0x0504.unpack('<f', _0x0504.pack('<f', _0x0608 / _0x0606))[0]
        _0x060a = _0x0504.unpack('<I', _0x0504.pack('<f', _0x0609))[0]
        if not 8388608 <= _0x060a < 2139095040:
            return repr(_0x0604)
        for _0x060b in range(-128, 129):
            _0x060c = _0x060a + _0x060b
            if not 8388608 <= _0x060c < 2139095040:
                continue
            _0x060d = _0x0504.unpack('<f', _0x0504.pack('<I', _0x060c))[0]
            if _0x0504.unpack('<I', _0x0504.pack('<f', _0x060d * _0x0606))[0] != _0x0285:
                continue
            for _0x0605 in range(0, 18):
                _0x0607 = ('%.*f' % (_0x0605, _0x060d)).rstrip('0').rstrip('.')
                if _0x0607 in ('-0', '', '-'):
                    _0x0607 = '0'
                try:
                    _0x060e = _0x0504.unpack('<f', _0x0504.pack('<f', float(_0x0607)))[0]
                except (OverflowError, ValueError):
                    continue
                if _0x060e == _0x060d:
                    return _0x0607
            return repr(_0x060d)
    except (OverflowError, ZeroDivisionError, ValueError):
        pass
    return repr(_0x0604)

def _0x012d(_0x0286: int) -> bool:
    
    from modules.ryl_compiler import _0x00a3 as _0x00a3
    if _0x0286 == 0:
        return True
    try:
        return _0x00a3(_0x012c(_0x0286)) == _0x0286
    except Exception:
        return False

def _0x012e(_0x0287: bytes, _0x0288: bool=False):
    _0x060f = [''] * 121
    _0x060f[0] = str(_0x0504.unpack_from('<H', _0x0287, 348)[0])
    _0x060f[1] = _0x0101(_0x0100(_0x0287[64:128]))
    _0x060f[2] = _0x0101(_0x0100(_0x0287[128:160]))
    _0x060f[3] = _0x0104(_0x0287[396])
    _0x060f[4] = str(_0x0287[370])
    _0x060f[5] = 'Siege' if _0x0287[392] else _0x012a.get(_0x0287[366], str(_0x0287[366]))
    _0x060f[6] = _0x0104(_0x0287[392])
    _0x060f[68] = str(_0x0287[366]) if _0x0287[392] else '0'
    _0x060f[7] = str(_0x0287[12])
    _0x060f[8] = _0x00ff(_0x0504.unpack_from('<I', _0x0287, 4)[0]) if _0x0288 else _0x012c(_0x0504.unpack_from('<I', _0x0287, 4)[0])
    _0x060f[9] = str(_0x0287[28])
    _0x060f[10] = _0x00ff(_0x0504.unpack_from('<I', _0x0287, 20)[0]) if _0x0288 else _0x012c(_0x0504.unpack_from('<I', _0x0287, 20)[0])
    _0x060f[11] = str(_0x0287[44])
    _0x060f[12] = str(_0x0287[44])
    for (_0x0610, _0x0611) in enumerate((160, 164, 168, 172), start=13):
        _0x060f[_0x0610] = _0x00ff(_0x0504.unpack_from('<I', _0x0287, _0x0611)[0])
    _0x060f[17] = str(_0x0504.unpack_from('<H', _0x0287, 364)[0])
    _0x060f[18] = _0x00ff(_0x0504.unpack_from('<I', _0x0287, 360)[0])
    _0x060f[19] = str(_0x0504.unpack_from('<I', _0x0287, 456)[0])
    _0x060f[20] = str(_0x0287[464])
    for (_0x0612, _0x0611) in ((21, 472), (22, 474), (23, 478), (24, 476), (25, 480), (26, 492), (28, 490), (30, 500), (31, 502)):
        _0x060f[_0x0612] = str(_0x0504.unpack_from('<H', _0x0287, _0x0611)[0])
    _0x060f[27] = '0'
    _0x060f[29] = str(_0x0287[544])
    _0x060f[32] = str(_0x0287[494])
    for (_0x0612, _0x0611) in ((33, 482), (34, 486), (35, 484), (36, 488)):
        _0x060f[_0x0612] = str(_0x0504.unpack_from('<H', _0x0287, _0x0611)[0])
    _0x060f[37] = _0x00ff(_0x0504.unpack_from('<I', _0x0287, 356)[0])
    _0x060f[38] = str(_0x0287[367])
    _0x060f[39] = _0x0104(_0x0287[393])
    _0x060f[40] = _0x0104(_0x0287[394])
    _0x060f[41] = _0x0104(_0x0287[395])
    _0x060f[42] = _0x0104(_0x0287[369])
    _0x060f[43] = str(_0x0287[368])
    _0x060f[44] = str(_0x0287[372])
    for (_0x0612, _0x0611) in ((45, 374), (46, 376), (47, 378), (48, 380), (49, 382)):
        _0x060f[_0x0612] = _0x0126(_0x0504.unpack_from('<H', _0x0287, _0x0611)[0])
    _0x060f[50] = str(_0x0287[384])
    _0x060f[51] = str(_0x0287[385])
    _0x060f[52] = _0x00ff(_0x0504.unpack_from('<I', _0x0287, 388)[0])
    _0x060f[53] = str(_0x0504.unpack_from('<I', _0x0287, 352)[0])
    for (_0x0612, _0x0611) in ((54, 176), (55, 178), (56, 180), (57, 182), (58, 184), (59, 188), (60, 192), (61, 196), (62, 200), (63, 204)):
        _0x060f[_0x0612] = str(_0x0504.unpack_from('<H', _0x0287, _0x0611)[0])
    _0x060f[64] = str(_0x0504.unpack_from('<I', _0x0287, 208)[0])
    _0x060f[65] = str(_0x0504.unpack_from('<I', _0x0287, 212)[0])
    _0x060f[66] = str(_0x0504.unpack_from('<I', _0x0287, 216)[0])
    for _0x0612 in range(67, 74):
        if _0x0612 not in (68, 73):
            _0x060f[_0x0612] = '0'
    _0x060f[73] = str(_0x0287[244])
    for (_0x0612, _0x0611) in ((74, 220), (75, 224), (76, 228), (77, 232), (78, 236)):
        _0x060f[_0x0612] = str(_0x0504.unpack_from('<I', _0x0287, _0x0611)[0])
    for (_0x0612, _0x0611) in ((79, 240), (80, 242), (82, 246), (83, 248), (84, 250), (85, 252), (86, 260), (87, 264), (88, 268), (120, 454)):
        _0x060f[_0x0612] = str(_0x0504.unpack_from('<H', _0x0287, _0x0611)[0])
    _0x060f[81] = str(_0x0287[245])
    for (_0x0612, _0x0611) in ((89, 272), (90, 276), (91, 280), (92, 284), (93, 288), (94, 292), (95, 296), (96, 300), (97, 304), (104, 308), (105, 312), (106, 316)):
        _0x060f[_0x0612] = str(_0x0504.unpack_from('<I', _0x0287, _0x0611)[0])
    _0x060f[107] = str(_0x0504.unpack_from('<H', _0x0287, 190)[0])
    for (_0x0612, _0x0611) in ((108, 408), (109, 412), (110, 416), (111, 420), (112, 424), (113, 428), (114, 432), (116, 436), (117, 440), (118, 444), (119, 448)):
        _0x060f[_0x0612] = str(_0x0504.unpack_from('<I', _0x0287, _0x0611)[0])
    _0x060f[98] = str(_0x0287[344])
    _0x060f[99] = str(_0x0287[344])
    _0x060f[100] = _0x012b.get(_0x0287[452], str(_0x0287[452]))
    _0x060f[101] = str(_0x0287[453])
    _0x060f[102] = str(_0x0504.unpack_from('<I', _0x0287, 400)[0])
    _0x060f[103] = str(_0x0504.unpack_from('<I', _0x0287, 404)[0])
    _0x0613 = _0x0504.unpack_from('<H', _0x0287, 348)[0]
    _0x060f[115] = '0' if _0x0613 >= 40232 else ''
    return _0x060f

_0x0130 = {0: 'NONE', 1: 'PASSIVE', 2: 'INSTANCE', 3: 'CAST', 4: 'CHANT', 5: 'ENCHANT', 6: 'ITEM', 7: 'SET', 8: 'ACTION', 9: 'ABILITY', 10: 'GATHER'}
_0x0131 = {0: 'NONE', 1: 'FORFIGHTER', 2: 'WITHSHIELD', 3: 'FORFIGHTERTWOHAND', 4: 'FORALLONEHAND', 5: 'WITHDAGGER', 6: 'WITHTHROWINGDAGGER', 7: 'RANGED', 8: 'LEFTARM', 9: 'GUARDARM', 10: 'WITHWEAPON', 11: 'ATTACKARM', 12: 'GUNARM', 13: 'KNIFEARM', 14: 'WITHCLOW'}
_0x0132 = {0: 'NONE', 1: 'STR', 2: 'DEX', 3: 'CON', 4: 'INT', 5: 'WIS', 6: 'LEVEL'}
_0x0133 = {0: 'NONE', 1: 'MELEE', 2: 'FRIEND', 3: 'ENEMY', 4: 'FRDEAD', 5: 'ENDEAD', 6: 'FROBJ', 7: 'ENOBJ', 8: 'PARTY', 9: 'FREXME', 10: 'ENLINE', 11: 'SUMMON'}
_0x0134 = ['ID', 'Type', 'ClassSkill', 'Name[5]', 'Limit', 'Stat[0]', 'Value[0]', 'Stat[1]', 'Value[1]', 'Target', 'mRange', 'Range', 'Region', 'StartMP', 'LevelMP', 'LockAdd', 'Starttick', 'LevelTick', 'CastingFlag', 'EffectFlag', 'HitFlag', 'CoolDownTime', 'EndCoolDown', 'dds', 'MinX', 'MinY', 'MaxX', 'MaxY', 'Hit', 'EndScript', 'Protection', 'Interrupt', 'Counter', 'Gauge', 'Parent', 'Child', 'Text']

def _0x0135(_0x028a: int) -> int:
    return _0x028a - 256 if _0x028a >= 128 else _0x028a

def _0x0136(_0x028b: bytes):
    _0x0618 = [f"0x{_0x0504.unpack_from('<H', _0x028b, 472)[0]:04X}", _0x0130.get(_0x0504.unpack_from('<I', _0x028b, 456)[0], '?'), str(1 if _0x028b[506] else 0), _0x0101(_0x0100(_0x028b[96:160])), _0x0131.get(_0x0504.unpack_from('<I', _0x028b, 464)[0], '?'), _0x0132.get(_0x028b[468], str(_0x028b[468])), str(_0x0135(_0x028b[470])), _0x0132.get(_0x028b[469], str(_0x028b[469])), str(_0x0135(_0x028b[471])), _0x0133.get(_0x0504.unpack_from('<I', _0x028b, 460)[0], '?'), _0x00ff(_0x0504.unpack_from('<I', _0x028b, 492)[0]), _0x00ff(_0x0504.unpack_from('<I', _0x028b, 496)[0]), _0x00ff(_0x0504.unpack_from('<I', _0x028b, 500)[0]), str(_0x0504.unpack_from('<H', _0x028b, 474)[0]), str(_0x0504.unpack_from('<H', _0x028b, 476)[0]), str(_0x0504.unpack_from('<H', _0x028b, 478)[0]), str(_0x0504.unpack_from('<H', _0x028b, 480)[0]), str(_0x0504.unpack_from('<H', _0x028b, 482)[0]), _0x0101(_0x0100(_0x028b[64:96])), _0x0101(_0x0100(_0x028b[0:32])), _0x0101(_0x0100(_0x028b[32:64])), str(_0x0504.unpack_from('<I', _0x028b, 488)[0]), str(_0x028b[510]), _0x0101(_0x0100(_0x028b[160:192])), str(_0x0504.unpack_from('<H', _0x028b, 192)[0]), str(_0x0504.unpack_from('<H', _0x028b, 194)[0]), str(_0x0504.unpack_from('<H', _0x028b, 196)[0]), str(_0x0504.unpack_from('<H', _0x028b, 198)[0]), str(_0x028b[511]), str(_0x028b[509]), str(1 if _0x028b[504] else 0), str(1 if _0x028b[507] else 0), str(1 if _0x028b[508] else 0), str(1 if _0x028b[505] else 0)]
    for (_0x0619, _) in ((484, 37), (486, 37)):
        _0x061c = _0x0504.unpack_from('<H', _0x028b, _0x0619)[0]
        _0x0618.append(f'0x{_0x061c:04X}' if _0x061c else '0')
    _0x061b = _0x0100(_0x028b[200:456])
    _0x0618.append(_0x0103(_0x061b))
    return _0x0618

def _0x0137(_0x028c: bytes) -> bytes:
    _0x061d = ['\t'.join(_0x0134)]
    for _0x061e in range(len(_0x028c) // 2580):
        for _0x061f in range(5):
            _0x0620 = _0x028c[_0x061e * 2580 + _0x061f * 516:_0x061e * 2580 + (_0x061f + 1) * 516]
            if _0x0504.unpack_from('<H', _0x0620, 472)[0] == 0:
                continue
            _0x061d.append('\t'.join(_0x0136(_0x0620)))
    output.detail(f'SkillScript.gsf: {len(_0x061d) - 1:,} skill rows in {len(_0x028c) // 2580} groups.')
    return ('\r\n'.join(_0x061d) + '\r\n').encode('utf-8')
_0x0138 = b'PickkingItem\t\t\tTargetItem\t\t\tResultItem\t\t\r\nName\tID\tNum\tName\tID\tNum\r\n'
_0x0139 = 644
_0x013a = {0: 'HELM', 1: 'SHIRT', 2: 'TUNIC', 3: 'ARMOUR', 4: 'GLOVE', 5: 'BOOTS', 6: 'ONEHANDED_SWORD', 7: 'ONEHANDED_BLUNT', 8: 'ONEHANDED_AXE', 9: 'TWOHANDED_BLUNT', 10: 'TWOHANDED_AXE', 11: 'TWOHANDED_SWORD', 12: 'BOW', 13: 'CROSSBOW', 14: 'STAFF', 15: 'DAGGER', 16: 'SHIELD', 17: 'CLOAK', 18: 'RING', 19: 'NECKLACE', 20: 'POTION', 21: 'POISON', 22: 'TRAP', 23: 'SKILLBOOK', 24: 'GEM', 25: 'RUNE', 26: 'ORE', 27: 'AMMO', 28: 'ETC', 29: 'HEAD', 30: 'BODY', 31: 'PROTECT_A', 32: 'PELVIS', 33: 'COM_BLUNT', 34: 'COM_SWORD', 35: 'OPP_HAMMER', 36: 'OPP_AXE', 37: 'OPP_SLUSHER', 38: 'OPP_TALON', 39: 'OPP_SYTHE', 40: 'SKILL_A_GUARD', 41: 'SKILL_A_ATTACK', 42: 'SKILL_A_GUN', 43: 'SKILL_A_KNIFE', 44: 'ACCESSORY', 45: 'ARROW', 46: 'BOLT', 47: 'PORTAL', 48: 'EVENT_DROP', 49: 'EVENT_LOTTERY', 50: 'EXPBOOK', 51: 'CASHBOOK', 52: 'FIRE_CRACKER', 53: 'CAMP_KIT', 54: 'SHORT_RANGE_ARMS_KIT', 55: 'LONG_RANGE_ARMS_KIT', 56: 'AIRSHIP_KIT'}
_0x013b = {0: 'ETC', 1: 'NORMAL', 2: 'ENHANCED', 3: 'RARE'}
_0x013c = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46}
_0x013d = {20, 21, 22, 23, 27, 47, 49, 50, 51, 52, 53, 54, 55, 56}
_0x013e = ['ID', 'ItemName', 'FieldModelName', 'AttachedModelName', 'SpriteDDS', 'MinX', 'MinY', 'MaxX', 'MaxY', 'SizeX', 'SizeY', 'EffectSound', 'ItemLevel', 'ItemType', 'TypeName', 'Price', 'BlackPrice', 'MedalPrice', 'OptionLimit', 'Durability', 'MaxDurability', 'ClassLimit', 'SkillLimitType', 'SkillLimitLevel', 'LevelLimit', 'STRLimit', 'DEXLimit', 'CONLimit', 'INTLimit', 'WISLimit', 'CraftExp', 'CriticalType', 'CriticalPercentage', 'MinDamage', 'MaxDamage', 'DRC', 'OffenceRevision', 'Defence', 'DefenceRevision', 'Resistance', 'BlockingPercentage', 'AttackSpeed', 'MoveSpeed', 'AttackRange', 'LongRangeAttack', 'HpMaxPlus', 'MpMaxPlus', 'HPRegen', 'MPRegen', 'FireAttribute', 'LightingAttribute', 'ColdAttribute', 'DrainAttribute', 'PoisonAttribute', 'FireResistance', 'LightningResistance', 'ColdResistance', 'DrainResistance', 'PoisonResistance', 'STRAdd', 'DEXAdd', 'CONAdd', 'INTAdd', 'WISAdd', 'MaterialValue', 'MaxSocketNum']

def _0x013f(_0x028d: bytes, _0x028e: int, _0x028f: int) -> str:
    return _0x0101(_0x0100(_0x028d[_0x028e:_0x028e + _0x028f]))

def _0x0140(_0x0290: bytes):
    _0x0621 = _0x0290[4]
    _0x0622 = [str(_0x0504.unpack_from('<H', _0x0290, 0)[0]), _0x013f(_0x0290, 60, 64), _0x013f(_0x0290, 164, 32), _0x013f(_0x0290, 196, 32), _0x013f(_0x0290, 124, 32), str(_0x0504.unpack_from('<H', _0x0290, 156)[0]), str(_0x0504.unpack_from('<H', _0x0290, 158)[0]), str(_0x0504.unpack_from('<H', _0x0290, 160)[0]), str(_0x0504.unpack_from('<H', _0x0290, 162)[0]), str(_0x0290[5]), str(_0x0290[6]), _0x013f(_0x0290, 228, 32), _0x013b.get(_0x0504.unpack_from('<I', _0x0290, 16)[0], f"[{_0x0504.unpack_from('<I', _0x0290, 16)[0]:,}]"), _0x013a.get(_0x0621, f'[{_0x0621}]'), _0x013f(_0x0290, 260, 32) if not _0x0122(_0x013f(_0x0290, 260, 32)) else _0x0125(_0x0621), str(_0x0504.unpack_from('<I', _0x0290, 20)[0]), str(_0x0504.unpack_from('<I', _0x0290, 24)[0]), str(_0x0504.unpack_from('<I', _0x0290, 28)[0]), str(_0x0290[7]), str(_0x0290[8]), str(_0x0290[9]), str(_0x0504.unpack_from('<I', _0x0290, 56)[0]), str(_0x0504.unpack_from('<H', _0x0290, 50)[0]), str(_0x0290[52]), str(_0x0290[53]), str(_0x0504.unpack_from('<H', _0x0290, 40)[0]), str(_0x0504.unpack_from('<H', _0x0290, 42)[0]), str(_0x0504.unpack_from('<H', _0x0290, 44)[0]), str(_0x0504.unpack_from('<H', _0x0290, 46)[0]), str(_0x0504.unpack_from('<H', _0x0290, 48)[0]), str(_0x0504.unpack_from('<I', _0x0290, 12)[0])]
    if _0x0621 in _0x013c:
        _0x0623 = [_0x0504.unpack_from('<H', _0x0290, 548 + 2 * _0x0624)[0] for _0x0624 in range(1, 34)]
        _0x0622 += [str(_0x0625) for _0x0625 in _0x0623]
        _0x0622 += [str(_0x0290[10]), str(_0x0290[11])]
    elif _0x0621 in _0x013d:
        _0x0622 += [_0x0126(_0x0504.unpack_from('<H', _0x0290, 620)[0]), str(_0x0290[52]), str(_0x0290[624]), _0x00ff(_0x0504.unpack_from('<I', _0x0290, 628)[0]), _0x00ff(_0x0504.unpack_from('<I', _0x0290, 632)[0]), _0x00ff(_0x0504.unpack_from('<I', _0x0290, 636)[0]), str(_0x0504.unpack_from('<I', _0x0290, 640)[0]), _0x013f(_0x0290, 292, 256)]
        _0x0622 += [''] * 27
    else:
        _0x0622 += [_0x013f(_0x0290, 292, 256)]
        _0x0622 += [''] * 34
    return _0x0622

def _0x0141(_0x0291: bytes) -> bytes:
    (_0x0626, _0x0627) = divmod(len(_0x0291), _0x0139)
    if _0x0627:
        raise ValueError(f'ItemScript.gsf payload is {len(_0x0291):,} bytes; not a multiple of the RYL1 {_0x0139}-byte ItemInfo record.')
    _0x0628 = ['\t'.join(_0x013e)]
    for _0x0629 in range(_0x0626):
        _0x0628.append('\t'.join(_0x0140(_0x0291[_0x0629 * _0x0139:(_0x0629 + 1) * _0x0139])))
    output.detail(f'ItemScript.gsf (RYL1): {_0x0626:,} item rows ({_0x0139}-byte ItemInfo).')
    return ('\n'.join(_0x0628) + '\n').encode('utf-8')

def _0x0142(_0x0292: bytes) -> dict:
    _0x062a = {}
    for _0x062b in range(len(_0x0292) // _0x0139):
        _0x062c = _0x0292[_0x062b * _0x0139:(_0x062b + 1) * _0x0139]
        _0x062a[_0x0504.unpack_from('<H', _0x062c, 0)[0]] = _0x0101(_0x0100(_0x062c[60:124]))
    return _0x062a
_0x0143 = {0: 'Siege', 1: 'Warrior', 2: 'Defender', 3: 'Mage', 4: 'Acolyte', 5: 'Rogue', 6: 'BG', 7: 'Summon', 8: 'Structure', 9: 'Named', 10: 'Chief', 11: 'Object', 12: 'Guard'}
_0x0144 = ['ID', 'Name', 'Model', 'Nation', 'Class', 'Toggle', 'RespawnArea1', 'Speed1', 'RespawnArea2', 'Speed2', 'Param1', 'Param2', 'Zone1', 'Zone2', 'Zone3', 'Zone4', 'Value334', 'Velocity', 'BaseXP', 'Level', 'MinDamage', 'MaxDamage', 'Defense', 'HitRate', 'Evade', 'Unk25', 'CriticalRate', 'Unk27', 'Unk28', 'Skill29', 'Skill30', 'Unk31', 'Unk32', 'Unk33', 'Unk34', 'Unk35', 'Unk36', 'Unk37', 'Unk38', 'Unk39', 'Unk40', 'Skill41', 'Skill42', 'MP', 'HP', 'Unk45', 'Unk46', 'Scale', 'SkillByte197', 'Toggle229', 'Unk50', 'Toggle231', 'Unk52', 'Toggle232', 'Toggle199', 'Byte198', 'Byte202', 'Unk57', 'Unk58', 'Unk59', 'Unk60', 'Unk61', 'Unk62', 'Unk63', 'Float224', 'SpawnTime', 'Unk66', 'Unk67', 'Unk68', 'Unk69', 'Unk70', 'Unk71', 'Unk72', 'Unk73', 'Unk74', 'Unk75', 'Weight164', 'Unk77', 'Unk78', 'Unk79', 'Unk80', 'Unk81', 'Unk82', 'Unk83', 'Unk84', 'Unk85', 'Unk86', 'Unk87', 'Unk88', 'Unk89', 'Unk90', 'Unk91', 'Unk92', 'Unk93', 'Unk94', 'Unk95', 'Unk96']

def _0x0145(_0x0293: int) -> str:
    _0x062d = _0x0504.unpack('<f', _0x0504.pack('<I', _0x0293))[0] * 100.0
    _0x062e = '%.6g' % _0x062d
    return _0x062e

def _0x0146(_0x0294: bytes):
    _0x062f = [str(_0x0504.unpack_from('<I', _0x0294, 180)[0]), _0x0101(_0x0100(_0x0294[64:96])), _0x0101(_0x0100(_0x0294[96:128])), str(_0x0294[200]), _0x0143.get(_0x0294[196], str(_0x0294[196])), _0x0104(_0x0504.unpack_from('<I', _0x0294, 0)[0]), str(_0x0504.unpack_from('<I', _0x0294, 12)[0]), _0x0145(_0x0504.unpack_from('<I', _0x0294, 4)[0]), str(_0x0504.unpack_from('<I', _0x0294, 28)[0]), _0x0145(_0x0504.unpack_from('<I', _0x0294, 20)[0]), str(_0x0504.unpack_from('<I', _0x0294, 44)[0]), str(_0x0504.unpack_from('<I', _0x0294, 60)[0])]
    _0x062f += [_0x00ff(_0x0504.unpack_from('<I', _0x0294, 128 + 4 * _0x0630)[0]) for _0x0630 in range(4)]
    _0x062f += [str(_0x0504.unpack_from('<H', _0x0294, 334)[0]), _0x00ff(_0x0504.unpack_from('<I', _0x0294, 192)[0])]
    _0x062f += [str(_0x0504.unpack_from('<I', _0x0294, 288)[0]), str(_0x0504.unpack_from('<I', _0x0294, 296)[0]), str(_0x0504.unpack_from('<H', _0x0294, 308)[0]), str(_0x0504.unpack_from('<H', _0x0294, 310)[0]), str(_0x0504.unpack_from('<H', _0x0294, 312)[0]), str(_0x0504.unpack_from('<H', _0x0294, 320)[0]), str(_0x0504.unpack_from('<H', _0x0294, 322)[0]), '0', _0x00ff(_0x0504.unpack_from('<I', _0x0294, 316)[0]), str(_0x0504.unpack_from('<H', _0x0294, 306)[0]), '0', str(_0x0504.unpack_from('<H', _0x0294, 326)[0]), str(_0x0504.unpack_from('<H', _0x0294, 328)[0])]
    _0x062f += ['0'] * 10
    _0x062f += [str(_0x0504.unpack_from('<H', _0x0294, 330)[0]), str(_0x0504.unpack_from('<H', _0x0294, 332)[0]), str(_0x0504.unpack_from('<H', _0x0294, 338)[0]), str(_0x0504.unpack_from('<H', _0x0294, 340)[0]), '0', '0']
    _0x062f += [_0x00ff(_0x0504.unpack_from('<I', _0x0294, 188)[0]), str(_0x0294[197]), _0x0104(_0x0294[229]), _0x0104(0), _0x0104(_0x0294[231]), _0x0104(0), _0x0104(_0x0294[232]), _0x0104(_0x0294[199]), str(_0x0294[198]), str(_0x0294[202])]
    _0x062f += ['0'] * 5
    _0x062f += ['0', str(_0x0504.unpack_from('<H', _0x0294, 220)[0]), _0x00ff(_0x0504.unpack_from('<I', _0x0294, 224)[0]), str(_0x0504.unpack_from('<I', _0x0294, 184)[0])]
    _0x062f += ['0'] * 10
    _0x062f += [str(_0x0504.unpack_from('<H', _0x0294, 164)[0])]
    _0x062f += ['0'] * 20
    while _0x062f and _0x062f[-1] in ('', '0'):
        _0x062f.pop()
    return _0x062f

def _0x0147(_0x0295: bytes) -> bytes:
    _0x0631 = 368
    (_0x0632, _0x0633) = divmod(len(_0x0295), _0x0631)
    if _0x0633:
        raise ValueError(f'MonsterProtoType.gsf payload is {len(_0x0295):,} bytes; not a multiple of the RYL1 368-byte record.')
    _0x0634 = ['\t'.join(_0x0144)]
    for _0x0635 in range(_0x0632):
        _0x0634.append('\t'.join(_0x0146(_0x0295[_0x0635 * _0x0631:(_0x0635 + 1) * _0x0631])))
    output.detail(f'MonsterProtoType.gsf (RYL1): {_0x0632:,} records (368-byte MonsterProto).')
    return ('\n'.join(_0x0634) + '\n').encode('utf-8')

def _0x0149(_0x0299: bytes, _0x029a: dict) -> bytes:
    _0x0637 = [_0x0138.rstrip(b'\r\n')]
    _0x0638 = _0x058d()
    _0x0639 = len(_0x0299) // 10
    for _0x063a in range(_0x0639):
        _0x063b = _0x0299[_0x063a * 10:(_0x063a + 1) * 10]
        (_0x063c, _0x063d, _0x063e) = _0x0504.unpack_from('<HHH', _0x063b, 0)
        _0x063f = []
        for (_0x0640, _0x0641) in ((_0x063c, _0x063b[6]), (_0x063d, _0x063b[7]), (_0x063e, _0x063b[8])):
            _0x0642 = _0x029a.get(_0x0640)
            if _0x0642 is None:
                _0x0638[_0x0640] += 1
                _0x0642 = f'ITEM_{_0x0640}'
            _0x063f += [_0x0642, str(_0x0640), str(_0x0641)]
        _0x0637.append('\t'.join(_0x063f).encode('utf-8'))
    if _0x0638:
        _0x063f = sum(_0x0638.values())
        output.warn(f'Chemical.gsf references {len(_0x0638)} unknown item IDs ({_0x063f:,} cells); wrote ITEM_<id> placeholders instead.')
        output.warn(f'Chemical.gsf most-missed IDs: {_0x0638.most_common(5)}.')
    output.detail(f'Chemical.gsf: {_0x0639:,} recipes.')
    return b'\r\n'.join(_0x0637) + b'\r\n'

def _0x014a(_0x029b: bytes) -> dict:
    _0x0643 = {}
    for _0x0644 in range(len(_0x029b) // 616):
        _0x0645 = _0x029b[_0x0644 * 616:(_0x0644 + 1) * 616]
        _0x0643[_0x0504.unpack_from('<H', _0x0645, 0)[0]] = _0x0101(_0x0100(_0x0645[52:116]))
    return _0x0643

def _0x014b(_0x029c: bytes, _0x029d: bytes=b'\r\n', _0x029e=None) -> bytes:
    
    from modules.banners import _0x000e as _0x000e
    _0x0646 = _0x029d.join((_0x0648.encode('ascii') for _0x0648 in _0x000e()))
    if _0x029e:
        _0x0647 = [_0x0649 if _0x0649.startswith('//') else '// ' + _0x0649 for _0x0649 in _0x029e]
        _0x0646 += _0x029d + _0x029d.join((_0x064a.encode('ascii') for _0x064a in _0x0647))
    return _0x0646 + _0x029d + _0x029d + _0x029c

def _0x014c(_0x029f: bytes, _0x02a0: dict) -> bytes:
    
    (_0x064b, _0x064c) = ([], [])
    for _0x064d in range(0, len(_0x029f) - 1, 2):
        _0x0652 = _0x0504.unpack_from('<H', _0x029f, _0x064d)[0]
        if _0x0652 == 0:
            _0x064b.append(_0x064c)
            _0x064c = []
        else:
            _0x064c.append(_0x0652)
    if _0x064c:
        _0x064b.append(_0x064c)
    output.detail(f'SpeacialCompensation.gsf: {len(_0x064b):,} group(s) carried verbatim (case-only layout).')
    _0x064e = ['// SpeacialLayout: case-only (no auto slot groups)']
    for (_0x064f, _0x0650) in enumerate(_0x064b, 1):
        _0x064e.append(f';Case {_0x064f} - ()')
        if _0x0650:
            _0x064e.append('\t'.join((str(_0x0653) for _0x0653 in _0x0650)))
    _0x0651 = ('\r\n'.join(_0x064e) + '\r\n').encode('utf-8')
    return _0x0651

def _0x014d(_0x02a1: bytes) -> bytes:
    _0x0654 = []
    for _0x0655 in range(len(_0x02a1) // 15):
        _0x0656 = _0x02a1[_0x0655 * 15:(_0x0655 + 1) * 15].split(b'\x00')[0]
        _0x0654.append(_0x0656)
    output.detail(f'Script1.gsf: {len(_0x0654)} abuse words.')
    return b'\r\n'.join(_0x0654) + b'\r\n'
_0x014e = 1048576

def _0x0150(_0x02a3: bytes) -> bool:
    
    if len(_0x02a3) < 4 + _0x014e + 60:
        return False
    (_0x0658,) = _0x0504.unpack_from('<I', _0x02a3, 0)
    if _0x0658 == 0 or _0x0658 > 100000:
        return False
    _0x0659 = 4 + _0x014e
    for _ in range(_0x0658):
        if _0x0659 + 60 > len(_0x02a3):
            return False
        if _0x02a3[_0x0659:_0x0659 + 4] != _0x02a3[_0x0659 + 56:_0x0659 + 60]:
            return False
        (_0x065b,) = _0x0504.unpack_from('<I', _0x02a3, _0x0659)
        _0x0659 += 60 + 4 * _0x065b
    return _0x0659 == len(_0x02a3)

def _0x0151(_0x02a4: bytes):
    
    (_0x065c,) = _0x0504.unpack_from('<I', _0x02a4, 0)
    if len(_0x02a4) < 4 + _0x014e:
        raise ValueError(f'MineralVein plain too short: {len(_0x02a4):,} bytes')
    _0x065d = _0x02a4[4:4 + _0x014e]
    (_0x065e, _0x065f) = ([], 4 + _0x014e)
    for _0x0660 in range(_0x065c):
        if _0x065f + 60 > len(_0x02a4):
            raise ValueError(f'MineralVein record {_0x0660} truncated at {_0x065f:,}')
        (_0x0661,) = _0x0504.unpack_from('<I', _0x02a4, _0x065f)
        _0x0662 = _0x02a4[_0x065f + 4:_0x065f + 60]
        (_0x0663, _0x0664, _0x0665, _0x0666, _0x0667, _0x0668) = _0x0504.unpack_from('<6I', _0x0662, 32)
        if _0x0661 != _0x0668:
            raise ValueError(f'MineralVein record {_0x0660}: count stamp {_0x0661} != struct count {_0x0668}')
        _0x0669 = list(_0x0504.unpack_from(f'<{_0x0661}I', _0x02a4, _0x065f + 60)) if _0x0661 else []
        _0x066a = _0x065f + 60 + _0x0661 * 4
        if _0x066a > len(_0x02a4):
            raise ValueError(f'MineralVein record {_0x0660} overruns the plain')
        _0x065e.append({'color': _0x0663, 'fert': _0x0664, 'count': _0x0661, 'list_head': _0x0667, 'name32': _0x0662[0:32], 'raw_name': _0x0662[0:32], 'raw_v28': _0x0665, 'raw_v2c': _0x0666, 'raw_count_stamp': _0x0668, 'minerals': _0x0669})
        _0x065f = _0x066a
    if _0x065f != len(_0x02a4):
        raise ValueError(f'MineralVein records leave {len(_0x02a4) - _0x065f:,} unclaimed trailing bytes')
    return (_0x065d, _0x065e)

def _0x0152(_0x02a5: bytes) -> str:
    
    _0x066b = _0x02a5.find(b'\n')
    if _0x066b >= 0:
        return _0x02a5[:_0x066b].decode('latin-1')
    _0x066b = _0x02a5.find(b'\x00')
    return _0x02a5[:_0x066b if _0x066b >= 0 else 32].decode('latin-1')

def _0x0153(_0x02a6: bytes) -> bytes:
    (_0x066c, _0x066d) = _0x0151(_0x02a6)
    output.detail(f"MineralVein: {len(_0x066d):,} veins, {len({_0x0672['color'] for _0x0672 in _0x066d}):,} distinct colours, {_0x066c[:4].hex()}... map.")
    _0x066e = []
    for _0x066f in _0x066d:
        _0x0670 = f"0x{_0x066f['color']:08X}"
        _0x066e.append(f'VEIN_COLOR\t{_0x0670}')
        _0x066e.append(f"VEIN_NAME\t{_0x0152(_0x066f['raw_name'])}")
        _0x066e.append(f"VEIN_RAW\t{_0x066f['raw_name'].hex()}\t0x{_0x066f['raw_v28']:08X}\t0x{_0x066f['raw_v2c']:08X}\t0x{_0x066f['list_head']:08X}")
        _0x066e.append(f"FERTILITY\t{_0x066f['fert']}")
        for _0x0671 in _0x066f['minerals']:
            _0x066e.append(f'MINERAL\t{_0x0671 & 65535}\t{_0x0671 >> 16 & 255}\t{_0x0671 >> 24 & 255}')
    return ('\n'.join(_0x066e) + '\n').encode('utf-8')

def _0x0154(_0x02a7: bytes) -> bytes:
    
    if len(_0x02a7) != _0x014e:
        raise ValueError(f'MineralVein map is {len(_0x02a7):,} bytes; {_0x014e:,} expected.')
    _0x0673 = _0x0504.pack('<3B', 0, 0, 2) + b'\x00' * 9 + _0x0504.pack('<HHBB', 512, 512, 32, 0)
    return _0x0673 + b''.join((_0x02a7[_0x0674 * 2048:(_0x0674 + 1) * 2048] for _0x0674 in range(511, -1, -1)))

def _0x0155(_0x02a8: _0x0506, _0x02a9: _0x0506):
    
    _0x0675 = _0x02a8.read_bytes()
    if _0x0675[:3] not in (b'\x1bLu', b'\x1bLJ'):
        try:
            _0x0677 = _0x00fc(_0x0675, _0x02a8.name)
        except Exception:
            _0x0677 = None
        if _0x0677 is not None:
            for _0x0678 in _0x00fe(_0x02a8.name):
                _0x0679 = _0x00fb(_0x0677, _0x0678)
                if _0x0150(_0x0679):
                    (_0x067a, _) = _0x0151(_0x0679)
                    _0x067c = _0x02a9.with_suffix('.tga')
                    _0x067c.write_bytes(_0x0154(_0x067a))
                    output.success(f'{_0x02a8.name}: wrote {_0x067c.name} ({_0x014e + 18:,} B zone map).')
                    break
    _0x0676 = _0x02a9.with_suffix('.junk')
    if _0x0676.exists():
        _0x0676.unlink()
        output.warn(f'{_0x02a9.name}: removed stale {_0x0676.name} companion (schema data now rides inside the txt).')

def _0x0158(_0x02ac, _0x02ad=None) -> dict:
    return _0x00e6(_0x02ac, _0x02ad)

def _0x0159(_0x02ae: _0x0506):
    (_0x068b, _, _0x068d, _0x068e, _0x068f) = _0x00de(_0x02ae)
    return (_0x068b, len(_0x068d), len(_0x068e) + len(_0x068f))

def _0x015a(_0x02af: _0x0506, _0x02b0: dict, _0x02b1=None) -> bytes:
    return _0x00fa(_0x02af, _0x02b0, _0x02b1)
if __name__ == '__main__':
    import sys as _0x0690
    _0x0690.exit('run main.py instead')
