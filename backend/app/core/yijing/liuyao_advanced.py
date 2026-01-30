"""
玄心理命 - 六爻高级算法
世应、六亲、六神、用神、进退神
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

from .hexagram import (
    Hexagram, Yao, YaoType, BAGUA, 
    NUMBER_TO_GUA, GUA_TO_NUMBER, SIXTY_FOUR_GUA
)


# ==================== 地支与五行 ====================

DIZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

DIZHI_WUXING = {
    "子": "水", "丑": "土", "寅": "木", "卯": "木",
    "辰": "土", "巳": "火", "午": "火", "未": "土",
    "申": "金", "酉": "金", "戌": "土", "亥": "水"
}

WUXING_SHENG = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
WUXING_KE = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}


# ==================== 六亲定义 ====================

class LiuQin(Enum):
    """六亲"""
    FUMU = "父母"      # 生我者
    XIONGDI = "兄弟"   # 同我者
    ZISUN = "子孙"     # 我生者
    QICAI = "妻财"     # 我克者
    GUANGUI = "官鬼"   # 克我者


def get_liuqin(yao_wuxing: str, gua_wuxing: str) -> LiuQin:
    """
    根据爻的五行和卦的五行确定六亲
    
    Args:
        yao_wuxing: 爻的五行
        gua_wuxing: 卦的五行（世爻五行）
    
    Returns:
        六亲
    """
    if yao_wuxing == gua_wuxing:
        return LiuQin.XIONGDI
    elif WUXING_SHENG.get(yao_wuxing) == gua_wuxing:
        return LiuQin.FUMU
    elif WUXING_SHENG.get(gua_wuxing) == yao_wuxing:
        return LiuQin.ZISUN
    elif WUXING_KE.get(gua_wuxing) == yao_wuxing:
        return LiuQin.QICAI
    else:
        return LiuQin.GUANGUI


# ==================== 六神定义 ====================

class LiuShen(Enum):
    """六神"""
    QINGLONG = "青龙"    # 吉神，主喜庆
    ZHUQUE = "朱雀"      # 主口舌是非
    GOUCHEN = "勾陈"     # 主拖延
    TENGSHE = "腾蛇"     # 主惊恐
    BAIHU = "白虎"       # 主凶丧
    XUANWU = "玄武"      # 主暗昧


# 六神按日干起
LIUSHEN_TABLE = {
    "甲": ["青龙", "朱雀", "勾陈", "腾蛇", "白虎", "玄武"],
    "乙": ["青龙", "朱雀", "勾陈", "腾蛇", "白虎", "玄武"],
    "丙": ["朱雀", "勾陈", "腾蛇", "白虎", "玄武", "青龙"],
    "丁": ["朱雀", "勾陈", "腾蛇", "白虎", "玄武", "青龙"],
    "戊": ["勾陈", "腾蛇", "白虎", "玄武", "青龙", "朱雀"],
    "己": ["勾陈", "腾蛇", "白虎", "玄武", "青龙", "朱雀"],
    "庚": ["白虎", "玄武", "青龙", "朱雀", "勾陈", "腾蛇"],
    "辛": ["白虎", "玄武", "青龙", "朱雀", "勾陈", "腾蛇"],
    "壬": ["玄武", "青龙", "朱雀", "勾陈", "腾蛇", "白虎"],
    "癸": ["玄武", "青龙", "朱雀", "勾陈", "腾蛇", "白虎"]
}


def get_liushen(day_gan: str, yao_position: int) -> str:
    """
    获取六神
    
    Args:
        day_gan: 日干
        yao_position: 爻位置(1-6)
    
    Returns:
        六神名称
    """
    if day_gan not in LIUSHEN_TABLE:
        day_gan = "甲"
    
    return LIUSHEN_TABLE[day_gan][yao_position - 1]


# ==================== 世应定位 ====================

# 世应表（根据本卦确定世应位置）
# 键：(上卦, 下卦)，值：世爻位置
SHIYAO_TABLE = {
    # 八纯卦
    ("乾", "乾"): 6, ("坤", "坤"): 6, ("震", "震"): 6, ("巽", "巽"): 6,
    ("坎", "坎"): 6, ("离", "离"): 6, ("艮", "艮"): 6, ("兑", "兑"): 6,
    
    # 一世卦（上卦与下卦仅初爻不同）
    ("乾", "巽"): 1, ("坤", "艮"): 1, ("震", "坤"): 1, ("巽", "乾"): 1,
    ("坎", "兑"): 1, ("离", "坎"): 1, ("艮", "坤"): 1, ("兑", "坎"): 1,
    
    # 二世卦
    ("乾", "离"): 2, ("坤", "坎"): 2, ("震", "艮"): 2, ("巽", "兑"): 2,
    ("坎", "震"): 2, ("离", "巽"): 2, ("艮", "震"): 2, ("兑", "巽"): 2,
    
    # 三世卦
    ("乾", "兑"): 3, ("坤", "震"): 3, ("震", "离"): 3, ("巽", "坎"): 3,
    ("坎", "艮"): 3, ("离", "兑"): 3, ("艮", "巽"): 3, ("兑", "离"): 3,
    
    # 四世卦
    ("乾", "坎"): 4, ("坤", "巽"): 4, ("震", "兑"): 4, ("巽", "离"): 4,
    ("坎", "离"): 4, ("离", "艮"): 4, ("艮", "坎"): 4, ("兑", "震"): 4,
    
    # 五世卦
    ("乾", "震"): 5, ("坤", "兑"): 5, ("震", "坎"): 5, ("巽", "艮"): 5,
    ("坎", "巽"): 5, ("离", "坤"): 5, ("艮", "离"): 5, ("兑", "坤"): 5,
    
    # 游魂卦
    ("乾", "艮"): 4, ("坤", "离"): 4, ("震", "巽"): 4, ("巽", "震"): 4,
    ("坎", "坤"): 4, ("离", "乾"): 4, ("艮", "兑"): 4, ("兑", "艮"): 4,
    
    # 归魂卦
    ("乾", "坤"): 3, ("坤", "乾"): 3, ("震", "乾"): 3, ("巽", "坤"): 3,
    ("坎", "乾"): 3, ("离", "坤"): 3, ("艮", "乾"): 3, ("兑", "坤"): 3,
}


def get_shi_ying(upper_gua: str, lower_gua: str) -> Tuple[int, int]:
    """
    获取世应位置
    
    Args:
        upper_gua: 上卦
        lower_gua: 下卦
    
    Returns:
        (世爻位置, 应爻位置)
    """
    shi_position = SHIYAO_TABLE.get((upper_gua, lower_gua), 1)
    
    # 应爻在世爻相隔三位
    ying_position = ((shi_position - 1 + 3) % 6) + 1
    
    return shi_position, ying_position


# ==================== 装卦（纳甲） ====================

# 八卦纳甲表
NAJIA_TABLE = {
    "乾": {"天干": "甲壬", "地支": ["子", "寅", "辰", "午", "申", "戌"]},
    "坤": {"天干": "乙癸", "地支": ["未", "巳", "卯", "丑", "亥", "酉"]},
    "震": {"天干": "庚", "地支": ["子", "寅", "辰", "午", "申", "戌"]},
    "巽": {"天干": "辛", "地支": ["丑", "亥", "酉", "未", "巳", "卯"]},
    "坎": {"天干": "戊", "地支": ["寅", "辰", "午", "申", "戌", "子"]},
    "离": {"天干": "己", "地支": ["卯", "丑", "亥", "酉", "未", "巳"]},
    "艮": {"天干": "丙", "地支": ["辰", "午", "申", "戌", "子", "寅"]},
    "兑": {"天干": "丁", "地支": ["巳", "卯", "丑", "亥", "酉", "未"]}
}


def get_yao_dizhi(gua_name: str, yao_position: int, is_upper: bool) -> str:
    """
    获取爻的地支（纳甲）
    
    Args:
        gua_name: 卦名（乾坤震巽坎离艮兑）
        yao_position: 爻在该卦中的位置(1-3)
        is_upper: 是否上卦
    
    Returns:
        地支
    """
    if gua_name not in NAJIA_TABLE:
        return "子"
    
    dizhi_list = NAJIA_TABLE[gua_name]["地支"]
    
    if is_upper:
        # 上卦取后三个地支
        return dizhi_list[yao_position + 2]
    else:
        # 下卦取前三个地支
        return dizhi_list[yao_position - 1]


# ==================== 高级六爻数据结构 ====================

@dataclass
class LiuYaoYao:
    """六爻详细爻信息"""
    position: int           # 位置(1-6)
    yao_type: YaoType       # 爻类型
    is_dong: bool           # 是否动爻
    dizhi: str              # 地支
    wuxing: str             # 五行
    liuqin: str            # 六亲
    liushen: str           # 六神
    is_shi: bool           # 是否世爻
    is_ying: bool          # 是否应爻
    
    @property
    def symbol(self) -> str:
        if self.yao_type in [YaoType.YANG, YaoType.YANG_DONG]:
            return "———"
        else:
            return "— —"
    
    def to_dict(self) -> Dict:
        return {
            "position": self.position,
            "type": self.yao_type.value,
            "symbol": self.symbol,
            "is_dong": self.is_dong,
            "dizhi": self.dizhi,
            "wuxing": self.wuxing,
            "liuqin": self.liuqin,
            "liushen": self.liushen,
            "is_shi": self.is_shi,
            "is_ying": self.is_ying
        }


@dataclass 
class LiuYaoGua:
    """完整六爻卦象"""
    name: str                    # 卦名
    upper_gua: str               # 上卦
    lower_gua: str               # 下卦
    yaos: List[LiuYaoYao]        # 六爻详情
    shi_position: int            # 世爻位置
    ying_position: int           # 应爻位置
    dong_yao: Optional[int]      # 动爻位置
    gua_wuxing: str              # 卦的五行
    changed_gua: Optional['LiuYaoGua'] = None  # 变卦
    
    def get_shi_yao(self) -> LiuYaoYao:
        """获取世爻"""
        return self.yaos[self.shi_position - 1]
    
    def get_ying_yao(self) -> LiuYaoYao:
        """获取应爻"""
        return self.yaos[self.ying_position - 1]
    
    def get_dong_yaos(self) -> List[LiuYaoYao]:
        """获取所有动爻"""
        return [yao for yao in self.yaos if yao.is_dong]


def create_liuyao_gua(hexagram: Hexagram, day_gan: str = "甲") -> LiuYaoGua:
    """
    创建完整六爻卦象
    
    Args:
        hexagram: 基础卦象
        day_gan: 日干（用于起六神）
    
    Returns:
        完整六爻卦象
    """
    # 获取世应位置
    shi_pos, ying_pos = get_shi_ying(hexagram.upper_gua, hexagram.lower_gua)
    
    # 获取卦的五行（以世爻所在卦的五行为准）
    gua_wuxing = BAGUA[hexagram.lower_gua if shi_pos <= 3 else hexagram.upper_gua]["element"]
    
    # 构建六爻详情
    yaos = []
    for i, yao in enumerate(hexagram.yaos):
        pos = i + 1
        is_upper = pos > 3
        in_gua_pos = pos if not is_upper else pos - 3
        gua_name = hexagram.upper_gua if is_upper else hexagram.lower_gua
        
        # 获取地支
        dizhi = get_yao_dizhi(gua_name, in_gua_pos, is_upper)
        wuxing = DIZHI_WUXING[dizhi]
        
        # 获取六亲
        liuqin = get_liuqin(wuxing, gua_wuxing).value
        
        # 获取六神
        liushen = get_liushen(day_gan, pos)
        
        liuyao = LiuYaoYao(
            position=pos,
            yao_type=yao.yao_type,
            is_dong=yao.is_dong,
            dizhi=dizhi,
            wuxing=wuxing,
            liuqin=liuqin,
            liushen=liushen,
            is_shi=(pos == shi_pos),
            is_ying=(pos == ying_pos)
        )
        yaos.append(liuyao)
    
    # 获取卦名
    gua_name = SIXTY_FOUR_GUA.get(
        (hexagram.upper_gua, hexagram.lower_gua),
        f"{hexagram.upper_gua}{hexagram.lower_gua}"
    )
    
    return LiuYaoGua(
        name=gua_name,
        upper_gua=hexagram.upper_gua,
        lower_gua=hexagram.lower_gua,
        yaos=yaos,
        shi_position=shi_pos,
        ying_position=ying_pos,
        dong_yao=hexagram.dong_yao,
        gua_wuxing=gua_wuxing
    )


# ==================== 用神分析 ====================

YONGSHEN_MAPPING = {
    "求财": "妻财",
    "问事业": "官鬼",
    "问婚姻": "妻财",  # 男问婚姻看妻财
    "问子女": "子孙",
    "问父母": "父母",
    "问兄弟": "兄弟",
    "问健康": "子孙",
    "问考试": "父母",
    "问官司": "官鬼",
    "问出行": "子孙",
    "问失物": "妻财"
}


def find_yongshen(liuyao_gua: LiuYaoGua, question_type: str) -> Dict:
    """
    找出用神
    
    Args:
        liuyao_gua: 六爻卦象
        question_type: 问题类型
    
    Returns:
        用神信息
    """
    yongshen_liuqin = YONGSHEN_MAPPING.get(question_type, "官鬼")
    
    yongshen_yaos = [yao for yao in liuyao_gua.yaos if yao.liuqin == yongshen_liuqin]
    
    if not yongshen_yaos:
        return {
            "found": False,
            "liuqin": yongshen_liuqin,
            "message": f"卦中无{yongshen_liuqin}，需找飞伏"
        }
    
    # 找出最有力的用神（动爻优先）
    yong = None
    for yao in yongshen_yaos:
        if yao.is_dong:
            yong = yao
            break
    if not yong:
        yong = yongshen_yaos[0]
    
    return {
        "found": True,
        "liuqin": yongshen_liuqin,
        "position": yong.position,
        "dizhi": yong.dizhi,
        "wuxing": yong.wuxing,
        "is_dong": yong.is_dong,
        "is_shi": yong.is_shi
    }


# ==================== 综合断卦 ====================

def analyze_liuyao(liuyao_gua: LiuYaoGua, question: str = "", question_type: str = "问事业") -> Dict:
    """
    综合分析六爻卦象
    
    Args:
        liuyao_gua: 六爻卦象
        question: 具体问题
        question_type: 问题类型
    
    Returns:
        分析结果
    """
    # 找用神
    yongshen = find_yongshen(liuyao_gua, question_type)
    
    # 世应分析
    shi_yao = liuyao_gua.get_shi_yao()
    ying_yao = liuyao_gua.get_ying_yao()
    
    shi_ying_relation = _analyze_shi_ying_relation(shi_yao, ying_yao)
    
    # 动爻分析
    dong_yaos = liuyao_gua.get_dong_yaos()
    dong_analysis = _analyze_dong_yaos(dong_yaos, liuyao_gua)
    
    # 综合判断
    fortune = _calculate_liuyao_fortune(liuyao_gua, yongshen, shi_ying_relation)
    
    return {
        "question": question,
        "question_type": question_type,
        "gua_name": liuyao_gua.name,
        "gua_wuxing": liuyao_gua.gua_wuxing,
        "shi_ying": {
            "shi": {
                "position": shi_yao.position,
                "dizhi": shi_yao.dizhi,
                "liuqin": shi_yao.liuqin,
                "liushen": shi_yao.liushen
            },
            "ying": {
                "position": ying_yao.position,
                "dizhi": ying_yao.dizhi,
                "liuqin": ying_yao.liuqin,
                "liushen": ying_yao.liushen
            },
            "relation": shi_ying_relation
        },
        "yongshen": yongshen,
        "dong_analysis": dong_analysis,
        "yaos_detail": [yao.to_dict() for yao in liuyao_gua.yaos],
        "fortune": fortune
    }


def _analyze_shi_ying_relation(shi_yao: LiuYaoYao, ying_yao: LiuYaoYao) -> Dict:
    """分析世应关系"""
    shi_wuxing = shi_yao.wuxing
    ying_wuxing = ying_yao.wuxing
    
    if shi_wuxing == ying_wuxing:
        relation = "比和"
        meaning = "双方势均力敌，事情可成"
    elif WUXING_SHENG.get(shi_wuxing) == ying_wuxing:
        relation = "世生应"
        meaning = "我方主动付出，需看对方态度"
    elif WUXING_SHENG.get(ying_wuxing) == shi_wuxing:
        relation = "应生世"
        meaning = "对方愿意配合，事情易成"
    elif WUXING_KE.get(shi_wuxing) == ying_wuxing:
        relation = "世克应"
        meaning = "我方占优势，可主动出击"
    else:
        relation = "应克世"
        meaning = "对方较强势，需谨慎应对"
    
    return {
        "relation": relation,
        "meaning": meaning,
        "shi_wuxing": shi_wuxing,
        "ying_wuxing": ying_wuxing
    }


def _analyze_dong_yaos(dong_yaos: List[LiuYaoYao], gua: LiuYaoGua) -> Dict:
    """分析动爻"""
    if not dong_yaos:
        return {
            "has_dong": False,
            "message": "无动爻，事情暂无变化"
        }
    
    analysis = []
    for yao in dong_yaos:
        meaning = _get_dong_yao_meaning(yao, gua)
        analysis.append({
            "position": yao.position,
            "liuqin": yao.liuqin,
            "liushen": yao.liushen,
            "meaning": meaning
        })
    
    return {
        "has_dong": True,
        "dong_count": len(dong_yaos),
        "analysis": analysis
    }


def _get_dong_yao_meaning(yao: LiuYaoYao, gua: LiuYaoGua) -> str:
    """获取动爻含义"""
    base_meaning = {
        1: "初动，事情起步阶段",
        2: "二动，事情正在进行",
        3: "三动，事情到转折点",
        4: "四动，事情接近成功",
        5: "五动，贵人相助",
        6: "上动，事情到极点"
    }
    
    liuqin_meaning = {
        "父母": "文书、长辈有动态",
        "兄弟": "朋友、竞争者有变化",
        "子孙": "阻碍消除，有转机",
        "妻财": "财务、女性有变化",
        "官鬼": "压力、工作有变动"
    }
    
    return f"{base_meaning.get(yao.position, '')}，{liuqin_meaning.get(yao.liuqin, '')}"


def _calculate_liuyao_fortune(gua: LiuYaoGua, yongshen: Dict, shi_ying: Dict) -> Dict:
    """计算六爻运势"""
    score = 50
    factors = []
    
    # 用神分析
    if yongshen["found"]:
        if yongshen.get("is_dong"):
            score += 15
            factors.append("用神发动")
        if yongshen.get("is_shi"):
            score += 10
            factors.append("用神临世")
    else:
        score -= 15
        factors.append("用神不现")
    
    # 世应关系
    if shi_ying["relation"] == "应生世":
        score += 15
        factors.append("应生世")
    elif shi_ying["relation"] == "世克应":
        score += 10
        factors.append("世克应")
    elif shi_ying["relation"] == "应克世":
        score -= 10
        factors.append("应克世")
    
    # 六神分析
    shi_yao = gua.get_shi_yao()
    if shi_yao.liushen == "青龙":
        score += 10
        factors.append("青龙临世")
    elif shi_yao.liushen == "白虎":
        score -= 10
        factors.append("白虎临世")
    
    score = max(0, min(100, score))
    
    if score >= 70:
        level = "吉"
        suggestion = "事情可行，积极推进"
    elif score >= 50:
        level = "平"
        suggestion = "事情尚可，需要努力"
    elif score >= 30:
        level = "凶"
        suggestion = "事情阻碍较多，需谨慎"
    else:
        level = "大凶"
        suggestion = "暂不宜行动，等待时机"
    
    return {
        "score": score,
        "level": level,
        "suggestion": suggestion,
        "factors": factors
    }
